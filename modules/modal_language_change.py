import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
import PyQt6.QtCore as core
import json
import sys
import subprocess

from utils.translate import set_language, current_language
from utils import translater

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

class LanguageSettings(widgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(544, 578)
        self.setStyleSheet("background: transparent; border: none;")

        layout = widgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 16, 0, 0)
        layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        title = widgets.QLabel(translater("modal_language_change", "title"))
        title.setStyleSheet("""
            font-family: Roboto;
            font-size: 20px;
            font-weight: 400;
            color: white;
            background: transparent;
            border: none;
        """)
        layout.addWidget(title)
        
        layout.addSpacing(15)

        lang_label = widgets.QLabel(translater("modal_language_change", "lang_label"))
        lang_label.setStyleSheet("""
            font-family: Roboto;
            font-size: 15px;
            font-weight: 500;
            color: white;
            background: transparent;
            border: none;
        """)
        layout.addWidget(lang_label)
        
        combo_widget = widgets.QFrame(self)
        combo_widget.setFixedHeight(50)

        self.lang_combo = widgets.QComboBox()
        self.lang_combo.setFixedSize(239, 36)
        self.lang_combo.addItems(["Українська", "English"])
        lang_to_option = {"uk": "Українська", "en": "English"}
        self.lang_combo.setCurrentText(lang_to_option.get(current_language, "Українська"))
        self.lang_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 1);
                border: 1px solid rgba(236, 236, 236, 1);
                border-radius: 4px;
                padding: 6px 10px;
                color: rgba(30, 30, 30, 1);
                font-family: Roboto;
                font-size: 13px;
                font-weight: 400;
            }
            QComboBox:hover {
                border: 1px solid rgba(180, 180, 180, 1);
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QComboBox::down-arrow {
                image: url(media/title_bar/drop-down.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid rgba(236, 236, 236, 1);
                border-radius: 4px;
                selection-background-color: rgba(210, 210, 210, 1);
                color: rgba(30, 30, 30, 1);
                font-family: Roboto;
                font-size: 13px;
                outline: none;
            }
        """)
        layout.addWidget(self.lang_combo)

        layout.addSpacing(15)

        self.save_btn = widgets.QPushButton(translater("modal_language_change", "save"))
        self.save_btn.setFixedSize(130, 38)
        self.save_btn.setCursor(gui.QCursor(core.Qt.CursorShape.PointingHandCursor))
        self.save_btn.setStyleSheet("""
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
        """)
        layout.addWidget(self.save_btn)
        self.save_btn.clicked.connect(self._open_exit_screen)
        
        self.screen: widgets.QWidget = widgets.QWidget(self.window())
        self.window_layout = widgets.QVBoxLayout(self.screen)
        self.window_layout.setContentsMargins(0,20,0,0)
        self.window_layout.setSpacing(50)
        self.window_layout.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.screen.hide()
        self.screen.setFixedSize(400, 350)
        self.screen.setStyleSheet(
        """
            background-color: rgba(35, 35, 35, 1);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        
        """)
        window_label = widgets.QLabel(text = translater("modal_language_change", "reopen_warn"), parent = self.screen)
        self.window_layout.addWidget(window_label)
        window_label.setStyleSheet(
        """
            color: rgba(255, 255, 255, 0.7);
            font-family: Roboto;
            font-size: 14px;
            font-weight: 400;
            background: transparent;
            border: none;
        """)
        self.accept_button = widgets.QPushButton(parent = self.screen, text = "OK")
        self.window_layout.addWidget(self.accept_button, alignment = core.Qt.AlignmentFlag.AlignCenter)
        self.accept_button.setFixedSize(130, 38)
        self.accept_button.setStyleSheet(SAVE_BTN_ACTIVE)
        self.accept_button.clicked.connect(self._on_save)
        
    def _on_save(self):
        self._timer.stop()
        lang_map = {"Українська": "uk", "English": "en"}
        lang = lang_map.get(self.lang_combo.currentText(), "uk")
        set_language(lang)
        subprocess.Popen([sys.executable] + sys.argv)
        widgets.QApplication.quit()
        
    def _open_exit_screen(self):
        self.screen.show()
        self.screen.raise_()
        self.timer_count = 10
        self._timer = core.QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(1000)
        
    def _tick(self):
        self.timer_count -= 1
        self.accept_button.setText(f"OK ({self.timer_count})")
        if self.timer_count <= 0:
            self._on_save()
        