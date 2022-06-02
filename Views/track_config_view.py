from tkinter import ttk, Button, Scale, Listbox, END
from tkinter.ttk import Combobox

from Utils.constants import DEFAULT_BGCOLOR, DEFAULT_PADX, DEFAULT_PADY, TFRAME_STYLE, MOCKUP_KEYS, SOUNDFONT_KEYS, \
    MAPPING_OPTIONS
from Views.parameter_mapping_view import ParameterMappingView


class TrackConfigView(ttk.Frame):
    """
    View module for tracks in config mode. Each track should have its own view. Config view enables the user to configure
    each track independantly with buttons and sliders.
    """
    def __init__(self, parent, ctrl=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.ctrl = ctrl
        self.create_widgets()
        self.setup_widgets()

    def create_widgets(self):
        self.pickSoundfontButton = Combobox(self, values = SOUNDFONT_KEYS)#, padx=DEFAULT_PADX)#, pady=DEFAULT_PADY)
        self.pickKeyListbox = Combobox(self, values=MOCKUP_KEYS)
        self.pickSoundfontButton.current(0)
        self.pickKeyListbox.current(0)
        self.pickFilterButton = Button(self, text="Pick Filter")
        self.mapValueButton = Button(self, text="Value Mapping", command=self.map_values)
        self.mapDurationButton = Button(self, text="Duration Mapping", command=self.map_durations)
        self.exportButton = Button(self, text="Export")
        self.importButton = Button(self, text="Import")
        self.deleteButton = Button(self, text="Delete track", command=self.ctrl.remove)
        self.local_gain_slider = Scale(self, from_=0, to=100, sliderrelief='solid', command=self.ctrl.change_gain) #flat, groove, raised, ridge, solid, sunken

    def setup_widgets(self):
        self.pickKeyListbox.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.pickSoundfontButton.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.pickFilterButton.grid(column=0, row=1, columnspan=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.mapValueButton.grid(column=1, row=1, columnspan=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.mapDurationButton.grid(column=2, row=1, columnspan=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        # self.exportButton.grid(column=0, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        # self.importButton.grid(column=1, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.deleteButton.grid(column=2, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.local_gain_slider.grid(column=0, row=3, columnspan=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX)



    def map_durations(self):
        self.ctrl.open_mapping("duration")
    def map_values(self):
        self.ctrl.open_mapping("value")


    def setup_controller(self, controller):
        self.ctrl = controller
