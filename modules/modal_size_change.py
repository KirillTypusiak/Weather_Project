import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui

from utils import translater
from modules import window, application


RADIO_BUTTON_STYLE = """
    QRadioButton {
    spacing: 8px;
    }
    QRadioButton::indicator {
    width: 16px;
    height: 16px;
    }
    QRadioButton::indicator:unchecked {
        image: url(media/Round.png);
    }
    QRadioButton::indicator:checked {
        image: url(media/Radio.png);
    }
"""

SAVE_BTN_INACTIVE = """
    QPushButton {
        background-color: rgba(80, 80, 80, 1);
        border-radius: 6px;
        color: rgba(160, 160, 160, 1);
        font-family: Roboto;
        font-size: 13px;
        font-weight: 500;
        border: none;
    }
"""

SAVE_BTN_ACTIVE = """
    QPushButton {
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 6px;
        color: rgba(255, 255, 255, 1);
        font-family: Roboto;
        font-size: 13px;
        font-weight: 500;
        border: none;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 0.22);
    }
    QPushButton:pressed {
        background-color: rgba(255, 255, 255, 0.28);
    }
"""


class ModalSizeChange(widgets.QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setFixedSize(544, 578)
        self.setStyleSheet("background: transparent; border: none;")

        layout = widgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 16, 0, 0)
        layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(15)
        
        self.settings = core.QSettings("MyApp", "settings")
        
        title = widgets.QLabel(translater("modal_size_change", "title"))
        title.setStyleSheet("""
            font-family: Roboto;
            font-size: 20px;
            font-weight: 400;
            color: white;
            background: transparent;
            border: none;
        """)
        layout.addWidget(title)
        layout.addSpacing(5)
        
        self.group = widgets.QButtonGroup(self)
        button1 = widgets.QRadioButton(text = "1200x800")
        button1.setStyleSheet(RADIO_BUTTON_STYLE)
        button2 = widgets.QRadioButton(text = "1440x1024")
        button2.setStyleSheet(RADIO_BUTTON_STYLE)
        button3 = widgets.QRadioButton(text = "1512x982")
        button3.setStyleSheet(RADIO_BUTTON_STYLE)
        button4 = widgets.QRadioButton(text = "1728x1117")
        button4.setStyleSheet(RADIO_BUTTON_STYLE)
        
        self.group.addButton(button1)
        self.group.addButton(button2)
        self.group.addButton(button3)
        self.group.addButton(button4)
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)
        layout.addSpacing(5)
        
        self.accept_button = widgets.QPushButton(parent = self, text = translater("modal_size_change", "accept_button"))
        self.accept_button.setFixedSize(130, 38)
        self.accept_button.setDisabled(True)
        self.accept_button.setStyleSheet(SAVE_BTN_INACTIVE)
        layout.addWidget(self.accept_button)
        self.accept_button.clicked.connect(self._on_save)
        
        default_value = self.settings.value("window_size", "1200x800")
        
        for button in self.group.buttons():
            if button.text() == default_value:
                button.setChecked(True)
        
        self.group.buttonClicked.connect(self._on_button_clicked)
        
        
    def _on_button_clicked(self):
        self.accept_button.setDisabled(False)
        self.accept_button.setStyleSheet(SAVE_BTN_ACTIVE)
        
    def _on_save(self):
        text = self.group.checkedButton().text()
        width, height = text.split("x")
        width = int(width)
        height = int(height)
        size = application.primaryScreen().size()
        screen_width = size.width()
        screen_height = size.height()
        width = min(width, screen_width)
        height = min(height, screen_height)
        self.settings.setValue("window_size", text)
        window.main_window.resize(width, height)
        center_x = (screen_width // 2) - (width // 2)
        center_y = (screen_height // 2) - (height // 2)
        window.main_window.move(center_x, center_y)