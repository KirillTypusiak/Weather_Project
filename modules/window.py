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
        
        window_width = 1200
        window_height = 800

        screen = application.primaryScreen()
        screen_size = screen.size()

        screen_width = screen_size.width()
        screen_height = screen_size.height()

        center_x = (screen_width // 2) - (window_width // 2)
        center_y = (screen_height // 2) - (window_height // 2)

        self.setGeometry(center_x, center_y, window_width, window_height)
        self.setWindowTitle("Project")
        
        content_container = widgets.QWidget(self)
        content_container.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4a90e2, stop:1 #1c3c72);"
            "border: none;"
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
        
        self.LEFT_CONTAINER = LeftContainer(parent = central_widget)
        self.WEATHER_CONTAINER = RightContainer(parent = central_widget, city_name = "Dnipro") #позже сделать определение города по локации
        
        center_widget_layout.addWidget(self.LEFT_CONTAINER)
        center_widget_layout.addWidget(self.WEATHER_CONTAINER, stretch = 1)

main_window = MainWindow()