import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as QtGui
import PyQt6.QtCore as core
import PyQt6.QtWebEngineWidgets as WebEngine

import io
import folium


class LeftContainer(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setFixedSize(370, 800)
        self.setStyleSheet("background-color: red")
        
        self.open_modal_button = widgets.QPushButton(parent = self, text = "Открыть окно")
        self.open_modal_button.setGeometry(50,50,150,40)
        self.open_modal_button.clicked.connect(self.open_modal)

    def open_modal(self):

        main_window = self.window()
        
        self.MODAL = widgets.QWidget(main_window)
        self.MODAL.setGeometry(10,10, 790, 688)
        self.MODAL.setStyleSheet("background-color: white")
        modal_layout = widgets.QVBoxLayout()
        modal_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        
        # scroll = QScrollArea()
        # scroll.setWidgetResizable(True)

        
        
        
        self.MODAL.setLayout(modal_layout)
        
        header_frame = widgets.QFrame(parent = self.MODAL)
        frame_layout = widgets.QHBoxLayout()
        frame_layout.setAlignment(core.Qt.AlignmentFlag.AlignRight)
        header_frame.setLayout(frame_layout)
        header_frame.setFixedSize(742, 28)
        modal_layout.addWidget(header_frame)
        header_frame.setStyleSheet("background-color: cyan")
        
        close_button = widgets.QPushButton(parent = header_frame)
        frame_layout.addWidget(close_button)
        close_button.setFixedSize(24, 24)
        
        icon = QtGui.QIcon("media/close.svg")
        close_button.setIcon(icon)
        close_button.clicked.connect(self.MODAL.hide)
        
        data = io.BytesIO()

        map = folium.Map(location = (50, 50))
        
        map.save(data,close_file = False)

        self.MODAL.show()
        web_engine_view = WebEngine.QWebEngineView(parent = self.MODAL)
        web_engine_view.setFixedSize(289,256)
        modal_layout.addWidget(web_engine_view)