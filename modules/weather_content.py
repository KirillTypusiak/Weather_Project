import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui

class Weather_Content(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("background-color: yellow")
        self.setFixedSize(330,90)
        
        
        