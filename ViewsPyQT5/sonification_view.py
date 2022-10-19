import logging
import threading
import tkinter as tk
from collections import deque
from tkinter import ttk
from tkinter.constants import DISABLED, NORMAL
from tkinter.filedialog import askopenfilename, asksaveasfile

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy, \
    QFileDialog

from Models.music_model import Music
from Utils.constants import DEFAULT_PADDING, TFRAME_STYLE, DEFAULT_PADX, DEFAULT_PADY, FILE_PATH
from Utils.scrollable_frame import ScrollableFrame
from Utils.tktable_table import Table
from Views.grapical_view import GraphicalView
from Views.track_config_view import TrackConfigView
from Views.track_midi_view import TrackMidiView
from ViewsPyQT5.ViewsUtils.advanced_track_view import AdvancedTrackView
from ViewsPyQT5.ViewsUtils.table_view import TableView
from ViewsPyQT5.ViewsUtils.top_bar import TopSettingsBar
from ViewsPyQT5.ViewsUtils.track_view import TrackView
from ViewsPyQT5.ViewsUtils.graphical_view import GraphView
from ViewsPyQT5.settings_view import SettingsView


class SonificationView(QWidget):
    """
    Main view for the sonification process, handling both configuration and midi representation of the loaded data.
    Modules: list of tracks, each with their own config and midi view.
    view to control the start, pause and stop of the current music
    view to configurate time settings
    """

    # TODO: Add fast forward and backward +x/-x seconds
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        # #Ctrl and model
        # self.model = Music.getInstance()
        # self.ctrl = self.model.ctrl
        # self.model.sonification_view = self
        # self.ctrl.sonification_view = self
        self.parent = parent
        # View data
        self.configView = True  # Inform which view is currently displqyed
        self.trackConfigViews = []
        self.trackMidiViews = []
        self.log = deque()
        self.logMax = 10
        self.first_log_line = "Log:" + " " * 205 + "\n"
        self.model = Music.getInstance()
        self.model.sonification_view = self

        self.setGeometry(0, 0, 1980, 1020)
        self.windowLayout = QVBoxLayout(self)
        self.centralLayout = QHBoxLayout()
        self.trackLayout = QVBoxLayout()
        self.graphLayout = QVBoxLayout()

        self.settingsView = SettingsView(self)
        self.topBarView = TopSettingsBar(self)
        self.topBarView.setupUi()
        self.trackView = TrackView(self)
        self.advancedTrackView = AdvancedTrackView(self)
        self.trackView.setupUi()
        self.advancedTrackView.setupUi()
        self.visualisationView = GraphView(self)
        self.tableView = TableView(self)
        self.tableView.setupUi()
        # self.visualisation_layout.addWidget(visu._main)
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
        #self.trackView.TrackSelectScrollArea.hide()
        # self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.graphLayout.addItem(self.verticalSpacer)

    def set_status_text(self, line, timing=5000):
        self.parent.statusbar.showMessage(line, timing)

    def add_log_line(self, log_line, debug=False):
        if (debug or not self.model.timeSettings.debugVerbose):
            if (len(self.log) > self.logMax):
                self.log.popleft()
            self.log.append(log_line)
            self.logVar.set(self.first_log_line + "\n".join(self.log))
            logging.info(log_line)

    def open_settings(self):
        self.model.timeSettings.ctrl.open_time_settings(self.settingsView)

    def open_time_setting(self):
        self.model.timeSettings.ctrl.open_time_settings()

    def export_music(self):
        file, check = QFileDialog.getSaveFileName(None, "Export music",
                                                  "saved_music", "Wav file (*.wav)")
        if check:
            self.set_status_text("writing {}".format(file))
            threading.Thread(target=self.model.ctrl.export_music, args=[file], daemon=True).start()

    def export_all_tracks(self):
        file, check = QFileDialog.getSaveFileName(None, "Save project",
                                                  "project with {} tracks".format(len(self.model.tracks)),
                                                  "Soda4LA Project file (*.soda4la)")
        if check:
            self.model.ctrl.export_all_tracks(file)

    def import_all_tracks(self):
        file, check = QFileDialog.getOpenFileName(None, "Open project", "", "Soda4LA Project file (*.soda4la)")
        if check:
            self.model.ctrl.import_all_tracks(file)
