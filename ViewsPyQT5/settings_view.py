from PyQt5.QtCore import Qt, QRect, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QTextEdit
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLineEdit, QComboBox, QGridLayout, QLabel

from Utils.constants import TIME_SETTINGS_OPTIONS, TIME_SETTINGS_OPTIONS_TOOLTIP
from Utils.utils import is_float
from ViewsPyQT5.ViewsUtils.views_utils import buttonStyle


class SettingsView(QMainWindow):
    def __init__(self, parent=None):
        super(SettingsView, self).__init__(parent)
        self.parent = parent
        self.updatingBpm = False
        self.updatingLenght = False
        self.model = None
        self.setWindowTitle("Soda - Settings")
        self.settingsFrame = QFrame()
        self.setCentralWidget(self.settingsFrame)
        self.settingsFrame.setObjectName(u"settingsFrame")
        self.settingsFrame.setGeometry(QRect(70, 72, 521, 421))
        self.settingsFrame.setFrameShape(QFrame.Panel)
        self.settingsFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.settingsFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.optionsFrame = QFrame(self.settingsFrame)
        self.optionsFrame.setObjectName(u"optionsFrame")
        self.optionsFrame.setFrameShape(QFrame.Panel)
        self.optionsFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout_timesettings = QGridLayout(self.optionsFrame)
        self.gridLayout_timesettings.setObjectName(u"gridLayout_timesettings")
        self.bpmLineEdit = QLineEdit(self.optionsFrame)
        self.bpmLineEdit.setObjectName(u"bpmLineEdit")

        self.gridLayout_timesettings.addWidget(self.bpmLineEdit, 1, 1, 1, 1)

        self.songLengthLineEdit = QLineEdit(self.optionsFrame)
        self.songLengthLineEdit.setObjectName(u"songLengthLineEdit")

        self.gridLayout_timesettings.addWidget(self.songLengthLineEdit, 0, 1, 1, 1)

        self.songLengthLabel = QLabel(self.optionsFrame)
        self.songLengthLabel.setObjectName(u"songLengthLabel")

        self.gridLayout_timesettings.addWidget(self.songLengthLabel, 0, 0, 1, 1)

        self.batchSizeLabel = QLabel(self.optionsFrame)
        self.batchSizeLabel.setObjectName(u"batchSizeLabel")

        self.gridLayout_timesettings.addWidget(self.batchSizeLabel, 2, 0, 1, 1)

        self.bpmLabel = QLabel(self.optionsFrame)
        self.bpmLabel.setObjectName(u"bpmLabel")

        self.gridLayout_timesettings.addWidget(self.bpmLabel, 1, 0, 1, 1)

        self.NoteTimingLabel = QLabel(self.optionsFrame)
        self.NoteTimingLabel.setObjectName(u"NoteTimingLabel")

        self.gridLayout_timesettings.addWidget(self.NoteTimingLabel, 4, 0, 1, 1)

        self.sampleSizeLabel = QLabel(self.optionsFrame)
        self.sampleSizeLabel.setObjectName(u"sampleSizeLabel")

        self.gridLayout_timesettings.addWidget(self.sampleSizeLabel, 5, 0, 1, 1)

        self.batchSizeLineEdit = QLineEdit(self.optionsFrame)
        self.batchSizeLineEdit.setObjectName(u"batchSizeLineEdit")

        self.gridLayout_timesettings.addWidget(self.batchSizeLineEdit, 2, 1, 1, 1)

        self.batchPlannedLabel = QLabel(self.optionsFrame)
        self.batchPlannedLabel.setObjectName(u"batchPlannedLabel")

        self.batchPlannedLineEdit = QLineEdit(self.optionsFrame)
        self.batchPlannedLineEdit.setObjectName(u"batchPlanned")
        self.gridLayout_timesettings.addWidget(self.batchPlannedLabel, 3, 0, 1, 1)
        self.gridLayout_timesettings.addWidget(self.batchPlannedLineEdit, 3, 1, 1, 1)

        self.noteTimingLineEdit = QLineEdit(self.optionsFrame)
        self.noteTimingLineEdit.setObjectName(u"noteTimingLineEdit")

        self.gridLayout_timesettings.addWidget(self.noteTimingLineEdit, 4, 1, 1, 1)

        self.sampleSizeLineEdit = QLineEdit(self.optionsFrame)
        self.sampleSizeLineEdit.setObjectName(u"sampleSizeLineEdit")

        self.gridLayout_timesettings.addWidget(self.sampleSizeLineEdit, 5, 1, 1, 1)

        self.gridLayout.addWidget(self.optionsFrame, 2, 1, 1, 1)

        self.checkboxFrame = QFrame(self.settingsFrame)
        self.checkboxFrame.setObjectName(u"checkboxFrame")
        self.checkboxFrame.setFrameShape(QFrame.Panel)
        self.checkboxFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.checkboxFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.previousDataCheckBox = QCheckBox(self.checkboxFrame)
        self.previousDataCheckBox.setObjectName(u"previousDataCheckBox")

        self.verticalLayout.addWidget(self.previousDataCheckBox)

        self.gridLayout.addWidget(self.checkboxFrame, 0, 3, 1, 1)

        self.tempoModeFrame = QFrame(self.settingsFrame)
        self.tempoModeFrame.setObjectName(u"tempoModeFrame")
        self.tempoModeFrame.setFrameShape(QFrame.Panel)
        self.tempoModeFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.tempoModeFrame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tempoModeComboBox = QComboBox(self.tempoModeFrame)
        self.tempoModeComboBox.setObjectName(u"tempoModeComboBox")
        self.tempoModeComboBox.setEditable(False)
        self.tempoModeComboBox.addItems(TIME_SETTINGS_OPTIONS)

        self.gridLayout_3.addWidget(self.tempoModeComboBox, 0, 1, 1, 1)

        self.tempoModeLabel = QLabel(self.tempoModeFrame)
        self.tempoModeLabel.setObjectName(u"tempoModeLabel")

        self.gridLayout_3.addWidget(self.tempoModeLabel, 0, 0, 1, 1)

        self.tempoNLabel = QLabel(self.tempoModeFrame)
        self.tempoNLabel.setObjectName(u"tempoNLabel")
        self.tempoNLineedit = QLineEdit(self.tempoModeFrame)
        self.tempoNLineedit.setObjectName(u"tempoNLineedit")

        self.gridLayout_3.addWidget(self.tempoNLabel, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.tempoNLineedit, 1, 1, 1, 1)

        self.tempoDureeLabel = QLabel(self.tempoModeFrame)
        self.tempoDureeLabel.setObjectName(u"tempoDureeLabel")
        self.tempoDureeLineedit = QLineEdit(self.tempoModeFrame)
        self.tempoDureeLineedit.setObjectName(u"tempoDureeLineedit")

        self.gridLayout_3.addWidget(self.tempoDureeLabel, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.tempoDureeLineedit, 2, 1, 1, 1)

        self.tempoOffsetLabel = QLabel(self.tempoModeFrame)
        self.tempoOffsetLabel.setObjectName(u"tempoOffsetLabel")
        self.tempoOffsetLineedit = QLineEdit(self.tempoModeFrame)
        self.tempoOffsetLineedit.setObjectName(u"tempoOffsetLineedit")

        self.gridLayout_3.addWidget(self.tempoOffsetLabel, 3, 0, 1, 1)
        self.gridLayout_3.addWidget(self.tempoOffsetLineedit, 3, 1, 1, 1)


        self.gridLayout.addWidget(self.tempoModeFrame, 0, 1, 1, 1)

        self.closeFrame = QFrame(self.settingsFrame)
        self.closeFrame.setObjectName(u"closeFrame")
        self.closeFrame.setFrameShape(QFrame.Panel)
        self.closeFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout = QHBoxLayout(self.closeFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.validateButton = QPushButton(self.closeFrame)
        self.validateButton.setObjectName(u"validateButton")
        self.validateButton.setStyleSheet(buttonStyle)

        self.horizontalLayout.addWidget(self.validateButton)

        self.cancelButton = QPushButton(self.closeFrame)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setStyleSheet(buttonStyle)

        self.horizontalLayout.addWidget(self.cancelButton)

        self.gridLayout.addWidget(self.closeFrame, 5, 1, 1, 3)

        self.aboutFrame = QFrame(self.settingsFrame)
        self.aboutFrame.setObjectName(u"aboutFrame")
        self.aboutFrame.setFrameShape(QFrame.Box)
        self.aboutFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.aboutFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.aboutText = QTextEdit(self.aboutFrame)
        self.aboutText.setObjectName(u"aboutText")
        self.aboutText.setTextInteractionFlags(Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)

        self.verticalLayout_2.addWidget(self.aboutText)

        self.gridLayout.addWidget(self.aboutFrame, 2, 3, 1, 1)

        self.graphicalOptionsFrame = QFrame(self.settingsFrame)
        self.graphicalOptionsFrame.setObjectName(u"graphicalOptionsFrame")
        self.graphicalOptionsFrame.setFrameShape(QFrame.Panel)
        self.graphicalOptionsFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout_graphsettings = QGridLayout(self.graphicalOptionsFrame)
        self.gridLayout_graphsettings.setObjectName(u"gridLayout_graphsettings")

        self.graphicalLengthLabel = QLabel(self.graphicalOptionsFrame)
        self.graphicalLengthLabel.setObjectName(u"graphicalLengthLabel")
        self.graphicalLengthLineedit = QLineEdit(self.graphicalOptionsFrame)
        self.graphicalLengthLineedit.setObjectName(u"graphicalLengthLineedit")

        self.graphicalPercentageLabel = QLabel(self.graphicalOptionsFrame)
        self.graphicalPercentageLabel.setObjectName(u"graphicalPercentageLabel")
        self.graphicalPercentageLineedit = QLineEdit(self.graphicalOptionsFrame)
        self.graphicalPercentageLineedit.setObjectName(u"graphicalPercentageLineedit")

        self.gridLayout_graphsettings.addWidget(self.graphicalLengthLabel, 1, 0, 1, 1)
        self.gridLayout_graphsettings.addWidget(self.graphicalLengthLineedit, 1, 1, 1, 1)
        self.gridLayout_graphsettings.addWidget(self.graphicalPercentageLabel, 2, 0, 1, 1)
        self.gridLayout_graphsettings.addWidget(self.graphicalPercentageLineedit, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.graphicalOptionsFrame, 4, 1, 1, 3)

        self.retranslate_ui()
        self.set_tools_tips()

        # setupUi

    def retranslate_ui(self):
        self.songLengthLabel.setText(QCoreApplication.translate("Form", u"Song length, in seconds", None))
        self.batchSizeLabel.setText(QCoreApplication.translate("Form", u"Batch size to sonify", None))
        self.batchPlannedLabel.setText(QCoreApplication.translate("Form", u"#Batches to sonify in advance", None))
        self.bpmLabel.setText(QCoreApplication.translate("Form", u"Beat/Row Per Minutes ", None))
        self.sampleSizeLabel.setText(QCoreApplication.translate("Form", u"#Rows displayed ", None))

        self.graphicalLengthLabel.setText(QCoreApplication.translate("Form", u"#seconds displayed on the x axis of the graph", None))
        self.graphicalPercentageLabel.setText(QCoreApplication.translate("Form", u"% of graph displayed in the past", None))

        self.NoteTimingLabel.setText(QCoreApplication.translate("Form", u"Note Timing", None))
        self.previousDataCheckBox.setText(QCoreApplication.translate("Form", u"Load previous data on start", None))
        self.tempoModeLabel.setText(QCoreApplication.translate("Form", u"Tempo", None))
        self.tempoNLabel.setText(QCoreApplication.translate("Form", u"Tempo N Value", None))
        self.tempoDureeLabel.setText(QCoreApplication.translate("Form", u"Tempo pause duration", None))
        self.tempoOffsetLabel.setText(QCoreApplication.translate("Form", u"Tempo offset duration", None))
        self.validateButton.setText(QCoreApplication.translate("Form", u"Validate", None))
        self.cancelButton.setText(QCoreApplication.translate("Form", u"Cancel", None))
        self.aboutText.setHtml(QCoreApplication.translate("Form",
                                                          u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                          "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                          "p, li { white-space: pre-wrap; }\n"
                                                          "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
                                                          "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">"
                                                          "Soda, a generalist sonification software.<br>"
                                                          "Made by TECFA at Unige. Pr. Eric Sanchez & Andre Cibils. <br>GNU GENERAL PUBLIC LICENSE"
                                                          "</span></p></body></html>",
                                                          None))

    # retranslateUi
    def set_tools_tips(self):
        self.songLengthLineEdit.setToolTip("Length of the music, in seconds. \nChanging this will change the bpm")
        self.sampleSizeLabel.setToolTip("Number of rows displayed on the table below the graph.\n You will need to restart the program.")
        self.batchPlannedLineEdit.setToolTip("Number of batches to process in advance.\n"
                                          "A smaller value will make the program more responsive to changes to encoding "
                                          "but it may results in rows being skipped if they are close too each others timing wise. "
                                          "Less notes will be planned in advance, and the graph may not display all future notes.")
        self.batchSizeLineEdit.setToolTip("Number of rows to process as a batch.\n"
                                          "A smaller value will make the program more responsive to changes to encoding "
                                          "but it may results in rows being skipped if they are close too each others timing wise. "
                                          "Less notes will be planned in advance, and the graph may not display all future notes.")
        self.bpmLineEdit.setToolTip("Beat per minute, equivalent to the number of row being processed per minute.\n"
                                    "Changing this will affect the final song length")
        self.tempoModeComboBox.setToolTip("Which tempo settings to use.\n"
                                          "{}".format("\n".join(TIME_SETTINGS_OPTIONS_TOOLTIP)))
        self.previousDataCheckBox.setToolTip("Automatically load previously loaded data and time column choice.")
        self.noteTimingLineEdit.setToolTip("The number of ms that the manager will wait before planning a note.\n"
                                           "A shorter value will make the program more responsive to changes to encodings but "
                                           "it may results in rows being skipped if they are close too each others timing wise.")

    def update_ui(self):
        if self.model is None:
            return
        self.tempoModeComboBox.setCurrentIndex(TIME_SETTINGS_OPTIONS.index(self.model.type))
        self.tempoNLineedit.setText(str(self.model.tempoNValue))
        self.tempoDureeLineedit.setText(str(self.model.tempoDurValue))
        self.tempoOffsetLineedit.setText(str(self.model.tempoOffsetValue))
        self.songLengthLineEdit.setText(str(self.model.get_music_duration()))
        self.batchSizeLineEdit.setText(str(self.model.batchSize))
        self.batchPlannedLineEdit.setText(str(self.model.batchPlanned))
        self.sampleSizeLineEdit.setText(str(self.model.sampleSize))
        self.bpmLineEdit.setText(str(self.model.get_bpm()))
        self.noteTimingLineEdit.setText(str(self.model.timeBuffer))
        self.previousDataCheckBox.setChecked(self.model.autoload)
        self.graphicalPercentageLineedit.setText(str(int(self.model.graphicalBarPercentage*100)))
        self.graphicalLengthLineedit.setText(str(int(self.model.graphicalLength/1000)))

        self.connect_ui()

    def disconnect_ui(self):
        self.songLengthLineEdit.textEdited.disconnect()
        self.bpmLineEdit.textEdited.disconnect()
        self.validateButton.clicked.disconnect()
        self.cancelButton.clicked.disconnect()

    def connect_ui(self):
        self.songLengthLineEdit.textEdited.connect(self.on_music_length_change)
        self.bpmLineEdit.textEdited.connect(self.on_bpm_change)
        self.validateButton.clicked.connect(self.validate)
        self.cancelButton.clicked.connect(self.cancel)

    def on_bpm_change(self):
        if (self.updatingLenght):
            self.updatingLenght = False
        elif (is_float(self.bpmLineEdit.text()) and float(self.bpmLineEdit.text()) != 0):
            self.updatingBpm = True
            self.songLengthLineEdit.setText(str(int(60 * float(self.model.data.get_size()) / float(self.bpmLineEdit.text()))))

    def on_music_length_change(self):
        if (self.updatingBpm):
            self.updatingBpm = False
        elif (is_float(self.songLengthLineEdit.text()) and float(self.songLengthLineEdit.text()) != 0):
            self.updatingLenght = True
            self.bpmLineEdit.setText(
                str(round(60 * (float(self.model.data.get_size()) / float(self.songLengthLineEdit.text())), 2)))

    def validate(self):
        self.model.ctrl.validate(self.batchSizeLineEdit.text(), self.batchPlannedLineEdit.text(), self.songLengthLineEdit.text(),
                                 self.noteTimingLineEdit.text(), self.sampleSizeLineEdit.text(),
                                 self.tempoModeComboBox.currentIndex(), self.tempoNLineedit.text(),
                                 self.tempoDureeLineedit.text(), self.tempoOffsetLineedit.text(),
                                 self.previousDataCheckBox.isChecked(),
                                 self.graphicalLengthLineedit.text(), self.graphicalPercentageLineedit.text())

        self.cancel()

    def cancel(self):
        self.disconnect_ui()
        self.hide()
