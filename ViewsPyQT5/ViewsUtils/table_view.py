from __future__ import annotations

import logging
import time
from collections import deque
from pathlib import Path

import pandas as pd
from PyQt5.QtCore import QSize, Qt, QCoreApplication, QAbstractTableModel, pyqtProperty, pyqtSlot, QVariant, \
    QModelIndex
from PyQt5.QtWidgets import QSizePolicy, QPushButton, QSpacerItem, QFrame, QLineEdit, QComboBox, QGridLayout, QLabel, \
    QTableView, QFileDialog, QTabWidget

import ViewsPyQT5.sonification_view as sv
from Models.data_model import Data
from Utils.error_manager import ErrorManager


class TableView(object):

    def __init__(self, parent: sv.SonificationView):
        self.parent = parent
        self.data_model = []
        self.currentDataModel = None
        self.currentTableView = None

    def setupUi(self):
        self.data = Data.getInstance()
        self.tableFrame = QFrame()
        self.tableFrame.setObjectName(u"tableFrame")
        self.tableFrame.setFrameShape(QFrame.Panel)
        self.tableFrame.setFrameShadow(QFrame.Raised)
        self.tableFrame.setMinimumSize(QSize(720, 300))

        self.verticalLayout = QGridLayout(self.tableFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.tabWidget = QTabWidget()
        self.tableViews = [QTableView()]
        self.currentTableView = self.tableViews[0]
        self.tabWidget.addTab(self.tableViews[0], "")

        self.generate_ui()

        self.verticalLayout.addWidget(self.dataViewFrame, 0, 0, 1, 2)
        self.verticalLayout.addWidget(self.tabWidget, 1, 0, 1, 5)
        self.dataViewFrame.hide()

        self.retranslate_ui()
        self.connect_ui()
        self.set_tool_tips()

    def set_tool_tips(self):
        self.browseDataButton.setToolTip("Browse to a datafile.")
        self.dataColumnComboBox.setToolTip("Select a column as a master timestamp, that will be used to order notes.\n"
                                           "It must be sequential.")
        self.validateDataButton.setToolTip("Validate data selection, starting the sonification process.")
        self.timestampFormatLineEdit.setToolTip("Informs Soda about the format of the timestamp in the file\n"
                                                "If the format is invalid or not informed, default formats will be tried.\n"
                                                "Exemple of format: \"%d/%m/%Y %H:%M:%S\" for day/month/year hours/minutes/seconds.")

    def connect_ui(self):
        self.browseDataButton.clicked.connect(self.load_data)
        self.dataColumnComboBox.currentIndexChanged.connect(self.column_select)
        self.validateDataButton.clicked.connect(self.validate_data)
        self.tabWidget.currentChanged.connect(self.change_tab)

    def change_tab(self):
        self.parent.topBarView.press_stop_button()
        self.data.set_data_index(self.tabWidget.currentIndex())
        self.currentTableView = self.tableViews[self.tabWidget.currentIndex()]
        self.currentDataModel = self.data_model[self.tabWidget.currentIndex()]
        self.currentDataModel.reset(self.data.sample_size, self.data.get_first(), self.data.get_second())

    def column_select(self):
        if self.dataColumnComboBox.currentText() != "":
            self.tableViews[0].selectColumn(
                self.data_model[0]._dataframe.columns.get_loc(self.dataColumnComboBox.currentText()))

    def load_data(self):
        file, check = QFileDialog.getOpenFileName(None, "Load data file",
                                                  "", "CSV (*.csv)")
        if check:
            self.data.read_primary_data(file)
            self.dataPathLineEdit.setText(file)
            self.setup_data_model()
            self.dataColumnComboBox.setEnabled(True)
            candidates = self.data.get_candidates_timestamp_columns()
            if (len(candidates) == 0):
                candidates = self.data.header
                ErrorManager.getInstance().timestamp_warning()
            self.dataColumnComboBox.addItems(candidates)
            self.validateDataButton.setEnabled(True)
            self.tabWidget.setTabText(0, Path(file).stem)

    def load_additional_data(self):
        file, check = QFileDialog.getOpenFileName(None, "Load data file",
                                                  "", "CSV (*.csv)")
        if check:
            header = self.data.current_dataset.columns
            self.data.read_additional_data(file)
            print(header)
            print(list(self.data.current_dataset.columns))
            if (not ErrorManager.compare_headers(list(header), list(self.data.current_dataset.columns))):
                self.data.set_data_index(self.data.data_index - 1)
                del self.data.df[-1]
                ErrorManager.getInstance().wrong_data_error()
                return
            self.data.assign_timestamps(self.timestampFormatLineEdit.text())
            self.tableViews.append(QTableView())

            self.data_model.append(DataFrameModel(self.data.get_first(), self.data.get_second(), mom=self,
                                                  size=self.data.sample_size))
            self.tableViews[self.data.data_index].setModel(self.data_model[self.data.data_index])
            self.tabWidget.addTab(self.tableViews[self.data.data_index], Path(file).stem)
            self.tabWidget.setCurrentIndex(len(self.tableViews) - 1)

    def setup_data_model(self):
        self.data_model = []
        self.data_model.append(
            DataFrameModel(self.data.get_first(), self.data.get_second(), mom=self, size=self.data.sample_size))
        self.tableViews[0].setModel(self.data_model[0])
        self.currentDataModel = self.data_model[0]
        self.currentTableView = self.tableViews[0]

    def validate_data(self):
        self.data.date_column = self.data.get_candidates_timestamp_columns()[self.dataColumnComboBox.currentIndex()]
        self.data.assign_timestamps(self.timestampFormatLineEdit.text())
        self.dataViewFrame.hide()
        self.parent.trackView.TrackSelectScrollArea.show()
        self.parent.topBarView.AddTrackButton.setEnabled(True)
        self.parent.topBarView.SettingsButton.setEnabled(True)
        self.parent.parent.settingsAction.setEnabled(True)
        self.parent.set_status_text(
            "Data loaded: {} with timestamp column {}".format(self.dataPathLineEdit.text(), self.data.date_column))
        self.dataColumnComboBox.clear()
        self.dataPathLineEdit.setText("")
        if len(self.parent.model.tracks) > 0:
            self.parent.model.ctrl.purge_tracks()

    def generate_ui(self):
        self.dataViewFrame = QFrame()
        self.dataViewFrame.setObjectName(u"dataViewFrame")
        self.dataViewFrame.setFrameShape(QFrame.Box)
        self.dataViewFrame.setLineWidth(3)
        self.dataViewFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.dataViewFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

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

        self.dataColumnLabel = QLabel(self.dataViewFrame)
        self.dataColumnLabel.setObjectName(u"dataColumnLabel")
        self.dataColumnComboBox.setEnabled(False)

        self.gridLayout.addWidget(self.dataColumnLabel, 1, 1, 1, 1)

        self.timestampFormatLabel = QLabel(self.dataViewFrame)
        self.timestampFormatLabel.setObjectName(u"timestampFormatLabel")
        self.timestampFormatLineEdit = QLineEdit(self.dataViewFrame)
        self.timestampFormatLineEdit.setObjectName(u"timestampFormatLineEdit")
        self.gridLayout.addWidget(self.timestampFormatLabel, 2, 1, 1, 3)
        self.gridLayout.addWidget(self.timestampFormatLineEdit, 2, 2, 1, 3)

        self.validateDataButton = QPushButton(self.dataViewFrame)
        self.validateDataButton.setObjectName(u"validateDataButton")
        self.validateDataButton.setEnabled(False)

        self.gridLayout.addWidget(self.validateDataButton, 3, 1, 1, 3)

        self.dataPathLabel = QLabel(self.dataViewFrame)
        self.dataPathLabel.setObjectName(u"dataPathLabel")

        self.gridLayout.addWidget(self.dataPathLabel, 0, 1, 1, 1)

    def retranslate_ui(self):
        self.dataPathLabel.setStyleSheet("font-size:18px")
        self.dataColumnLabel.setStyleSheet("font-size:18px")
        self.timestampFormatLabel.setStyleSheet("font-size:18px")
        self.dataColumnLabel.setText(QCoreApplication.translate("Form", u"Timestamp Column", None))
        self.dataPathLabel.setText(QCoreApplication.translate("Form", u"Data file", None))
        self.browseDataButton.setText(QCoreApplication.translate("Form", u"Browse...", None))
        self.validateDataButton.setText(QCoreApplication.translate("Form", u"Validate", None))
        self.timestampFormatLabel.setText(QCoreApplication.translate("Form", u"TimeStamp Format", None))
    # retranslateUi


class DataFrameModel(QAbstractTableModel):
    DtypeRole = Qt.UserRole + 1000
    ValueRole = Qt.UserRole + 1001

    def __init__(self, df=pd.DataFrame(), dfb=pd.DataFrame(), size=20, parent=None, mom=None):
        super(DataFrameModel, self).__init__(parent)
        self._dataframe = df
        self.size = size
        self.buffer = deque()
        self.mom = mom
        for d in dfb.itertuples():
            self.buffer.append(d)

    def reset(self, size=None, df=pd.DataFrame(), dfb=pd.DataFrame()):
        if size is not None:
            self.size = size
        self.buffer.clear()
        for d in dfb.itertuples():
            self.buffer.append(d)
        self.beginResetModel()
        self._dataframe = df
        self.endResetModel()

    def load_row(self, row):
        if (self._dataframe.shape[0] <= self.size - 1):
            self.beginResetModel()
            self._dataframe = pd.concat([self._dataframe.iloc[1:], pd.DataFrame([row], columns=row._fields)],
                                        ignore_index=True)
            self._dataframe.reset_index(inplace=True, drop=True)
            self.endResetModel()
        elif (row not in self.buffer and row not in self._dataframe):
            self.buffer.append(row)

    def push_row_to_data_frame(self, note_timing):
        if note_timing > 0:
            time.sleep(note_timing / 1000)
        if not self.mom.parent.model.ctrl.playing:
            return
        self.mom.parent.model.ctrl.pausedEvent.wait()  # wait if we are paused
        try:
            self.beginResetModel()
            if (len(self.buffer) > 0):
                row = [self.buffer.popleft()]
                if (self._dataframe.shape[0] <= self.size - 1 and len(self.buffer) > 0):
                    row.append(self.buffer.popleft())
                # row['internal_filter'] = row["internal_filter"].astype(bool)
                self._dataframe = pd.concat([self._dataframe.iloc[1:], pd.DataFrame(row, columns=row[0]._fields)],
                                            ignore_index=True)
            else:
                # print("reducing from {}".format(self._dataframe.shape))
                self._dataframe = self._dataframe.iloc[1:]
            self._dataframe.reset_index(inplace=True, drop=True)
            self.endResetModel()
        except Exception:
            logging.log(logging.WARNING, "Exception while pushing rows to data table.")

    def set_data_frame(self, dataframe):
        self.beginResetModel()
        self._dataframe = dataframe.copy()
        self.endResetModel()

    def data_frame(self):
        return self._dataframe

    dataFrame = pyqtProperty(pd.DataFrame, fget=data_frame, fset=set_data_frame)

    @pyqtSlot(int, Qt.Orientation, result=str)
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._dataframe.columns[section]
            else:
                try:
                    return str(self._dataframe.index[section])
                except IndexError:
                    return QVariant()
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
        try:
            # val = self._dataframe.loc[index.row(), index.column()]
            val = self._dataframe.iloc[row][col]
        except IndexError:
            val = 0
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
