import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
from datetime import datetime, timezone, timedelta

from utils import request_forecast

WEATHER_ICONS = {
    "Clear":       "media/Sun_table.png",
    "Clouds":      "media/Cloudy_table.png",
    "Rain":        "media/Rainy_table.png",
    "Thunderstorm":"media/Thunderstorm_table.png",
    "Snow":        "media/Snowy_table.png",
}

SUN_ICONS = {
    "sunrise": "media/Sunrise.png",
    "sunset":  "media/Sunset.png",
}


class HourlyCard(widgets.QFrame):
    def __init__(self, parent, time_str: str, temp: int, weather_main: str):
        super().__init__(parent)
        self.setFixedSize(45, 76)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255,255,255,0.15);
                border-radius: 14px;
                background: transparent;
            }
        """)

        layout = widgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.setAlignment(core.Qt.AlignmentFlag.AlignHCenter)

        time_label = widgets.QLabel(time_str)
        time_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        time_label.setStyleSheet("""
            font-family: Roboto;
            font-size: 16px;
            font-weight: 500;
            color: rgba(255,255,255,1);
            background: transparent;
            border: none;
            letter-spacing: 0%;
            line-height: 100%;
        """)
        layout.addWidget(time_label)

        icon_label = widgets.QLabel()
        icon_label.setFixedSize(24, 24)
        icon_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("background: transparent; border: none;")
        icon_path = WEATHER_ICONS.get(weather_main)
        if icon_path:
            pm = gui.QPixmap(icon_path).scaled(
                24, 24,
                core.Qt.AspectRatioMode.KeepAspectRatio,
                core.Qt.TransformationMode.SmoothTransformation
            )
            icon_label.setPixmap(pm)
        layout.addWidget(icon_label, alignment=core.Qt.AlignmentFlag.AlignHCenter)

        temp_label = widgets.QLabel(f"{temp}°")
        temp_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        temp_label.setStyleSheet("""
            font-family: Roboto;
            font-size: 16px;
            font-weight: 500;
            color: white;
            background: transparent;
            border: none;
            line-height: 100%;
            letter-spacing: 0%;
        """)
        layout.addWidget(temp_label)


class SunCard(widgets.QFrame):
    """Карточка з часом сходу або заходу сонця."""

    def __init__(self, parent, kind: str, time_str: str):
        """
        kind: 'sunrise' або 'sunset'
        time_str: час у форматі 'HH:MM'
        """
        super().__init__(parent)
        self.setFixedSize(55, 76)
        self.setStyleSheet("""
            QFrame {
                background: transparent;
            }
        """)

        layout = widgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.setAlignment(core.Qt.AlignmentFlag.AlignHCenter)

        # Время
        time_label = widgets.QLabel(time_str)
        time_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        time_label.setStyleSheet("""
            font-family: Roboto;
            font-size: 16px;
            font-weight: 500;
            color: white;
            background: transparent;
            border: none;
            line-height: 100%;
            letter-spacing: 0%;
        """)
        layout.addWidget(time_label)

        # Иконка
        icon_label = widgets.QLabel()
        icon_label.setFixedSize(24, 24)
        icon_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("background: transparent; border: none;")
        icon_path = SUN_ICONS.get(kind)
        if icon_path:
            pm = gui.QPixmap(icon_path).scaled(
                24, 24,
                core.Qt.AspectRatioMode.KeepAspectRatio,
                core.Qt.TransformationMode.SmoothTransformation
            )
            icon_label.setPixmap(pm)
        layout.addWidget(icon_label, alignment=core.Qt.AlignmentFlag.AlignHCenter)
        
        # Надпись «Схід» / «Захід»
        label_text = "Схід" if kind == "sunrise" else "Захід"
        label = widgets.QLabel(label_text)
        label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            font-family: Roboto;
            font-size: 16px;
            font-weight: 500;
            color: rgba(255, 255, 255, 1);
            background: transparent;
            border: none;
            line-height: 100%;
            letter-spacing: 0%;
        """)
        layout.addWidget(label)
        
        


