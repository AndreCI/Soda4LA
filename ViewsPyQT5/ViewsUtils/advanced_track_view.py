# -*- coding: utf-8 -*-
from collections import namedtuple

from PyQt5.QtCore import QSize, Qt, QRect, QCoreApplication
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy, QWidget, \
    QPushButton, QSpacerItem, QFrame, QLineEdit, QComboBox, QGridLayout, QLabel, \
    QSpinBox, QPlainTextEdit, QCheckBox

from Models.note_model import int_to_note
from ViewsPyQT5.ViewsUtils.views_utils import buttonStyle, selectedButtonStyle

EncodingBox = namedtuple('EncodingBox', ['frame', 'checkbox', 'valueLine', 'dlabel'])


class AdvancedTrackView(object):

    def __init__(self, parent):
        self.parent = parent
        self.key = "value"
        self.track = None
        self.model = None
        self.encoding_boxs = []

    def disconnect_ui(self):
        self.variableComboBox.activated.disconnect()
        self.checkAllButton.clicked.disconnect()
        self.switchAllCheckButton.released.disconnect()
        self.defaultValueLineEdit.textEdited.disconnect()
        self.octaveSpinBox.valueChanged.disconnect()

    def connect_ui(self):
        self.octaveSpinBox.valueChanged.connect(lambda : self.set_octave())
        self.variableComboBox.activated.connect(lambda: self.select_variable(self.variableComboBox.currentText()))
        self.checkAllButton.clicked.connect(lambda: self.set_all_check(True))
        self.switchAllCheckButton.released.connect(self.inverse_all_check)
        self.defaultValueLineEdit.textEdited.connect(self.set_default_value)
        self.applyToAllButton.clicked.connect(self.apply_to_all)

    def display_track(self, track, key=None):
        self.track = track
        if (key is not None and key is not self.key):
            self.track.generalView.advancedOptionButtons[self.key].setStyleSheet(buttonStyle)
            self.track.generalView.advancedOptionButtons[key].setStyleSheet(selectedButtonStyle)
            self.key = key
        if (self.key == "filter"):
            self.detailsScrollArea.hide()
            self.octaveSpinBox.hide()
            self.octaveLabel.hide()
            self.nameLabel.hide()
            self.changeModeButton.hide()
            self.select_variable(self.track.filter.column)
            return
        self.detailsScrollArea.show()
        self.model = track.pencodings[self.key]
        self.select_variable(self.model.filter.column)
        self.defaultValueLineEdit.setText(str(int_to_note(self.model.defaultValue) if self.key == "value"
                                              else self.model.defaultValue))
        #self.nameLabel.show()
        #self.changeModeButton.show()
        if self.key == "value":
            self.octaveSpinBox.show()
            self.octaveLabel.show()
            self.octaveSpinBox.setValue(int(self.model.octave))
        else:
            self.octaveSpinBox.hide()
            self.octaveLabel.hide()
        self.disconnect_ui()
        self.connect_ui()

    def set_default_value(self):
        self.model.ctrl.set_default_value(self.defaultValueLineEdit.text())
        for eb in self.encoding_boxs:
            if eb.checkbox.text() not in self.model.handpickEncoding:
                value = self.model.defaultValue
                if (self.key == "value"):
                    value = int_to_note(value)
                eb.valueLine.setText(str(value))
                eb.dlabel.show()

    def apply_to_all(self):
        for eb in self.encoding_boxs:
            value = self.model.defaultValue
            eb.valueLine.setText(str(int_to_note(value) if self.key == "value" else value))
            self.model.ctrl.reset_value(eb.checkbox.text())
            eb.dlabel.show()

    def inverse_all_check(self):
        bools = [eb.checkbox.isChecked() for eb in self.encoding_boxs]
        for i, eb in enumerate(self.encoding_boxs):
            eb.checkbox.setChecked(not bools[i])
            self.set_qualitative_filter(eb)

    def set_all_check(self, v):
        for eb in self.encoding_boxs:
            if (not eb.checkbox.isChecked()):
                eb.checkbox.setChecked(v)
                self.set_qualitative_filter(eb)

    def select_variable(self, variable):
        self.variableComboBox.clear()
        self.variableComboBox.addItems(self.track.data.get_variables())
        self.variableComboBox.setCurrentIndex(self.track.data.get_variables().index(variable))
        if (self.key == "filter"):
            self.track.ctrl.set_main_var(variable)
            return
        self.model.ctrl.assign_main_var(variable)
        # #Destroy objects linked to previous variable
        for var in self.encoding_boxs:
            self.detailsQModeLayout.removeWidget(var.frame)
            var.valueLine.textEdited.disconnect()
            var.checkbox.clicked.disconnect()
            var.frame.destroy()
            var.checkbox.destroy()
            var.valueLine.destroy()
        self.encoding_boxs = []
        # Create and setup object linked to new variable
        for i, variable in enumerate(self.model.get_variables_instances()):
            if i > 20:
                break
            ebox = self.add_encoding_box()
            ebox.checkbox.setText(str(variable))
            ebox.checkbox.setChecked(self.model.filter.evaluate(variable))
            if str(variable) in self.model.handpickEncoding:
                ebox.dlabel.hide()
                value = self.model.handpickEncoding[str(variable)]
            else:
                value = self.model.defaultValue
            if (self.key == "value"):
                value = int_to_note(value)
            ebox.valueLine.setText(str(value))
            ebox.valueLine.textEdited.connect(lambda ch, ebx=ebox: self.set_value(ebox=ebx))
            ebox.checkbox.clicked.connect(lambda ch2, ebx=ebox: self.set_qualitative_filter(ebox=ebx))
            self.detailsQModeLayout.insertWidget(len(self.encoding_boxs) + 1, ebox.frame)
            self.encoding_boxs.append(ebox)
        self.filterPlainTextEdit.setPlainText(self.model.filter.get_current_filter())

    def set_octave(self):
        self.track.pencodings[self.key].ctrl.change_octave(self.octaveSpinBox.text())

    def set_value(self, ebox):
        self.model.ctrl.set_value(value=ebox.valueLine.text(), variable=ebox.checkbox.text())
        ebox.dlabel.hide()

    def set_qualitative_filter(self, ebox):
        self.model.filter.assign_quali_value(ebox.checkbox.text(), not ebox.checkbox.isChecked())

    def add_encoding_box(self):
        encoding_box = QFrame()
        encoding_box.setObjectName(u"encoding_box")
        encoding_box.setGeometry(QRect(64, 80, 251, 41))
        encoding_box.setFrameShape(QFrame.Panel)
        encoding_box.setFrameShadow(QFrame.Raised)
        encoding_box.setContentsMargins(2, 2, 2, 2)
        encoding_h_layout = QHBoxLayout(encoding_box)
        encoding_h_layout.setObjectName(u"horizontalLayout")
        encoding_check_box = QCheckBox(encoding_box)
        encoding_check_box.setObjectName(u"encoding_check_box")
        encoding_check_box.setToolTip("Add or remove this value from this filter.")

        encoding_h_layout.addWidget(encoding_check_box)
        encoding_h_layout.setContentsMargins(2, 2, 2, 2)
        encoding_h_layout.setSpacing(2)

        encoding_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        encoding_h_layout.addItem(encoding_spacer)

        encoding_value_line_edit = QLineEdit(encoding_box)
        encoding_value_line_edit.setObjectName(u"encoding_value_line_edit")
        # encoding_value_line_edit.setMinimumSize(10, encoding_value_line_edit.minimumHeight())
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(encoding_value_line_edit.sizePolicy().hasHeightForWidth())
        encoding_value_line_edit.setSizePolicy(size_policy)
        encoding_value_line_edit.setToolTip(
            "Assign this encoding to this value.\n"
            "Each non filtered row containing this value will use this encoding for the {} of the note".format(
                self.key))

        default_label = QLabel(encoding_box)
        default_label.setText("default")
        default_label.setToolTip("This value will play the default encoding if not filtered.")

        encoding_h_layout.addWidget(encoding_value_line_edit)
        encoding_h_layout.addWidget(default_label)

        return EncodingBox(frame=encoding_box, checkbox=encoding_check_box, valueLine=encoding_value_line_edit,
                           dlabel=default_label)

    def setup_ui(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.SettingsFrame = QFrame()
        self.SettingsFrame.setObjectName(u"SettingsFrame")
        self.SettingsFrame.setFrameShape(QFrame.Panel)
        self.SettingsFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.SettingsFrame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.octaveLabel = QLabel(self.SettingsFrame)
        self.octaveLabel.setObjectName(u"octaveLabel")

        self.gridLayout_2.addWidget(self.octaveLabel, 2, 0, 1, 1)

        self.variableLabel = QLabel(self.SettingsFrame)
        self.variableLabel.setObjectName(u"variableLabel")

        self.gridLayout_2.addWidget(self.variableLabel, 0, 0, 1, 1)

        self.nameLabel = QLabel()#self.SettingsFrame)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setAlignment(Qt.AlignCenter)

        #self.gridLayout_2.addWidget(self.nameLabel, 1, 0, 1, 1)

        self.octaveSpinBox = QSpinBox(self.SettingsFrame)
        self.octaveSpinBox.setObjectName(u"octaveSpinBox")
        self.octaveSpinBox.setBaseSize(QSize(0, 0))
        self.octaveSpinBox.setWrapping(True)
        self.octaveSpinBox.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.octaveSpinBox.setMaximum(9)
        self.octaveSpinBox.setValue(4)
        self.octaveSpinBox.setToolTip(
            "Select an octave between 1 and 9.\nThe octave is set for each track and influence the value of all notes.")

        self.gridLayout_2.addWidget(self.octaveSpinBox, 2, 1, 1, 1)

        self.changeModeButton = QPushButton()#self.SettingsFrame)
        self.changeModeButton.setObjectName(u"changeModeButton")

        #self.gridLayout_2.addWidget(self.changeModeButton, 1, 1, 1, 1)

        self.variableComboBox = QComboBox(self.SettingsFrame)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.variableComboBox.sizePolicy().hasHeightForWidth())
        self.variableComboBox.setObjectName(u"variableComboBox")
        self.variableComboBox.setSizePolicy(size_policy)
        self.variableComboBox.setToolTip("Select a variable to filter and/or encode")

        self.gridLayout_2.addWidget(self.variableComboBox, 0, 1, 1, 2)

        self.horizontalSpacerName = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalSpacerVariable = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_2.addItem(self.horizontalSpacerVariable, 1, 2, 1, 1)

        self.horizontalSpacerOctave = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_2.addItem(self.horizontalSpacerOctave, 2, 2, 1, 1)

        self.gridLayout.addWidget(self.SettingsFrame, 0, 0, 1, 1)

        self.filterFrame = QFrame()
        self.filterFrame.setObjectName(u"filterFrame")
        self.filterFrame.setFrameShape(QFrame.Panel)
        self.filterFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.filterFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.filterLabel = QLabel(self.filterFrame)
        self.filterLabel.setObjectName(u"filterLabel")

        self.verticalLayout.addWidget(self.filterLabel)

        self.filterPlainTextEdit = QPlainTextEdit(self.filterFrame)
        self.filterPlainTextEdit.setObjectName(u"filterPlainTextEdit")
        self.filterPlainTextEdit.setToolTip(
            "Filter for this track or encoding. Rows which contains a variable found in this filter will not be encoded"
            " into notes.")

        self.verticalLayout.addWidget(self.filterPlainTextEdit)

        self.gridLayout.addWidget(self.filterFrame, 1, 0, 1, 1)

        self.detailsScrollArea = QScrollArea()
        self.detailsScrollArea.setObjectName(u"detailsScrollArea")
        self.detailsScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.detailsScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.detailsScrollArea.setWidgetResizable(True)
        self.detailsScrollArea.setFrameShape(QFrame.Panel)
        self.detailsScrollArea.setFrameShadow(QFrame.Raised)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 308, 397))
        self.detailsQModeLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.detailsQModeLayout.setObjectName(u"verticalLayout_4")
        self.detailsQModeLayout.setSpacing(2)
        self.controlFrame = QFrame(self.scrollAreaWidgetContents)
        self.controlFrame.setObjectName(u"controlFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controlFrame.sizePolicy().hasHeightForWidth())
        self.controlFrame.setSizePolicy(sizePolicy)
        self.controlFrame.setFrameShape(QFrame.Panel)
        self.controlFrame.setFrameShadow(QFrame.Raised)
        self.qualitiveModeOptionsLayout = QGridLayout(self.controlFrame)
        self.qualitiveModeOptionsLayout.setObjectName(u"gridLayout_4")
        self.defaultValueLayout = QHBoxLayout()
        self.defaultValueLayout.setObjectName(u"defaultValueLayout")
        self.defaultValueLabel = QLabel(self.controlFrame)
        self.defaultValueLabel.setObjectName(u"defaultValueLabel")

        self.defaultValueLayout.addWidget(self.defaultValueLabel)

        self.defaultValueLineEdit = QLineEdit(self.controlFrame)
        self.defaultValueLineEdit.setObjectName(u"defaultValueLineEdit")
        self.defaultValueLineEdit.setToolTip(
            "If a value is not filtered and has not been assigned an encoding yet, this will be its encoding")

        self.defaultValueLayout.addWidget(self.defaultValueLineEdit)

        self.checkAllButton = QPushButton(self.controlFrame)
        self.checkAllButton.setObjectName(u"checkAllButton")
        self.checkAllButton.setStyleSheet(buttonStyle)
        self.checkAllButton.setToolTip("Remove all variables from the filter, resetting it.")

        self.switchAllCheckButton = QPushButton(self.controlFrame)
        self.switchAllCheckButton.setObjectName(u"switchAllCheckButton")
        self.switchAllCheckButton.setStyleSheet(buttonStyle)
        self.switchAllCheckButton.setToolTip("Inverse the filter")

        self.applyToAllButton = QPushButton(self.controlFrame)
        self.applyToAllButton.setObjectName(u"applyToAllButton")
        self.applyToAllButton.setStyleSheet(buttonStyle)
        self.applyToAllButton.setToolTip("Apply the default value to all the encoding below.")

        self.qualitiveModeOptionsLayout.addLayout(self.defaultValueLayout, 0, 2, 1, 1)
        self.qualitiveModeOptionsLayout.addWidget(self.applyToAllButton, 1, 2, 1, 1)
        self.qualitiveModeOptionsLayout.addWidget(self.checkAllButton, 1, 0, 1, 1)
        self.qualitiveModeOptionsLayout.addWidget(self.switchAllCheckButton, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.qualitiveModeOptionsLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.qualitiveModeOptionsLayout.addItem(self.horizontalSpacer_2, 1, 1, 1, 1)

        self.detailsQModeLayout.addWidget(self.controlFrame)

        self.detailsVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.detailsQModeLayout.addItem(self.detailsVerticalSpacer)

        self.detailsScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.detailsScrollArea, 0, 1, 2, 1)

        self.retranslate_ui()
        self.connect_ui()
        self.detailsScrollArea.hide()
        self.filterFrame.hide()
        self.SettingsFrame.hide()

    def retranslate_ui(self):
        self.octaveLabel.setText(QCoreApplication.translate("Form", u"Select Octave", None))
        self.variableLabel.setText(QCoreApplication.translate("Form", u"Select Variable", None))
        self.nameLabel.setText(QCoreApplication.translate("Form", u"Track Name", None))
        self.changeModeButton.setText(QCoreApplication.translate("Form", u"Change Mode", None))
        self.filterLabel.setText(QCoreApplication.translate("Form", u"Filter", None))
        self.defaultValueLabel.setText(QCoreApplication.translate("Form", u"Default:", None))
        self.checkAllButton.setText(QCoreApplication.translate("Form", u"Check all", None))
        self.switchAllCheckButton.setText(QCoreApplication.translate("Form", u"Switch all", None))
        self.applyToAllButton.setText(QCoreApplication.translate("Form", u"Apply to all", None))