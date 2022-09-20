from tkinter import Toplevel, Button, Listbox, END, Entry, Label, StringVar, Radiobutton, W, IntVar, Checkbutton
from tkinter.ttk import Frame, Combobox

from Models.data_model import Data
from Utils.constants import DEFAULT_PADDING, TFRAME_STYLE, DEFAULT_PADY, DEFAULT_PADX
from Utils.utils import is_float


class TimeSettingsView(Toplevel):
    '''
    Presents options relative to time to the user, enabling them to configure time settings
    Future
    '''

    def __init__(self, ctrl, model, **kwargs):
        Toplevel.__init__(self, **kwargs)
        # ctrl and model
        self.ctrl = ctrl
        self.model = model

        # View data
        self.title("Time Settings")
        self.updating = False
        # self.geometry('450x400')

        # setup view
        self.optionsFrame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["TIMESETTINGS"][0])
        self.settingsFrame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["TIMESETTINGS"][0])
        self.options = []
        self.selectedTimeType = StringVar()
        self.selectedTimeType.set(self.model.type)
        for t in self.model.possible_types:
            self.options.append(Radiobutton(self.optionsFrame, text=t, variable=self.selectedTimeType, value=t, indicatoron=False))

        self.musicLengthValue = StringVar(self, value=self.model.get_music_duration())
        self.musicLengthEntry = Entry(self.settingsFrame, textvariable=self.musicLengthValue)
        self.musicLengthLabel = Label(self.settingsFrame, text="Music total length (s) :")

        self.musicBPMValue = StringVar(self, value=round(self.model.get_bpm(), 2))
        self.musicBPMEntry = Entry(self.settingsFrame, textvariable=self.musicBPMValue)
        self.musicBPMLabel = Label(self.settingsFrame, text="Music bpm (beat per minute) :")

        self.musicLengthValue.trace("w", self.on_music_length_change)
        self.musicBPMValue.trace("w", self.on_bpm_change)

        self.batchSizeValue = IntVar(self, value=self.model.batchSize)
        self.batchSizeEntry = Entry(self.settingsFrame, textvariable=self.batchSizeValue)
        self.batchSizeLabel = Label(self.settingsFrame, text="Data batch size (not working while playing):")

        self.bufferSizeValue = IntVar(self, value=self.model.timeBuffer)
        self.bufferSizeEntry = Entry(self.settingsFrame, textvariable=self.bufferSizeValue)
        self.bufferSizeLabel = Label(self.settingsFrame, text="Future look ahead (ms):")

        self.autoloadVar = IntVar(self, value=self.model.autoload)
        self.autoLoadCB = Checkbutton(self.settingsFrame, text="Automatically load previously selected data", variable=self.autoloadVar)

        self.debuggingVerboseVar = IntVar(self, value=self.model.debugVerbose)
        self.debuggingVerboseCB = Checkbutton(self.settingsFrame, text="Display additional log information", variable=self.debuggingVerboseVar)

        self.exitFrame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.validateButton = Button(self.exitFrame, text="Validate", command=self.ctrl.validate)
        self.cancelButton = Button(self.exitFrame, text="Cancel", command=self.destroy)

        self.setup_widgets()

    def setup_widgets(self):
        self.optionsFrame.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.settingsFrame.grid(column=0, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.exitFrame.grid(column=0, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

        for i, t in enumerate(self.options):
            t.grid(column=0, row=i, pady=0, padx=0)

        self.musicLengthLabel.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.musicLengthEntry.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.musicBPMLabel.grid(column=0, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.musicBPMEntry.grid(column=1, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

        self.batchSizeLabel.grid(column=0, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.batchSizeEntry.grid(column=1, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.bufferSizeLabel.grid(column=0, row=3, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.bufferSizeEntry.grid(column=1, row=3, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.autoLoadCB.grid(column=0, row=4, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.debuggingVerboseCB.grid(column=0, row=5, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

        self.validateButton.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.cancelButton.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

    def on_bpm_change(self, *args):
        if(self.updating):
            self.updating = False
        elif(is_float(self.musicBPMValue.get())):
            self.updating = True
            self.musicLengthValue.set(int(60 * float(self.model.data.size)/float(self.musicBPMValue.get())))

    def on_music_length_change(self, *args):
        if(self.updating):
            self.updating = False
        elif(is_float(self.musicLengthValue.get())):
            self.updating = True
            self.musicBPMValue.set(round(60*(float(self.model.data.size) / float(self.musicLengthValue.get())), 2))

    def update_batch_size(self):
        self.ctrl.update_batch_size(self.batchSizeValue.get())

    def update_music_length(self):
        self.ctrl.update_music_length(self.musicLengthValue.get())

    def destroy(self) -> None:
        self.ctrl.remove_window()
        super().destroy()

