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
    QApplication, QFileDialog

from Models.data_model import Data
#from ViewsPyQT5.sonification_view import SonificationView


class TableView(object):

    def __init__(self, parent):
        self.parent = parent
        self.data_model = None

    def setupUi(self):
        self.data = Data.getInstance()
        self.tableFrame = QFrame()
        self.tableFrame.setObjectName(u"tableFrame")
        self.tableFrame.setFrameShape(QFrame.Panel)
        self.tableFrame.setFrameShadow(QFrame.Raised)
        self.tableFrame.setMinimumSize(QSize(720, 300))

        self.verticalLayout = QGridLayout(self.tableFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.tableView = QTableView()

        self.generate_Ui()

        self.verticalLayout.addWidget(self.dataViewFrame, 0, 0 ,1, 2)
        self.verticalLayout.addWidget(self.tableView, 1, 0 ,1, 5)
        self.dataViewFrame.hide()

        self.retranslateUi()
        self.connectUi()
        self.setToolTips()


    def setToolTips(self):
        self.browseDataButton.setToolTip("Browse to a datafile.")
        self.dataColumnComboBox.setToolTip("Select a column as a master timestamp, that will be used to order notes.\n"
                                           "It must be sequential.")
        self.validateDataButton.setToolTip("Validate data selection, starting the sonification process.")

    def connectUi(self):
        self.browseDataButton.clicked.connect(self.loadData)
        self.dataColumnComboBox.currentIndexChanged.connect(self.columnSelect)
        self.validateDataButton.clicked.connect(self.validateData)

    def columnSelect(self):
        if self.dataColumnComboBox.currentText() != "":
            self.tableView.selectColumn(self.data_model._dataframe.columns.get_loc(self.dataColumnComboBox.currentText()))

    def loadData(self):
        file, check = QFileDialog.getOpenFileName(None, "Load data file",
                                                  "", "CSV (*.csv)")
        if check:
            self.data.read_data(file)
            self.dataPathLineEdit.setText(file)
            self.setupDataModel()
            self.dataColumnComboBox.setEnabled(True)
            self.dataColumnComboBox.addItems(self.data.get_candidates_timestamp_columns())
            self.validateDataButton.setEnabled(True)

    def setupDataModel(self):
        self.data_model = DataFrameModel(self.data.get_first(), self.data.get_second(), mom=self)
        self.tableView.setModel(self.data_model)

    def validateData(self):
        self.data.date_column = self.data.get_candidates_timestamp_columns()[self.dataColumnComboBox.currentIndex()]
        self.data.assign_timestamps()
        self.dataViewFrame.hide()
        self.parent.trackView.TrackSelectScrollArea.show()
        self.parent.topBarView.AddTrackButton.setEnabled(True)
        self.parent.topBarView.SettingsButton.setEnabled(True)
        self.parent.parent.settingsAction.setEnabled(True)
        self.parent.set_status_text("Data loaded: {} with timestamp column {}".format(self.dataPathLineEdit.text(), self.data.date_column))
        self.dataColumnComboBox.clear()
        self.dataPathLineEdit.setText("")
        if len(self.parent.model.tracks) > 0:
            self.parent.model.ctrl.purge_tracks()

    def generate_Ui(self):
        self.dataViewFrame = QFrame()
        self.dataViewFrame.setObjectName(u"dataViewFrame")
        self.dataViewFrame.setFrameShape(QFrame.Box)
        self.dataViewFrame.setLineWidth(3)
        self.dataViewFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.dataViewFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        #self.gridLayout.addItem(self.horizontalSpacer, 0, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        #self.gridLayout.addItem(self.horizontalSpacer_3, 2, 4, 1, 1)

        self.browseDataButton = QPushButton(self.dataViewFrame)
        self.browseDataButton.setObjectName(u"browseDataButton")

        self.gridLayout.addWidget(self.browseDataButton, 0, 3, 1, 1)

        self.dataPathLineEdit = QLineEdit(self.dataViewFrame)
        self.dataPathLineEdit.setObjectName(u"dataPathLineEdit")
        self.dataPathLineEdit.setReadOnly(True)

        self.gridLayout.addWidget(self.dataPathLineEdit, 0, 2, 1, 1)

        self.dataColumnComboBox = QComboBox(self.dataViewFrame)
        self.dataColumnComboBox.setObjectName(u"dataColumnComboBox")

        self.gridLayout.addWidget(self.dataColumnComboBox, 1, 2, 1, 2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        #self.gridLayout.addItem(self.horizontalSpacer_2, 1, 4, 1, 1)

        self.dataColumnLabel = QLabel(self.dataViewFrame)
        self.dataColumnLabel.setObjectName(u"dataColumnLabel")
        self.dataColumnComboBox.setEnabled(False)

        self.gridLayout.addWidget(self.dataColumnLabel, 1, 1, 1, 1)

        self.validateDataButton = QPushButton(self.dataViewFrame)
        self.validateDataButton.setObjectName(u"validateDataButton")
        self.validateDataButton.setEnabled(False)

        self.gridLayout.addWidget(self.validateDataButton, 2, 1, 1, 3)

        self.dataPathLabel = QLabel(self.dataViewFrame)
        self.dataPathLabel.setObjectName(u"dataPathLabel")

        self.gridLayout.addWidget(self.dataPathLabel, 0, 1, 1, 1)

    def retranslateUi(self):
        self.dataPathLabel.setStyleSheet("font-size:25px")
        self.dataColumnLabel.setStyleSheet("font-size:25px")
        self.dataColumnLabel.setText(QCoreApplication.translate("Form", u"Date Column", None))
        self.dataPathLabel.setText(QCoreApplication.translate("Form", u"Data file", None))
        self.browseDataButton.setText(QCoreApplication.translate("Form", u"Browse...", None))
        self.validateDataButton.setText(QCoreApplication.translate("Form", u"Validate", None))
    # retranslateUi

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


