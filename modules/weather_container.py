import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import json
from utils import request_sender

class WeatherContainer(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setFixedSize(828, 800)
        self.setStyleSheet("background-color: green")

        self.WEATHER_CONTRINER_LAYOUT = widgets.QVBoxLayout(self)
        self.setLayout(self.WEATHER_CONTRINER_LAYOUT)
        
        self.TOP_FRAME = widgets.QFrame(parent = self)
        self.TOP_FRAME.setFixedSize(788, 36)
        self.TOP_FRAME.setStyleSheet("background-color: pink")
        self.WEATHER_CONTRINER_LAYOUT.addWidget(self.TOP_FRAME)

        self.CENTER_FRAME = widgets.QFrame(parent=self)
        self.CENTER_FRAME.setFixedSize(788, 303)
        self.CENTER_FRAME.setStyleSheet("background-color: blue")
        self.WEATHER_CONTRINER_LAYOUT.addWidget(self.CENTER_FRAME)

        self.CENTER_LAYOUT = widgets.QHBoxLayout(self.CENTER_FRAME)
        self.CENTER_FRAME.setLayout(self.CENTER_LAYOUT)

        response = request_sender("Dnipro")

        print(response)

        if response["cod"] != 404:
            label = widgets.QLabel(self.TOP_FRAME, text = str(response["main"]["temp"]))
            self.CENTER_LAYOUT.addWidget(label)
            
            
            city_label = widgets.QLabel(self.TOP_FRAME, text = str(response["name"]))
            self.CENTER_LAYOUT.addWidget(city_label)
        
        self.FOOTER = widgets.QFrame(parent = self)
        self.FOOTER.setFixedSize(788, 364)
        self.FOOTER.setStyleSheet("background-color: grey")
        self.WEATHER_CONTRINER_LAYOUT.addWidget(self.FOOTER)
