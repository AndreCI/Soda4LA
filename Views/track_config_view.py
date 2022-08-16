from tkinter import ttk, Button, Scale, Entry, Label, DoubleVar, StringVar, Checkbutton
from tkinter.filedialog import asksaveasfile, askopenfile, askopenfilename
from tkinter.ttk import Combobox

from Models.data_model import Data
from Utils.constants import DEFAULT_PADX, DEFAULT_PADY, DATA_PATH, FILE_PATH
from Utils.soundfont_loader import SoundfontLoader


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
        self.soundfontUtil = SoundfontLoader.get_instance()

        #View data
        self.data = Data.getInstance()

        #setup view
        self.idStr = StringVar(value=self.model.id)
        self.idLabel = Label(self, textvariable=self.idStr)
        self.soundfontLabel = Label(self, text="Instrument")

        self.selectSoundfontCB = Combobox(self, values=self.soundfontUtil.get_names(), state='readonly')  # , padx=DEFAULT_PADX)#, pady=DEFAULT_PADY)
        self.selectSoundfontCB.bind('<<ComboboxSelected>>', self.select_soundfont)
        self.selectSoundfontCB.set(self.soundfontUtil.default)

        self.varlistLabel = Label(self, text="Main Variable")
        self.selectVarListBox = Combobox(self, values=self.data.get_variables(), state="readonly")
        self.selectVarListBox.bind('<<ComboboxSelected>>', self.select_variable)
        self.selectVarListBox.current(0)

        #https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
        self.filterValue = StringVar(self)
        self.filterValue.trace_add("write", self.update_filter)
        self.filterEntry = Entry(self, textvariable=self.filterValue)
        self.filterLabel = Label(self, text="Filter")
        self.encodeValueButton = Button(self, text="Value Encoding", command=self.encode_values)
        self.encodeDurationButton = Button(self, text="Duration Encoding", command=self.encode_durations)
        self.encodeVelocityButton = Button(self, text="Velocity Encoding", command=self.encode_velocity)
        self.exportButton = Button(self, text="Export", command=self.export)
        self.importButton = Button(self, text="Import", command=self.import_track)
        self.deleteButton = Button(self, text="Delete track", command=self.ctrl.remove)
        self.local_gain_slider = Scale(self, from_=0, to=100, sliderrelief='solid',
                                       command=self.ctrl.change_gain)  # flat, groove, raised, ridge, solid, sunken

        self.setup_widgets()

    def setup_widgets(self):
        self.idLabel.grid(column=0, row=0, columnspan=4, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.soundfontLabel.grid(column=0, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.selectSoundfontCB.grid(column=1, row=1, columnspan=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")

        self.varlistLabel.grid(column=0, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.selectVarListBox.grid(column=1, row=2,columnspan=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")

        self.filterLabel.grid(column=0, row=3, columnspan=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.filterEntry.grid(column=1, row=3, columnspan=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")

        self.local_gain_slider.grid(column=0, row=4, rowspan=5, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

        self.encodeValueButton.grid(column=1, row=4, columnspan=2, pady=0, padx=DEFAULT_PADX, sticky="ew")
        self.encodeDurationButton.grid(column=1, row=5, columnspan=2, pady=0, padx=DEFAULT_PADX, sticky="ew")
        self.encodeVelocityButton.grid(column=1, row=6, columnspan=2, pady=0, padx=DEFAULT_PADX, sticky="ew")

        self.exportButton.grid(column=2, row=7, pady=0, padx=DEFAULT_PADX)
        self.importButton.grid(column=1, row=7, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.deleteButton.grid(column=1, row=8, columnspan=2, pady=0, padx=DEFAULT_PADX)

    def export(self):
        f = asksaveasfile(title="Export selected track to a file", initialdir=FILE_PATH,
                          initialfile="exported_track_{}".format(self.model.id), mode='w', defaultextension=".pkl")
        if f is not None:  # asksaveasfile return `None` if dialog closed with "cancel".
            self.model.serialize(f.name)

    def import_track(self):
        f = askopenfilename(title="Import selected file to a track")
        if f is not None:  # asksaveasfile return `None` if dialog closed with "cancel".
            self.model.unserialize(f)
            self.reset_view()

    def reset_view(self):
        self.selectSoundfontCB.set(SoundfontLoader.get_instance().get_name_from_path(self.model.soundfont))
        self.select_soundfont(None)
        self.selectVarListBox.set(self.model.filter.column)
        self.select_variable(None)

    def select_soundfont(self, event):
        self.ctrl.set_soundfont(self.selectSoundfontCB.get())

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