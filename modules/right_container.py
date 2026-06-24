import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
import json
from datetime import datetime, timedelta, timezone


from .Horizontal_bar_card import HourlyForecastWidget
from .temperature_chart import TemperatureChartWidget
from .top_frame import TopFrameWidget

from utils import weather_translater, translater
from utils import request_sender

class RightContainer(widgets.QFrame):
    city_selected = core.pyqtSignal(str)
    city_deleted = core.pyqtSignal(str)
    city_saved = core.pyqtSignal(str)
    def __init__(self, parent, city_name, settings: core.QSettings = None):
        super().__init__(parent)
        
        self.settings = settings
        
        defaults = {
            "Clear": "media/Sun.png",
            "Clouds": "media/Cloudy.png",
            "Rain": "media/Rainy.png",
            "Snow": "media/Snowy.png",
            "Thunderstorm": "media/Thunderstorm.png",
        }
        for key, val in defaults.items():
            if not settings.contains(key):
                settings.setValue(key, val)
        
        self._modal = None
        self.city_name = city_name
        self.setMinimumWidth(830)
        self.setSizePolicy(widgets.QSizePolicy.Policy.Expanding, widgets.QSizePolicy.Policy.Expanding)
        self.setStyleSheet("""
                        background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #FFDF56, stop:1 #87CEFA);
                        
                        """)

        self.WEATHER_CONTAINER_LAYOUT = widgets.QVBoxLayout(self)
        self.setLayout(self.WEATHER_CONTAINER_LAYOUT)
        self.WEATHER_CONTAINER_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.WEATHER_CONTAINER_LAYOUT.setContentsMargins(15, 15, 15, 15)
        self.WEATHER_CONTAINER_LAYOUT.setSpacing(14)

        self.timezone_offset = 0
        self.DAYS = translater("right_container", "days")
        
        self.clock_timer = core.QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        
        self.build_empty_ui()
        
    def build_empty_ui(self):
        self.clock_timer.stop()
    
        self.time_label = None
        self.date_label = None
        self.day_label = None
        
        self.clear_layout(self.WEATHER_CONTAINER_LAYOUT)
        
        self.clear_layout(self.WEATHER_CONTAINER_LAYOUT)
        self.TOP_FRAME = TopFrameWidget(parent=self, settings=self.settings, modal=self._modal)
        self.TOP_FRAME.city_selected.connect(self.city_selected)
        self.TOP_FRAME.city_deleted.connect(self.city_deleted)
        self.TOP_FRAME.city_saved.connect(self.city_saved)
        self.TOP_FRAME.modal_created.connect(self._on_modal_created)
        self.WEATHER_CONTAINER_LAYOUT.addWidget(self.TOP_FRAME)
        self.TOP_FRAME.icons_changed.connect(self._on_icons_changed_rebuild)
        
        self.dropdown = widgets.QListWidget(self)
        self.dropdown.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.dropdown.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.dropdown.setSpacing(5)
        self.dropdown.setFixedWidth(261)
        self.dropdown.setFixedHeight(200)
        self.dropdown.setStyleSheet(
            "background-color: rgba(0,0,0,0.2); border: none; border-radius: 10px;"
        )
        self.dropdown.hide()
        self.dropdown.itemClicked.connect(self.TOP_FRAME.on_city_selected)
        self.TOP_FRAME.set_dropdown(self.dropdown)

        placeholder = widgets.QLabel(translater("right_container", "select_city"))
        placeholder.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("""
            color: rgba(255, 255, 255, 0.5);
            font-family: Roboto;
            font-size: 32px;
            font-weight: 300;
            background: transparent;
            border: none;
        """)
        self.WEATHER_CONTAINER_LAYOUT.addWidget(placeholder, stretch=1)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def city_datetime(self):
        utc_now = datetime.now(timezone.utc)
        tz = timezone(timedelta(seconds=self.timezone_offset))
        return utc_now.astimezone(tz)

    def update_clock(self):
        try:
            if hasattr(self, 'time_label'):
                city_now = self.city_datetime()
                self.time_label.setText(city_now.strftime("%H:%M"))
            if hasattr(self, 'date_label'):
                city_now = self.city_datetime()
                self.date_label.setText(city_now.strftime("%d.%m.%Y"))
            if hasattr(self, 'day_label'):
                city_now = self.city_datetime()
                self.day_label.setText(self.DAYS[city_now.weekday()])
        except RuntimeError:
            self.clock_timer.stop()

    def update_city(self, city_name, display_name=None):
        self.clock_timer.stop()
    
        self.time_label = None
        self.date_label = None  
        self.day_label = None
        
        self.city_name = city_name
        self.display_name = display_name or city_name
        self.clear_layout(self.WEATHER_CONTAINER_LAYOUT)
        response = request_sender(city_name)
        self.timezone_offset = response.get("timezone", 0) if isinstance(response, dict) else 0
        self.build_ui(response)
        if not self.clock_timer.isActive():
            self.clock_timer.start(1000)
        self.update_clock()
        
    def set_search_callback(self, callback):
        self._search_callback = callback

    def _on_modal_created(self, modal):
        if self._modal is modal:
            return
        self._modal = modal
        modal.icons_changed.connect(self._on_icons_changed_rebuild)
    
    def _on_icons_changed_rebuild(self):
        if self.city_name:
            self.update_city(self.city_name, getattr(self, 'display_name', self.city_name))
        else:
            self.build_empty_ui()
    
    def set_theme(self, dark: bool):
        if dark:
            self.setStyleSheet("""
                background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1,
                    stop:0 #4A4A4A, stop:1 #5DADE2);
                border-bottom-right-radius: 10px;
                border-bottom-left-radius: 0px;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
            """)
        else:
            self.setStyleSheet("""
                background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1,
                    stop:0 #FFDF56, stop:1 #87CEFA);
                border-bottom-right-radius: 10px;
                border-bottom-left-radius: 0px;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
            """)
    
    def build_ui(self, response):
        
        self.TOP_FRAME = TopFrameWidget(parent=self, settings=self.settings, modal = self._modal)
        self.TOP_FRAME.city_selected.connect(self.city_selected)
        self.TOP_FRAME.city_deleted.connect(self.city_deleted)
        self.TOP_FRAME.city_saved.connect(self.city_saved)
        self.TOP_FRAME.modal_created.connect(self._on_modal_created)
        self.TOP_FRAME.icons_changed.connect(self._on_icons_changed_rebuild)
        
        
        self.WEATHER_CONTAINER_LAYOUT.addWidget(self.TOP_FRAME)
        

        self.dropdown = widgets.QListWidget(self)
        self.dropdown.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.dropdown.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        
        self.dropdown.setSpacing(5)
        self.dropdown.setFixedWidth(261)
        self.dropdown.setFixedHeight(200)
        self.dropdown.setStyleSheet(
            "background-color: rgba(0,0,0,0.2); border: none; border-radius: 10px;"
        )
        self.dropdown.hide()
        self.dropdown.itemClicked.connect(self.TOP_FRAME.on_city_selected)
        self.TOP_FRAME.set_dropdown(self.dropdown)
        
        self.CENTER_FRAME = widgets.QFrame(parent=self)
        self.CENTER_FRAME.setMinimumHeight(303)
        self.CENTER_FRAME.setStyleSheet("background: transparent")
        self.WEATHER_CONTAINER_LAYOUT.addWidget(self.CENTER_FRAME)
        
        left_center_container = widgets.QFrame(parent = self.CENTER_FRAME)
        left_center_container.setStyleSheet("background-color: rgba(0, 0, 0, 0.1); border-radius: 10px ")
        left_center_container.setMinimumWidth(390)
        left_center_container.setSizePolicy(widgets.QSizePolicy.Policy.Expanding, widgets.QSizePolicy.Policy.Expanding)

        left_center_container_layout = widgets.QVBoxLayout()
        left_center_container_layout.setContentsMargins(10, 10, 20, 10)
        left_center_container_layout.setSpacing(12)
        left_center_container.setLayout(left_center_container_layout)

        top_label_widget = widgets.QFrame(parent = left_center_container)
        top_label_widget.setFixedHeight(27)
        top_label_widget.setStyleSheet("background: transparent; border: none")
        left_center_container_layout.addWidget(top_label_widget)
        top_label_widget_layout = widgets.QHBoxLayout()
        top_label_widget_layout.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        top_label_widget_layout.setContentsMargins(10, 10, 0, 0)
        top_label_widget_layout.setSpacing(10)
        top_label_widget.setLayout(top_label_widget_layout)
        left_center_container_layout.addWidget(top_label_widget)

        navigation_icon = gui.QIcon("media/Navigation.png")
        pixmap = gui.QPixmap(navigation_icon.pixmap(core.QSize(16, 16)))
        navigation_label = widgets.QLabel(parent = top_label_widget)
        navigation_label.setPixmap(pixmap)
        navigation_label.setStyleSheet("background: transparent; border: none")
        top_label_widget_layout.addWidget(navigation_label)

        top_label = widgets.QLabel(top_label_widget, text = translater("right_container", "current_position"))
        top_label.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        top_label.setFixedHeight(27)
        top_label.setStyleSheet("""
            font-family: Roboto;
            font-size: 16px;
            font-weight: 500;
            border: none;
            background: transparent;
        """)
        top_label_widget_layout.addWidget(top_label)

        top_line = widgets.QFrame(parent = left_center_container)
        left_center_container_layout.addWidget(top_line)
        top_line.setFixedHeight(1)
        top_line.setMinimumWidth(358)
        top_line.setSizePolicy(widgets.QSizePolicy.Policy.Expanding, widgets.QSizePolicy.Policy.Fixed)
        top_line.setStyleSheet("""
                background-color: rgba(255,255,255,0.30);
                border: none;
            """)    

        if response["cod"] != 404:
            label1 = widgets.QLabel(left_center_container, text = self.display_name)
            label1.setWordWrap(True)
            label1.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            label1.setStyleSheet("""
                                    font-family: Roboto;
                                    font-size: 44px;
                                    font-weight: 500;
                                    border: none;
                                    background: transparent;
                                    """)
            left_center_container_layout.addWidget(label1)

            weather_widget = widgets.QFrame(parent = left_center_container)
            weather_widget.setFixedHeight(87)
            weather_widget.setStyleSheet("background: transparent; border: none")
            left_center_container_layout.addWidget(weather_widget)
            weather_widget_layout = widgets.QHBoxLayout()
            weather_widget_layout.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            weather_widget_layout.setContentsMargins(0, 0, 0, 0)
            weather_widget_layout.setSpacing(0)
            weather_widget.setLayout(weather_widget_layout)

            icon_label = widgets.QLabel(parent = weather_widget)
            icon_label.setFixedSize(87, 87)
            icon_label.setStyleSheet("background: transparent; border: none;")
            icon_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            weather_widget_layout.addWidget(icon_label)
            icon_path = None

            weather_main = response["weather"][0]["main"]
            icon_path = self.settings.value(weather_main)

            if icon_path:
                pixmap = gui.QPixmap(icon_path)
                icon_label.setPixmap(pixmap)
                icon_label.setScaledContents(True)

            temp_label = widgets.QLabel(weather_widget, text = str(int(response["main"]["temp"] - 273.3)) + "°")
            temp_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            temp_label.setStyleSheet("""
                                    font-family: Roboto;
                                    font-size: 74px;
                                    font-weight: 500;
                                    border: none;
                                    background: transparent;
                                    """)
            weather_widget_layout.addWidget(temp_label)

            label3 = widgets.QLabel(left_center_container, text = str(weather_translater(response["weather"][0]["main"])))
            label3.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            label3.setStyleSheet("""
                                    font-family: Roboto;
                                    font-size: 24px;
                                    font-weight: 500;
                                    border: none;
                                    background: transparent;
                                    """)
            left_center_container_layout.addWidget(label3)

            label4 = widgets.QLabel(left_center_container, text = f"{translater("right_container", "max")}:{str(int(response["main"]["temp_max"] - 273.3))}°, {translater("right_container", "min")}:{str(int(response["main"]["temp_min"] - 273.3))}°")
            label4.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            label4.setStyleSheet("""
                                    font-family: Roboto;
                                    font-size: 16px;
                                    font-weight: 500;
                                    border: none;
                                    background: transparent;
                                    color: rgba(255,255,255,0.8);
                                    """)
            left_center_container_layout.addWidget(label4)

        right_center_container = widgets.QFrame(parent = self.CENTER_FRAME)
        right_center_container.setStyleSheet("background-color: rgba(0, 0, 0, 0.1); border-radius: 10px ")
        right_center_container.setMinimumWidth(390)
        right_center_container.setSizePolicy(widgets.QSizePolicy.Policy.Expanding, widgets.QSizePolicy.Policy.Expanding)

        center_frame_layout = widgets.QHBoxLayout(self.CENTER_FRAME)
        center_frame_layout.setContentsMargins(0, 0, 0, 0)
        center_frame_layout.setSpacing(15)
        center_frame_layout.addWidget(left_center_container, stretch = 1)
        center_frame_layout.addWidget(right_center_container, stretch = 1)

        right_center_container_layout = widgets.QVBoxLayout()
        right_center_container_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        right_center_container_layout.setContentsMargins(20, 20, 20, 15)
        right_center_container_layout.setSpacing(12)
        right_center_container.setLayout(right_center_container_layout)
        
        top_right_label = widgets.QLabel(right_center_container, text = translater("right_container", "today"))
        top_right_label.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        top_right_label.setStyleSheet("""
            font-family: Roboto;
            font-size: 16px;
            font-weight: 500;
            border: none;
            background: transparent;
        """)
        right_center_container_layout.addWidget(top_right_label, alignment = core.Qt.AlignmentFlag.AlignTop)

        top_right_line = widgets.QFrame(parent = right_center_container)
        right_center_container_layout.addWidget(top_right_line, alignment = core.Qt.AlignmentFlag.AlignTop)
        top_right_line.setFixedHeight(1)
        top_right_line.setMinimumWidth(358)
        top_right_line.setSizePolicy(widgets.QSizePolicy.Policy.Expanding, widgets.QSizePolicy.Policy.Fixed)
        top_right_line.setStyleSheet("""
                background-color: rgba(255,255,255,0.30);
                border: none;
            """)

        right_label_layout = widgets.QHBoxLayout()
        right_label_layout.setContentsMargins(0, 0, 0, 0)
        right_label_layout.setSpacing(0)

        right_label_widget = widgets.QFrame(parent = right_center_container)
        right_label_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        right_label_widget.setFixedHeight(44)
        right_label_widget.setStyleSheet("background: transparent; border: none;")
        right_label_widget.setLayout(right_label_layout)
        right_center_container_layout.addWidget(right_label_widget, alignment = core.Qt.AlignmentFlag.AlignTop)

        city_now = self.city_datetime()
        day_name = self.DAYS[city_now.weekday()]
        current_date = city_now.strftime("%d.%m.%Y")

        self.day_label = widgets.QLabel(right_center_container, text = day_name)
        self.day_label.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        self.day_label.setStyleSheet("""
            font-family: Roboto;
            font-size: 24px;
            font-weight: 500;
            border: none;
            background: transparent;
            """)
        right_label_layout.addWidget(self.day_label)

        self.date_label = widgets.QLabel(right_center_container, text = current_date)
        self.date_label.setAlignment(core.Qt.AlignmentFlag.AlignRight)
        self.date_label.setStyleSheet("""
            font-family: Roboto;
            font-size: 24px;
            font-weight: 500;
            border: none;
            background: transparent;
            """)
        right_label_layout.addWidget(self.date_label)

