import tkinter as tk
from tkinter import ttk

from Models.music_model import Music
from Utils.constants import DEFAULT_PADDING, TFRAME_STYLE, DEFAULT_PADX, DEFAULT_PADY
from Utils.scrollable_frame import ScrollableFrame
from Views.time_settings_view import TimeSettingsView
from Views.track_config_view import TrackConfigView
from Views.track_midi_view import TrackMidiView


class SonificationView(ttk.Frame):
    """
    Main view for the sonification process, handling both configuration and midi representation of the loaded data.
    Modules: list of tracks, each with their own config and midi view.
    view to control the start, pause and stop of the current music
    view to configurate time settings
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        #Ctrl and model
        self.model = Music()
        self.ctrl = self.model.ctrl
        self.ctrl.model.sonification_view = self

        #View data
        self.configView = True #Inform which view is currently displqyed
        self.trackConfigViews = []
        self.trackMidiViews = []

        #setup view
        self.create_widgets()
        self.setup_widgets()

    def create_widgets(self):
        self.switch_view_button = tk.Button(self, text="Change view", command=self.switch_view)
        self.time_setting_button = tk.Button(self, text="Time Settings", command=self.open_time_setting)
        self.add_track_button = tk.Button(self, text="Add track", command=self.ctrl.create_track)

        self.audio_view = ttk.Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["TRACK_COLLECTION"][0])
        self.play_button = tk.Button(self.audio_view, text="Play", command=self.ctrl.play)
        self.pause_button = tk.Button(self.audio_view, text="Pause", command=self.ctrl.pause)
        self.stop_button = tk.Button(self.audio_view, text="Stop", command=self.ctrl.stop)
        self.generate_button = tk.Button(self.audio_view, text="Generate", command=self.ctrl.generate)

        self.track_config_frame = ScrollableFrame(self, orient="horizontal", padding=DEFAULT_PADDING, style=TFRAME_STYLE["TRACK_COLLECTION"][0],
                                                  width=1250, height=300)
        self.track_midi_frame = ScrollableFrame(self, orient="vertical", padding=DEFAULT_PADDING, style=TFRAME_STYLE["TRACK_COLLECTION"][0],
                                                width=250, height=650)

    def setup_widgets(self):
        self.switch_view_button.grid(column=0, row=0, sticky="ew")
        self.time_setting_button.grid(column=0, row=1, sticky="ew")
        self.add_track_button.grid(column=0, row=2, sticky="ew")
        self.audio_view.grid(column=1, row=0, columnspan=4,pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.play_button.grid(column=0, row=0, sticky="ew")
        self.pause_button.grid(column=1, row=0, sticky="ew")
        self.stop_button.grid(column=2, row=0, sticky="ew")
        self.generate_button.grid(column=3, row=0, sticky="ew")
        self.track_config_frame.grid(column=1, row=1, rowspan=1000, columnspan=1000, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

    def reset_track_view(self):
        for i, t in enumerate(self.trackConfigViews):
            t.grid_remove()
        for i, t in enumerate(self.trackMidiViews):
            t.grid_remove()

    def setup_track_view(self):
        for i, t in enumerate(self.trackConfigViews):
            t.grid(column=i, row=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY)
        for i, t in enumerate(self.trackMidiViews):
            t.grid(column=0, row=i, padx=DEFAULT_PADX, pady=DEFAULT_PADY)

    def add_track(self, track):
        """
        Add a track to the view, creating and assigning views to it
        :param track: a trackModel
        """
        config_view = TrackConfigView(self.track_config_frame.scrollable_frame, ctrl=track.ctrl, model=track, padding=DEFAULT_PADDING,
                                      style=TFRAME_STYLE["TRACK"][0])
        midi_view = TrackMidiView(self.track_midi_frame.scrollable_frame, ctrl=track.ctrl, model=track, padding=DEFAULT_PADDING,
                                  style=TFRAME_STYLE["TRACK"][0])
        track.ctrl.setup(config_view, midi_view)

        self.reset_track_view()
        self.trackConfigViews.append(config_view)
        self.trackMidiViews.append(midi_view)
        self.setup_track_view()

    def remove_track(self, track):
        """
        Remove a track model from the view
        :param track: a track model
        """
        self.reset_track_view()
        self.trackConfigViews.remove(track.configView)
        self.trackMidiViews.remove(track.midiView)
        self.setup_track_view()

    def switch_view(self):
        """
        Switch the view between midi and config, upon user input
        """
        self.configView = not self.configView
        if (self.configView):
            self.track_midi_frame.grid_forget()
            self.track_config_frame.grid(column=1, row=1, rowspan=1000, columnspan=1000, pady=DEFAULT_PADY,
                                         padx=DEFAULT_PADX)
        else:
            self.track_config_frame.grid_forget()
            self.track_midi_frame.grid(column=1, row=1, rowspan=1000, columnspan=1000, pady=DEFAULT_PADY,
                                         padx=DEFAULT_PADX)

    def open_time_setting(self):
        self.ctrl.open_time_settings()
