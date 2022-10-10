from PyQt5.QtCore import QRect, QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenuBar, QMenu, QStatusBar, QAction

from ViewsPyQT5.sonification_view import SonificationView


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Soda4LA")
        #self.setGeometry(0,0,1920, 1080)
        self.sonification_main_widget = SonificationView(self)

        # Set the central widget of the Window.
        self.setCentralWidget(self.sonification_main_widget)

        self.menubar = self.menuBar()
        self.menubar.setObjectName(u"menubar")
        self.menuFile = self.menubar.addMenu("File")
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = self.menubar.addMenu("Edit")
        self.menuEdit.setObjectName(u"menuEdit")

        self.menuFile.addAction(QAction('Open', self))
        self.setMenuBar(self.menubar)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Pyqt5 for a new look!", 10000)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)
