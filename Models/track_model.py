import itertools

from Ctrls.track_controller import TrackCtrl
from Models.note_model import TNote
from Models.parameter_encoding_model import ParameterEncoding
from Utils.constants import ENCODING_OPTIONS


class Track():
    """
    Model class for a track, regrouping multiples notes and a soundfont. Each track is unique and can be viewed either
    via config view or midi view.
    Notes and soundfont are defined via a parameter encoding model alongside loaded data.
    """
    newid = itertools.count()

    def __init__(self, music):
        #Data
        self.id = next(Track.newid)
        self.soundfont = None
        self.mainVar = None
        self.gain = 100
        self.muted = False
        self.filter = None
        self.music = music #Needed to backtrack and remove itself upon deletion

        #Other models
        self.notes = [TNote(0, 0, 55, 100, 100), TNote(0.5, 0, 55, 100, 100)]
        self.pencodings = []
        for pe in ENCODING_OPTIONS:
            self.pencodings.append(ParameterEncoding(encoded_var=pe))

        #Ctrls
        self.ctrl = TrackCtrl(self)

        #Views
        self.midiView = None
        self.configView = None

    def set_main_var(self, variable):
        self.mainVar = variable

    def set_soundfont(self, soundfont):
        self.soundfont = soundfont

    def remove(self):
        self.music.ctrl.remove_track(track=self)
