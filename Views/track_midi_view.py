from tkinter import ttk, Scale, Button

from Utils.constants import DEFAULT_PADY, DEFAULT_PADX, DEFAULT_PADDING, TFRAME_STYLE


class TrackMidiView(ttk.Frame):
    """
    View module for tracks in midi mode. Each track should have its own view. Midi view enables the user to see notes
    inside a track and to modifiy specific parameters (such as gain) to update the song in real time
    """

    def __init__(self, parent, ctrl, model, **kwargs):
        super().__init__(parent, **kwargs)
        #ctrl and model
        self.ctrl = ctrl
        self.model = model

        #view data
        self.note_view = []

        #setup
        self.create_widgets()
        self.setup_widgets()

    def create_widgets(self):
        self.local_gain_slider = Scale(self, from_=0, to=100,
                                       sliderrelief='solid',
                                       command=self.ctrl.change_gain)  # flat, groove, raised, ridge, solid, sunken
        self.mute_button = Button(self, text="Mute")
        self.notes = ttk.Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["NOTE"][0])

    def setup_widgets(self):
        self.local_gain_slider.grid(column=0, row=0, columnspan=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.mute_button.grid(column=2, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

    def setup_controller(self, controller):
        self.ctrl = controller
