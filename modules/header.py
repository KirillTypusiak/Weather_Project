import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui


class Header(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setFixedHeight(40)

        self.setStyleSheet("""
            background: transparent;
            border: none;
        """)

        main_layout = widgets.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        left_header = widgets.QFrame()
        left_header.setFixedWidth(370)
        #тут изменил
        left_header.setStyleSheet("""
            background: qlineargradient(
                x1:1, y1:0,
                x2:0, y2:1,
                stop:0 #7e8680,
                stop:1 #6da6c8
            );
        """)

        right_header = widgets.QFrame()

        right_header.setStyleSheet("""
            background: qlineargradient(
                x1:1, y1:0,
                x2:0, y2:1,
                stop:0 #efd95f,
                stop:1 #b8d0b1
            );
        """)

        main_layout.addWidget(left_header)
        main_layout.addWidget(right_header)

        left_layout = widgets.QHBoxLayout(left_header)
        left_layout.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        left_layout.setContentsMargins(5, 0, 0, 0)

        close_button = widgets.QPushButton()
        close_button.setIcon(gui.QIcon("media/title_bar/Close_Button_Hover.svg"))
        close_button.setStyleSheet("border:none;")
        left_layout.addWidget(close_button)

        close_button.clicked.connect(self.window().close)
        minimized_button = widgets.QPushButton()
        minimized_button.setIcon(gui.QIcon("media/title_bar/Minimize_Button_Hover.svg"))
        minimized_button.setStyleSheet("border:none;")
        left_layout.addWidget(minimized_button)

        minimized_button.clicked.connect(self.window().showMinimized)

        max_button = widgets.QPushButton()
        max_button.setIcon(gui.QIcon("media/title_bar/Maximize_Button_Hover.svg"))
        max_button.setStyleSheet("border:none;")
        left_layout.addWidget(max_button)
        #тут что бы окно возвращалось 
        def toggle_window():
            if self.window().isMaximized():
                self.window().showNormal()
            else:
                self.window().showMaximized()

        max_button.clicked.connect(toggle_window)

    def mousePressEvent(self, event: gui.QMouseEvent):
        if event.button() == core.Qt.MouseButton.LeftButton:
            self.CLICK_COORD = event.position().toPoint()
        else:
            self.CLICK_COORD = None

    def mouseMoveEvent(self, event: gui.QMouseEvent):
        window = self.window()

        if self.CLICK_COORD:
            coord = event.position().toPoint() - self.CLICK_COORD

            window.move(
                window.x() + coord.x(),
                window.y() + coord.y()
            )