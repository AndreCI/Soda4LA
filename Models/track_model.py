import itertools

from Ctrls.track_controller import TrackCtrl
from Models.data_model import Data

from Utils.constants import ENCODING_OPTIONS, SF_Default, SOUNDFONTS

from Models.note_model import TNote, CNote
from Models.parameter_encoding_model import ParameterEncoding
from Utils.filter_module import FilterModule
import pandas as pd


class Track:
    """
    Model class for a track, regrouping multiples notes and a soundfont. Each track is unique and can be viewed either
    via config view or midi view.
    Notes and soundfont are defined via a parameter encoding model alongside loaded data.
    """
    newid = itertools.count()

    def __init__(self, music):
        #Data
        self.id = next(Track.newid)
        self.soundfont = SOUNDFONTS["default"] #soundfont selected by user, <=< instrument

        self.filter = FilterModule() #Filter module linked to the column, dictating which row in data is used to generate notes
        self.datas = Data().getInstance()
        self.filter.column = self.datas.get_variables()[0]
        self.gain = 100 #Volume of the current track, between 0 and 100
        self.muted = False
        self.music = music #Needed to backtrack and remove itself upon deletion

        #Other models
        self.notes = []
        self.pencodings = {}
        for pe in ENCODING_OPTIONS:
            self.pencodings[pe] = ParameterEncoding(encoded_var=pe)

        #Ctrls
        self.ctrl = TrackCtrl(self)

        #Views
        self.midiView = None
        self.configView = None

    def generate_notes(self, batch):
        """
        Generate notes for the current track, based on main variable, parameter encoding and filters.
        :param batch: pandas Dataframe,
            a subset of the dataset regardless the considered filter
        """
        # TODO time parameter is not defined here,
        for i, r in self.filter.eval_batch(batch).iterrows():  # iterate over index and row
            self.notes.append(TNote(tfactor=self.music.timeSettings.get_temporal_position(r.timestamp), #TODO only send timestamp.
                                    channel=self.id,
                                    value=self.pencodings["value"].get_parameter(r),
                                    velocity=self.pencodings["velocity"].get_parameter(r),
                                    duration=self.pencodings["duration"].get_parameter(r),
                                    ))

    def set_main_var(self, variable : str):
        self.filter.column = variable

    def set_soundfont(self, soundfont):
        self.soundfont = soundfont

    def remove(self):
        self.music.ctrl.remove_track(track=self)
