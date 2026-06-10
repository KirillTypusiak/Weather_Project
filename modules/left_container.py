import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
import PyQt6.QtCore as core

from utils.request import request_sender

from .weather_content import Weather_Content


DEFAULT_CITIES = ["Dnipro", "Bratislava"]


class LeftContainer(widgets.QFrame):
    def __init__(self, parent, on_city_selected=None):
        super().__init__(parent)

        self.setFixedWidth(370)
        self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #808080, stop:1 #5DADE2)")

        self.selected_card = None
        self.on_city_selected = on_city_selected
        self.BUTTON_TOOGLE = False

        # QSettings — зберігає міста між запусками
        self.settings = core.QSettings("MyApp", "WeatherApp")

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

        scroll_area = widgets.QScrollArea(parent=self)
        left_container_layout.addWidget(scroll_area)

        self.scroll_frame = widgets.QFrame(parent=scroll_area)
        scroll_area.setWidget(self.scroll_frame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("background: transparent; border: none")

        self.scroll_layout = widgets.QVBoxLayout()
        self.scroll_frame.setLayout(self.scroll_layout)

        # --- Завантажуємо міста: збережені або дефолтні ---
        saved_cities = self.settings.value("cities", DEFAULT_CITIES)
        for city in saved_cities:
            self._add_card(city)

    def _icon_change(self):
        if self.BUTTON_TOOGLE:
            self.theme_button.setIcon(gui.QIcon("media/title_bar/Dark_theme_button.svg"))
            self.BUTTON_TOOGLE = False
        else:
            self.theme_button.setIcon(gui.QIcon("media/title_bar/Light_theme_button.svg"))
            self.BUTTON_TOOGLE = True

    def _on_card_select(self, city_name, card):
        if self.selected_card and self.selected_card is not card:
            self.selected_card.set_selected(False)
        card.set_selected(True)
        self.selected_card = card
        if self.on_city_selected:
            self.on_city_selected(city_name)

    def _add_card(self, city_name: str):
        card = Weather_Content(
            parent=self.scroll_frame,
            city_name=city_name,
            on_select=self._on_card_select,
        )
        self.scroll_layout.addWidget(card)

    def add_city_card(self, city_name: str):
        current_cities: list = self.settings.value("cities", DEFAULT_CITIES)
        if city_name in current_cities:
            return

        response = request_sender(city_name)
        if response.get("cod") == "404" or response.get("cod") == 404:
            return

        self._add_card(city_name)
        current_cities.append(city_name)
        self.settings.setValue("cities", current_cities)