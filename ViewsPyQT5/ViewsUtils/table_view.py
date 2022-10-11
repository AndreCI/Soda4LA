
from PyQt5.QtCore import QSize, Qt, QRect, QCoreApplication
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy, QAbstractScrollArea, QWidget, \
    QPushButton, QSpacerItem, QFrame, QLineEdit, QComboBox, QSlider, QGridLayout, QLayout, QProgressBar, QLabel, \
    QSpinBox, QAbstractSpinBox, QPlainTextEdit, QTableView, QTableWidget


class TableView(object):
    def setupUi(self):

        self.tableFrame = QFrame()
        self.tableFrame.setObjectName(u"tableFrame")
        self.tableFrame.setFrameShape(QFrame.Panel)
        self.tableFrame.setFrameShadow(QFrame.Raised)
        self.tableFrame.setMinimumSize(QSize(720, 300))

        self.verticalLayout = QVBoxLayout(self.tableFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")



        self.table = QTableWidget()#QTableView() better? https://stackoverflow.com/questions/44603119/how-to-display-a-pandas-data-frame-with-pyqt5-pyside2

        self.table.setRowCount(10)
        self.table.setColumnCount(20)

        self.verticalLayout.addWidget(self.table)