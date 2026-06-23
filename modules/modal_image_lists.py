import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
import PyQt6.QtCore as core

from utils import translater
from modules import right_container

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

CARD_SELECTED = "background: rgba(255, 255, 255, 0.15); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.3);"
CARD_DEFAULT = "background: rgba(255, 255, 255, 0.07); border-radius: 12px; border: none;"

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

WEATHER_KEYS = ["Clear", "Clouds", "Rain", "Snow", "Thunderstorm"]

DEFAULT_ICONS = [
    "media/Sun.png",
    "media/Cloudy.png",
    "media/Rainy.png",
    "media/Snowy.png",
    "media/Thunderstorm.png",
]

DEFAULT_ICONS2 = [
    "media/Sun2.png",
    "media/Cloudy2.png",
    "media/Rainy2.png",
    "media/Snowy2.png",
    "media/Thunderstorm2.png",
]


class ImageTab(widgets.QFrame):
    clicked = core.pyqtSignal(object)
    def __init__(self, name: str, icon_paths: list[str], parent=None):
        super().__init__(parent)
        
        self.icon_paths = icon_paths

        self.setStyleSheet("background: transparent; border: none;")
        self.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Fixed,
        )
        self.setStyleSheet("background: rgba(255, 255, 255, 0.07); border-radius: 12px; border: none;")

        root = widgets.QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(10)

        title = widgets.QLabel(name)
        title.setStyleSheet("""
            font-family: Roboto;
            font-size: 14px;
            font-weight: 400;
            color: rgba(255, 255, 255, 0.7);
            background: transparent;
            border: none;
        """)
        root.addWidget(title)

        icons_frame = widgets.QFrame()
        icons_frame.setStyleSheet("background: transparent; border: none;")
        icons_layout = widgets.QHBoxLayout(icons_frame)
        icons_layout.setContentsMargins(10, 0, 0, 10)
        icons_layout.setSpacing(15)
        icons_layout.setAlignment(core.Qt.AlignmentFlag.AlignLeft)

        for path in icon_paths:
            cell = widgets.QFrame()
            cell.setFixedSize(74, 74)
            cell.setStyleSheet("""
                background-color: rgba(255, 255, 255, 0.08);
                border-radius: 10px;
                border: none;
            """)
            cell_layout = widgets.QVBoxLayout(cell)
            cell_layout.setContentsMargins(8, 8, 8, 8)

            icon_label = widgets.QLabel()
            icon_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet("background: transparent; border: none;")
            pixmap = gui.QPixmap(path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    70, 70,
                    core.Qt.AspectRatioMode.KeepAspectRatio,
                    core.Qt.TransformationMode.SmoothTransformation,
                )
            icon_label.setPixmap(pixmap)
            cell_layout.addWidget(icon_label)
            icons_layout.addWidget(cell)

        root.addWidget(icons_frame)
    
    def set_selected(self, selected: bool):
        self.setStyleSheet(CARD_SELECTED if selected else CARD_DEFAULT)
        
    def mousePressEvent(self, event):
        self.clicked.emit(self)


class ImageList(widgets.QFrame):
    icons_changed = core.pyqtSignal()
    def __init__(self, parent=None, settings: core.QSettings=None):
        super().__init__(parent)
        
        self.settings = settings

        self.setFixedWidth(544)
        self.setStyleSheet("background: transparent; border: none;")

        root = widgets.QVBoxLayout(self)
        root.setContentsMargins(0, 16, 0, 0)
        root.setSpacing(16)
        root.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        # заголовок
        title = widgets.QLabel(translater("modal_image_lists", "title"))
        title.setStyleSheet("""
            font-family: Roboto;
            font-size: 18px;
            font-weight: 400;
            color: white;
            background: transparent;
            border: none;
        """)
        root.addWidget(title)

        # кнопка Додати
        add_icon = gui.QIcon(gui.QPixmap("media/plus_circle.png"))
        self.add_button = widgets.QPushButton(
            icon=add_icon,
            text=translater("modal_image_lists", "add_button"),
        )
        self.add_button.setFixedSize(120, 36)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 4px;
                color: white;
                font-family: Roboto;
                font-size: 15px;
                font-weight: 400;
                border: none;
                padding-left: 8px;
                text-align: left;
            }
            QPushButton:hover  { background-color: rgba(255,255,255,0.22); }
            QPushButton:pressed{ background-color: rgba(255,255,255,0.28); }
        """)
        root.addWidget(self.add_button)

        # скролл
        self.scroll = widgets.QScrollArea()
        self.scroll.setFixedSize(490, 300)
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(
            core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll.setHorizontalScrollBarPolicy(
            core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll.setStyleSheet("background: transparent; border: none;")

        self.scroll_widget = widgets.QFrame()
        self.scroll_widget.setStyleSheet("background: transparent; border: none;")
        self.scroll_layout = widgets.QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_layout.setSpacing(5)
        self.scroll_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        # дефолтний список
        default_tab = ImageTab(
            name=translater("modal_image_lists", "default_list_name"),
            icon_paths=DEFAULT_ICONS,
        )
        default_tab.clicked.connect(self.on_tab_clicked)
        self.scroll_layout.addWidget(default_tab)
        default_tab2 = ImageTab(
            name=translater("modal_image_lists", "default_list_name"),
            icon_paths=DEFAULT_ICONS2,
        )
        default_tab2.clicked.connect(self.on_tab_clicked)
        self.scroll_layout.addWidget(default_tab2)

        self.scroll.setWidget(self.scroll_widget)
        root.addWidget(self.scroll)

        # кнопка Зберегти
        self.save_button = widgets.QPushButton(
            text=translater("modal_image_lists", "accept_button")
        )
        self.save_button.setFixedSize(130, 38)
        self.save_button.setDisabled(True)
        self.save_button.setStyleSheet(SAVE_BTN_INACTIVE)
        root.addWidget(self.save_button)
        self.save_button.clicked.connect(self.on_save)
        
    def on_tab_clicked(self, tab: ImageTab):
        for i in range(self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i).widget()
            if isinstance(item, ImageTab):
                item.set_selected(False)
    
        tab.set_selected(True)
        self.selected_tab = tab
        
        self.save_button.setDisabled(False)
        self.save_button.setStyleSheet(SAVE_BTN_ACTIVE)
        
    def on_save(self):
        if not hasattr(self, "selected_tab"):
            return
        
        new_paths = self.selected_tab.icon_paths
        current_paths = [self.settings.value(k) for k in WEATHER_KEYS]

        if new_paths == current_paths:
            return

        for i, key in enumerate(WEATHER_KEYS):
            self.settings.setValue(key, new_paths[i])

        self.icons_changed.emit()