from __future__ import annotations

from collections import namedtuple

from PyQt5.QtCore import QSize, Qt, QRect, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy, QWidget, \
    QPushButton, QSpacerItem, QFrame, QLineEdit, QComboBox, QGridLayout, QLabel, \
    QSpinBox, QCheckBox

import ViewsPyQT5.sonification_view as sv
from Models.note_model import int_to_note, TNote
from ViewsPyQT5.ViewsUtils.views_utils import buttonStyle, selectedButtonStyle

EncodingBox = namedtuple('EncodingBox', ['frame', 'checkbox', 'testButton', 'valueLine'])


class AdvancedTrackView(object):

    def __init__(self, parent: sv.SonificationView):
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
        self.octaveSpinBox.valueChanged.connect(lambda: self.set_octave())
        self.variableComboBox.activated.connect(lambda: self.select_variable(self.variableComboBox.currentText()))
        self.checkAllButton.clicked.connect(lambda: self.set_all_check(True))
        self.switchAllCheckButton.released.connect(self.inverse_all_check)
        self.defaultValueLineEdit.textEdited.connect(self.set_default_value)
        self.applyToAllButton.clicked.connect(self.apply_default_to_all)
        self.randomToAllButton.clicked.connect(self.apply_random_to_all)

    def display_track(self, track, key=None):
        self.track = track
        if (key is not None and key is not self.key):
            self.track.generalView.advancedOptionButtons[self.key].setStyleSheet(buttonStyle)
            self.track.generalView.advancedOptionButtons[key].setStyleSheet(selectedButtonStyle)
            self.key = key
        self.detailsScrollArea.show()
        self.model = track.pencodings[self.key]
        self.select_variable(self.model.filter.column)
        self.defaultValueLineEdit.setText(str(int_to_note(self.model.defaultValue) if self.key == "value"
                                              else self.model.defaultValue))
        # self.nameLabel.show()
        # self.changeModeButton.show()
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

    def apply_random_to_all(self):
        variables = []
        for eb in self.encoding_boxs:
            variables.append(eb.checkbox.text())
        values = self.model.generate_preset(variables)
        for i, eb in enumerate(self.encoding_boxs):
            value = int(values[i])
            eb.valueLine.setText(str(int_to_note(value) if self.key == "value" else value))
            self.set_value(eb)
            # self.model.ctrl.set_value(eb.checkbox.text(), str(value))

    def apply_default_to_all(self):
        for eb in self.encoding_boxs:
            value = self.model.defaultValue
            eb.valueLine.setText(str(int_to_note(value) if self.key == "value" else value))
            self.model.ctrl.reset_value(eb.checkbox.text())

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
            var.testButton.clicked.disconnect()
            var.frame.destroy()
            var.checkbox.destroy()
            var.valueLine.destroy()
            var.testButton.destroy()
        self.encoding_boxs = []
        # Create and setup object linked to new variable
        for i, variable in enumerate(self.model.get_variables_instances()):
            if i > 20:
                break
            ebox = self.add_encoding_box()
            ebox.checkbox.setText(str(variable))
            ebox.checkbox.setChecked(self.model.filter.evaluate(variable))
            if str(variable) in self.model.handpickEncoding:
                value = self.model.handpickEncoding[str(variable)]
            else:
                value = self.model.defaultValue
            if (self.key == "value"):
                value = int_to_note(value)
            ebox.valueLine.setText(str(value))
            ebox.valueLine.textEdited.connect(lambda ch, ebx=ebox: self.set_value(ebox=ebx))
            ebox.checkbox.clicked.connect(lambda ch2, ebx=ebox: self.set_qualitative_filter(ebox=ebx))
            ebox.testButton.clicked.connect(lambda ch3, ebx=ebox: self.play_test_sound(ebox=ebx))
            self.detailsQModeLayout.insertWidget(len(self.encoding_boxs) + 1, ebox.frame)
            self.encoding_boxs.append(ebox)
        # self.filterPlainTextEdit.setPlainText(self.model.filter.get_current_filter())

    def set_octave(self):
        self.track.pencodings[self.key].ctrl.change_octave(self.octaveSpinBox.text())

    def set_value(self, ebox):
        self.model.ctrl.set_value(value=ebox.valueLine.text(), variable=ebox.checkbox.text())

    def set_qualitative_filter(self, ebox):
        self.model.filter.assign_quali_value(ebox.checkbox.text(), not ebox.checkbox.isChecked())

    def play_test_sound(self, ebox):
        value = self.track.pencodings["value"].get_parameter_from_variable(ebox.checkbox.text())
        duration = self.track.pencodings["duration"].get_parameter_from_variable(ebox.checkbox.text())
        velocity = self.track.pencodings["velocity"].get_parameter_from_variable(ebox.checkbox.text())
        self.parent.model.ctrl.play_note(
            TNote(tfactor=0, channel=self.track.id, id=0, duration=duration, velocity=velocity, value=value,
                  void=False))

    def add_encoding_box(self):
        """
        Create an encoding box, with these elements: checkbox, name, spacer, sound button, lineedit
        :return: a QFrame with all elements to customize the encoding of a value
        """
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

        # encoding_h_layout.addItem(encoding_spacer)

        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)

        soundButton = QPushButton(encoding_box)
        soundButton.setObjectName(u"soundButton")
        soundButton.setSizePolicy(size_policy)
        soundButton.setMinimumSize(QSize(0, 0))
        soundButton.setMaximumSize(QSize(36, 16777215))
        soundButton.setStyleSheet(buttonStyle)
        soundIcon = QIcon()
        soundIcon.addFile(u"data/img/icons/volume-up.svg", QSize(), QIcon.Normal, QIcon.Off)
        soundButton.setIcon(soundIcon)
        soundButton.setToolTip("Test this sound")

        encoding_value_line_edit = QLineEdit(encoding_box)
        encoding_value_line_edit.setObjectName(u"encoding_value_line_edit")
        size_policy.setHeightForWidth(encoding_value_line_edit.sizePolicy().hasHeightForWidth())
        # encoding_value_line_edit.setMinimumSize(10, encoding_value_line_edit.minimumHeight())
        encoding_value_line_edit.setSizePolicy(size_policy)
        encoding_value_line_edit.setToolTip(
            "Assign this encoding to this value.\n"
            "Each non filtered row containing this value will use this encoding for the {} of the note".format(
                self.key))

        encoding_h_layout.addWidget(soundButton)
        encoding_h_layout.addWidget(encoding_value_line_edit)

        return EncodingBox(frame=encoding_box, checkbox=encoding_check_box, valueLine=encoding_value_line_edit,
                           testButton=soundButton)

    def setup_ui(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")

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

        self.randomToAllButton = QPushButton(self.controlFrame)
        self.randomToAllButton.setObjectName(u"randomToAllButton")
        self.randomToAllButton.setStyleSheet(buttonStyle)
        self.randomToAllButton.setToolTip("Apply a random value to all the encoding below.")

        self.applyToAllButton = QPushButton(self.controlFrame)
        self.applyToAllButton.setObjectName(u"applyToAllButton")
        self.applyToAllButton.setStyleSheet(buttonStyle)
        self.applyToAllButton.setToolTip("Apply the default value to all the encoding below.")

        self.variableGridLayout = QGridLayout()  # self.controlFrame)
        self.variableGridLayout.setObjectName(u"variableGridLayout")

        self.variableLabel = QLabel(self.controlFrame)
        self.variableLabel.setObjectName(u"variableLabel")

        self.variableGridLayout.addWidget(self.variableLabel, 0, 0, 1, 1)

        self.variableComboBox = QComboBox(self.controlFrame)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.variableComboBox.sizePolicy().hasHeightForWidth())
        self.variableComboBox.setObjectName(u"variableComboBox")
        self.variableComboBox.setSizePolicy(size_policy)
        self.variableComboBox.setToolTip("Select a variable to filter and/or encode")

        self.variableGridLayout.addWidget(self.variableComboBox, 0, 1, 1, 1)

        # self.horizontalSpacerOctave = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.gridLayout_2.addItem(self.horizontalSpacerOctave, 2, 2, 1, 1)

        self.octaveLayout = QHBoxLayout()
        self.octaveLayout.setObjectName(u"octaveLayout")

        self.octaveLabel = QLabel(self.controlFrame)
        self.octaveLabel.setObjectName(u"octaveLabel")
        self.octaveSpinBox = QSpinBox(self.controlFrame)
        self.octaveSpinBox.setObjectName(u"octaveSpinBox")
        self.octaveSpinBox.setBaseSize(QSize(0, 0))
        self.octaveSpinBox.setWrapping(True)
        self.octaveSpinBox.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.octaveSpinBox.setMaximum(9)
        self.octaveSpinBox.setValue(4)
        self.octaveSpinBox.setToolTip(
            "Select an octave between 1 and 9.\nThe octave is set for each track and influence the value of all notes.")
        self.octaveLayout.addWidget(self.octaveLabel)
        self.octaveLayout.addWidget(self.octaveSpinBox)

        self.horizontalSpacerTop = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalSpacerBottom = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.qualitiveModeOptionsLayout.addLayout(self.defaultValueLayout, 1, 0, 1, 1)
        self.qualitiveModeOptionsLayout.addLayout(self.variableGridLayout, 0, 0, 1, 1)
        self.qualitiveModeOptionsLayout.addItem(self.horizontalSpacerTop, 0, 1, 1, 1)
        self.qualitiveModeOptionsLayout.addItem(self.horizontalSpacerBottom, 1, 2, 1, 1)
        self.qualitiveModeOptionsLayout.addWidget(self.applyToAllButton, 0, 3, 1, 1)
        self.qualitiveModeOptionsLayout.addWidget(self.randomToAllButton, 1, 3, 1, 1)
        self.qualitiveModeOptionsLayout.addWidget(self.checkAllButton, 0, 4, 1, 1)
        self.qualitiveModeOptionsLayout.addWidget(self.switchAllCheckButton, 1, 4, 1, 1)
        self.qualitiveModeOptionsLayout.addLayout(self.octaveLayout, 1, 1, 1, 1)
        # self.gridLayout.addWidget(self.SettingsFrame, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.qualitiveModeOptionsLayout.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.qualitiveModeOptionsLayout.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.qualitiveModeOptionsLayout.addItem(self.horizontalSpacer_2, 2, 2, 1, 1)

        self.detailsQModeLayout.addWidget(self.controlFrame)

        self.detailsVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.detailsQModeLayout.addItem(self.detailsVerticalSpacer)

        self.detailsScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.detailsScrollArea, 0, 1, 2, 1)

        self.retranslate_ui()
        self.connect_ui()
        self.detailsScrollArea.hide()

    def retranslate_ui(self):
        self.octaveLabel.setText(QCoreApplication.translate("Form", u"Select Octave", None))
        self.variableLabel.setText(QCoreApplication.translate("Form", u"Select Variable", None))
        self.defaultValueLabel.setText(QCoreApplication.translate("Form", u"Default:", None))
        self.checkAllButton.setText(QCoreApplication.translate("Form", u"Check all", None))
        self.switchAllCheckButton.setText(QCoreApplication.translate("Form", u"Switch all", None))
        self.applyToAllButton.setText(QCoreApplication.translate("Form", u"Apply default to all", None))
        self.randomToAllButton.setText(QCoreApplication.translate("Form", u"Randomize all", None))
