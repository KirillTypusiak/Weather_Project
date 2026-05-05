import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui

class Weather_content(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("background-color: white")
        self.setFixedSize(300,100)

        self.content = widgets.QWidget(parent=self)
        self.layout_content = widgets.QVBoxLayout(self.content)
        