#1
        clock_frame = widgets.QFrame(parent = right_center_container)
        clock_frame.setFixedSize(168, 168)
        clock_frame.setStyleSheet("background: transparent; border: None;")
        right_center_container_layout.addWidget(clock_frame, alignment = core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignHCenter)

        clock_frame_layout = widgets.QStackedLayout(clock_frame)
        clock_frame_layout.setStackingMode(widgets.QStackedLayout.StackingMode.StackAll)
        clock_frame.setLayout(clock_frame_layout)

        current_time = self.city_datetime().strftime("%H:%M")
        self.time_label = widgets.QLabel(parent = clock_frame, text = current_time)
        self.time_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("""
            font-family: Roboto;
            font-size: 29px;
            font-weight: 500;
            border: none;
            background: transparent;
            """)
        clock_frame_layout.addWidget(self.time_label)

        clock_icon = gui.QIcon("media/Clock.png")
        pixmap = gui.QPixmap(clock_icon.pixmap(core.QSize(200, 200)))
        clock_label = widgets.QLabel(parent = clock_frame)
        clock_label.setPixmap(pixmap)
        clock_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        clock_label.setStyleSheet("background: transparent; border: none;")
        clock_frame_layout.addWidget(clock_label)
#
        self.FOOTER = widgets.QFrame(parent = self)
        self.FOOTER.setMinimumHeight(364)
        self.FOOTER.setStyleSheet("background: transparent")
        self.WEATHER_CONTAINER_LAYOUT.addWidget(self.FOOTER)

        footer_layout = widgets.QVBoxLayout(self.FOOTER)
        footer_layout.setContentsMargins(0,0,0,0)
        footer_layout.setSpacing(15)

        top_footer = widgets.QFrame()
        top_footer.setMinimumHeight(157)
        top_footer.setStyleSheet("""
            background-color: rgba(0,0,0,0.1);
            border-radius: 10px;
        """)



        bottom_footer = widgets.QFrame()
        bottom_footer.setMinimumHeight(197)
        bottom_footer.setStyleSheet("""
            background-color: rgba(0,0,0,0.1);
            border-radius: 10px;
        """)

        bottom_footer_layout = widgets.QVBoxLayout()
        bottom_footer.setLayout(bottom_footer_layout)

        footer_layout.addWidget(top_footer)
        footer_layout.addWidget(bottom_footer)
        
        chart_title_label = widgets.QLabel(translater("right_container", "forecast_12h"))
        chart_title_label.setStyleSheet("""
            font-family: Roboto;
            font-size: 15px;
            font-weight: 400;
            color: white;
            background: transparent;
        """)
        bottom_footer_layout.addWidget(chart_title_label)

        chart_line = widgets.QFrame(parent=bottom_footer)
        chart_line.setFixedHeight(1)
        chart_line.setStyleSheet("""
        background-color: rgba(255, 255, 255, 0.30); border: none;
                                """)
        bottom_footer_layout.addWidget(chart_line, alignment=core.Qt.AlignmentFlag.AlignTop)

        chart = TemperatureChartWidget(
        parent=bottom_footer,
        city_name=self.city_name,
        timezone_offset=self.timezone_offset,
        )
        bottom_footer_layout.addWidget(chart)

        
        top_footer_layout = widgets.QVBoxLayout()
        top_footer_layout.setContentsMargins(15,15,15,15)
        top_footer_layout.setSpacing(10)
        top_footer.setLayout(top_footer_layout)

        label5 = widgets.QLabel(translater("right_container", "weather_today"))
        label5.setStyleSheet("""
            font-family: Roboto;
            font-size: 15px;
            font-weight: 400;
            color: white;
            background: transparent;
        """)

        top_footer_layout.addWidget(label5, alignment = core.Qt.AlignmentFlag.AlignTop)

        line = widgets.QFrame(parent = top_footer)
        line.setFixedHeight(1)
        line.setStyleSheet("""
            background-color: rgba(255,255,255,0.3);
            border: none;
        """)
        top_footer_layout.addWidget(line, alignment = core.Qt.AlignmentFlag.AlignTop)
        
        top_footer_scroll = HourlyForecastWidget(
            parent=self.FOOTER,
            city_name=self.city_name,      
            timezone_offset=self.timezone_offset
        )
        top_footer_layout.addWidget(top_footer_scroll)
        
