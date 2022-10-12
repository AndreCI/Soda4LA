# -*- coding: utf-8 -*-
from collections import namedtuple

################################################################################
## Form generated from reading UI file 'trackconfigdWoYMd.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PyQt5.QtCore import QSize, Qt, QRect, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy, QAbstractScrollArea, QWidget, \
    QPushButton, QSpacerItem, QFrame, QLineEdit, QComboBox, QSlider, QGridLayout, QLayout

from Models.track_model import Track
from ViewsPyQT5.ViewsUtils.views_utils import GTrackView, buttonStyle, selectTrackButtonStyle, sliderGainStyle, sliderOffsetStyle, \
    buttonStyle3


class TrackView(object):
    def __init__(self):
        self.gTrackList = []
        self.selectedTrack = None

    def setupUi(self):
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.GlobalTrackView = QHBoxLayout()
        self.GlobalTrackView.setObjectName(u"GlobalTrackView")
        self.TrackSelectScrollArea = QScrollArea()
        self.TrackSelectScrollArea.setObjectName(u"TrackSelectScrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TrackSelectScrollArea.sizePolicy().hasHeightForWidth())
        self.TrackSelectScrollArea.setSizePolicy(sizePolicy)
        self.TrackSelectScrollArea.setMaximumSize(QSize(16777215, 210))
        self.TrackSelectScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.TrackSelectScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.TrackSelectScrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.TrackSelectScrollArea.setFrameShape(QFrame.Panel)
        self.TrackSelectScrollArea.setFrameShadow(QFrame.Raised)


        self.TrackSelectScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 321, 198))
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy1)
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.AddTrackButton = QPushButton(self.scrollAreaWidgetContents)
        self.AddTrackButton.setObjectName(u"AddTrackButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.AddTrackButton.sizePolicy().hasHeightForWidth())
        self.AddTrackButton.setSizePolicy(sizePolicy2)
        self.AddTrackButton.setMinimumSize(QSize(0, 0))
        self.AddTrackButton.setStyleSheet(buttonStyle)

        icon = QIcon()
        icon.addFile(u"data/img/icons/circle-add.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.AddTrackButton.setIcon(icon)

        self.verticalLayout_4.addWidget(self.AddTrackButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.TrackSelectScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.GlobalTrackView.addWidget(self.TrackSelectScrollArea)

        self.TrackSettings_2 = QFrame()
        self.TrackSettings_2.setObjectName(u"TrackSettings_2")
        self.TrackSettings_2.setMaximumSize(QSize(16777215, 210))
        self.TrackSettings_2.setFrameShape(QFrame.Panel)
        self.TrackSettings_2.setFrameShadow(QFrame.Raised)


        self.TrackSettings = QVBoxLayout(self.TrackSettings_2)
        self.TrackSettings.setSpacing(7)
        self.TrackSettings.setObjectName(u"TrackSettings")
        self.TrackNameFrame = QFrame(self.TrackSettings_2)
        self.TrackNameFrame.setObjectName(u"TrackNameFrame")
        sizePolicy.setHeightForWidth(self.TrackNameFrame.sizePolicy().hasHeightForWidth())
        self.TrackNameFrame.setSizePolicy(sizePolicy)
        self.TrackNameFrame.setMinimumSize(QSize(0, 0))
        self.TrackNameFrame.setFrameShape(QFrame.StyledPanel)
        self.TrackNameFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.TrackNameFrame)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)

        self.ImportButton = QPushButton(self.TrackNameFrame)
        self.ImportButton.setObjectName(u"ImportButton")
        sizePolicy2.setHeightForWidth(self.ImportButton.sizePolicy().hasHeightForWidth())
        self.ImportButton.setSizePolicy(sizePolicy2)
        self.ImportButton.setMinimumSize(QSize(0, 0))
        self.ImportButton.setMaximumSize(QSize(33, 16777215))
        self.ImportButton.setStyleSheet(buttonStyle)

        icon = QIcon()
        icon.addFile(u"data/img/icons/download.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.ImportButton.setIcon(icon)

        self.horizontalLayout_13.addWidget(self.ImportButton)

        self.ExportButton = QPushButton(self.TrackNameFrame)
        self.ExportButton.setObjectName(u"ExportButton")
        sizePolicy2.setHeightForWidth(self.ExportButton.sizePolicy().hasHeightForWidth())
        self.ExportButton.setSizePolicy(sizePolicy2)
        self.ExportButton.setMinimumSize(QSize(0, 0))
        self.ExportButton.setMaximumSize(QSize(33, 16777215))
        self.ExportButton.setStyleSheet(buttonStyle)

        icon = QIcon()
        icon.addFile(u"data/img/icons/export.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.ExportButton.setIcon(icon)

        self.horizontalLayout_13.addWidget(self.ExportButton)


        self.TrackNameLineEdit = QLineEdit(self.TrackNameFrame)
        self.TrackNameLineEdit.setObjectName(u"TrackNameLineEdit")

        self.horizontalLayout_13.addWidget(self.TrackNameLineEdit)

        self.horizontalLayout_13.setStretch(0, 1)

        self.TrackSettings.addWidget(self.TrackNameFrame)

        self.SoundfontComboBox = QComboBox(self.TrackSettings_2)
        self.SoundfontComboBox.setObjectName(u"SoundfontComboBox")

        self.TrackSettings.addWidget(self.SoundfontComboBox)

        self.GainSlider = QSlider(self.TrackSettings_2)
        self.GainSlider.setObjectName(u"GainSlider")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.GainSlider.sizePolicy().hasHeightForWidth())
        self.GainSlider.setSizePolicy(sizePolicy3)
        self.GainSlider.setMinimumSize(QSize(100, 0))
        self.GainSlider.setStyleSheet(sliderGainStyle)
        self.GainSlider.setValue(65)
        self.GainSlider.setSliderPosition(65)
        self.GainSlider.setOrientation(Qt.Horizontal)

        self.TrackSettings.addWidget(self.GainSlider)

        self.OffsetSlider = QSlider(self.TrackSettings_2)
        self.OffsetSlider.setObjectName(u"OffsetSlider")
        sizePolicy3.setHeightForWidth(self.OffsetSlider.sizePolicy().hasHeightForWidth())
        self.OffsetSlider.setSizePolicy(sizePolicy3)
        self.OffsetSlider.setMinimumSize(QSize(100, 0))
        self.OffsetSlider.setStyleSheet(sliderOffsetStyle)
        self.OffsetSlider.setValue(65)
        self.OffsetSlider.setSliderPosition(65)
        self.OffsetSlider.setOrientation(Qt.Horizontal)

        self.TrackSettings.addWidget(self.OffsetSlider)

        self.AdvancedTrackSettings = QGridLayout()
        self.AdvancedTrackSettings.setObjectName(u"AdvancedTrackSettings")
        self.AdvancedTrackSettings.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.AdvancedTrackSettings.setHorizontalSpacing(2)
        self.AdvancedTrackSettings.setVerticalSpacing(11)
        self.DurationButton = QPushButton(self.TrackSettings_2)
        self.DurationButton.setObjectName(u"DurationButton")
        sizePolicy1.setHeightForWidth(self.DurationButton.sizePolicy().hasHeightForWidth())
        self.DurationButton.setSizePolicy(sizePolicy1)
        self.DurationButton.setMinimumSize(QSize(30, 30))
        self.DurationButton.setMaximumSize(QSize(16777215, 16777215))
        self.DurationButton.setStyleSheet(buttonStyle)

        self.AdvancedTrackSettings.addWidget(self.DurationButton, 1, 0, 1, 1)

        self.VelocityButton = QPushButton(self.TrackSettings_2)
        self.VelocityButton.setObjectName(u"VelocityButton")
        sizePolicy1.setHeightForWidth(self.VelocityButton.sizePolicy().hasHeightForWidth())
        self.VelocityButton.setSizePolicy(sizePolicy1)
        self.VelocityButton.setMinimumSize(QSize(30, 30))
        self.VelocityButton.setMaximumSize(QSize(16777215, 16777215))
        self.VelocityButton.setStyleSheet(buttonStyle)

        self.AdvancedTrackSettings.addWidget(self.VelocityButton, 1, 1, 1, 1)

        self.FilterButton = QPushButton(self.TrackSettings_2)
        self.FilterButton.setObjectName(u"FilterButton")
        sizePolicy1.setHeightForWidth(self.FilterButton.sizePolicy().hasHeightForWidth())
        self.FilterButton.setSizePolicy(sizePolicy1)
        self.FilterButton.setMinimumSize(QSize(30, 30))
        self.FilterButton.setMaximumSize(QSize(16777215, 16777215))
        self.FilterButton.setStyleSheet(buttonStyle)
        icon = QIcon()
        icon.addFile(u"data/img/icons/filter.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.FilterButton.setIcon(icon)
        self.AdvancedTrackSettings.addWidget(self.FilterButton, 0, 0, 1, 1)

        self.ValueButton = QPushButton(self.TrackSettings_2)
        self.ValueButton.setObjectName(u"ValueButton")
        sizePolicy1.setHeightForWidth(self.ValueButton.sizePolicy().hasHeightForWidth())
        self.ValueButton.setSizePolicy(sizePolicy1)
        self.ValueButton.setMinimumSize(QSize(30, 30))
        self.ValueButton.setMaximumSize(QSize(16777215, 16777215))
        self.ValueButton.setStyleSheet(buttonStyle)

        self.AdvancedTrackSettings.addWidget(self.ValueButton, 0, 1, 1, 1)


        self.TrackSettings.addLayout(self.AdvancedTrackSettings)
       # self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
       # self.TrackSettings.addItem(self.verticalSpacer_2)

        self.GlobalTrackView.addWidget(self.TrackSettings_2)

        self.GlobalTrackView.setStretch(0, 1)
        self.GlobalTrackView.setStretch(1, 2)

        self.verticalLayout.addLayout(self.GlobalTrackView)

        self.AdvancedSettingsFrame = QFrame()
        self.AdvancedSettingsFrame.setObjectName(u"AdvancedSettingsFrame")
        self.AdvancedSettingsFrame.setFrameShape(QFrame.StyledPanel)
        self.AdvancedSettingsFrame.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.AdvancedSettingsFrame)


        self.retranslateUi()
        self.add_track(Track())
        self.add_track(Track())
        self.add_track(Track())
        self.add_track(Track())
        self.add_track(Track())
        self.add_track(Track())
        self.add_track(Track())
        self.add_track(Track())

    # setupUi

    def retranslateUi(self):
        #self.AddTrackButton.setText(QCoreApplication.translate("TrackConfigView", u"+", None))
        self.ExportButton.setText("")
        self.ImportButton.setText("")
        self.DurationButton.setText(QCoreApplication.translate("TrackConfigView", u"Duration", None))
        self.VelocityButton.setText(QCoreApplication.translate("TrackConfigView", u"Velocity", None))
        self.FilterButton.setText(QCoreApplication.translate("TrackConfigView", u"Filter", None))
        self.ValueButton.setText(QCoreApplication.translate("TrackConfigView", u"Value", None))
    # retranslateUi

    def display_track(self, track):
        self.TrackNameLineEdit.setText(track.name)
        self.GainSlider.setValue(track.gain)
        self.OffsetSlider.setValue(track.offset)
        #self.SoundfontComboBox.set

    def add_track(self, track):
        g_track_frame = QFrame()
        g_track_frame.setObjectName(u"gTrackFrame")
        g_track_frame.setGeometry(QRect(30, 120, 251, 31))
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(g_track_frame.sizePolicy().hasHeightForWidth())
        g_track_frame.setSizePolicy(size_policy)
        #g_track_frame.setFrameShape(QFrame.Box)
        #g_track_frame.setFrameShadow(QFrame.Raised)
        horizontal_layout = QHBoxLayout(g_track_frame)
        horizontal_layout.setSpacing(0)
        horizontal_layout.setObjectName(u"horizontalLayout")
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        g_track_delete_button = QPushButton(g_track_frame)
        g_track_delete_button.setObjectName(u"gTrackDeleteButton")
        size_policy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        size_policy1.setHorizontalStretch(0)
        size_policy1.setVerticalStretch(0)
        size_policy1.setHeightForWidth(g_track_delete_button.sizePolicy().hasHeightForWidth())
        g_track_delete_button.setSizePolicy(size_policy1)
        g_track_delete_button.setMinimumSize(QSize(20,20))
        icon = QIcon()
        icon.addFile(u"data/img/icons/delete.svg", QSize(), QIcon.Normal, QIcon.Off)
        g_track_delete_button.setIcon(icon)
        g_track_delete_button.setStyleSheet(buttonStyle3)
        horizontal_layout.addWidget(g_track_delete_button)

        g_track_select_button = QPushButton(g_track_frame)
        g_track_select_button.setObjectName(u"gTrackSelectButton")
        size_policy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy2.setHorizontalStretch(0)
        size_policy2.setVerticalStretch(0)
        size_policy2.setHeightForWidth(g_track_select_button.sizePolicy().hasHeightForWidth())
        g_track_select_button.setSizePolicy(size_policy2)
        g_track_select_button.setStyleSheet(selectTrackButtonStyle)
        horizontal_layout.addWidget(g_track_select_button)
        gTrackView = GTrackView(frame=g_track_frame, deleteButton=g_track_delete_button, selectButton=g_track_select_button, hLayout=horizontal_layout)

        self.gTrackList.append(gTrackView)
        track.gTrackView = gTrackView
        track.generalView = self
        gTrackView.selectButton.setText(track.name)

        gTrackView.selectButton.clicked.connect(lambda : track.ctrl.select())
        gTrackView.deleteButton.clicked.connect(lambda : track.ctrl.remove())

        self.verticalLayout_4.insertWidget(len(self.gTrackList) - 1, g_track_frame)
