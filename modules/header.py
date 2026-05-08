import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui

class Header(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("background-color: white")
        self.setFixedSize(self.window().width(), 40)

        layout = widgets.QHBoxLayout()

        layout.setAlignment(core.Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)
        
        close_button = widgets.QPushButton(parent=self)
        close_icon = gui.QIcon("media/title_bar/Close_Button_Hover.svg")
        close_button.setIcon(close_icon)
        layout.addWidget(close_button)
        close_button.setStyleSheet("border:none")

        close_button.clicked.connect(self.window().close)
        
        minimized_button = widgets.QPushButton(parent=self)
        minimized_icon = gui.QIcon("media/title_bar/Minimize_Button_Hover.svg")
        minimized_button.setIcon(minimized_icon)
        layout.addWidget(minimized_button)
        minimized_button.setStyleSheet("border:none")

        minimized_button.clicked.connect(self.window().showMinimized)

        max_button = widgets.QPushButton(parent=self)
        max_close_icon = gui.QIcon("media/title_bar/Maximize_Button_Hover.svg")
        max_button.setIcon(max_close_icon)
        layout.addWidget(max_button)
        max_button.setStyleSheet("border:none")

        max_button.clicked.connect(self.window().showMaximized)
        
    def mousePressEvent(self, event: gui.QMouseEvent):
        if event.button() == core.Qt.MouseButton.LeftButton:
            self.CLICK_COORD = event.position().toPoint()
        else:
            self.CLICK_COORD = None
                
    def mouseMoveEvent(self, event: gui.QMouseEvent):
        window = self.window()
        if self.CLICK_COORD:
            coord = event.position().toPoint() - self.CLICK_COORD
            window.move(window.x() + coord.x(),
                        window.y() + coord.y())