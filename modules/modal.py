import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
import PyQt6.QtCore as core
import json

from .modal_city_finder import CityFinder


class ModalTab(widgets.QFrame):
    def __init__(self, parent, label: str, on_select = None):
        super().__init__(parent)
        self.setFixedSize(158, 35)
        self.on_select = on_select
        self.set_selected(False)
        
        layout = widgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 0, 0)
        
        self.label = widgets.QLabel(label)
        self.label.setStyleSheet("""
                            color: white;
                            font-family: Roboto;
                            font-size: 16px;
                            font-weight: 400;
                            background: transparent;
                            border: none;
                                """)
        layout.addWidget(self.label)
    
    def set_selected(self, selected: bool):
        if selected:
            self.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border: none; border-radius: 10px")
        else:
            self.setStyleSheet("background: transparent; border: none; border-radius: 10px")
        
    def mousePressEvent(self, event):
        if event.button() == core.Qt.MouseButton.LeftButton and self.on_select:
            self.on_select(self)
        
class Modal(widgets.QWidget):
    city_deleted = core.pyqtSignal(str)
    city_saved = core.pyqtSignal(str)
    def __init__(self, parent=None, on_tab_selected=None, settings=None):
        super().__init__(parent)
        self.setFixedSize(790, 660)
        self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint | core.Qt.WindowType.Tool)
        self.setAttribute(core.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(35, 35, 35);
            }
        """)
        
        self.settings = settings
        self.city_finder = None
        self.on_tab_selected = on_tab_selected
        self.selected_tab = None
        self.right_modal_frame: widgets.QFrame = None

        root_layout = widgets.QVBoxLayout(self)
        root_layout.setContentsMargins(0, 15, 0, 0)
        root_layout.setSpacing(20)

        header = widgets.QFrame(self)
        header.setFixedHeight(28)
        
        header_layout = widgets.QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 12, 0)
        header_layout.setSpacing(0)

        title = widgets.QLabel("Налаштування")
        title.setStyleSheet("""
            color: white;
            font-family: Roboto;
            font-size: 24px;
            font-weight: 500;
            border: none;
            background: transparent;
        """)
        header_layout.addWidget(title, alignment=core.Qt.AlignmentFlag.AlignLeft | core.Qt.AlignmentFlag.AlignVCenter)

        header_layout.addStretch()

        close_btn = widgets.QPushButton()
        close_btn.setIcon(gui.QIcon("media/title_bar/close_button"))
        close_btn.setIconSize(core.QSize(24, 24))
        close_btn.setFixedSize(28, 28)
        close_btn.setCursor(gui.QCursor(core.Qt.CursorShape.PointingHandCursor))
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.2);
            }
        """)
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn, alignment=core.Qt.AlignmentFlag.AlignVCenter)

        root_layout.addWidget(header)

        content = widgets.QWidget(self)
        self.content = content
        content.setStyleSheet("border: none;")
        root_layout.addWidget(content, stretch=1)
        
        content_layout = widgets.QHBoxLayout()
        self.content_layout = content_layout
        content_layout.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        content.setLayout(content_layout)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(15)
        
        left_modal_frame = widgets.QFrame(content)
        left_modal_frame.setFixedWidth(174)

        left_modal_layout = widgets.QVBoxLayout()
        left_modal_layout.setContentsMargins(16,10,0,10)
        left_modal_layout.setSpacing(15)
        left_modal_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        left_modal_frame.setLayout(left_modal_layout)
        
        content_layout.addWidget(left_modal_frame)
        
        tab_names = ["Пошук міста", "Розмір додатку", "Мова додатку", "Списки зображень"]
        for name in tab_names:
            tab = ModalTab(left_modal_frame, name, on_select = self._on_tab_select)
            left_modal_layout.addWidget(tab)
                
                
        vertical_line = widgets.QFrame(content)
        vertical_line.setFixedSize(1, 578)
        vertical_line.setStyleSheet("""
                        background-color: rgba(255, 255, 255, 0.2);
                        """)
        content_layout.addWidget(vertical_line, alignment = core.Qt.AlignmentFlag.AlignLeft)
        
        first_tab = left_modal_layout.itemAt(0).widget()
        self._on_tab_select(first_tab)

        

    def show_below_button(self, button: widgets.QWidget):
        btn_global = button.mapToGlobal(core.QPoint(0, button.height() + 6))
        self.move(btn_global)
        self.show()
        self.raise_()
        
    def _on_tab_select(self, tab: ModalTab):
        if self.selected_tab and self.selected_tab is not tab:
            self.selected_tab.set_selected(False)
        tab.set_selected(True)
        self.selected_tab = tab
        
        if self.right_modal_frame is not None:
            self.right_modal_frame.hide()
            self.content_layout.removeWidget(self.right_modal_frame)
            self.right_modal_frame = None
        
        tab_name = tab.label.text()
        if tab_name == "Пошук міста":
            if self.city_finder is None:
                self.city_finder = CityFinder(self.content, settings=self.settings)
                self.city_finder.added_cities.city_deleted.connect(self.city_deleted)
                self.city_finder.city_saved.connect(self.city_saved)
            self.right_modal_frame = self.city_finder
            
        elif tab_name == "Розмір додатку":
            self.right_modal_frame = widgets.QLabel("Розмір додатку — в розробці", self.content)
            self.right_modal_frame.setStyleSheet("color: white; font-size: 16px;")
            self.right_modal_frame.setFixedSize(544, 578)

        
        elif tab_name == "Мова додатку":
            self.right_modal_frame = widgets.QLabel("Мова додатку — в розробці", self.content)
            self.right_modal_frame.setStyleSheet("color: white; font-size: 16px;")
            self.right_modal_frame.setFixedSize(544, 578)

        
        elif tab_name == "Списки зображень":
            self.right_modal_frame = widgets.QLabel("Списки зображень — в розробці", self.content)
            self.right_modal_frame.setStyleSheet("color: white; font-size: 16px;")
            self.right_modal_frame.setFixedSize(544, 578)
        
        else:
            self.right_modal_frame = widgets.QWidget(self.content)
            self.right_modal_frame.setFixedSize(544, 578)
        
        self.content_layout.addWidget(self.right_modal_frame, alignment=core.Qt.AlignmentFlag.AlignLeft |core.Qt.AlignmentFlag.AlignTop)
        self.right_modal_frame.show()
        