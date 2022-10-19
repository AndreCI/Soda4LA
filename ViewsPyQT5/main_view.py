from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QAction

from Models.data_model import Data
from Models.music_model import Music
from ViewsPyQT5.sonification_view import SonificationView


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = Data.getInstance()

        self.setWindowTitle("Soda4LA")
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

        self.dataAction = QAction('Import data', self)
        self.menuFile.addAction(self.dataAction)
        self.exportAction = QAction('Export to .wav', self)
        self.menuFile.addAction(self.exportAction)
        self.exportAction.setEnabled(False)
        self.openAction = QAction('Open project', self)
        self.menuFile.addAction(self.openAction)
        self.saveAction = QAction('Save project', self)
        self.menuFile.addAction(self.saveAction)
        self.saveAction.setEnabled(False)
        self.settingsAction = QAction('Settings', self)
        self.menuFile.addAction(self.settingsAction)
        self.exitAction = QAction('Exit', self)
        self.menuFile.addAction(self.exitAction)

        #self.menuEdit.addAction(QAction('Undo', self))
        self.setMenuBar(self.menubar)

        self.exportAction.triggered.connect(self.sonification_main_widget.export_music)
        self.settingsAction.triggered.connect(self.sonification_main_widget.open_settings)
        self.exitAction.triggered.connect(QCoreApplication.quit)
        self.dataAction.triggered.connect(self.show_load_data)
        self.saveAction.triggered.connect(self.sonification_main_widget.export_all_tracks)
        self.openAction.triggered.connect(self.sonification_main_widget.import_all_tracks)

    def setup_statusbar(self):
        self.statusbar = self.statusBar()
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

    def show_load_data(self):
        if self.sonification_main_widget.tableView.data_model is not None:
            self.sonification_main_widget.tableView.data_model.reset()
        self.sonification_main_widget.trackView.TrackSelectScrollArea.hide()
        self.sonification_main_widget.visualisationView.GraphFrame.hide()
        self.sonification_main_widget.tableView.dataViewFrame.show()

        self.sonification_main_widget.trackView.TrackSettings_2.hide()
        self.sonification_main_widget.trackView.retranslate_ui()
        self.sonification_main_widget.advancedTrackView.filterFrame.hide()
        self.sonification_main_widget.advancedTrackView.SettingsFrame.hide()
        self.sonification_main_widget.advancedTrackView.detailsScrollArea.hide()
        self.saveAction.setEnabled(False)
        self.exportAction.setEnabled(False)
        self.settingsAction.setEnabled(False)
        self.sonification_main_widget.topBarView.AddTrackButton.setEnabled(False)
        self.sonification_main_widget.topBarView.SettingsButton.setEnabled(False)
        self.sonification_main_widget.tableView.load_data()

    def load_data(self):
        # TODO add other filetype
        # TODO load multiples datafiles in tab?
        m = Music.getInstance()
        if (m.timeSettings.autoload):
            self.db.read_data(m.timeSettings.autoloadDataPath)
            self.db.date_column = m.timeSettings.autoloadTimestampcol
            self.db.assign_timestamps()
            self.sonification_main_widget.tableView.setup_data_model()
            self.statusbar.showMessage("Data loaded automatically from {} with timestamp column {}. "
                                       "You can disable this in the settings.".format(m.timeSettings.autoloadDataPath,
                                                                                      m.timeSettings.autoloadTimestampcol),
                                       20000)
        else:
            self.sonification_main_widget.trackView.TrackSelectScrollArea.hide()
            self.sonification_main_widget.tableView.dataViewFrame.show()
            self.sonification_main_widget.topBarView.AddTrackButton.setEnabled(False)
            self.sonification_main_widget.topBarView.SettingsButton.setEnabled(False)
            self.settingsAction.setEnabled(False)
