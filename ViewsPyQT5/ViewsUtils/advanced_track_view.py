# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'advancedtrackconfigLIPlSj.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PyQt5.QtCore import QSize, Qt, QRect, QCoreApplication
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy, QAbstractScrollArea, QWidget, \
    QPushButton, QSpacerItem, QFrame, QLineEdit, QComboBox, QSlider, QGridLayout, QLayout, QProgressBar, QLabel, \
    QSpinBox, QAbstractSpinBox, QPlainTextEdit


class AdvancedTrackView(object):

    def display_track(self, track, key):
        pass

    def setupUi(self):
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

        self.gridLayout_2.addWidget(self.variableLabel, 1, 0, 1, 1)

        self.nameLabel = QLabel(self.SettingsFrame)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.nameLabel, 0, 0, 1, 1)

        self.octaveSpinBox = QSpinBox(self.SettingsFrame)
        self.octaveSpinBox.setObjectName(u"octaveSpinBox")
        self.octaveSpinBox.setBaseSize(QSize(0, 0))
        self.octaveSpinBox.setWrapping(True)
        self.octaveSpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.octaveSpinBox.setMaximum(9)
        self.octaveSpinBox.setValue(4)

        self.gridLayout_2.addWidget(self.octaveSpinBox, 2, 1, 1, 1)

        self.changeModeButton = QPushButton(self.SettingsFrame)
        self.changeModeButton.setObjectName(u"changeModeButton")

        self.gridLayout_2.addWidget(self.changeModeButton, 0, 1, 1, 1)

        self.variableComboBox = QComboBox(self.SettingsFrame)
        self.variableComboBox.setObjectName(u"variableComboBox")

        self.gridLayout_2.addWidget(self.variableComboBox, 1, 1, 1, 1)

        self.horizontalSpacerName = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacerName, 0, 2, 1, 1)

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
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.controlFrame = QFrame(self.scrollAreaWidgetContents)
        self.controlFrame.setObjectName(u"controlFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controlFrame.sizePolicy().hasHeightForWidth())
        self.controlFrame.setSizePolicy(sizePolicy)
        self.controlFrame.setFrameShape(QFrame.Panel)
        self.controlFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.controlFrame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.defaultValueLayout = QHBoxLayout()
        self.defaultValueLayout.setObjectName(u"defaultValueLayout")
        self.defaultValueLabel = QLabel(self.controlFrame)
        self.defaultValueLabel.setObjectName(u"defaultValueLabel")

        self.defaultValueLayout.addWidget(self.defaultValueLabel)

        self.defaultValueLineEdit = QLineEdit(self.controlFrame)
        self.defaultValueLineEdit.setObjectName(u"defaultValueLineEdit")

        self.defaultValueLayout.addWidget(self.defaultValueLineEdit)


        self.gridLayout_4.addLayout(self.defaultValueLayout, 0, 0, 1, 1)

        self.uncheckAllButton = QPushButton(self.controlFrame)
        self.uncheckAllButton.setObjectName(u"uncheckAllButton")

        self.gridLayout_4.addWidget(self.uncheckAllButton, 1, 0, 1, 1)

        self.checkAllButton = QPushButton(self.controlFrame)
        self.checkAllButton.setObjectName(u"checkAllButton")

        self.gridLayout_4.addWidget(self.checkAllButton, 1, 1, 1, 1)

        self.applyToAllButton = QPushButton(self.controlFrame)
        self.applyToAllButton.setObjectName(u"applyToAllButton")

        self.gridLayout_4.addWidget(self.applyToAllButton, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)


        self.verticalLayout_4.addWidget(self.controlFrame)

        self.detailsVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.detailsVerticalSpacer)

        self.detailsScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.detailsScrollArea, 0, 1, 2, 1)


        self.retranslateUi()

    # setupUi

    def retranslateUi(self):
        self.octaveLabel.setText(QCoreApplication.translate("Form", u"Select Octave", None))
        self.variableLabel.setText(QCoreApplication.translate("Form", u"Select Variable", None))
        self.nameLabel.setText(QCoreApplication.translate("Form", u"Track Name", None))
        self.changeModeButton.setText(QCoreApplication.translate("Form", u"Change Mode", None))
        self.filterLabel.setText(QCoreApplication.translate("Form", u"Filter", None))
        self.defaultValueLabel.setText(QCoreApplication.translate("Form", u"Default Value", None))
        self.uncheckAllButton.setText(QCoreApplication.translate("Form", u"Uncheck all", None))
        self.checkAllButton.setText(QCoreApplication.translate("Form", u"Check all", None))
        self.applyToAllButton.setText(QCoreApplication.translate("Form", u"Apply to all", None))
    # retranslateUi

