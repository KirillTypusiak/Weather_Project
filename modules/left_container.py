import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
import PyQt6.QtCore as core
import json

from utils.request import request_sender
from utils.request_cities import translate_city_name
from .weather_content import Weather_Content


DEFAULT_CITIES = ["Dnipro", "Bratislava"]


class LeftContainer(widgets.QFrame):
    theme_changed = core.pyqtSignal(bool)
    def __init__(self, parent, on_city_selected=None, settings= None, app_settings=None):
        super().__init__(parent)

        self.setFixedWidth(370)
        self.setStyleSheet("""
                background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #808080, stop:1 #5DADE2);
                "border-bottom-left-radius: 10px;"
                "border-bottom-right-radius: 0"
                
                """)

        self.selected_card = None
        self.on_city_selected = on_city_selected
        self.BUTTON_TOOGLE = False

        # QSettings — зберігає міста між запусками
        self.settings = settings or core.QSettings("MyApp", "WeatherApp")
        print(self.settings.value("cities"))
        self.app_settings = app_settings or core.QSettings("MyApp", "settings")
        
        
        # Временно — очистить кривые данные
        raw = self.settings.value("cities", None)
        if isinstance(raw, list):  # старый формат Python list
            self.settings.setValue("cities", json.dumps(raw))

        button_frame = widgets.QFrame(parent=self)
        button_frame.setFixedSize(330, 44)
        button_frame.setStyleSheet("background: transparent;")

        left_container_layout = widgets.QVBoxLayout()
        self.setLayout(left_container_layout)
        left_container_layout.addWidget(button_frame)
        left_container_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        theme_button = widgets.QPushButton(parent=button_frame)
        theme_button.setFixedSize(52, 24)
        theme_button.setIconSize(core.QSize(52, 24))
        theme_button.setStyleSheet("border: none")
        button_layout = widgets.QHBoxLayout()
        button_frame.setLayout(button_layout)
        button_layout.addWidget(theme_button)
        button_layout.setAlignment(core.Qt.AlignmentFlag.AlignRight)
        theme_button.setIcon(gui.QIcon("media/title_bar/Dark_theme_button.svg"))
        theme_button.clicked.connect(self._icon_change)
        self.theme_button = theme_button
        
        is_dark = self.app_settings.value("theme", "light") == "dark"
        self.BUTTON_TOOGLE = is_dark
        icon = "media/title_bar/Light_theme_button.svg" if is_dark else "media/title_bar/Dark_theme_button.svg"
        self.theme_button.setIcon(gui.QIcon(icon))

        scroll_area = widgets.QScrollArea(parent=self)
        left_container_layout.addWidget(scroll_area)

        self.scroll_frame = widgets.QFrame(parent=scroll_area)
        scroll_area.setWidget(self.scroll_frame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("background: transparent; border: none")

        self.scroll_layout = widgets.QVBoxLayout()
        self.scroll_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(0)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_frame.setLayout(self.scroll_layout)

        saved_cities = self.settings.value("cities", None)
        if saved_cities is None:
            saved_cities = DEFAULT_CITIES
            self.settings.setValue("cities", json.dumps(saved_cities))
        elif isinstance(saved_cities, str):
            try:
                saved_cities = json.loads(saved_cities)
            except Exception:
                saved_cities = DEFAULT_CITIES
        for entry in saved_cities:
            if isinstance(entry, str):
                api_name = entry
                display_name = translate_city_name(api_name)
            else:
                api_name = entry.get("api_name", "")
                display_name = translate_city_name(api_name)
            self._add_card(api_name, display_name=display_name)
        
        is_dark = self.settings.value("theme", "light") == "dark"
        self.BUTTON_TOOGLE = is_dark
        icon = "media/title_bar/Light_theme_button.svg" if is_dark else "media/title_bar/Dark_theme_button.svg"
        self.theme_button.setIcon(gui.QIcon(icon))
            
    def remove_city_card(self, city_name: str):
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget and hasattr(widget, 'city_name') and widget.city_name == city_name:
                if self.selected_card is widget:
                    self.selected_card = None
                self.scroll_layout.removeWidget(widget)
                widget.setParent(None)
                widget.deleteLater()
                break

        raw = self.settings.value("cities", None)
        if isinstance(raw, str):
            try:
                current_cities = json.loads(raw)
            except Exception:
                current_cities = []
        elif isinstance(raw, list):
            current_cities = raw
        else:
            current_cities = []

        if city_name in current_cities:
            current_cities.remove(city_name)
            self.settings.setValue("cities", json.dumps(current_cities))

    def _icon_change(self):
        self.BUTTON_TOOGLE = not self.BUTTON_TOOGLE
        icon = "media/title_bar/Light_theme_button.svg" if self.BUTTON_TOOGLE else "media/title_bar/Dark_theme_button.svg"
        self.theme_button.setIcon(gui.QIcon(icon))
        self.app_settings.setValue("theme", "dark" if self.BUTTON_TOOGLE else "light")
        self.theme_changed.emit(self.BUTTON_TOOGLE)

    def _on_card_select(self, city_name, card):
        if self.selected_card and self.selected_card is not card:
            try:
                self.selected_card.set_selected(False)
            except RuntimeError:
                pass
            self.selected_card = None
        card.set_selected(True)
        self.selected_card = card
        if self.on_city_selected:
            self.on_city_selected(city_name, card.display_name)

    def _add_card(self, city_name: str, display_name: str = ""):
        card = Weather_Content(
            parent=self.scroll_frame,
            city_name=city_name,
            display_name=display_name or city_name,
            on_select=self._on_card_select,
        )
        self.scroll_layout.addWidget(card)
        card.show()
        self.scroll_frame.adjustSize()

    def add_city_card(self, city_name: str):
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget and hasattr(widget, 'city_name') and widget.city_name == city_name:
                return

        # response = request_sender(city_name)
        # if int(response.get("cod")) >= 400 :
        #     return
        

        self._add_card(city_name, display_name = translate_city_name(city_name))

        # Обновляем settings
        raw = self.settings.value("cities", None)
        if isinstance(raw, str):
            try:
                current_cities = json.loads(raw)
            except Exception:
                current_cities = []
        elif isinstance(raw, list):
            current_cities = raw
        else:
            current_cities = list(DEFAULT_CITIES)

        if city_name not in current_cities:
            current_cities.append(city_name)
            self.settings.setValue("cities", json.dumps(current_cities))
    
    def set_theme(self, dark: bool):
        if dark:
            self.setStyleSheet("""
                background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1,
                    stop:0 #4A4A4A, stop:1 #5DADE2);
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 0px;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
            """)
        else:
            self.setStyleSheet("""
                background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1,
                    stop:0 #808080, stop:1 #5DADE2);
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 0px;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
            """)