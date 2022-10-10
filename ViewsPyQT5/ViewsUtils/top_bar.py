# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy, QAbstractScrollArea, QWidget, \
    QPushButton, QSpacerItem, QFrame, QLineEdit, QComboBox, QSlider, QGridLayout, QLayout, QProgressBar


################################################################################
##  generated from reading UI file 'topsettingszfbzda.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

class TopSettingsBar(object):
    def setupUi(self):
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.TopControlFrame = QFrame()
        self.TopControlFrame.setObjectName(u"TopControlFrame")
        self.TopControlFrame.setFrameShape(QFrame.Panel)
        self.TopControlFrame.setFrameShadow(QFrame.Raised)
        self.TopControlFrame.setLineWidth(3)
        self.TopControlFrame.setMaximumSize(16777215, 40)
        self.horizontalLayout_3 = QHBoxLayout(self.TopControlFrame)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.LeftSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.LeftSpacer)

        self.AddTrackButton = QPushButton(self.TopControlFrame)
        self.AddTrackButton.setObjectName(u"AddTrackButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddTrackButton.sizePolicy().hasHeightForWidth())
        self.AddTrackButton.setSizePolicy(sizePolicy)
        self.AddTrackButton.setMinimumSize(QSize(0, 0))
        self.AddTrackButton.setMaximumSize(QSize(36, 16777215))
        self.AddTrackButton.setStyleSheet(u"QPushButton{\n"
                                          "    background-color: red;\n"
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
        icon = QIcon()
        icon.addFile(u"../../icons/circle-add.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.AddTrackButton.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.AddTrackButton)

        self.SettingsButton = QPushButton(self.TopControlFrame)
        self.SettingsButton.setObjectName(u"SettingsButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.SettingsButton.sizePolicy().hasHeightForWidth())
        self.SettingsButton.setSizePolicy(sizePolicy1)
        self.SettingsButton.setMinimumSize(QSize(0, 0))
        self.SettingsButton.setMaximumSize(QSize(36, 16777215))
        self.SettingsButton.setStyleSheet(u"QPushButton{\n"
                                          "    background-color: red;\n"
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
        icon1 = QIcon()
        icon1.addFile(u"../../icons/settings.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.SettingsButton.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.SettingsButton)

        self.MusicProgressBar = QProgressBar(self.TopControlFrame)
        self.MusicProgressBar.setObjectName(u"MusicProgressBar")
        self.MusicProgressBar.setValue(24)

        self.horizontalLayout_3.addWidget(self.MusicProgressBar)

        self.FbwButton = QPushButton(self.TopControlFrame)
        self.FbwButton.setObjectName(u"FbwButton")
        sizePolicy.setHeightForWidth(self.FbwButton.sizePolicy().hasHeightForWidth())
        self.FbwButton.setSizePolicy(sizePolicy)
        self.FbwButton.setMinimumSize(QSize(0, 0))
        self.FbwButton.setMaximumSize(QSize(36, 16777215))
        self.FbwButton.setStyleSheet(u"QPushButton{\n"
                                     "    background-color: red;\n"
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
        icon2 = QIcon()
        icon2.addFile(u"../../icons/previous.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.FbwButton.setIcon(icon2)

        self.horizontalLayout_3.addWidget(self.FbwButton)

        self.PPButton = QPushButton(self.TopControlFrame)
        self.PPButton.setObjectName(u"PPButton")
        sizePolicy.setHeightForWidth(self.PPButton.sizePolicy().hasHeightForWidth())
        self.PPButton.setSizePolicy(sizePolicy)
        self.PPButton.setMinimumSize(QSize(0, 0))
        self.PPButton.setMaximumSize(QSize(36, 16777215))
        self.PPButton.setStyleSheet(u"QPushButton{\n"
                                    "    background-color: red;\n"
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
        icon3 = QIcon()
        icon3.addFile(u"../../icons/pause.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.PPButton.setIcon(icon3)

        self.horizontalLayout_3.addWidget(self.PPButton)

        self.StopButton = QPushButton(self.TopControlFrame)
        self.StopButton.setObjectName(u"StopButton")
        sizePolicy.setHeightForWidth(self.StopButton.sizePolicy().hasHeightForWidth())
        self.StopButton.setSizePolicy(sizePolicy)
        self.StopButton.setMinimumSize(QSize(0, 0))
        self.StopButton.setMaximumSize(QSize(36, 16777215))
        self.StopButton.setStyleSheet(u"QPushButton{\n"
                                      "    background-color: red;\n"
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
        icon4 = QIcon()
        icon4.addFile(u"../../icons/stop.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.StopButton.setIcon(icon4)
        self.StopButton.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.StopButton)

        self.FfwButton = QPushButton(self.TopControlFrame)
        self.FfwButton.setObjectName(u"FfwButton")
        sizePolicy.setHeightForWidth(self.FfwButton.sizePolicy().hasHeightForWidth())
        self.FfwButton.setSizePolicy(sizePolicy)
        self.FfwButton.setMinimumSize(QSize(0, 0))
        self.FfwButton.setMaximumSize(QSize(36, 16777215))
        self.FfwButton.setStyleSheet(u"QPushButton{\n"
                                     "    background-color: red;\n"
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
        icon5 = QIcon()
        icon5.addFile(u"../../icons/next.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.FfwButton.setIcon(icon5)

        self.horizontalLayout_3.addWidget(self.FfwButton)

        self.GainSlider = QSlider(self.TopControlFrame)
        self.GainSlider.setObjectName(u"GainSlider")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.GainSlider.sizePolicy().hasHeightForWidth())
        self.GainSlider.setSizePolicy(sizePolicy2)
        self.GainSlider.setMinimumSize(QSize(100, 0))
        self.GainSlider.setStyleSheet(u"QSlider::groove:horizontal {\n"
                                      "    border: 1px solid #999999;\n"
                                      "    height: 8px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */\n"
                                      "    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);\n"
                                      "    margin: 2px 0;\n"
                                      "}\n"
                                      "QSlider::handle:horizontal {\n"
                                      "    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);\n"
                                      "    border: 1px solid #5c5c5c;\n"
                                      "    width: 18px;\n"
                                      "    margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */\n"
                                      "    border-radius: 3px;\n"
                                      "}\n"
                                      "\n"
                                      "QSlider::groove:horizontal {\n"
                                      "    background: red;\n"
                                      "    position: absolute; /* absolutely position 4px from the left and right of the widget. setting margins on the widget should work too... */\n"
                                      "    left: 4px; right: 4px;\n"
                                      "}\n"
                                      "\n"
                                      "\n"
                                      "QSlider::add-page:horizontal {\n"
                                      "    background: white;\n"
                                      "}\n"
                                      "\n"
                                      "QSlider::sub-page:horizontal {\n"
                                      "    back"
                                      "ground: pink;\n"
                                      "}")
        self.GainSlider.setValue(65)
        self.GainSlider.setSliderPosition(65)
        self.GainSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.GainSlider)

        self.RightSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.RightSpacer)

        self.horizontalLayout.addWidget(self.TopControlFrame)

        self.retranslateUi()

    # setupUi

    def retranslateUi(self):
        self.AddTrackButton.setText("")
        self.SettingsButton.setText("")
        self.FbwButton.setText("")
        self.PPButton.setText("")
        self.StopButton.setText("")
        self.FfwButton.setText("")
    # retranslateUi
