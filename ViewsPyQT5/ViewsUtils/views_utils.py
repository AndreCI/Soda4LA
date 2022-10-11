import os.path
from collections import namedtuple

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from qtpy import QtWidgets, QtCore

GTrackView = namedtuple('gTrack', ["frame", "deleteButton", "selectButton", "hLayout"])

sliderGainStyle = (u"QSlider::groove:horizontal {\n"
                   "    border: 1px solid #999999;\n"
                   "    height: 8px;\n"
                   # /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */\n"
                   "    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);\n"
                   "    margin: 2px 0;\n"
                   "}\n"
                   "QSlider::handle:horizontal {\n"
                   "    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);\n"
                   "    border: 1px solid #5c5c5c;\n"
                   "    width: 18px;\n"
                   "    margin: -2px 0;\n "
                   #"/* handle is placed by default on the contents rect of the groove. Expand outside the groove *"
                   "    border-radius: 3px;\n"
                   "}\n"
                   # "QSlider::groove:horizontal {\n"
                   # "    background: red;\n"
                   # "    position: absolute; /* absolutely position 4px from the left and right of the widget. setting margins on the widget should work too... */\n"
                   # "    left: 4px; right: 4px;\n"
                   # "}\n"
                   "QSlider::add-page:horizontal {\n"
                   "    background: white;\n"
                   "}\n"
                   # "QSlider::sub-page:horizontal {\n"
                   # "    back"
                   # "ground: pink;\n"
                   # "}"
                   )

progressBarStyle = (u"QProgressBar {\n"
                    "    border: 2px solid grey;\n"
                    "    border-radius: 5px;\n"
                    "}\n"
                    "QProgressBar::chunk {\n"
                    "    background-color: #05B8CC;\n"
                    "    width: 100px;\n"
                    "}\n"
                    "QProgressBar {\n"
                    "    border: 2px solid grey;\n"
                    "    border-radius: 5px;\n"
                    "    text-align: center;\n"
                    "}")

buttonStyle = (u"QPushButton{\n"
               "    background-color: grey;\n"
               "    border-style: outset;\n"
               "    border-width: 2px;\n"
               "    border-radius: 10px;\n"
               "    border-color: beige;\n"
               "    padding: 6px;\n"
               "}\n"
               "QPushButton:pressed {\n"
               "    background-color: rgb(224, 0, 0);\n"
               "    border-style: inset;\n"
               "}")

buttonStyle2 = (u"QPushButton{\n"
                "    background-color: grey;\n"
                "    border-style: outset;\n"
                "    border-width: 2px;\n"
                "    border-radius: 1px;\n"
                # "    border-color: red;\n"
                "    border: none;\n"
                "    padding: 6px;\n"
                "}\n"
                "QPushButton:pressed {\n"
                "    background-color: rgb(224, 0, 0);\n"
                "    border-style: inset;\n"
                "}")


def generate_button(parent, width=85, height=85, icon_name="default.png"):
    dbutton = QtWidgets.QPushButton(parent)
    dbutton.setFixedSize(int(width * 1.2), int(height * 1.2))
    # self.pushButton.setObjectName("pushButton")
    label = QLabel(dbutton)
    # label.setStyleSheet("QLabel {background-color: red;}")
    path = os.path.join("data/img/icons", icon_name)
    pixmap = QPixmap(path)
    print(pixmap)
    label.setPixmap(pixmap.scaled(width, height))
    label.setFixedSize(int(width * 1.2), int(height * 1.2))
    label.setAlignment(QtCore.Qt.AlignCenter)
    return dbutton
