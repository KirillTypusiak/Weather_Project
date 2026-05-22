import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui

from utils import request_sender

class RightContainer(widgets.QFrame):
    def __init__(self, parent, city_name):
        super().__init__(parent)
        
        response = request_sender(city_name)

        self.setMinimumWidth(830)
        self.setSizePolicy(widgets.QSizePolicy.Policy.Expanding, widgets.QSizePolicy.Policy.Expanding)
        self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #FFDF56, stop:1 #87CEFA);")

        self.WEATHER_CONTAINER_LAYOUT = widgets.QVBoxLayout(self)
        self.setLayout(self.WEATHER_CONTAINER_LAYOUT)
        self.WEATHER_CONTAINER_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.WEATHER_CONTAINER_LAYOUT.setContentsMargins(15, 15, 15, 15)
        self.WEATHER_CONTAINER_LAYOUT.setSpacing(14)
        
        self.TOP_FRAME = widgets.QFrame(parent = self)
        self.TOP_FRAME.setFixedHeight(36)
        self.TOP_FRAME.setStyleSheet("background-color: pink")
        self.WEATHER_CONTAINER_LAYOUT.addWidget(self.TOP_FRAME)

        self.CENTER_FRAME = widgets.QFrame(parent=self)
        self.CENTER_FRAME.setMinimumHeight(303)
        self.CENTER_FRAME.setStyleSheet("background: transparent")
        self.WEATHER_CONTAINER_LAYOUT.addWidget(self.CENTER_FRAME)
        
        left_center_container = widgets.QFrame(parent = self.CENTER_FRAME)
        left_center_container.setStyleSheet("background-color: rgba(0, 0, 0, 0.1); border-radius: 10px ")
        left_center_container.setMinimumWidth(390)
        left_center_container.setSizePolicy(widgets.QSizePolicy.Policy.Expanding, widgets.QSizePolicy.Policy.Expanding)
        
        left_center_container_layout = widgets.QVBoxLayout()
        left_center_container_layout.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        left_center_container_layout.setContentsMargins(0, 0, 0, 0)
        left_center_container_layout.setSpacing(12)
        left_center_container.setLayout(left_center_container_layout)
        
        if response["cod"] != 404:
            label1 = widgets.QLabel(left_center_container, text = str(response["name"]))
            label1.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            label1.setStyleSheet("""
                                    font-family: Roboto;
                                    font-size: 44px;
                                    font-weight: 500;
                                    line-height: 100%;
                                    letter-spacing: 0%;
                                    vertical-align: middle;
                                    style: medium;
                                    border: none;
                                    background: transparent;
                                    """)
            left_center_container_layout.addWidget(label1)
            
            weather_widget = widgets.QFrame(parent = left_center_container)
            weather_widget.setFixedHeight(87)
            weather_widget.setStyleSheet("background: transparent; border: none")
            left_center_container_layout.addWidget(weather_widget)
            weather_widget_layout = widgets.QHBoxLayout()
            weather_widget_layout.setContentsMargins(0, 0, 0, 0)
            weather_widget_layout.setSpacing(0)
            weather_widget.setLayout(weather_widget_layout)
            
            icon_label = widgets.QLabel(parent = weather_widget)
            icon_label.setFixedSize(87, 87)
            icon_label.setStyleSheet("background: transparent; border: none;")
            icon_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            weather_widget_layout.addWidget(icon_label)
            icon_path = None
            weather_widget_layout.addWidget(icon_label)

            icon_path = None
            if response["weather"][0]["main"] == "Clear":
                icon_path = "media/Sun.png"
            elif response["weather"][0]["main"] == "Clouds" and response["weather"][0]["description"] == "scattered clouds":
                icon_path = "media/Partially_cloudy.png"
            elif response["weather"][0]["main"] == "Clouds" and response["weather"][0]["description"] == "broken clouds":
                icon_path = "media/Cloudy.png"
            elif response["weather"][0]["main"] == "Rain":
                icon_path = "media/Rainy.png"
            elif response["weather"][0]["main"] == "Snow":
                icon_path = "media/Snowy.png"

            if icon_path:
                pixmap = gui.QPixmap(icon_path)
                icon_label.setPixmap(pixmap)
                icon_label.setScaledContents(True)
            
            temp_label = widgets.QLabel(weather_widget, text = str(int(response["main"]["temp"] - 273.3)) + "°")
            temp_label.setStyleSheet("""
                                    font-family: Roboto;
                                    font-size: 74px;
                                    font-weight: 500;
                                    line-height: 100%;
                                    letter-spacing: 0%;
                                    vertical-align: middle;
                                    style: medium;
                                    border: none;
                                    background: transparent;
                                    horizontal-align: center;
                                    """)
            weather_widget_layout.addWidget(temp_label)
            
            label3 = widgets.QLabel(left_center_container, text = str(response["weather"][0]["main"]))
            label3.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            label3.setStyleSheet("""
                                    font-family: Roboto;
                                    font-size: 24px;
                                    font-weight: 500;
                                    line-height: 100%;
                                    letter-spacing: 0%;
                                    vertical-align: middle;
                                    style: medium;
                                    border: none;
                                    background: transparent;
                                    """)
            left_center_container_layout.addWidget(label3)
            
            label4 = widgets.QLabel(left_center_container, text = f"Макс.:{str(int(response["main"]["temp_max"] - 273.3)) + "°"}, Мін.:{str(int(response["main"]["temp_min"] - 273.3)) + "°"}")
            label4.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            label4.setStyleSheet("""
                                    font-family: Roboto;
                                    font-size: 16px;
                                    font-weight: 500;
                                    line-height: 100%;
                                    letter-spacing: 0%;
                                    vertical-align: middle;
                                    style: medium;
                                    border: none;
                                    background: transparent;
                                    """)
            left_center_container_layout.addWidget(label4)


        right_center_container = widgets.QFrame(parent = self.CENTER_FRAME)
        right_center_container.setStyleSheet("background-color: rgba(0, 0, 0, 0.1); border-radius: 10px ")
        right_center_container.setMinimumWidth(390)
        right_center_container.setSizePolicy(widgets.QSizePolicy.Policy.Expanding, widgets.QSizePolicy.Policy.Expanding)
        
        center_frame_layout = widgets.QHBoxLayout(self.CENTER_FRAME)
        center_frame_layout.setContentsMargins(0, 0, 0, 0)
        center_frame_layout.setSpacing(15)
        center_frame_layout.addWidget(left_center_container)
        center_frame_layout.addWidget(right_center_container)
        
        


        self.FOOTER = widgets.QFrame(parent = self)
        self.FOOTER.setMinimumHeight(364)
        self.FOOTER.setStyleSheet("background: transparent")
        self.WEATHER_CONTAINER_LAYOUT.addWidget(self.FOOTER)
        
        footer_layout = widgets.QVBoxLayout(self.FOOTER)
        footer_layout.setContentsMargins(0,0,0,0)
        footer_layout.setSpacing(15)
        

        top_footer = widgets.QFrame()
        top_footer.setMinimumHeight(150)

        top_footer.setStyleSheet("""
            background-color: rgba(0,0,0,0.1);
            border-radius: 10px;
        """)

        bottom_footer = widgets.QFrame()
        bottom_footer.setMinimumHeight(190)

        bottom_footer.setStyleSheet("""
            background-color: rgba(0,0,0,0.1);
            border-radius: 10px;
        """)

        footer_layout.addWidget(top_footer)
        footer_layout.addWidget(bottom_footer)
