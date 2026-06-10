import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
import datetime
import json

from utils import request_sender


class Weather_Content(widgets.QFrame):
    def __init__(self, parent, city_name, on_select = None):
        super().__init__(parent)

        self.on_select = on_select  # callback из LeftContainer

        # self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #FFDF56, stop:1 #87CEFA); background: transparent; border: 1px solid black; border-radius: 10px ")
        self.setStyleSheet("background: transparent; border: none; border-radius: 10px")
        self.setFixedSize(320,90)
        
        main_layout = widgets.QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
        main_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        
        left_card = widgets.QFrame(self)
        left_card.setFixedHeight(90)
        left_card.setStyleSheet("background: transparent; border: None; border-radius: 10px ")
        main_layout.addWidget(left_card, stretch = 1)
        
        right_card = widgets.QFrame(self)
        right_card.setFixedHeight(90)
        right_card.setStyleSheet("background: transparent; border: None; border-radius: 10px ")
        main_layout.addWidget(right_card, stretch = 1)
        
        response = request_sender(city_name)
        self.timezone_offset = response.get("timezone", 0) if isinstance(response, dict) else 0
        self.clock_timer = core.QTimer(self)
        self.clock_timer.timeout.connect(self.update_city_time)
        self.clock_timer.start(1000)
        # print(json.dumps(response, indent = 4))
        
        left_card_layout = widgets.QVBoxLayout()
        left_card_layout.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        left_card_layout.setSpacing(6)
        left_card_layout.setContentsMargins(15,10,15,10)
        
        left_card.setLayout(left_card_layout)
        
        if response["cod"] != 404:
            label1 = widgets.QLabel(left_card, text = str(response["name"]))
            
            label1.setStyleSheet("""
                font-family: Roboto;
                font-size: 20px;
                font-weight: 400;
                color: white;
                
            """)
            
            current_time = self.city_datetime()
            city_time = current_time.strftime("%H:%M")
            label2 = widgets.QLabel(left_card, text = str(city_time))
            label2.setFixedSize(100, 14)
            label2.setStyleSheet(
                """font-family: Roboto; 
                font-size: 10px; 
                font-weight: 300; 
                color: #white
                background: transparent
            """)
            
            label3 = widgets.QLabel(left_card, text = str(response["weather"][0]["main"]))
            
            label3.setStyleSheet("""
                font-family: Roboto;
                font-size: 10px;
                font-weight: 300;
                color: white;
                background: transparent
            """)
            
            left_card_layout.addWidget(label1)
            left_card_layout.addWidget(label2)
            left_card_layout.addWidget(label3)
            self.city_time_label = label2
            
            card_button = widgets.QPushButton(self)
            card_button.setFixedSize(320, 90)
            card_button.setStyleSheet("border-radius: 10px")
            card_button.clicked.connect(lambda _, city=city_name, card=self: self.on_select(city, card) if self.on_select else None)
            card_button.raise_()



        right_card_layout = widgets.QVBoxLayout()
        right_card_layout.setAlignment(core.Qt.AlignmentFlag.AlignRight)
        right_card_layout.setSpacing(5)
        
        right_card.setLayout(right_card_layout)
        
        if response["cod"] != 404:
            label1 = widgets.QLabel(right_card, text = str(int(response["main"]["temp"] - 273.3)) + "°")
            label1.setAlignment(core.Qt.AlignmentFlag.AlignRight)
            label1.setStyleSheet("""
                font-family: Roboto;
                font-size: 42px;
                font-weight: 400;
                color: white;
                background: transparent
            """)


            label2 = widgets.QLabel(right_card, text = f"Макс.:{str(int(response["main"]["temp_max"] - 273.3)) + "°"}, Мін.:{str(int(response["main"]["temp_min"] - 273.3)) + "°"}")
            
            label2.setStyleSheet("""
                font-family: Roboto;
                font-size: 16px;
                font-weight: 500;
                color: white;
                background: transparent                
            """)
            
            right_card_layout.setContentsMargins(0,0,0,0)
            right_card_layout.addWidget(label1)
            right_card_layout.addWidget(label2)
            
            bottom_line = widgets.QFrame(self)

            bottom_line.setGeometry(10, 88, 300, 1)

            bottom_line.setStyleSheet("""
                background-color: rgba(255,255,255,0.15);
                border: none;
            """)    

    def city_datetime(self):
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        local_tz = datetime.timezone(datetime.timedelta(seconds=self.timezone_offset))
        return utc_now.astimezone(local_tz)

    def update_city_time(self):
        if hasattr(self, 'city_time_label'):
            self.city_time_label.setText(self.city_datetime().strftime("%H:%M"))

    def set_selected(self, selected: bool):
        if selected:
            self.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border: none; border-radius: 10px")
        else:
            self.setStyleSheet("background: transparent; border: none; border-radius: 10px")

