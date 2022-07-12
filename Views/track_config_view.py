from tkinter import ttk, Button, Scale, Entry, Label, DoubleVar, StringVar
from tkinter.ttk import Combobox

from Ctrls.data_controller import DataCtrl
from Models.data_model import Data
from Utils.constants import DEFAULT_PADX, DEFAULT_PADY, SOUNDFONT


class TrackConfigView(ttk.Frame):
    """
    View module for tracks in config mode. Each track should have its own view. Config view enables the user to configure
    each track independantly with buttons and sliders.
    View to export/import a specific track
    """

    def __init__(self, parent, ctrl, model, **kwargs):
        super().__init__(parent, **kwargs)
        #Ctrl and model
        self.model = model
        self.ctrl = ctrl

        #View data
        self.data = Data()

        #setup view
        self.create_widgets()
        self.setup_widgets()

    def create_widgets(self):
        self.soundfontLabel = Label(self, text="Instrument")
        self.selectSoundfontButton = Combobox(self, values=SOUNDFONT)  # , padx=DEFAULT_PADX)#, pady=DEFAULT_PADY)

        self.varlistLabel = Label(self, text="Main Variable")
        self.selectVarListBox = Combobox(self, values=self.data.get_variables())
        self.selectVarListBox.bind('<<ComboboxSelected>>', self.select_variable)
        self.selectSoundfontButton.current(0)
        self.selectVarListBox.current(0)

        #https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
        self.filterValue = StringVar(self)
        self.filterValue.trace_add("write", self.update_filter)
        self.filterEntry = Entry(self, textvariable=self.filterValue)
        self.filterLabel = Label(self, text="Filter")
        self.encodeValueButton = Button(self, text="Value Encoding", command=self.encode_values)
        self.encodeDurationButton = Button(self, text="Duration Encoding", command=self.encode_durations)
        self.encodeVelocityButton = Button(self, text="Velocity Encoding", command=self.encode_velocity)
        self.exportButton = Button(self, text="Export")
        self.importButton = Button(self, text="Import")
        self.deleteButton = Button(self, text="Delete track", command=self.ctrl.remove)
        self.local_gain_slider = Scale(self, from_=0, to=100, sliderrelief='solid',
                                       command=self.ctrl.change_gain)  # flat, groove, raised, ridge, solid, sunken

    def setup_widgets(self):
        self.soundfontLabel.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.selectSoundfontButton.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

        self.varlistLabel.grid(column=0, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.selectVarListBox.grid(column=1, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)


        self.filterLabel.grid(column=0, row=2, columnspan=1, pady=DEFAULT_PADY)
        self.filterEntry.grid(column=1, row=2, columnspan=1, pady=DEFAULT_PADY)

        self.local_gain_slider.grid(column=0, row=3, rowspan=4, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

        self.encodeValueButton.grid(column=1, row=3, columnspan=1, pady=0, padx=DEFAULT_PADX)
        self.encodeDurationButton.grid(column=1, row=4, columnspan=1, pady=0, padx=DEFAULT_PADX)
        self.encodeVelocityButton.grid(column=1, row=5, columnspan=1, pady=0, padx=DEFAULT_PADX)
        # self.exportButton.grid(column=0, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        # self.importButton.grid(column=1, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.deleteButton.grid(column=1, row=6, pady=0, padx=DEFAULT_PADX)

    def select_variable(self, event):
        self.ctrl.set_main_var(self.selectVarListBox.get())

    def update_filter(self, *args):
        self.ctrl.update_filter(self.filterValue.get())

    def encode_durations(self):
        self.ctrl.open_encoding("duration")

    def encode_values(self):
        self.ctrl.open_encoding("value")

    def encode_velocity(self):
        self.ctrl.open_encoding("velocity")