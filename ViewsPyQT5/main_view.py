from PyQt5.QtCore import QRect, QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenuBar, QMenu, QStatusBar, QAction

import Models
from Models.data_model import Data
from Models.music_model import Music
from ViewsPyQT5.sonification_view import SonificationView


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = Data.getInstance()
        self.load_data()

        self.setWindowTitle("Soda4LA")
        #self.setGeometry(0,0,1920, 1080)
        self.sonification_main_widget = SonificationView(self)
        #self.sonification_main_widget.setStyleSheet("background-color: black;")

        # Set the central widget of the Window.
        self.setCentralWidget(self.sonification_main_widget)
        self.setupMenu()

    def setupMenu(self):
        self.menubar = self.menuBar()
        self.menubar.setObjectName(u"menubar")
        self.menuFile = self.menubar.addMenu("File")
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = self.menubar.addMenu("Edit")
        self.menuEdit.setObjectName(u"menuEdit")

        self.menuAbout = self.menubar.addAction("About")
        self.menuAbout.setObjectName(u"menuEdit")

        self.menuFile.addAction(QAction('Import data', self))
        self.menuFile.addAction(QAction('Export to .wav', self))
        self.menuFile.addAction(QAction('Open project', self))
        self.menuFile.addAction(QAction('Save project', self))
        self.menuFile.addAction(QAction('Settings', self))
        self.menuFile.addAction(QAction('Exit', self))

        self.menuEdit.addAction(QAction('Undo', self))
        self.setMenuBar(self.menubar)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Pyqt5 for a new look!", 10000)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

    def load_data(self):
        #TODO add other filetype
        m = Music.getInstance()
        if(m.timeSettings.autoload):
            self.db.read_data(m.timeSettings.autoloadDataPath)
            self.db.date_column = m.timeSettings.autoloadTimestampcol
            self.db.assign_timestamps()
            #m.sonification_view.dataTable.set_data(self.db.get_first_and_last().to_dict('records'))
        # else:
        #     filename = askopenfilename(filetypes=[("csv file", "*.csv")])#, (" file",'*.png'), ("All files", " *.* "),))
        #     self.db.read_data(filename)
        #     self.show_data()