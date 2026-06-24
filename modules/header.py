import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui


class Header(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(40)
        self._dark = False
        
        self.setStyleSheet("background: transparent; border: none; border-radius: 10px;")

        main_layout = widgets.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        left_header = widgets.QFrame()
        left_header.setFixedWidth(370)
        left_header.setStyleSheet("background: transparent; border: none; border-top-left-radius: 10px;")

        right_header = widgets.QFrame()
        right_header.setStyleSheet("background: transparent; border: none; border-top-right-radius: 10px;")

        main_layout.addWidget(left_header)
        main_layout.addWidget(right_header, stretch=1)

        left_layout = widgets.QHBoxLayout(left_header)
        left_layout.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        left_layout.setContentsMargins(5, 0, 0, 0)

        close_button = widgets.QPushButton()
        close_button.setIcon(gui.QIcon("media/title_bar/Close_Button_Hover.svg"))
        close_button.setStyleSheet("border:none; background: transparent;")
        left_layout.addWidget(close_button)
        close_button.clicked.connect(self.window().close)

        minimized_button = widgets.QPushButton()
        minimized_button.setIcon(gui.QIcon("media/title_bar/Minimize_Button_Hover.svg"))
        minimized_button.setStyleSheet("border:none; background: transparent;")
        left_layout.addWidget(minimized_button)
        minimized_button.clicked.connect(self.window().showMinimized)

        max_button = widgets.QPushButton()
        max_button.setIcon(gui.QIcon("media/title_bar/Maximize_Button_Hover.svg"))
        max_button.setStyleSheet("border:none; background: transparent;")
        left_layout.addWidget(max_button)
        self.set_theme(self._dark)

        def toggle_window():
            if self.window().isMaximized():
                self.window().showNormal()
            else:
                self.window().showMaximized()
        max_button.clicked.connect(toggle_window)

    def set_theme(self, dark: bool):
        self._dark = dark
        self.update()  # перемалювати

    # def paintEvent(self, event):
    #     painter = gui.QPainter(self)
    #     painter.setRenderHint(gui.QPainter.RenderHint.Antialiasing)

    #     rect = self.rect()
    #     gradient = gui.QLinearGradient(rect.width(), 0, 0, rect.height())

    #     if self._dark:
    #         gradient.setColorAt(0, gui.QColor("#4A4A4A"))
    #         gradient.setColorAt(1, gui.QColor("#5DADE2"))
    #     else:
    #         gradient.setColorAt(0, gui.QColor("#efd95f"))
    #         gradient.setColorAt(1, gui.QColor("#5DADE2"))
            
    #     painter.fillRect(rect, gradient)
    #     painter.end()
    def set_theme(self, dark: bool):
        if dark:
            self.setStyleSheet("""
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #5DADE2, stop:1 #4A4A4A);
                border-top-right-radius: 10px;
                border-top-left-radius: 10px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            """)
        else:
            self.setStyleSheet("""
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #87CEFA, stop:1 #FFDF56);
                border-top-right-radius: 10px;
                border-top-left-radius: 10px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            """)

    def mousePressEvent(self, event):
        if event.button() == core.Qt.MouseButton.LeftButton:
            self.CLICK_COORD = event.position().toPoint()
        else:
            self.CLICK_COORD = None

    def mouseMoveEvent(self, event):
        if self.CLICK_COORD:
            coord = event.position().toPoint() - self.CLICK_COORD
            window = self.window()
            window.move(window.x() + coord.x(), window.y() + coord.y())