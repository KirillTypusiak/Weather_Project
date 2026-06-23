import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
import PyQt6.QtCore as core
import PyQt6.QtWebEngineWidgets as web
import folium
import io
import json

from utils import request_cities
from utils import translater
from utils import get_english_city_name
from utils import translate_city_name
from utils.request_cities import request_countries

# Стили

LABEL_STYLE = """
    font-family: Roboto;
    font-weight: 500;
    font-size: 14px;
    color: rgba(255, 255, 255, 1);
    background: transparent;
    border: none;
"""

FIELD_INPUT_STYLE = """
    QLineEdit {
        border-radius: 4px;
        background-color: rgba(255, 255, 255, 1);
        border: 1px solid rgba(236, 236, 236, 1);
        padding: 8px 10px;
        color: rgba(30, 30, 30, 1);
        font-family: Roboto;
        font-size: 12px;
        font-weight: 400;
    }
    QLineEdit:hover {
        border: 1px solid rgba(180, 180, 180, 1);
    }
    QLineEdit:focus {
        border: 1px solid rgba(150, 150, 150, 1);
    }
"""

DROPDOWN_STYLE = """
    QListWidget {
        background-color: rgba(255, 255, 255, 1);
        border: 1px solid rgba(236, 236, 236, 1);
        border-radius: 4px;
        color: rgba(30, 30, 30, 1);
        font-family: Roboto;
        font-size: 12px;
        outline: none;
    }
    QListWidget::item {
        padding: 6px 10px;
    }
    QListWidget::item:hover {
        background-color: rgba(236, 236, 236, 1);
    }
    QListWidget::item:selected {
        background-color: rgba(210, 210, 210, 1);
        color: rgba(30, 30, 30, 1);
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


# Хелперы

def apply_placeholder_color(widget: widgets.QWidget):
    palette = widget.palette()
    palette.setColor(gui.QPalette.ColorRole.PlaceholderText, gui.QColor(113, 113, 122))
    palette.setColor(gui.QPalette.ColorRole.Highlight, gui.QColor(100, 150, 255, 120))
    palette.setColor(gui.QPalette.ColorRole.HighlightedText, gui.QColor(30, 30, 30))
    widget.setPalette(palette)

def make_label(parent, text: str) -> widgets.QLabel:
    label = widgets.QLabel(text, parent)
    label.setStyleSheet(LABEL_STYLE)
    return label


# Выпадающий список (попап)

class DropdownPopup(widgets.QFrame):
    item_selected = core.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent, core.Qt.WindowType.Popup)
        self.setStyleSheet("border: none;")
        layout = widgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.list_widget = widgets.QListWidget()
        self.list_widget.setStyleSheet(DROPDOWN_STYLE)
        self.list_widget.setFixedWidth(239)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.list_widget)

    def show_items(self, items: list[str], anchor: widgets.QWidget):
        self.list_widget.clear()
        self.list_widget.addItems(items)
        count = min(len(items), 6)
        item_h = 30
        self.list_widget.setFixedHeight(count * item_h if count > 0 else item_h)
        self.setFixedSize(239, count * item_h if count > 0 else item_h)

        global_pos = anchor.mapToGlobal(core.QPoint(0, anchor.height() + 2))
        self.move(global_pos)
        self.show()
        self.raise_()

    def _on_item_clicked(self, item: widgets.QListWidgetItem):
        self.item_selected.emit(item.text())
        self.hide()


# Поле с поиском (страна / город)

class SearchField(widgets.QFrame):
    value_selected = core.pyqtSignal(str)

    def __init__(self, parent, label_text: str, placeholder: str, fetch_fn):
        super().__init__(parent)
        self.setFixedSize(239, 54)
        self.setStyleSheet("background: transparent; border: none")
        self.fetch_fn = fetch_fn
        self._selected_value = None

        layout = widgets.QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        label = make_label(self, label_text)
        layout.addWidget(label, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)

        self.input = widgets.QLineEdit()
        self.input.setClearButtonEnabled(True)
        self.input.setFixedSize(239, 32)
        self.input.setPlaceholderText(placeholder)
        self.input.setStyleSheet(FIELD_INPUT_STYLE)
        apply_placeholder_color(self.input)
        layout.addWidget(self.input)

        self.dropdown = DropdownPopup(self.window())
        self.dropdown.item_selected.connect(self._on_selected)

        #debounce
        self._search_timer = core.QTimer(self)
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self._run_search)

        self.input.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self, text: str):
        self._selected_value = None
        self._search_timer.stop()
        if not text.strip():
            self.dropdown.hide()
            return
        self._search_timer.start(350)
        
    def _on_selected(self, value: str):
        self._selected_value = value
        self.input.blockSignals(True)
        self.input.setText(value)
        self.input.blockSignals(False)
        self.value_selected.emit(value)
        
    def _run_search(self):
        results = self.fetch_fn(self.input.text())
        if results:
            self.dropdown.show_items(results, self.input)
        else:
            self.dropdown.hide()

    def selected_value(self) -> str | None:
        return self._selected_value

    def clear(self):
        self._selected_value = None
        self.input.blockSignals(True)
        self.input.clear()
        self.input.blockSignals(False)


# Карточка города

class CityCard(widgets.QFrame):
    clicked = core.pyqtSignal(str)
    deleted = core.pyqtSignal(str)

    def __init__(self, parent, api_name: str, display_name: str):
        super().__init__(parent)
        self.city_name = api_name
        self.api_name = api_name
        self.setFixedHeight(44)
        self.setCursor(gui.QCursor(core.Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            }
            QFrame:hover {
                background: rgba(255, 255, 255, 0.05);
            }
        """)

        layout = widgets.QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)

        name_label = widgets.QLabel(display_name)
        name_label.setStyleSheet("""
            color: white;
            font-family: Roboto;
            font-size: 14px;
            font-weight: 400;
            background: transparent;
            border: none;
        """)
        layout.addWidget(name_label)
        layout.addStretch()

        trash_btn = widgets.QPushButton()
        trash_btn.setFixedSize(24, 24)
        trash_btn.setIcon(gui.QIcon("media/trash.png"))
        trash_btn.setIconSize(core.QSize(16, 16))
        trash_btn.setCursor(gui.QCursor(core.Qt.CursorShape.PointingHandCursor))
        trash_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: rgba(255, 80, 80, 0.2);
            }
        """)
        trash_btn.clicked.connect(lambda: self.deleted.emit(self.api_name))
        layout.addWidget(trash_btn)

    def mousePressEvent(self, event):
        if event.button() == core.Qt.MouseButton.LeftButton:
            self.clicked.emit(self.city_name)


# Виджет "Додані міста"

class AddedCitiesWidget(widgets.QScrollArea):
    city_clicked = core.pyqtSignal(str)
    city_deleted = core.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("""
            QScrollArea {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                border: none;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                margin: 4px 2px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.25);
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.4);
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        

        self._container = widgets.QWidget()
        self._container.setStyleSheet("background: transparent; border: none;")
        self._container.setFixedWidth(544)
        self.cards_layout = widgets.QVBoxLayout(self._container)
        self.cards_layout.setSpacing(0)
        self.cards_layout.setContentsMargins(0, 8, 0, 8)
        self.cards_layout.addStretch()

        self.setWidget(self._container)
        self.setFixedWidth(544)
        self.setFixedHeight(200)
        self._cards: dict[str, CityCard] = {}

    def add_city(self, api_name: str, display_name: str = None):
        if api_name in self._cards:
            return
        card = CityCard(self, api_name, display_name or api_name)
        card.clicked.connect(self.city_clicked)
        card.deleted.connect(self._remove_city)
        self._cards[api_name] = card
        self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)
        
    def city_pairs(self) -> list[tuple[str, str]]:
        return [(api_name, card.city_name) for api_name, card in self._cards.items()]

    def _remove_city(self, city_name: str):
        card = self._cards.pop(city_name, None)
        if card:
            card.setParent(None)
        self.city_deleted.emit(city_name)

    def city_names(self) -> list[str]:
        return list(self._cards.keys())