class HourlyForecastWidget(widgets.QFrame):
    """
    Вставляється замість top_footer у FOOTER.
    Містить горизонтальний скрол з картками
    та дві кнопки (← →) для переходу до країв.
    """
    def __init__(self, parent, city_name: str, timezone_offset: int = 0):
        super().__init__(parent)
        self.setFixedHeight(100)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(0,0,0,0.1);
                border-radius: 10px;
                background: transparent;
            }
        """)

        root = widgets.QHBoxLayout(self)
        root.setContentsMargins(10, 12, 10, 12)
        root.setSpacing(8)

        self.btn_left = self._make_nav_btn("‹")
        root.addWidget(self.btn_left, alignment=core.Qt.AlignmentFlag.AlignVCenter)

        self.scroll = widgets.QScrollArea()
        self.scroll.setFrameShape(widgets.QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        root.addWidget(self.scroll, stretch=1)

        self.btn_right = self._make_nav_btn("›")
        root.addWidget(self.btn_right, alignment=core.Qt.AlignmentFlag.AlignVCenter)

        self.btn_left.clicked.connect(self._scroll_to_start)
        self.btn_right.clicked.connect(self._scroll_to_end)

        self.load(city_name, timezone_offset)

    def _make_nav_btn(self, symbol: str) -> widgets.QPushButton:
        btn = widgets.QPushButton(symbol)
        btn.setFixedSize(16, 16)
        btn.setCursor(gui.QCursor(core.Qt.CursorShape.PointingHandCursor))
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.20);
                color: white;
                border: none;
                border-radius: 16px;
                font-size: 22px;
                font-weight: 300;
                padding-bottom: 2px;
                background: transparent;
            }
            QPushButton:pressed {
                background-color: rgba(255,255,255,0.50);
                border-radius: 16px;
            }
        """)
        return btn

    def _scroll_to_start(self):
        bar = self.scroll.horizontalScrollBar()
        self._animate_scroll(bar, bar.value(), bar.minimum())

    def _scroll_to_end(self):
        bar = self.scroll.horizontalScrollBar()
        self._animate_scroll(bar, bar.value(), bar.maximum())

    def _animate_scroll(self, bar, from_val: int, to_val: int):
        anim = core.QPropertyAnimation(bar, b"value", self)
        anim.setDuration(400)
        anim.setStartValue(from_val)
        anim.setEndValue(to_val)
        anim.setEasingCurve(core.QEasingCurve.Type.OutCubic)
        anim.start(core.QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
        self._anim = anim

    def load(self, city_name: str, timezone_offset: int):
        data = request_forecast(city_name)

        inner = widgets.QWidget()
        inner.setStyleSheet("background: transparent;")
        row = widgets.QHBoxLayout(inner)
        row.setContentsMargins(4, 0, 4, 0)
        row.setSpacing(8)
        row.setAlignment(core.Qt.AlignmentFlag.AlignLeft | core.Qt.AlignmentFlag.AlignVCenter)

        if data.get("cod") != "200" and data.get("cod") != 200:
            err = widgets.QLabel("Не вдалося завантажити прогноз")
            err.setStyleSheet("color: white; font-family: Roboto; font-size: 14px; background: transparent; border: none;")
            row.addWidget(err)
            self.scroll.setWidget(inner)
            return

        tz = timezone(timedelta(seconds=timezone_offset))
        now = datetime.now(tz)
        today = now.date()

        # --- Збираємо hourly-карточки ---
        hourly_cards: list[tuple[datetime, widgets.QFrame]] = []

        for entry in data["list"]:
            dt_utc = datetime.fromtimestamp(entry["dt"], tz=timezone.utc)
            dt_local = dt_utc.astimezone(tz)

            if dt_local.date() != today:
                break
            if dt_local <= now:
                continue

            time_str = dt_local.strftime("%H:%M")
            temp = int(entry["main"]["temp"] - 273.15)
            weather_main = entry["weather"][0]["main"]

            card = HourlyCard(inner, time_str, temp, weather_main)
            hourly_cards.append((dt_local, card))

        # --- Карточки сходу/заходу ---
        city_info = data.get("city", {})
        sun_events: list[tuple[datetime, widgets.QFrame]] = []

        for kind in ("sunrise", "sunset"):
            ts = city_info.get(kind)
            if ts:
                dt_utc = datetime.fromtimestamp(ts, tz=timezone.utc)
                dt_local = dt_utc.astimezone(tz)
                if dt_local.date() == today and dt_local > now:
                    time_str = dt_local.strftime("%H:%M")
                    card = SunCard(inner, kind, time_str)
                    sun_events.append((dt_local, card))

        # --- Об'єднуємо та сортуємо за часом ---
        all_cards = sorted(hourly_cards + sun_events, key=lambda x: x[0])

        for _, card in all_cards:
            row.addWidget(card)

        self.scroll.setWidget(inner)