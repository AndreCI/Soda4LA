import threading
import time
from collections import deque

import pandas as pd
from PyQt5.QtCore import QSize, Qt, QRect, QCoreApplication, QAbstractTableModel, pyqtProperty, pyqtSlot, QVariant, \
    QModelIndex
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy, QAbstractScrollArea, QWidget, \
    QPushButton, QSpacerItem, QFrame, QLineEdit, QComboBox, QSlider, QGridLayout, QLayout, QProgressBar, QLabel, \
    QSpinBox, QAbstractSpinBox, QPlainTextEdit, QTableView, QTableWidget, QTableWidgetItem, QStyledItemDelegate, QStyle, \
    QApplication

from Models.data_model import Data


class TableView(object):

    def __init__(self, parent):
        self.parent = parent

    def setupUi(self):
        self.data = Data.getInstance()
        self.tableFrame = QFrame()
        self.tableFrame.setObjectName(u"tableFrame")
        self.tableFrame.setFrameShape(QFrame.Panel)
        self.tableFrame.setFrameShadow(QFrame.Raised)
        self.tableFrame.setMinimumSize(QSize(720, 300))

        self.verticalLayout = QVBoxLayout(self.tableFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.tableView = QTableView()
        self.model = DataFrameModel(self.data.get_first(), self.data.get_second(), mom=self)
        self.tableView.setModel(self.model)

        self.verticalLayout.addWidget(self.tableView)

class DataFrameModel(QAbstractTableModel):
    DtypeRole = Qt.UserRole + 1000
    ValueRole = Qt.UserRole + 1001

    def __init__(self, df=pd.DataFrame(), dfb=pd.DataFrame(), parent=None, mom=None):
        super(DataFrameModel, self).__init__(parent)
        self._dataframe = df
        self.buffer = deque()
        self.mom = mom
        for d in dfb.itertuples():
            self.buffer.append(d)

    def reset(self, df=pd.DataFrame(), dfb=pd.DataFrame()):
        self.buffer.clear()
        for d in dfb.itertuples():
            self.buffer.append(d)
        self.beginResetModel()
        self._dataframe = df
        self.endResetModel()

    def loadRow(self, row):
        if(row not in self.buffer and row not in self._dataframe):
            self.buffer.append(row)

    def pushRowToDataFrame(self, note_timing):
        time.sleep(note_timing/1000)
        if(len(self.buffer)>0 and self.mom.parent.model.ctrl.playing):
            self.mom.parent.model.ctrl.pausedEvent.wait()  # wait if we are paused
            self.beginResetModel()
            row = self.buffer.popleft()
            self._dataframe = pd.concat([self._dataframe.iloc[1:], pd.DataFrame([row],columns = row._fields)], ignore_index=True)
            self.endResetModel()

    def setDataFrame(self, dataframe):
        self.beginResetModel()
        self._dataframe = dataframe.copy()
        self.endResetModel()

    def dataFrame(self):
        return self._dataframe

    dataFrame = pyqtProperty(pd.DataFrame, fget=dataFrame, fset=setDataFrame)

    @pyqtSlot(int, Qt.Orientation, result=str)
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._dataframe.columns[section]
            else:
                return str(self._dataframe.index[section])
        return QVariant()

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._dataframe.index)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return self._dataframe.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount() and 0 <= index.column() < self.columnCount()):
            return QVariant()
        row = self._dataframe.index[index.row()]
        col = self._dataframe.columns[index.column()]
        dt = self._dataframe[col].dtype

        val = self._dataframe.iloc[row][col]
        if role == Qt.DisplayRole:
            return str(val)
        elif role == DataFrameModel.ValueRole:
            return val
        if role == DataFrameModel.DtypeRole:
            return dt
        return QVariant()

    def roleNames(self):
        roles = {
            Qt.DisplayRole: b'display',
            DataFrameModel.DtypeRole: b'dtype',
            DataFrameModel.ValueRole: b'value'
        }
        return roles


