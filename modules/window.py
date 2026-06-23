import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
from .header import Header

from .app import application
from .left_container import LeftContainer
from .right_container import RightContainer


class MainWindow(widgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent; border: none;")
        
        self.settings = core.QSettings("MyApp", "settings")
        text: str = self.settings.value("window_size")
        width, height = text.split("x")
        window_width = int(width)
        window_height = int(height)
        
        # window_width = 1200
        # window_height = 800
        

        screen = application.primaryScreen()
        screen_size = screen.size()

        screen_width = screen_size.width()
        screen_height = screen_size.height()

        center_x = (screen_width // 2) - (window_width // 2)
        center_y = (screen_height // 2) - (window_height // 2)

        self.setGeometry(center_x, center_y, window_width, window_height)
        self.setWindowTitle("Project")
        
        self.shared_settings = core.QSettings("MyApp", "WeatherApp")
        
        content_container = widgets.QWidget(self)
        content_container.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4a90e2, stop:1 #1c3c72);"
            "border: none;"
            "border-bottom-left-radius: 10px;"
            "border-bottom-right-radius: 10px"
        )
        self.setCentralWidget(content_container)

        content_layout = widgets.QVBoxLayout(content_container)
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)

        header = Header(parent = content_container)
        content_layout.addWidget(header)
        
        central_widget = widgets.QWidget(content_container)
        central_widget.setStyleSheet("background: transparent;")
        content_layout.addWidget(central_widget)
        
        center_widget_layout = widgets.QHBoxLayout(central_widget)
        center_widget_layout.setSpacing(0)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        
        self.LEFT_CONTAINER = LeftContainer(parent = central_widget, on_city_selected=self.on_city_selected, settings = self.shared_settings, app_settings=self.settings)
        self.WEATHER_CONTAINER = RightContainer(parent = central_widget, city_name = "Dnipro", settings=self.shared_settings)
        
        center_widget_layout.addWidget(self.LEFT_CONTAINER)
        center_widget_layout.addWidget(self.WEATHER_CONTAINER, stretch = 1)
        
        self.WEATHER_CONTAINER.city_deleted.connect(self.LEFT_CONTAINER.remove_city_card)
        self.WEATHER_CONTAINER.city_selected.connect(self.LEFT_CONTAINER.add_city_card)
        self.WEATHER_CONTAINER.city_saved.connect(self.LEFT_CONTAINER.add_city_card)
        self.WEATHER_CONTAINER.city_selected.connect(self._sync_to_city_finder)
        self.WEATHER_CONTAINER._modal_icons_connect = self._connect_image_list
        
        self.LEFT_CONTAINER.theme_changed.connect(self._apply_theme)
        is_dark = self.settings.value("theme", "light") == "dark"
        self._apply_theme(is_dark)


    def _sync_to_city_finder(self, city_name: str):
        modal = self.WEATHER_CONTAINER._modal
        if modal and modal.city_finder:
            modal.city_finder.added_cities.add_city(city_name)
            modal.city_finder._persist_cities()
    def on_city_selected(self, city_name, display_name=None):
        self.WEATHER_CONTAINER.update_city(city_name, display_name)
    def _connect_image_list(self, image_list):
        image_list.icons_changed.connect(self._on_icons_changed)
    def _on_icons_changed(self):
        self.WEATHER_CONTAINER.build_empty_ui()
    def _apply_theme(self, dark: bool):
        self.LEFT_CONTAINER.set_theme(dark)
        self.WEATHER_CONTAINER.set_theme(dark)
        header = self.findChild(Header)
        if header:
            header.set_theme(dark)
main_window = MainWindow()