# Основной виджет

# Утилита для получения стран из данных request_cities
def _get_all_countries() -> list[str]:
    try:
        import requests
        response = requests.get("https://countriesnow.space/api/v0.1/countries", timeout=10)
        data = response.json()
        return [item["country"] for item in data["data"]]
    except Exception:
        return []


def _get_cities_for_country(country: str) -> list[str]:
    try:
        import requests
        response = requests.post(
            "https://countriesnow.space/api/v0.1/countries/cities",
            json={"country": country},
            timeout=10
        )
        data = response.json()
        return data.get("data", [])
    except Exception:
        return []


def _geocode_city(city: str) -> tuple[float, float] | None:
    try:
        import requests
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": city, "format": "json", "limit": 1},
            headers={"User-Agent": "CityFinderApp/1.0"},
            timeout=10
        )
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None


class CityFinder(widgets.QFrame):
    city_saved = core.pyqtSignal(str)
    def __init__(self, parent, settings=None):
        super().__init__(parent)
        self.setFixedWidth(544)

        self._settings = settings or core.QSettings("MyApp", "WeatherApp")
        self._country_codes: dict[str, str] = {}
        self._selected_country_code: str | None = None
        self._all_countries: list[str] = []
        self._cities_for_country: list[str] = []
        self._selected_country: str | None = None
        self._selected_city: str | None = None
        self._selected_coord: str | None = None
        
        

        root_layout = widgets.QVBoxLayout(self)
        root_layout.setContentsMargins(0, 16, 0, 0)
        root_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)
        root_layout.setSpacing(10)

        # Заголовок
        search_title = widgets.QLabel(translater("modal_city_finder", "search_city_title"))
        search_title.setStyleSheet("""
            font-size: 18px;
            font-weight: 400;
            color: white;
            font-family: Roboto;
        """)
        root_layout.addWidget(search_title, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)
        root_layout.addSpacing(8)

        # Средний фрейм
        middle_frame = widgets.QFrame(self)
        middle_frame.setFixedWidth(544)
        middle_frame_layout = widgets.QHBoxLayout(middle_frame)
        middle_frame_layout.setSpacing(16)
        middle_frame_layout.setContentsMargins(0, 0, 0, 0)
        middle_frame.setStyleSheet("background: transparent; border: none")
        root_layout.addWidget(middle_frame, alignment=core.Qt.AlignmentFlag.AlignTop)

        # Левая часть
        left_frame = widgets.QFrame(middle_frame)
        left_frame.setFixedWidth(239)
        left_frame.setStyleSheet("background: transparent; border: none")
        left_layout = widgets.QVBoxLayout(left_frame)
        left_layout.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        left_layout.setSpacing(12)
        left_layout.setContentsMargins(0, 0, 0, 0)
        middle_frame_layout.addWidget(left_frame)

        # Поле страны
        self.country_field = SearchField(
            left_frame, translater("modal_city_finder", "country"), translater("modal_city_finder", "select_country"),
            self._search_country
        )
        self.country_field.value_selected.connect(self._on_country_selected)
        left_layout.addWidget(self.country_field)

        # Поле города
        self.city_field = SearchField(
            left_frame, translater("modal_city_finder", "city"), translater("modal_city_finder", "select_city"),
            self._search_city
        )
        self.city_field.value_selected.connect(self._on_city_selected)
        left_layout.addWidget(self.city_field)

        # Поле координат
        coord_frame = widgets.QFrame(left_frame)
        coord_frame.setFixedSize(239, 54)
        coord_frame.setStyleSheet("background: transparent; border: none")
        coord_layout = widgets.QVBoxLayout(coord_frame)
        coord_layout.setSpacing(5)
        coord_layout.setContentsMargins(0, 0, 0, 0)
        coord_label = make_label(coord_frame, translater("modal_city_finder", "coordinates"))
        coord_layout.addWidget(coord_label, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)
        self.coord_input = widgets.QLineEdit()
        self.coord_input.textChanged.connect(self._on_coord_changed)
        self.coord_input.setFixedSize(239, 32)
        self.coord_input.setPlaceholderText("WGS 84 / UTM / MGRS")
        self.coord_input.setStyleSheet(FIELD_INPUT_STYLE)
        apply_placeholder_color(self.coord_input)
        coord_layout.addWidget(self.coord_input)
        left_layout.addWidget(coord_frame)

        # Кнопка Зберегти
        self.save_btn = widgets.QPushButton(translater("modal_city_finder", "save"))
        self.save_btn.setFixedSize(130, 38)
        self.save_btn.setCursor(gui.QCursor(core.Qt.CursorShape.PointingHandCursor))
        self.save_btn.setStyleSheet(SAVE_BTN_INACTIVE)
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self._on_save)
        left_layout.addWidget(self.save_btn, alignment = core.Qt.AlignmentFlag.AlignBottom)

        # Правая часть — карта
        right_frame = widgets.QFrame(middle_frame)
        right_frame.setFixedSize(289, 256)
        right_frame.setStyleSheet("background: transparent; border: none")
        right_layout = widgets.QVBoxLayout(right_frame)
        right_layout.setContentsMargins(0, 0, 0, 0)
        middle_frame_layout.addWidget(right_frame)

        self.map_view = web.QWebEngineView()
        self.map_view.setFixedSize(289, 256)
        right_layout.addWidget(self.map_view)
        self._show_default_map()

        # Секция "Додані міста"
        added_title = widgets.QLabel(translater("modal_city_finder", "added_cities"))
        added_title.setStyleSheet("""
            font-size: 18px;
            font-weight: 400;
            color: white;
            font-family: Roboto;
        """)
        root_layout.addSpacing(12) 
        root_layout.addWidget(added_title, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.added_cities = AddedCitiesWidget(self)
        root_layout.addWidget(self.added_cities)
        self.added_cities.city_clicked.connect(self._on_card_clicked)
        self.added_cities.city_deleted.connect(self._on_card_deleted)

        # Загрузка стран и сохранённых городов
        self._load_countries()
        self._restore_cities()

    #Поиск
    def _search_country(self, text: str) -> list[str]:
        if len(text) < 1:
            return []
        results = request_countries(text)
        self._country_codes = {item["name"]: item["code"] for item in results}
        return [item["name"] for item in results]
    
    def _search_city(self, text: str) -> list[str]:
        if len(text) < 2:
            return []
        return request_cities(text, country_code=self._selected_country_code)


    #Колбеки

    def _on_country_selected(self, country: str):
        self._selected_country = country
        self._selected_country_code = self._country_codes.get(country)
        self._selected_city = None
        self.city_field.clear()
        self._update_save_btn()

        # Загружаем города для страны в фоне
        loader = core.QThread.currentThread()
        self._cities_for_country = []
        worker = _CitiesLoader(country)
        worker.finished.connect(self._on_cities_loaded)
        worker.start()
        self._worker = worker  # держим ссылку

    def _on_cities_loaded(self, cities: list[str]):
        self._cities_for_country = cities

    def _on_city_selected(self, city: str):
        self._selected_city = city
        self._update_save_btn()
        coords = _geocode_city(city)
        if coords:
            lat, lon = coords
            self.coord_input.blockSignals(True)
            self.coord_input.setText(f"{lat}, {lon}")
            self.coord_input.blockSignals(False)
            self._show_map(lat, lon, city)
        
    def _on_coord_changed(self, text: str):
        try:
            parts = text.strip().split(",")
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            self._selected_coord = (lat, lon)
            self._show_map(lat, lon, "")
            self._update_save_btn()
        except (ValueError, IndexError):
            self._selected_coord = None
            self._update_save_btn()

    def _update_save_btn(self):
        ready = bool(self._selected_country and self._selected_city or self._selected_coord)
        self.save_btn.setEnabled(ready)
        self.save_btn.setStyleSheet(SAVE_BTN_ACTIVE if ready else SAVE_BTN_INACTIVE)

    def _on_save(self):
        if not self._selected_city:
            return
        api_name = get_english_city_name(self._selected_city)
        display_name = self._selected_city
        self.added_cities.add_city(api_name, display_name)  # ← было self._selected_city
        self._persist_cities()
        self.city_saved.emit(api_name)
        self.country_field.clear()
        self.city_field.clear()
        self._selected_country = None
        self._selected_city = None
        self._update_save_btn()

    def _on_card_clicked(self, city_name: str):
        coords = _geocode_city(city_name)
        if coords:
            self._show_map(*coords, city_name)

    def _on_card_deleted(self, city_name: str):
        self._persist_cities()

    #Карта
    def _show_default_map(self):
        self._show_map(48.3794, 31.1656, "Україна")

    def _show_map(self, lat: float, lon: float, label: str = ""):
        m = folium.Map(location=[lat, lon], zoom_start=12, tiles="OpenStreetMap")
        if label:
            folium.Marker([lat, lon], tooltip=label).add_to(m)
        html = m._repr_html_()
        self.map_view.setHtml(html)

    #Персистентность

    def _persist_cities(self):
        cities_data = [
            {"api_name": api_name, "display_name": display_name}
            for api_name, display_name in self.added_cities.city_pairs()
        ]
        self._settings.setValue("cities", json.dumps(self.added_cities.city_names()))

    def _restore_cities(self):
        raw = self._settings.value("cities", "[]")
        try:
            cities = json.loads(raw)
            for entry in cities:
                if isinstance(entry, str):
                    api_name = entry
                    display_name = translate_city_name(api_name)
                else:
                    api_name = entry.get("api_name", "")
                    display_name = translate_city_name(api_name)
                self.added_cities.add_city(api_name, display_name)
        except Exception:
            pass

    #Загрузка стран

    def _load_countries(self):
        self._countries_loader = _CountriesLoader()
        self._countries_loader.finished.connect(lambda countries: setattr(self, "_all_countries", countries))
        self._countries_loader.start()


# Фоновые загрузчики

class _CountriesLoader(core.QThread):
    finished = core.pyqtSignal(list)

    def run(self):
        countries = _get_all_countries()
        self.finished.emit(countries)


class _CitiesLoader(core.QThread):
    finished = core.pyqtSignal(list)

    def __init__(self, country: str):
        super().__init__()
        self.country = country

    def run(self):
        cities = _get_cities_for_country(self.country)
        self.finished.emit(cities)