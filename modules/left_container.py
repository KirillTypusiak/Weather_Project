import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
import PyQt6.QtCore as core
import PyQt6.QtWebEngineWidgets as WebEngine

from .weather_content import Weather_Content

class LeftContainer(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setFixedSize(370, 800)
        self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #808080, stop:1 #5DADE2)")
        
        self.BUTTON_TOOGLE = False #флажок для переключения иконки
        
        button_frame = widgets.QFrame(parent = self)
        button_frame.setFixedSize(330, 44)
        button_frame.setStyleSheet("""
            background: transparent;
        """)
        
        left_container_layout = widgets.QVBoxLayout()
        self.setLayout(left_container_layout)
        left_container_layout.addWidget(button_frame)
        left_container_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        
        theme_button = widgets.QPushButton(parent = button_frame)
        theme_button.setFixedSize(52, 24)
        theme_button.setIconSize(core.QSize(52,24))
        theme_button.setStyleSheet("border: none")
        button_layout = widgets.QHBoxLayout()
        button_frame.setLayout(button_layout)
        button_layout.addWidget(theme_button)
        button_layout.setAlignment(core.Qt.AlignmentFlag.AlignRight)
        button_icon = gui.QIcon("media/title_bar/Dark_theme_button.svg")
        theme_button.setIcon(button_icon)
        
        def icon_change():
            if self.BUTTON_TOOGLE == True:
                button_icon_1 = gui.QIcon("media/title_bar/Dark_theme_button.svg")
                theme_button.setIcon(button_icon_1)
                self.BUTTON_TOOGLE = False
            elif self.BUTTON_TOOGLE == False:
                button_icon_2 = gui.QIcon("media/title_bar/Light_theme_button.svg")
                theme_button.setIcon(button_icon_2)
                self.BUTTON_TOOGLE = True
        
        theme_button.clicked.connect(icon_change)
        
        
        
        scroll_area = widgets.QScrollArea(parent = self)
        left_container_layout.addWidget(scroll_area)
        scroll_frame = widgets.QFrame(parent = scroll_area)
        scroll_area.setWidget(scroll_frame)
        scroll_area.setWidgetResizable(True)
        scroll_layout = widgets.QVBoxLayout()
        scroll_frame.setLayout(scroll_layout)
        
        
        for i in range(15):
            card = Weather_Content(parent = scroll_frame)
            scroll_layout.addWidget(card)