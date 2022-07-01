import tkinter as tk
from tkinter import ttk

from Ctrls.sonification_controller import SonificationCtrl
from Utils.constants import DEFAULT_PADDING, TFRAME_STYLE, DEFAULT_PADX, DEFAULT_PADY
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
        self.config = True
        self.ctrl = SonificationCtrl(view=self)
        self.trackConfigViews = []
        self.trackMidiViews = []
        self.create_widgets()
        self.setup_widgets()

    def create_widgets(self):
        self.switch_view_button = tk.Button(self, text="Change view", command=self.switch_view)
        self.time_setting_button = tk.Button(self, text="Time Settings", command=self.open_time_setting)
        self.add_track_button = tk.Button(self, text="Add track", command=self.add_track)
        self.audio_view = ttk.Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["TRACK_COLLECTION"][0])
        self.play_button = tk.Button(self.audio_view, text="Play", command=self.play)
        self.pause_button = tk.Button(self.audio_view, text="Pause", command=self.pause)
        self.stop_button = tk.Button(self.audio_view, text="Stop", command=self.stop)
        self.generate_button = tk.Button(self.audio_view, text="Generate", command=self.generate)
        self.track_config_frame = ttk.Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["TRACK_COLLECTION"][0])
        self.track_midi_frame = ttk.Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["TRACK_COLLECTION"][0])
        # self.timeSettingView = TimeSettingView(self)

    def setup_widgets(self):
        self.switch_view_button.grid(column=0, row=0)
        self.time_setting_button.grid(column=0, row=1)
        self.add_track_button.grid(column=0, row=2)
        self.audio_view.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.play_button.grid(column=0, row=0)
        self.pause_button.grid(column=1, row=0)
        self.stop_button.grid(column=2, row=0)
        self.generate_button.grid(column=3, row=0)
        self.track_config_frame.grid(column=1, row=1, rowspan=10, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

    def generate(self):
        self.ctrl.generate()

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

    def add_track(self):
        tctrl = self.ctrl.add_track()
        config_view = TrackConfigView(self.track_config_frame, ctrl=tctrl, padding=DEFAULT_PADDING,
                                      style=TFRAME_STYLE["TRACK"][0])
        midi_view = TrackMidiView(self.track_midi_frame, ctrl=tctrl, padding=DEFAULT_PADDING,
                                  style=TFRAME_STYLE["TRACK"][0])
        tctrl.setup(config_view, midi_view)

        self.reset_track_view()
        self.trackConfigViews.append(config_view)
        self.trackMidiViews.append(midi_view)
        self.setup_track_view()

    def remove_track(self, config_view, midi_view):
        self.reset_track_view()
        self.trackConfigViews.remove(config_view)
        self.trackMidiViews.remove(midi_view)
        self.setup_track_view()

    def switch_view(self):
        self.config = not self.config
        if (self.config):
            self.track_midi_frame.grid_forget()
            self.track_config_frame.grid(column=1, row=1, rowspan=10, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        else:
            self.track_config_frame.grid_forget()
            self.track_midi_frame.grid(column=1, row=1, rowspan=10, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

    def play(self):
        self.ctrl.play()

    def pause(self):
        self.ctrl.pause()

    def stop(self):
        self.ctrl.stop()

    def open_time_setting(self):
        pass
