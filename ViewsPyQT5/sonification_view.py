import logging
import threading
from collections import deque

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog

from Models.music_model import Music
from ViewsPyQT5.ViewsUtils.advanced_track_view import AdvancedTrackView
from ViewsPyQT5.ViewsUtils.graphical_view import GraphView
from ViewsPyQT5.ViewsUtils.table_view import TableView
from ViewsPyQT5.ViewsUtils.top_bar import TopSettingsBar
from ViewsPyQT5.ViewsUtils.track_view import TrackView
from ViewsPyQT5.settings_view import SettingsView


class SonificationView(QWidget):
    """
    Main view for the sonification process, handling both configuration and representation of the loaded data.
    """
    messageChanged = pyqtSignal(str)
    # TODO: Add fast forward and backward +x/-x seconds
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.model = Music.getInstance()
        self.model.sonification_view = self

        self.setGeometry(0, 0, 1980, 1020)
        self.windowLayout = QVBoxLayout(self)
        self.centralLayout = QHBoxLayout()
        self.trackLayout = QVBoxLayout()
        self.graphLayout = QVBoxLayout()

        self.settingsView = SettingsView(self)
        self.visualisationView = GraphView(self)

        self.topBarView = TopSettingsBar(self)
        self.topBarView.setupUi()

        self.trackView = TrackView(self)
        self.advancedTrackView = AdvancedTrackView(self)
        self.trackView.setupUi()
        self.advancedTrackView.setup_ui()

        self.tableView = TableView(self)
        self.tableView.setupUi()

        self.windowLayout.addLayout(self.topBarView.horizontalLayout)
        self.windowLayout.addLayout(self.centralLayout)
        self.centralLayout.addLayout(self.trackLayout)
        self.centralLayout.addLayout(self.graphLayout)
        self.centralLayout.setStretch(0, 2)
        self.centralLayout.setStretch(1, 3)
        self.trackLayout.addLayout(self.trackView.verticalLayout)
        self.trackLayout.addLayout(self.advancedTrackView.gridLayout)
        self.graphLayout.addWidget(self.visualisationView.GraphFrame)
        self.graphLayout.addWidget(self.tableView.tableFrame)
        self.visualisationView.GraphFrame.hide()

        self.messageChanged.connect(self.show_message)

    def show_message(self, msg):
        self.parent.statusbar.showMessage(msg, 5000)

    def set_status_text(self, line, timing=5000):
        self.messageChanged.emit(line)

    def open_settings(self):
        self.model.settings.ctrl.open_settings(self.settingsView)

    def export_music(self):
        file, check = QFileDialog.getSaveFileName(None, "Export music",
                                                  "saved_music", "Wav file (*.wav)")
        if check:
            self.set_status_text("writing {}".format(file))
            threading.Thread(target=self.model.ctrl.export_music, args=[file], daemon=True, name="export_music_thread").start()

    def export_all_tracks(self):
        file, check = QFileDialog.getSaveFileName(None, "Save project",
                                                  "project with {} tracks".format(len(self.model.tracks)),
                                                  "Soda Project file (*.soda)")
        if check:
            self.model.ctrl.export_all_tracks(file)

    def import_all_tracks(self):
        file, check = QFileDialog.getOpenFileName(None, "Open project", "", "Soda Project file (*.soda)")
        if check:
            self.model.ctrl.import_all_tracks(file)
