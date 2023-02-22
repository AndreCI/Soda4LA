from __future__ import annotations

import logging

from PyQt5.QtCore import QSize, Qt, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QSizePolicy, QPushButton, QSpacerItem, QFrame, QSlider, QGridLayout, \
    QLabel, QStyle

import ViewsPyQT5.sonification_view as sv
from Models.music_model import Music
from ViewsPyQT5.ViewsUtils.views_utils import buttonStyle, sliderGainStyle, playButtonReadyStyle, \
    sliderProgressStyle


class QJumpSlider(QSlider):  # TODO: Change music value on click
    def __init__(self, parent=None):
        super(QJumpSlider, self).__init__(parent)

    def mousePressEvent(self, event):
        # Jump to click position
        position = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
        # self.setValue(position)

    def mouseMoveEvent(self, event):
        # Jump to pointer position while moving
        position = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
        # self.setValue(position)


class TopSettingsBar(QObject):
    progressBarSignal = pyqtSignal(int, name="ProgressBarSignal")

    def __init__(self, parent: sv.SonificationView):
        super(TopSettingsBar, self).__init__()
        self.parent = parent
        self.progress_bar_thread = External(parent=self)

    def setupUi(self):
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.TopControlFrame = QFrame()
        self.TopControlFrame.setObjectName(u"TopControlFrame")
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

        self.musicPBLayout = QGridLayout()
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

        self.musicProgressBar = QJumpSlider()
        self.musicProgressBar.setOrientation(Qt.Horizontal)
        self.musicProgressBar.setRange(0, 100)
        self.musicProgressBar.setObjectName(u"musicProgressBar")
        self.musicProgressBar.setValue(0)
        self.musicProgressBar.setSliderPosition(0)
        # self.musicProgressBar.setTextVisible(False)
        self.musicProgressBar.setStyleSheet(sliderProgressStyle)
        self.musicProgressBar.setMaximumSize(5000, 7)
        self.musicProgressBar.setContentsMargins(0, 0, 0, 10)

        self.musicStartLabel = QLabel(self.TopControlFrame)
        self.musicStartLabel.setText("0:00")
        self.musicStartLabel.setObjectName(u"musicStartLabel")
        self.musicStartLabel.setContentsMargins(10, 0, 0, 0)

        self.musicEndLabel = QLabel(self.TopControlFrame)
        self.musicEndLabel.setText("--:--")
        self.musicEndLabel.setObjectName(u"musicEndLabel")
        self.musicEndLabel.setContentsMargins(0, 0, 10, 0)

        self.musicPBLayout.addWidget(self.musicProgressBar, 1, 0, 1, 6)
        self.musicPBLayout.addWidget(self.musicStartLabel, 0, 0, 1, 1)
        self.musicPBLayout.addItem(self.musicPBSpacer, 0, 1, 1, 1)
        self.musicPBLayout.addWidget(self.GainSlider, 0, 2, 1, 1)
        self.musicPBLayout.addWidget(self.volumeButton, 0, 3, 1, 1)
        self.musicPBLayout.addItem(self.musicPBSpacer2, 0, 4, 1, 1)
        self.musicPBLayout.addWidget(self.musicEndLabel, 0, 5, 1, 1)

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

        self.MidSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.RightSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.MidSpacer)
        self.horizontalLayout_3.addLayout(self.musicPBLayout)
        self.horizontalLayout_3.addItem(self.RightSpacer)
        self.horizontalLayout.addWidget(self.TopControlFrame)

        self.retranslate_ui()
        self.connect_ui()

    def connect_ui(self):
        self.music_model = Music().getInstance()
        self.volumeButton.clicked.connect(self.music_model.ctrl.mute_click)
        self.GainSlider.sliderReleased.connect(
            lambda: self.music_model.ctrl.change_global_gain(self.GainSlider.value()))
        self.AddTrackButton.clicked.connect(self.parent.model.ctrl.create_track)
        self.PPButton.clicked.connect(self.press_pp_button)
        self.StopButton.clicked.connect(self.press_stop_button)
        self.SettingsButton.clicked.connect(self.press_settings_button)
        # self.progressBarSignal.connect(self.musicProgressBar.setValue)
        self.progress_bar_thread.progressBarSignal.connect(self.musicProgressBar.setValue)
        self.progress_bar_thread.start()
        self.GainSlider.setValue(self.music_model.gain)

    def press_settings_button(self):
        self.parent.open_settings()

    # def handle_progress(self):
    #     while True:
    #         self.parent.model.ctrl.playingEvent.wait()  # wait if we are stopped
    #         self.parent.model.ctrl.pausedEvent.wait()  # wait if we are paused
    #         mtime = self.parent.model.ctrl.get_music_time()
    #         em, es = divmod(self.parent.model.settings.get_music_duration(), 60)
    #         eh, em = divmod(em, 60)
    #         sm, ss = divmod(mtime, 60)
    #         sh, sm = divmod(sm, 60)
    #         try:
    #             self.musicEndLabel.setText("{:02.0f}:{:02.0f}:{:02.0f}".format(eh, em, es))
    #             self.musicStartLabel.setText("{:02.0f}:{:02.0f}:{:02.0f}".format(sh, sm, ss))
    #             self.progressBarSignal.emit(min(99, int(100 * mtime / self.parent.model.settings.get_music_duration())))
    #         except RuntimeError:
    #             print("Runtime error on updating music start and end label.")
    #         QThread.msleep(int(1000/5))

    def press_stop_button(self):
        if self.parent.model.ctrl.playing:
            self.parent.model.ctrl.stop()
            try:
                self.progress_bar_thread.progressBarSignal.emit(0)
                self.musicStartLabel.setText("{:02.0f}:{:02.0f}:{:02.0f}".format(0, 0, 0))
                self.PPButton.setIcon(self.playIcon)
                self.PPButton.setStyleSheet(playButtonReadyStyle)
                self.StopButton.setEnabled(False)
            except:
                logging.log(logging.DEBUG, "Issue with UI top bar")

    def press_pp_button(self):
        if (self.parent.model.ctrl.playing and not self.parent.model.ctrl.paused):
            self.parent.model.ctrl.pause()
            self.PPButton.setIcon(self.playIcon)
            self.PPButton.setStyleSheet(playButtonReadyStyle)
        else:
            self.parent.model.ctrl.play()
            self.PPButton.setIcon(self.pauseIcon)
            self.PPButton.setStyleSheet(buttonStyle)
        self.StopButton.setEnabled(True)

    def retranslate_ui(self):
        self.AddTrackButton.setText("")
        self.SettingsButton.setText("")
        self.FbwButton.setText("")
        self.PPButton.setText("")
        self.StopButton.setText("")
        self.FfwButton.setText("")


class External(QThread):
    """
    Runs a counter thread.
    """
    progressBarSignal = pyqtSignal(int)

    def __init__(self, parent: TopSettingsBar):
        super(External, self).__init__()
        self.parent = parent

    def run(self):
        while True:
            self.parent.parent.model.ctrl.playingEvent.wait()  # wait if we are stopped
            self.parent.parent.model.ctrl.pausedEvent.wait()  # wait if we are paused
            mtime = self.parent.parent.model.ctrl.get_music_time()
            em, es = divmod(self.parent.parent.model.settings.get_music_duration(), 60)
            eh, em = divmod(em, 60)
            sm, ss = divmod(mtime, 60)
            sh, sm = divmod(sm, 60)
            try:
                self.parent.musicEndLabel.setText("{:02.0f}:{:02.0f}:{:02.0f}".format(eh, em, es))
                self.parent.musicStartLabel.setText("{:02.0f}:{:02.0f}:{:02.0f}".format(sh, sm, ss))
                self.progressBarSignal.emit(
                    min(99, int(100 * mtime / self.parent.parent.model.settings.get_music_duration())))
            except RuntimeError:
                print("Runtime error on updating music start and end label.")
            QThread.msleep(int(1000 / 5))
