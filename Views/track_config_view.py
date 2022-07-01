from tkinter import ttk, Button, Scale, Entry, Label
from tkinter.ttk import Combobox

from Ctrls.data_controller import DataCtrl
from Utils.constants import DEFAULT_PADX, DEFAULT_PADY, SOUNDFONT


class TrackConfigView(ttk.Frame):
    """
    View module for tracks in config mode. Each track should have its own view. Config view enables the user to configure
    each track independantly with buttons and sliders.
    View to export/import a specific track
    """

    def __init__(self, parent, ctrl=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.db = DataCtrl()
        self.ctrl = ctrl
        self.create_widgets()
        self.setup_widgets()

    def create_widgets(self):
        self.selectSoundfontButton = Combobox(self, values=SOUNDFONT)  # , padx=DEFAULT_PADX)#, pady=DEFAULT_PADY)
        self.selectVarListBox = Combobox(self, values=self.db.get_variables())
        self.selectSoundfontButton.current(0)
        self.selectVarListBox.current(0)
        self.filterEntry = Entry(self)
        self.filterLabel = Label(self, text="Filter")
        self.encodeValueButton = Button(self, text="Value Encoding", command=self.map_values)
        self.encodeDurationButton = Button(self, text="Duration Encoding", command=self.map_durations)
        self.exportButton = Button(self, text="Export")
        self.importButton = Button(self, text="Import")
        self.deleteButton = Button(self, text="Delete track", command=self.ctrl.remove)
        self.local_gain_slider = Scale(self, from_=0, to=100, sliderrelief='solid',
                                       command=self.ctrl.change_gain)  # flat, groove, raised, ridge, solid, sunken

    def setup_widgets(self):
        self.selectVarListBox.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.selectSoundfontButton.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.local_gain_slider.grid(column=2, row=0, rowspan=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

        self.filterLabel.grid(column=0, row=1, columnspan=1, pady=DEFAULT_PADY)
        self.filterEntry.grid(column=1, row=1, columnspan=1, pady=DEFAULT_PADY)

        self.encodeValueButton.grid(column=0, row=2, columnspan=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.encodeDurationButton.grid(column=1, row=2, columnspan=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        # self.exportButton.grid(column=0, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        # self.importButton.grid(column=1, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.deleteButton.grid(column=3, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

    def map_durations(self):
        self.ctrl.open_mapping("duration")

    def map_values(self):
        self.ctrl.open_mapping("value")

    def setup_controller(self, controller):
        self.ctrl = controller
