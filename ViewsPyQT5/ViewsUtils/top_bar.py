# -*- coding: utf-8 -*-
import threading
import time

from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy, QAbstractScrollArea, QWidget, \
    QPushButton, QSpacerItem, QFrame, QLineEdit, QComboBox, QSlider, QGridLayout, QLayout, QProgressBar, QLabel

from Models.music_model import Music
from ViewsPyQT5.ViewsUtils.views_utils import buttonStyle, progressBarStyle, sliderGainStyle, playButtonReadyStyle


################################################################################
##  generated from reading UI file 'topsettingszfbzda.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

class TopSettingsBar(object):
    def __init__(self, parent):
        self.parent = parent

    #https://stackoverflow.com/questions/56275060/pyqt5-how-to-use-progress-bar-in-pyqt5
    def setupUi(self):
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.TopControlFrame = QFrame()
        self.TopControlFrame.setObjectName(u"TopControlFrame")
        #self.TopControlFrame.setFrameShape(QFrame.Panel)
        #self.TopControlFrame.setFrameShadow(QFrame.Raised)
        #self.TopControlFrame.setLineWidth(3)
        self.TopControlFrame.setMaximumSize(16777215, 40)
        self.horizontalLayout_3 = QHBoxLayout(self.TopControlFrame)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.LeftSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.AddTrackButton = QPushButton(self.TopControlFrame)
        self.AddTrackButton.setObjectName(u"AddTrackButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddTrackButton.sizePolicy().hasHeightForWidth())
        self.AddTrackButton.setSizePolicy(sizePolicy)
        self.AddTrackButton.setMinimumSize(QSize(0, 0))
        self.AddTrackButton.setMaximumSize(QSize(36, 16777215))
        self.AddTrackButton.setStyleSheet(buttonStyle)
        icon = QIcon()
        icon.addFile(u"data/img/icons/circle-add.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.AddTrackButton.setIcon(icon)
        self.AddTrackButton.setToolTip("Create a new track")

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
        self.SettingsButton.setStyleSheet(buttonStyle)
        icon1 = QIcon()
        icon1.addFile(u"data/img/icons/settings.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.SettingsButton.setIcon(icon1)
        self.SettingsButton.setToolTip("Open settings")

        self.horizontalLayout_3.addWidget(self.SettingsButton)
        self.horizontalLayout_3.addItem(self.LeftSpacer)

        self.musicPBLayout = QGridLayout()#self.gridLayoutWidget)
        self.musicPBLayout.setObjectName(u"musicPBLayout")
        self.musicPBLayout.setContentsMargins(0, 0, 0, 0)
        self.musicPBSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.musicPBSpacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.GainSlider = QSlider()
        self.GainSlider.setObjectName(u"GainSlider")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.GainSlider.sizePolicy().hasHeightForWidth())
        self.GainSlider.setSizePolicy(sizePolicy2)
        self.GainSlider.setMinimumSize(QSize(350, 0))
        self.GainSlider.setStyleSheet(sliderGainStyle)
        self.GainSlider.setValue(65)
        self.GainSlider.setSliderPosition(65)
        self.GainSlider.setOrientation(Qt.Horizontal)
        self.GainSlider.setToolTip("Change volume")
        self.volumeButton = QPushButton(self.TopControlFrame)
        self.volumeButton.setObjectName(u"volumeButton")
        self.volumeButton.setSizePolicy(sizePolicy)
        self.volumeButton.setMinimumSize(QSize(0, 0))
        self.volumeButton.setMaximumSize(QSize(36, 16777215))
        self.volumeButton.setStyleSheet(buttonStyle)
        self.volumeIcon = QIcon()
        self.mutedIcon = QIcon()
        self.volumeIcon.addFile(u"data/img/icons/volume-up.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.mutedIcon.addFile(u"data/img/icons/volume-off.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.volumeButton.setIcon(self.volumeIcon)
        self.volumeButton.setToolTip("Mute/Unmute")

        self.musicProgressBar = QProgressBar()
        self.musicProgressBar.setObjectName(u"musicProgressBar")
        self.musicProgressBar.setValue(0)
        self.musicProgressBar.setTextVisible(False)
        self.musicProgressBar.setStyleSheet(progressBarStyle)
        self.musicProgressBar.setMaximumSize(5000, 7)
        self.musicProgressBar.setContentsMargins(0,0,0,10)

        self.musicStartLabel = QLabel("0:00")
        self.musicStartLabel.setObjectName(u"musicStartLabel")
        self.musicStartLabel.setContentsMargins(10,0,0,0)

        self.musicEndLabel = QLabel("--:--")
        self.musicEndLabel.setObjectName(u"musicEndLabel")
        self.musicEndLabel.setContentsMargins(0,0,10,0)

        self.musicPBLayout.addWidget(self.musicProgressBar, 1, 0, 1, 6)
        self.musicPBLayout.addWidget(self.musicStartLabel, 0, 0, 1, 1)
        self.musicPBLayout.addItem(self.musicPBSpacer, 0, 1, 1, 1)
        self.musicPBLayout.addWidget(self.GainSlider, 0, 2, 1, 1)
        self.musicPBLayout.addWidget(self.volumeButton, 0, 3, 1, 1)
        self.musicPBLayout.addItem(self.musicPBSpacer2, 0, 4, 1, 1)
        self.musicPBLayout.addWidget(self.musicEndLabel, 0, 5, 1, 1)
        #TODO : inverser le blanc et le fond gris et rajouter un symbole haut parleur pour communiquer que c'est du son

        self.FbwButton = QPushButton(self.TopControlFrame)
        self.FbwButton.setObjectName(u"FbwButton")
        sizePolicy.setHeightForWidth(self.FbwButton.sizePolicy().hasHeightForWidth())
        self.FbwButton.setSizePolicy(sizePolicy)
        self.FbwButton.setMinimumSize(QSize(0, 0))
        self.FbwButton.setMaximumSize(QSize(36, 16777215))
        self.FbwButton.setStyleSheet(buttonStyle)
        icon2 = QIcon()
        icon2.addFile(u"data/img/icons/chevron-double-left.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.FbwButton.setIcon(icon2)
        self.FbwButton.setEnabled(False)
        self.FbwButton.setToolTip("Go back 10 seconds into the song")

        self.horizontalLayout_3.addWidget(self.FbwButton)

        self.PPButton = QPushButton(self.TopControlFrame)
        self.PPButton.setObjectName(u"PPButton")
        sizePolicy.setHeightForWidth(self.PPButton.sizePolicy().hasHeightForWidth())
        self.PPButton.setSizePolicy(sizePolicy)
        self.PPButton.setMinimumSize(QSize(0, 0))
        self.PPButton.setMaximumSize(QSize(36, 16777215))
        self.PPButton.setStyleSheet(buttonStyle)
        self.pauseIcon = QIcon()
        self.pauseIcon.addFile(u"data/img/icons/pause.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.playIcon = QIcon()
        self.playIcon.addFile(u"data/img/icons/caret-right.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.PPButton.setIcon(self.playIcon)
        self.PPButton.setEnabled(False)
        self.PPButton.setToolTip("Play/Pause")

        self.horizontalLayout_3.addWidget(self.PPButton)

        self.StopButton = QPushButton(self.TopControlFrame)
        self.StopButton.setObjectName(u"StopButton")
        sizePolicy.setHeightForWidth(self.StopButton.sizePolicy().hasHeightForWidth())
        self.StopButton.setSizePolicy(sizePolicy)
        self.StopButton.setMinimumSize(QSize(0, 0))
        self.StopButton.setMaximumSize(QSize(36, 16777215))
        self.StopButton.setStyleSheet(buttonStyle)
        icon4 = QIcon()
        icon4.addFile(u"data/img/icons/stop.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.StopButton.setIcon(icon4)
        self.StopButton.setIconSize(QSize(20, 20))
        self.StopButton.setEnabled(False)
        self.StopButton.setToolTip("Stop")

        self.horizontalLayout_3.addWidget(self.StopButton)

        self.FfwButton = QPushButton(self.TopControlFrame)
        self.FfwButton.setObjectName(u"FfwButton")
        sizePolicy.setHeightForWidth(self.FfwButton.sizePolicy().hasHeightForWidth())
        self.FfwButton.setSizePolicy(sizePolicy)
        self.FfwButton.setMinimumSize(QSize(0, 0))
        self.FfwButton.setMaximumSize(QSize(36, 16777215))
        self.FfwButton.setStyleSheet(buttonStyle)
        icon5 = QIcon()
        icon5.addFile(u"data/img/icons/chevron-double-right.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.FfwButton.setIcon(icon5)
        self.FfwButton.setEnabled(False)
        self.FfwButton.setToolTip("Skip 10 seconds into the song")

        self.horizontalLayout_3.addWidget(self.FfwButton)

        #self.horizontalLayout_3.addWidget(self.GainSlider)

        self.MidSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.RightSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.MidSpacer)
        self.horizontalLayout_3.addLayout(self.musicPBLayout)
        self.horizontalLayout_3.addItem(self.RightSpacer)
        self.horizontalLayout.addWidget(self.TopControlFrame)

        self.retranslateUi()
        self.connectUi()

    def connectUi(self):
        self.music_model = Music().getInstance()
        self.volumeButton.clicked.connect(self.music_model.ctrl.muteClick)
        self.GainSlider.sliderReleased.connect(lambda :self.music_model.ctrl.change_global_gain(self.GainSlider.value()))
        self.AddTrackButton.clicked.connect(self.parent.model.ctrl.create_track)
        self.PPButton.clicked.connect(self.pressPPButton)
        self.StopButton.clicked.connect(self.pressStopButton)
        self.SettingsButton.clicked.connect(self.pressSettingsButton)
        self.progress_bar_thread = threading.Thread(target=self.handle_progress, daemon=True)
        self.progress_bar_thread.start()
    # setupUi
    def pressSettingsButton(self):
        self.parent.settingsView.show()

    def handle_progress(self):
        while True:
            self.parent.model.ctrl.playingEvent.wait()  # wait if we are stopped
            self.parent.model.ctrl.pausedEvent.wait()  # wait if we are paused
            mtime = self.parent.model.ctrl.get_music_time()
            em, es = divmod(self.parent.model.timeSettings.musicDuration, 60)
            eh, em = divmod(em, 60)
            sm, ss = divmod(mtime, 60)
            sh, sm = divmod(sm, 60)
            self.musicEndLabel.setText("{:02.0f}:{:02.0f}:{:02.0f}".format(eh, em, es))
            self.musicStartLabel.setText("{:02.0f}:{:02.0f}:{:02.0f}".format(sh, sm, ss))
            self.musicProgressBar.setValue(int(mtime/self.parent.model.timeSettings.musicDuration))
            time.sleep(1)

    def pressStopButton(self):
        if self.parent.model.ctrl.playing:
            self.parent.model.ctrl.stop()
            self.musicProgressBar.setValue(0)
            self.musicStartLabel.setText("{:02.0f}:{:02.0f}:{:02.0f}".format(0, 0, 0))
            self.PPButton.setIcon(self.playIcon)
            self.PPButton.setStyleSheet(playButtonReadyStyle)
            self.StopButton.setEnabled(False)

    def pressPPButton(self):
        if(self.parent.model.ctrl.playing and not self.parent.model.ctrl.paused):
            self.parent.model.ctrl.pause()
            self.PPButton.setIcon(self.playIcon)
            self.PPButton.setStyleSheet(playButtonReadyStyle)
        else:
            self.parent.model.ctrl.play()
            self.PPButton.setIcon(self.pauseIcon)
            self.PPButton.setStyleSheet(buttonStyle)
        self.StopButton.setEnabled(True)

    def retranslateUi(self):
        self.AddTrackButton.setText("")
        self.SettingsButton.setText("")
        self.FbwButton.setText("")
        self.PPButton.setText("")
        self.StopButton.setText("")
        self.FfwButton.setText("")
    # retranslateUi
