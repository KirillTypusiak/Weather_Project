import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui

from modules.modal import Modal
from utils import request_cities


class TopFrameWidget(widgets.QFrame):
    city_selected = core.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("background: transparent; border: none;")
        self.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Fixed,
        )
        self.setFixedHeight(36)
        
        self.cities_list_widget = None

        # Таймер для затримки запиту (debounce)
        self.timer = core.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.fetch_cities)

        top_frame_layout = widgets.QHBoxLayout()
        top_frame_layout.setContentsMargins(0, 0, 0, 0)
        top_frame_layout.setSpacing(0)
        self.setLayout(top_frame_layout)

        button_widget = widgets.QWidget(self)
        button_layout = widgets.QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        button_widget.setLayout(button_layout)
        top_frame_layout.addWidget(button_widget, alignment=core.Qt.AlignmentFlag.AlignLeft)

        settings_icon = gui.QIcon("media/Settings.png")
        pixmap = gui.QPixmap(settings_icon.pixmap(36, 36))


        settings_button = widgets.QPushButton(self)
        self.settings_button = settings_button
        settings_button.setIcon(gui.QIcon(pixmap))
        settings_button.setIconSize(pixmap.size())
        settings_button.setFixedSize(36, 36)
        settings_button.setStyleSheet("""
                    QPushButton {
                        background: transparent; 
                        border: none; 
                        border-radius: 18px;
                        padding: 0; 
                        margin: 0;
                    }
                    QPushButton:hover {
                        background: rgba(255, 255, 255, 0.1);
                    }
                    QPushButton:pressed {
                        background: rgba(255, 255, 255, 0.2);
            }
                """)

        button_layout.addWidget(settings_button)



        settings_button.setContentsMargins(0, 0, 0, 0)
        button_layout.addWidget(settings_button)
        settings_button.clicked.connect(self.open_settings_modal)
        

        settings_label = widgets.QLabel("Налаштування", self)
        settings_label.setContentsMargins(0, 0, 0, 0)
        settings_label.setIndent(0)
        settings_label.setStyleSheet("""
            font-family: Roboto;
            font-size: 14px;
            font-weight: 500;
            border: none;
            background: transparent;
        """)
        button_layout.addWidget(settings_label)

        self.text_field = widgets.QLineEdit(self)
        self.text_field.addAction(
            gui.QIcon("media/Search Glyph.png"),
            widgets.QLineEdit.ActionPosition.LeadingPosition,
        )
        self.text_field.setClearButtonEnabled(True)
        self.text_field.setFixedSize(261, 36)
        self.text_field.setPlaceholderText("Пошук")
        self.text_field.setStyleSheet("""
            font-family: Roboto;
            font-size: 14px;
            font-weight: 400;
            border: none;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            padding: 5px 10px;
        """)
        top_frame_layout.addWidget(self.text_field, alignment=core.Qt.AlignmentFlag.AlignRight)
        self.text_field.textChanged.connect(self.on_text_changed)
        
    def open_settings_modal(self):
        if not hasattr(self, '_modal') or self._modal is None:
            self._modal = Modal(self.window())
    
        if self._modal.isVisible():
            self._modal.close()
        else:
            self._modal.show_below_button(self.settings_button)

    def reposition_dropdown(self):
        if self.cities_list_widget == None:
            return
        pos = self.text_field.mapTo(self.parent(), core.QPoint(0, self.text_field.height()))
        self.cities_list_widget.move(pos)
        self.cities_list_widget.raise_()

    def on_text_changed(self, text):
        if self.cities_list_widget == None:
            return
        if len(text.strip()) < 2:
            self.timer.stop()
            self.cities_list_widget.hide()
            return

        self.timer.stop()
        self.timer.start(400)

    def fetch_cities(self):
        if self.cities_list_widget == None:
            return
        text = self.text_field.text().strip()
        if not text:
            self.cities_list_widget.hide()
            return

        cities = request_cities(text)
        self.cities_list_widget.clear()

        if not cities:
            self.cities_list_widget.hide()
            return
        
        placeholder = widgets.QListWidgetItem("Результати пошуку")
        placeholder.setForeground(gui.QColor(255, 255, 255, 204))
        font = gui.QFont("Roboto", 12, 400)
        placeholder.setFont(font)
        placeholder.setFlags(core.Qt.ItemFlag.NoItemFlags)
        self.cities_list_widget.addItem(placeholder)

        for city in cities:
            self.cities_list_widget.addItem(city)

        self.reposition_dropdown()
        self.cities_list_widget.show()
        self.cities_list_widget.raise_()

    def on_city_selected(self, item):
        if not (item.flags() & core.Qt.ItemFlag.ItemIsEnabled):
            return
        selected_city = item.text()
        self.cities_list_widget.hide()
        self.text_field.clear()
        self.city_selected.emit(selected_city)
        
    def set_dropdown(self, list_widget):
        self.cities_list_widget = list_widget