import os.path

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QGroupBox, QGridLayout, QWidget, QHBoxLayout
from qtpy import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon, QPixmap
import datetime
import locale

def generate_button(parent, width=85, height=85, icon_name="default.png"):
    dbutton =QtWidgets.QPushButton(parent)
    dbutton.setFixedSize(int(width *1.2), int(height *1.2))
    # self.pushButton.setObjectName("pushButton")
    label = QLabel(dbutton)
    #label.setStyleSheet("QLabel {background-color: red;}")
    path = os.path.join("data/img/icons", icon_name)
    pixmap = QPixmap(path)
    print(pixmap)
    label.setPixmap(pixmap.scaled(width, height))
    label.setFixedSize(int(width *1.2), int(height *1.2))
    label.setAlignment(QtCore.Qt.AlignCenter)
    return dbutton