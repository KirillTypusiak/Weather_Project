import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
import datetime

from utils import request_sender


class Weather_Content(widgets.QFrame):
    def __init__(self, parent, city_name):
        super().__init__(parent)

        self.IF_SELECTED = False

        self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #FFDF56, stop:1 #87CEFA); background: transparent; border: 1px solid black; border-radius: 10px ")
        self.setFixedSize(300,90)
        
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
            
            time_difference = response["timezone"]
            current_time = datetime.datetime.now(datetime.timezone.utc)
            local_time = datetime.timezone(datetime.timedelta(seconds = time_difference))
            city_time = current_time.astimezone(local_time).strftime("%H:%M")
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
            
            def set_selected():

                self.IF_SELECTED = not self.IF_SELECTED

                if self.IF_SELECTED:
                    self.setStyleSheet("background-color: rgba(0, 0, 0, 0.1);border: 1px solid black; border-radius: 10px ")
                else:
                    self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #FFDF56, stop:1 #87CEFA); background: transparent; border: 1px solid black; border-radius: 10px ")
            
            
            card_button = widgets.QPushButton(self)
            card_button.setFixedSize(300, 90)
            card_button.setStyleSheet("border-radius: 10px")
            card_button.clicked.connect(set_selected)
        



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
            
        