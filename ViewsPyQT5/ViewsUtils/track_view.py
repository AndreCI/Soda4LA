from __future__ import annotations
import ViewsPyQT5.sonification_view as sv

from PyQt5.QtCore import QSize, Qt, QRect, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy, QAbstractScrollArea, QWidget, \
    QPushButton, QSpacerItem, QFrame, QLineEdit, QComboBox, QSlider, QGridLayout, QLayout, QLabel, QFileDialog

from Utils.soundfont_loader import SoundfontLoader
from ViewsPyQT5.ViewsUtils.views_utils import GTrackView, buttonStyle, selectTrackButtonStyle, sliderGainStyle, \
    sliderOffsetStyle, \
    buttonStyle3, selectedButtonStyle


class TrackView(object):

    def __init__(self, parent:sv.SonificationView):
        self.parent = parent
        self.track = None
        self.gTrackList = []
        self.selectedTrack = None
        self.soundfontUtil = SoundfontLoader.get_instance()

    def setupUi(self):
        topTrackSettingsMaxSize = 230

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.GlobalTrackView = QHBoxLayout()
        self.GlobalTrackView.setObjectName(u"GlobalTrackView")
        self.TrackSelectScrollArea = QScrollArea()
        self.TrackSelectScrollArea.setObjectName(u"TrackSelectScrollArea")
        self.TrackSelectScrollArea.setObjectName(u"TrackSelectScrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TrackSelectScrollArea.sizePolicy().hasHeightForWidth())
        self.TrackSelectScrollArea.setSizePolicy(sizePolicy)
        self.TrackSelectScrollArea.setMaximumSize(QSize(16777215, topTrackSettingsMaxSize))
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

        self.addTrackIcon = QIcon()
        self.addTrackIcon.addFile(u"data/img/icons/circle-add.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.AddTrackButton.setIcon(self.addTrackIcon)

        self.verticalLayout_4.addWidget(self.AddTrackButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.TrackSelectScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.GlobalTrackView.addWidget(self.TrackSelectScrollArea)

        self.TrackSettings_2 = QFrame()
        self.TrackSettings_2.setObjectName(u"TrackSettings_2")
        self.TrackSettings_2.setMaximumSize(QSize(16777215, topTrackSettingsMaxSize))
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
        self.trackNameHLayout = QHBoxLayout(self.TrackNameFrame)
        self.trackNameHLayout.setSpacing(0)
        self.trackNameHLayout.setObjectName(u"trackNameHLayout")
        self.trackNameHLayout.setContentsMargins(0, 0, 0, 0)

        self.importButton = QPushButton(self.TrackNameFrame)
        self.importButton.setObjectName(u"ImportButton")
        sizePolicy2.setHeightForWidth(self.importButton.sizePolicy().hasHeightForWidth())
        self.importButton.setSizePolicy(sizePolicy2)
        self.importButton.setMinimumSize(QSize(0, 0))
        self.importButton.setMaximumSize(QSize(33, 16777215))
        self.importButton.setStyleSheet(buttonStyle)

        icon = QIcon()
        icon.addFile(u"data/img/icons/download.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.importButton.setIcon(icon)

        self.exportButton = QPushButton(self.TrackNameFrame)
        self.exportButton.setObjectName(u"ExportButton")
        sizePolicy2.setHeightForWidth(self.exportButton.sizePolicy().hasHeightForWidth())
        self.exportButton.setSizePolicy(sizePolicy2)
        self.exportButton.setMinimumSize(QSize(0, 0))
        self.exportButton.setMaximumSize(QSize(33, 16777215))
        self.exportButton.setStyleSheet(buttonStyle)

        icon = QIcon()
        icon.addFile(u"data/img/icons/export.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.exportButton.setIcon(icon)

        self.trackNameLineEdit = QLineEdit(self.TrackNameFrame)
        self.trackNameLineEdit.setObjectName(u"TrackNameLineEdit")

        self.trackNameHLayout.addWidget(self.trackNameLineEdit)
        self.trackNameHLayout.addWidget(self.importButton)
        self.trackNameHLayout.addWidget(self.exportButton)

        self.trackNameHLayout.setStretch(0, 1)

        self.TrackSettings.addWidget(self.TrackNameFrame)

        self.soundfontComboBox = QComboBox(self.TrackSettings_2)
        self.soundfontComboBox.setObjectName(u"SoundfontComboBox")
        self.soundfontComboBox.setEditable(False)
        self.soundfontComboBox.addItems(self.soundfontUtil.get_names())

        self.TrackSettings.addWidget(self.soundfontComboBox)

        self.gainHLayout = QHBoxLayout()
        self.GainSlider = QSlider()
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

        self.gainButton = QPushButton()
        self.gainButton.setObjectName(u"SettingsButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.gainButton.sizePolicy().hasHeightForWidth())
        self.gainButton.setSizePolicy(sizePolicy1)
        self.gainButton.setMinimumSize(QSize(0, 0))
        self.gainButton.setMaximumSize(QSize(36, 16777215))
        self.gainButton.setStyleSheet(buttonStyle)
        self.volumeIcon = QIcon()
        self.mutedIcon = QIcon()
        self.volumeIcon.addFile(u"data/img/icons/volume-up.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.mutedIcon.addFile(u"data/img/icons/volume-off.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.gainButton.setIcon(self.volumeIcon)

        self.gainHLayout.addWidget(self.GainSlider)
        self.gainHLayout.addWidget(self.gainButton)
        self.TrackSettings.addLayout(self.gainHLayout)

        self.offsetHLayout = QHBoxLayout()
        self.offsetHLayout.setSpacing(0)
        self.offsetHLayout.setObjectName(u"offsetHLayout")
        self.offsetHLayout.setContentsMargins(0, 0, 0, 0)

        self.offsetSlider = QSlider(self.TrackSettings_2)
        self.offsetSlider.setObjectName(u"OffsetSlider")
        sizePolicy3.setHeightForWidth(self.offsetSlider.sizePolicy().hasHeightForWidth())
        self.offsetSlider.setSizePolicy(sizePolicy3)
        self.offsetSlider.setMinimumSize(QSize(100, 0))
        self.offsetSlider.setStyleSheet(sliderOffsetStyle)
        self.offsetSlider.setValue(65)
        self.offsetSlider.setSliderPosition(65)
        self.offsetSlider.setOrientation(Qt.Horizontal)

        self.offsetLabel = QLabel()
        self.offsetLabel.setMaximumSize(100, 36)
        self.offsetLabel.setContentsMargins(10, 0, 5, 0)
        self.offsetLabel.setText("0 % of bpm")
        self.offsetHLayout.addWidget(self.offsetSlider)
        self.offsetHLayout.addWidget(self.offsetLabel)

        self.TrackSettings.addLayout(self.offsetHLayout)

        self.AdvancedTrackSettings = QGridLayout()
        self.AdvancedTrackSettings.setObjectName(u"AdvancedTrackSettings")
        self.AdvancedTrackSettings.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.AdvancedTrackSettings.setHorizontalSpacing(2)
        self.AdvancedTrackSettings.setVerticalSpacing(10)
        self.durationButton = QPushButton(self.TrackSettings_2)
        self.durationButton.setObjectName(u"DurationButton")
        sizePolicy1.setHeightForWidth(self.durationButton.sizePolicy().hasHeightForWidth())
        self.durationButton.setSizePolicy(sizePolicy1)
        self.durationButton.setMinimumSize(QSize(30, 30))
        self.durationButton.setMaximumSize(QSize(16777215, 16777215))
        self.durationButton.setStyleSheet(buttonStyle)

        self.AdvancedTrackSettings.addWidget(self.durationButton, 1, 0, 1, 1)

        self.velocityButton = QPushButton(self.TrackSettings_2)
        self.velocityButton.setObjectName(u"VelocityButton")
        sizePolicy1.setHeightForWidth(self.velocityButton.sizePolicy().hasHeightForWidth())
        self.velocityButton.setSizePolicy(sizePolicy1)
        self.velocityButton.setMinimumSize(QSize(30, 30))
        self.velocityButton.setMaximumSize(QSize(16777215, 16777215))
        self.velocityButton.setStyleSheet(buttonStyle)

        self.AdvancedTrackSettings.addWidget(self.velocityButton, 1, 1, 1, 1)

        self.filterButton = QPushButton(self.TrackSettings_2)
        self.filterButton.setObjectName(u"FilterButton")
        sizePolicy1.setHeightForWidth(self.filterButton.sizePolicy().hasHeightForWidth())
        self.filterButton.setSizePolicy(sizePolicy1)
        self.filterButton.setMinimumSize(QSize(30, 30))
        self.filterButton.setMaximumSize(QSize(16777215, 16777215))
        self.filterButton.setStyleSheet(buttonStyle)
        icon = QIcon()
        icon.addFile(u"data/img/icons/filter.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.filterButton.setIcon(icon)
        self.AdvancedTrackSettings.addWidget(self.filterButton, 0, 0, 1, 1)

        self.valueButton = QPushButton(self.TrackSettings_2)
        self.valueButton.setObjectName(u"ValueButton")
        sizePolicy1.setHeightForWidth(self.valueButton.sizePolicy().hasHeightForWidth())
        self.valueButton.setSizePolicy(sizePolicy1)
        self.valueButton.setMinimumSize(QSize(30, 30))
        self.valueButton.setMaximumSize(QSize(16777215, 16777215))
        self.valueButton.setStyleSheet(selectedButtonStyle)

        self.advancedOptionButtons = {"filter": self.filterButton,
                                      "value": self.valueButton,
                                      "duration": self.durationButton,
                                      "velocity": self.velocityButton}
        self.AdvancedTrackSettings.addWidget(self.valueButton, 0, 1, 1, 1)

        self.TrackSettings.addLayout(self.AdvancedTrackSettings)
        # self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.TrackSettings.addItem(self.verticalSpacer_2)

        self.GlobalTrackView.addWidget(self.TrackSettings_2)

        self.GlobalTrackView.setStretch(0, 1)
        self.GlobalTrackView.setStretch(1, 2)

        self.verticalLayout.addLayout(self.GlobalTrackView)

        self.retranslate_ui()
        self.connect_ui()
        self.set_tool_tips()
        self.AddTrackButton.clicked.connect(lambda: self.parent.model.ctrl.create_track())
        #outside connect_ui to prevent future disconnects

        self.TrackSettings_2.hide()

    def set_tool_tips(self):
        self.valueButton.setToolTip("Change the pitch class encoding for this track. You can change the octave as well.")
        self.filterButton.setToolTip(
            "Change the global filter for this track. Rows will be skipped if they contain a value found in this filter")
        self.velocityButton.setToolTip(
            "Change the volume encoding for this track. Higher volume will result in louder notes")
        self.durationButton.setToolTip(
            "Change the duration encoding for this track. Smaller durations will result in shorter notes")
        self.offsetLabel.setToolTip("The offset (in percentage of the beat per minute) for this track, adding delay to all its notes.")
        self.offsetSlider.setToolTip("Change the offset for this track, adding delay to all its notes.")
        self.gainButton.setToolTip("Mute/Unmute this track")
        self.GainSlider.setToolTip("Change the volume for this track")
        self.exportButton.setToolTip("Export this track as a .track so that it can be loaded later.")

        self.AddTrackButton.setToolTip("Add a track to this project.\n"
                                       "Each track encode each row into maximum one note.\n"
                                       "All notes produced by a track will share the same instrument.")
        self.importButton.setToolTip("Import and replace this track with a .track file, previously exported."
                                     "\nAll settings on this track will be override.")

    # setupUi
    def disconnect_ui(self):
        self.trackNameLineEdit.textEdited.disconnect()
        self.GainSlider.sliderReleased.disconnect()
        self.gainButton.clicked.disconnect()
        self.offsetSlider.sliderReleased.disconnect()
        self.soundfontComboBox.activated.disconnect()
        self.durationButton.clicked.disconnect()
        self.valueButton.clicked.disconnect()
        self.velocityButton.clicked.disconnect()
        self.filterButton.clicked.disconnect()
        self.exportButton.clicked.disconnect()
        self.importButton.clicked.disconnect()

    def connect_ui(self):
        self.trackNameLineEdit.textEdited.connect(lambda: self.track.ctrl.change_name(self.trackNameLineEdit.text()))
        self.GainSlider.sliderReleased.connect(lambda: self.track.ctrl.change_gain(self.GainSlider.value()))
        self.gainButton.clicked.connect(lambda: self.mute_track())
        self.offsetSlider.sliderReleased.connect(lambda: self.change_offset())
        self.soundfontComboBox.activated.connect(
            lambda: self.track.ctrl.set_soundfont(self.soundfontComboBox.currentText()))
        self.durationButton.clicked.connect(lambda: self.track.advancedView.display_track(self.track, "duration"))
        self.valueButton.clicked.connect(lambda: self.track.advancedView.display_track(self.track, "value"))
        self.velocityButton.clicked.connect(lambda: self.track.advancedView.display_track(self.track, "velocity"))
        self.filterButton.clicked.connect(lambda: self.track.advancedView.display_track(self.track, "filter"))
        self.exportButton.clicked.connect(lambda: self.export_track())
        self.importButton.clicked.connect(lambda: self.import_track())

    def retranslate_ui(self):
        # self.AddTrackButton.setText(QCoreApplication.translate("TrackConfigView", u"+", None))
        self.exportButton.setText("")
        self.importButton.setText("")
        self.durationButton.setText(QCoreApplication.translate("TrackConfigView", u"Duration", None))
        self.velocityButton.setText(QCoreApplication.translate("TrackConfigView", u"Volume", None))
        self.filterButton.setText(QCoreApplication.translate("TrackConfigView", u"Filter", None))
        self.valueButton.setText(QCoreApplication.translate("TrackConfigView", u"Pitch", None))
        self.AddTrackButton.setText(
            QCoreApplication.translate("TrackConfigView", u"\tClick here to add your first track!", None))

    # retranslateUi
    def change_offset(self):
        self.track.ctrl.change_offset(self.offsetSlider.value())
        self.offsetLabel.setText(str(int(self.track.offset)) + " % of bpm")

    def mute_track(self):
        self.track.ctrl.mute_track()
        self.GainSlider.setValue(0 if self.track.muted else self.track.gain)
        if (not self.track.muted):
            self.gainButton.setIcon(self.volumeIcon)
        else:
            self.gainButton.setIcon(self.mutedIcon)

    def export_track(self):
        file, check = QFileDialog.getSaveFileName(None, "Export track",
                                                  self.track.name, "SodaTrack (*.soda_track)")
        if check:
            self.track.serialize(file)

    def import_track(self):
        file, check = QFileDialog.getOpenFileName(None, "Import track",
                                                  "", "SodaTrack (*.soda_track)")
        if check:
            self.track.unserialize(file)
            self.display_track(self.track)
            self.parent.advancedTrackView.display_track(self.track)

    def display_track(self, track):
        self.trackNameLineEdit.setText(track.name)
        self.GainSlider.setValue(0 if track.muted else track.gain)
        if (not track.muted):
            self.gainButton.setIcon(self.volumeIcon)
        else:
            self.gainButton.setIcon(self.mutedIcon)
        self.offsetSlider.setValue(int(track.offset))
        self.offsetLabel.setText(str(int(track.offset))+ " % of bpm")
        self.soundfontComboBox.setCurrentIndex(self.soundfontUtil.get_idx_from_path(track.soundfont))
        self.track = track
        self.disconnect_ui()
        self.connect_ui()

        self.TrackSettings_2.show()
        self.track.advancedView.filterFrame.show()
        self.track.advancedView.SettingsFrame.show()

        # self.SoundfontComboBox.set

    def add_track(self, track):
        g_track_frame = QFrame()
        g_track_frame.setObjectName(u"gTrackFrame")
        g_track_frame.setGeometry(QRect(30, 120, 251, 31))
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(g_track_frame.sizePolicy().hasHeightForWidth())
        g_track_frame.setSizePolicy(size_policy)

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
        g_track_delete_button.setMinimumSize(QSize(20, 20))
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

        g_track_view = GTrackView(frame=g_track_frame, deleteButton=g_track_delete_button,
                                selectButton=g_track_select_button, hLayout=horizontal_layout)

        self.gTrackList.append(g_track_view)
        track.gTrackView = g_track_view
        track.generalView = self
        track.advancedView = self.parent.advancedTrackView
        g_track_view.selectButton.setText(track.name)
        g_track_view.selectButton.clicked.connect(lambda: track.ctrl.select())
        g_track_view.deleteButton.clicked.connect(lambda: track.remove())

        self.verticalLayout_4.insertWidget(len(self.gTrackList) - 1, g_track_frame)
        if (len(self.gTrackList) == 1):
            track.ctrl.select()
            self.AddTrackButton.setText("")
            self.parent.visualisationView.GraphFrame.show()
            self.parent.parent.exportAction.setEnabled(True)
            self.parent.parent.saveAction.setEnabled(True)
