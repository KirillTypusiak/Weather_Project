import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
import PyQt6.QtCore as core

from datetime import datetime, timezone, timedelta

from utils import request_forecast, translater


class TemperatureChartWidget(widgets.QFrame):

    SCALE_MIN = -10
    SCALE_MAX = 25

    def __init__(self, parent, city_name: str, timezone_offset: int = 0):
        super().__init__(parent)
        self.setStyleSheet("background: transparent; border: none;")
        self.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Expanding,
        )

        root = widgets.QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)


        self.scroll = widgets.QScrollArea()
        self.scroll.setFrameShape(widgets.QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        root.addWidget(self.scroll, stretch=1)


        self.scale_widget = _ScaleWidget(self.SCALE_MIN, self.SCALE_MAX)
        root.addWidget(self.scale_widget)
        self.load(city_name, timezone_offset)


    def load(self, city_name: str, timezone_offset: int):
        data = request_forecast(city_name)

        inner = widgets.QWidget()
        inner.setStyleSheet("background: transparent;")
        row = widgets.QHBoxLayout(inner)
        row.setContentsMargins(4, 4, 4, 4)
        row.setSpacing(3)
        row.setAlignment(core.Qt.AlignmentFlag.AlignLeft | core.Qt.AlignmentFlag.AlignBottom)

        if data.get("cod") not in ("200", 200):
            err = widgets.QLabel(translater("temperature_chart", "forecast_error"))
            err.setStyleSheet(
                "color: white; font-family: Roboto; font-size: 14px;"
                "background: transparent; border: none;"
            )
            row.addWidget(err)
            self.scroll.setWidget(inner)
            return

        tz = timezone(timedelta(seconds=timezone_offset))

        # Берём первые 48 записей (при шаге в 3 часа это 6 дней)
        entries = data["list"][:48]

        for entry in entries:
            dt_local = datetime.fromtimestamp(entry["dt"], tz=timezone.utc).astimezone(tz)
            temp = entry["main"]["temp"] - 273.15
            weather_main = entry["weather"][0]["main"]

            bar = _TempBar(
                temp=temp,
                scale_min=self.SCALE_MIN,
                scale_max=self.SCALE_MAX,
                weather_main=weather_main,
                time_str=dt_local.strftime("%H"),
            )
            row.addWidget(bar)

        self.scroll.setWidget(inner)

class _TempBar(widgets.QWidget):
    """
    Один столбец диаграммы: иконка погоды + цветной столбец.
    Высота столбца пропорциональна температуре в диапазоне шкалы.
    """

    WEATHER_ICONS = {
        "Clear":        "media/Sun_table.png",
        "Clouds":       "media/Cloudy_table.png",
        "Rain":         "media/Rainy_table.png",
        "Thunderstorm": "media/Thunderstorm_table.png",
        "Snow":         "media/Snowy_table.png",
    }

    BAR_W = 14          
    ICON_SIZE = 14      
    MAX_BAR_H = 100
    ICON_ZONE_H = 20   # высота зоны для иконки (чтобы не было наложения на соседние столбцы)

    def __init__(self, temp: float, scale_min: int, scale_max: int,
        weather_main: str, time_str: str):
        super().__init__()
        self.temp = temp
        self.scale_min = scale_min
        self.scale_max = scale_max
        self.weather_main = weather_main

        self.setFixedWidth(self.BAR_W + 6)
        self.setStyleSheet("background: transparent;")

        layout = widgets.QVBoxLayout(self)
        layout.setContentsMargins(3, 0, 3, 0)
        layout.setSpacing(2)
        layout.setAlignment(core.Qt.AlignmentFlag.AlignHCenter)

        icon_container = widgets.QWidget()
        icon_container.setFixedHeight(self.ICON_ZONE_H)
        icon_container.setStyleSheet("background: transparent;")
        icon_layout = widgets.QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(core.Qt.AlignmentFlag.AlignHCenter | core.Qt.AlignmentFlag.AlignVCenter)
        
        # Иконка
        icon_lbl = widgets.QLabel()
        icon_lbl.setFixedSize(self.ICON_SIZE, self.ICON_SIZE)
        icon_lbl.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet("background: transparent; border: none;")
        icon_path = self.WEATHER_ICONS.get(weather_main)
        if icon_path:
            pm = gui.QPixmap(icon_path).scaled(
                self.ICON_SIZE, self.ICON_SIZE,
                core.Qt.AspectRatioMode.KeepAspectRatio,
                core.Qt.TransformationMode.SmoothTransformation,
            )
            icon_lbl.setPixmap(pm)
        icon_layout.addWidget(icon_lbl)
        layout.addWidget(icon_container)
        
        bar_container = widgets.QWidget()
        bar_container.setStyleSheet("background: transparent;")
        bar_layout = widgets.QVBoxLayout(bar_container)
        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.setAlignment(core.Qt.AlignmentFlag.AlignHCenter | core.Qt.AlignmentFlag.AlignBottom)


        # Столбец
        bar_h = self._calc_height()
        self.bar_label = _GradientBar(self.BAR_W, bar_h, temp, scale_min, scale_max)
        bar_layout.addWidget(self.bar_label, alignment=core.Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(bar_container, stretch = 1)

    def _calc_height(self) -> int:
        span = self.scale_max - self.scale_min
        ratio = (self.temp - self.scale_min) / span
        ratio = max(0.03, min(1.0, ratio))   # минимум 3% высоты
        return int(ratio * self.MAX_BAR_H)



class _GradientBar(widgets.QWidget):
    """Прямоугольный столбец с градиентом синий→жёлтый по температуре."""

    def __init__(self, width: int, height: int,
                temp: float, scale_min: int, scale_max: int):
        super().__init__()
        self.setFixedSize(width, height)
        self._temp = temp
        self._scale_min = scale_min
        self._scale_max = scale_max
        self.setStyleSheet("background: transparent;")

    def paintEvent(self, event):
        painter = gui.QPainter(self)
        painter.setRenderHint(gui.QPainter.RenderHint.Antialiasing)

        grad = gui.QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0.0, gui.QColor("#FFDF56"))   # жёлтый вверху
        grad.setColorAt(1.0, gui.QColor("#87CEFA"))   # синий внизу

        painter.setPen(core.Qt.PenStyle.NoPen)
        painter.setBrush(gui.QBrush(grad))
        painter.drawRect(self.rect())   # без закругления

        painter.end()



class _ScaleWidget(widgets.QWidget):

    LABELS = [25, 20, 15, 10, 5, 0, -5, -10]
    WIDTH  = 36

    def __init__(self, scale_min: int, scale_max: int):
        super().__init__()
        self.scale_min = scale_min
        self.scale_max = scale_max
        self.setFixedWidth(self.WIDTH)
        self.setStyleSheet("background: transparent;")

    def paintEvent(self, event):
        painter = gui.QPainter(self)
        painter.setRenderHint(gui.QPainter.RenderHint.Antialiasing)

        font = gui.QFont("Roboto", 9)
        painter.setFont(font)
        painter.setPen(gui.QColor(255, 255, 255, 200))

        h = 100
        span = self.scale_max - self.scale_min

        for val in self.LABELS:
            if not (self.scale_min <= val <= self.scale_max):
                continue
            ratio = (val - self.scale_min) / span
            y = int(h * (1.0 - ratio))
            text = f"{val}°"
            painter.drawText(5, y + 32, text) 

        painter.end()