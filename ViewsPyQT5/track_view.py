from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QGridLayout, QPushButton, QScrollArea, QLabel

from ViewsPyQT5.ViewsUtils.views_utils import generate_button


class TrackOldView(QWidget):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.central_layout = QGridLayout(self)
        self.setFixedSize(600, 850)
        # self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setColumnStretch(0, 1)
        self.central_layout.setColumnStretch(1, 1)
        # self.central_layout.setRowStretch(0, 1)
        # self.central_layout.setRowStretch(1, 1)

        self.select_layout = QVBoxLayout()
        for i in range(20):
            self.select_layout.addWidget(self.get_track_button())

        select_frame = QFrame()
        select_frame.setFrameShape(QFrame.StyledPanel)
        select_frame.setLineWidth(3)
        select_frame.setLayout(self.select_layout)

        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(select_frame)

        track_frame = QFrame()
        track_frame.setFrameShape(QFrame.StyledPanel)
        track_frame.setLineWidth(3)
        self.track_layout = QGridLayout(track_frame)
        tname = QLabel("track name")
        soundfont = QLabel()
        gain = QLabel()
        importb = QPushButton()
        exportb = QPushButton()
        filterb = QPushButton()
        add_button = QPushButton(self)
        self.track_layout.addWidget(add_button)
        detail_frame = QFrame()
        detail_frame.setFrameShape(QFrame.StyledPanel)
        detail_frame.setLineWidth(3)
        self.detail_frame = QGridLayout(detail_frame)

        self.central_layout.addWidget(self.scroll, 0, 0, 2, 1)
        self.central_layout.addWidget(track_frame, 0,1,2,3)
        self.central_layout.addWidget(detail_frame,2,0,3,4)


    def get_track_button(self):
        button = QPushButton(self)
        button.setStyleSheet("background-color: blue")
        deletebutton = QPushButton()
        return button