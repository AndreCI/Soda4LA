from pathlib import Path

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QAction, QShortcut

from Models.data_model import Data
from Models.music_model import Music
from ViewsPyQT5.sonification_view import SonificationView


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = Data.getInstance()

        self.setWindowTitle("Soda")
        self.setup_statusbar()
        self.sonification_main_widget = SonificationView(self)
        self.setup_menu()
        self.load_data()

        # Set the central widget of the Window.
        self.setCentralWidget(self.sonification_main_widget)

    def setup_menu(self):
        self.menubar = self.menuBar()
        self.menubar.setObjectName(u"menubar")
        self.menuFile = self.menubar.addMenu("File")
        self.menuFile.setObjectName(u"menuFile")
        #self.menuEdit = self.menubar.addMenu("Edit")
        #self.menuEdit.setObjectName(u"menuEdit")

        #self.menuAbout = self.menubar.addAction("About")
        #self.menuAbout.setObjectName(u"menuEdit")

        self.dataAction = QAction('Import data\tCtrl+D', self)
        self.dataActionShortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        self.menuFile.addAction(self.dataAction)
        self.dataAdditionalAction = QAction('Import additional data\tCtrl+A', self)
        self.dataAdditionalShortcut = QShortcut(QKeySequence("Ctrl+A"), self)
        self.menuFile.addAction(self.dataAdditionalAction)
        self.exportAction = QAction('Export to .wav\tCtrl+E', self)
        self.exportActionShortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        self.menuFile.addAction(self.exportAction)
        self.exportAction.setEnabled(False)
        self.openAction = QAction('Open project\tCtrl+L', self)
        self.openActionShortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        self.menuFile.addAction(self.openAction)
        self.saveAction = QAction('Save project\tCtrl+S', self)
        self.saveActionShortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.menuFile.addAction(self.saveAction)
        self.saveAction.setEnabled(False)
        self.settingsAction = QAction('Settings\tCtrl+T', self)
        self.settingsActionShortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        self.menuFile.addAction(self.settingsAction)
        self.playAction = QAction('Play/Pause\tSpace', self)
        self.playAction.setEnabled(False)
        self.playActionShortcut = QShortcut(QKeySequence("Space"), self)
        self.menuFile.addAction(self.playAction)
        self.exitAction = QAction('Exit', self)
        self.menuFile.addAction(self.exitAction)

        #self.menuEdit.addAction(QAction('Undo', self))
        self.setMenuBar(self.menubar)

        self.exportAction.triggered.connect(self.sonification_main_widget.export_music)
        self.exportActionShortcut.activated.connect(self.sonification_main_widget.export_music)
        self.settingsAction.triggered.connect(self.sonification_main_widget.open_settings)
        self.settingsActionShortcut.activated.connect(self.sonification_main_widget.open_settings)
        self.exitAction.triggered.connect(QCoreApplication.quit)
        self.dataAction.triggered.connect(self.show_load_data)
        self.dataActionShortcut.activated.connect(self.show_load_data)
        self.dataAdditionalAction.triggered.connect(self.show_load_additional_data)
        self.dataAdditionalShortcut.activated.connect(self.show_load_additional_data)
        self.saveAction.triggered.connect(self.sonification_main_widget.export_all_tracks)
        self.saveActionShortcut.activated.connect(self.sonification_main_widget.export_all_tracks)
        self.playAction.triggered.connect(self.sonification_main_widget.topBarView.press_pp_button)
        self.playActionShortcut.activated.connect(self.sonification_main_widget.topBarView.press_pp_button)
        self.openAction.triggered.connect(self.sonification_main_widget.import_all_tracks)
        self.openActionShortcut.activated.connect(self.sonification_main_widget.import_all_tracks)


    def setup_statusbar(self):
        self.statusbar = self.statusBar()
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

    def show_load_data(self):
        self.sonification_main_widget.topBarView.press_stop_button()
        if self.sonification_main_widget.tableView.currentDataModel is not None:
            self.sonification_main_widget.tableView.currentDataModel.reset()
        self.sonification_main_widget.trackView.TrackSelectScrollArea.hide()
        self.sonification_main_widget.visualisationView.GraphFrame.hide()
        self.sonification_main_widget.tableView.dataViewFrame.show()

        self.sonification_main_widget.trackView.TrackSettings_2.hide()
        self.sonification_main_widget.trackView.retranslate_ui()
        self.sonification_main_widget.advancedTrackView.detailsScrollArea.hide()
        self.saveAction.setEnabled(False)
        self.exportAction.setEnabled(False)
        self.settingsAction.setEnabled(False)
        self.sonification_main_widget.topBarView.AddTrackButton.setEnabled(False)
        self.sonification_main_widget.topBarView.SettingsButton.setEnabled(False)

        self.sonification_main_widget.tableView.load_data()

    def show_load_additional_data(self):
        self.sonification_main_widget.tableView.load_additional_data()

    def load_data(self):
        # TODO add other filetypes
        m = Music.getInstance()
        if (m.settings.autoload):
            self.db.read_primary_data(m.settings.autoloadDataPath)
            self.db.date_column = m.settings.autoloadTimestampcol
            self.db.assign_timestamps()
            self.sonification_main_widget.tableView.setup_data_model()
            self.sonification_main_widget.tableView.tabWidget.setTabText(0, Path(m.settings.autoloadDataPath).stem)

            self.statusbar.showMessage("Data loaded automatically from {} with timestamp column {}. "
                                       "You can disable this in the settings.".format(m.settings.autoloadDataPath,
                                                                                      m.settings.autoloadTimestampcol),
                                       20000)
        else:
            self.sonification_main_widget.trackView.TrackSelectScrollArea.hide()
            self.sonification_main_widget.tableView.dataViewFrame.show()
            self.sonification_main_widget.topBarView.AddTrackButton.setEnabled(False)
            self.sonification_main_widget.topBarView.SettingsButton.setEnabled(False)
            self.settingsAction.setEnabled(False)
