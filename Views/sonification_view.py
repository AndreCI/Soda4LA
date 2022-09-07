import tkinter as tk
from collections import deque
from tkinter import ttk
from tkinter.constants import DISABLED, NORMAL
from tkinter.filedialog import askopenfilename, asksaveasfile

from Models.music_model import Music
from Utils.constants import DEFAULT_PADDING, TFRAME_STYLE, DEFAULT_PADX, DEFAULT_PADY, FILE_PATH
from Utils.scrollable_frame import ScrollableFrame
from Utils.tktable_table import Table
from Views.track_config_view import TrackConfigView
from Views.track_midi_view import TrackMidiView


class SonificationView(ttk.Frame):
    """
    Main view for the sonification process, handling both configuration and midi representation of the loaded data.
    Modules: list of tracks, each with their own config and midi view.
    view to control the start, pause and stop of the current music
    view to configurate time settings
    """
    #TODO: Add fast forward and backward +x/-x seconds
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        #Ctrl and model
        self.model = Music.getInstance()
        self.ctrl = self.model.ctrl
        self.model.sonification_view = self
        self.ctrl.sonification_view = self

        #View data
        self.configView = True #Inform which view is currently displqyed
        self.trackConfigViews = []
        self.trackMidiViews = []
        self.log = deque()
        self.logMax = 10
        self.first_log_line = "Log:" + " "*205 + "\n"

        #setup view
        self.controlFrame = ttk.Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["CONFIG"][0])
        self.switchViewButton = tk.Button(self.controlFrame, text="Change view", command=self.switch_view)
        self.timeSettingsButton = tk.Button(self.controlFrame, text="General Settings", command=self.open_time_setting)
        self.addTrackButton = tk.Button(self.controlFrame, text="Add track", command=self.ctrl.create_track)
        self.exportAllTrackButton = tk.Button(self.controlFrame, text="Export all tracks", command=self.export_all_tracks)
        self.importAllTrackButton = tk.Button(self.controlFrame, text="Import all tracks", command=self.import_all_tracks)

        self.audioView = ttk.Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["TRACK_COLLECTION"][0])
        self.playButton = tk.Button(self.audioView, text="Play", command=self.ctrl.play, state=NORMAL)
        self.pauseButton = tk.Button(self.audioView, text="Pause", command=self.ctrl.pause, state=DISABLED)
        self.stopButton = tk.Button(self.audioView, text="Stop", command=self.ctrl.stop, state=DISABLED)
        self.ffwButton = tk.Button(self.audioView, text=">>>", command=self.ctrl.fast_forward, state=DISABLED)
        self.fbwButton = tk.Button(self.audioView, text="<<<", command=self.ctrl.fast_backward, state=DISABLED)
        self.generateButton = tk.Button(self.audioView, text="Write Midi File", command=self.model.generate_midi, state=NORMAL)
        self.gain_slider = tk.Scale(self.audioView, from_=0, to=100, sliderrelief='solid', orient="horizontal",
                                    command=self.ctrl.change_global_gain)  # flat, groove, raised, ridge, solid, sunken
        self.gain_slider.set(self.model.gain)
        #self.generateButton = tk.Button(self.audioView, text="Generate", command=self.ctrl.generate)

        self.tConfigFrame = ScrollableFrame(self, orient="horizontal", padding=DEFAULT_PADDING, style=TFRAME_STYLE["TRACK_COLLECTION"][0],
                                            width=1380, height=340)
        self.tMidiFrame = ScrollableFrame(self, orient="vertical", padding=DEFAULT_PADDING, style=TFRAME_STYLE["TRACK_COLLECTION"][0],
                                          width=1380, height=650)

        self.logVar = tk.StringVar(value=self.first_log_line)
        self.logLabel = ttk.Label(self, textvariable=self.logVar)

        self.dataTable = Table(self,  row=9, col=0, width=500, height=200)

        self.setup_widgets()

    def setup_widgets(self):
        self.controlFrame.grid(column=0, row=0, rowspan=6)
        self.switchViewButton.grid(column=0, row=0, sticky="ew")
        self.timeSettingsButton.grid(column=0, row=1, sticky="ew")
        self.addTrackButton.grid(column=0, row=2, rowspan=2, sticky="ew")
        self.importAllTrackButton.grid(column=0, row=4, sticky="ew")
        self.exportAllTrackButton.grid(column=0, row=5, sticky="ew")

        self.audioView.grid(column=1, row=0, columnspan=5, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.fbwButton.grid(column=0, row=0, sticky="ew")
        self.playButton.grid(column=1, row=0, sticky="ew")
        self.pauseButton.grid(column=2, row=0, sticky="ew")
        self.stopButton.grid(column=3, row=0, sticky="ew")
        self.ffwButton.grid(column=4, row=0, sticky="ew")
        self.generateButton.grid(column=5, row=0, sticky="ew")
        self.gain_slider.grid(column=6, row=0, sticky="ew")
        #self.generateButton.grid(column=3, row=0, sticky="ew")

        self.tConfigFrame.grid(column=1, row=1, rowspan=1000, columnspan=1000, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

        self.logLabel.grid(column=5, row=1005, rowspan=20, padx=DEFAULT_PADX, pady=DEFAULT_PADY)
        self.dataTable.grid(column=6, row=1005, rowspan=200)#, data=self.model.data.get_first_and_last().to_dict('records'))

    def add_log_line(self, log_line, debug=False):
        if(debug or not self.model.timeSettings.debugVerbose):
            if(len(self.log) > self.logMax):
                self.log.popleft()
            self.log.append(log_line)
            self.logVar.set(self.first_log_line + "\n".join(self.log))

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
        config_view = TrackConfigView(self.tConfigFrame.scrollableFrame, ctrl=track.ctrl, model=track, padding=DEFAULT_PADDING,
                                      style=TFRAME_STYLE["TRACK"][0])
        midi_view = TrackMidiView(self.tMidiFrame.scrollableFrame, ctrl=track.ctrl, model=track, padding=DEFAULT_PADDING,
                                  style=TFRAME_STYLE["TRACK"][0])
        track.configView = config_view
        track.midiView = midi_view
        #track.ctrl.setup(config_view, midi_view)

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
            self.tMidiFrame.grid_forget()
            self.tConfigFrame.grid(column=1, row=1, rowspan=1000, columnspan=1000, pady=DEFAULT_PADY,
                                   padx=DEFAULT_PADX)
        else:
            self.tConfigFrame.grid_forget()
            self.tMidiFrame.grid(column=1, row=1, rowspan=1000, columnspan=1000, pady=DEFAULT_PADY,
                                 padx=DEFAULT_PADX)

    def open_time_setting(self):
        self.ctrl.open_time_settings()

    def export_all_tracks(self):
        f = asksaveasfile(title="Save project as a file", initialdir=FILE_PATH,
                          initialfile="saved_project_{}".format(len(self.model.tracks)), mode='w', defaultextension=".pkl")
        if f is not None:  # asksaveasfile return `None` if dialog closed with "cancel".
            self.ctrl.export_all_tracks(f.name)

    def import_all_tracks(self):
        f = askopenfilename(title="Load selected project")
        if f != "":
            self.ctrl.import_all_tracks(f)

