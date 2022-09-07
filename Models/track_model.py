import itertools
import pickle
import Models.music_model

from Ctrls.track_controller import TrackCtrl
from Models.data_model import Data

from Utils.constants import ENCODING_OPTIONS

from Models.note_model import TNote, CNote
from Models.parameter_encoding_model import ParameterEncoding
from Utils.filter_module import FilterModule
import pandas as pd

from Utils.soundfont_loader import SoundfontLoader


class Track:
    """
    Model class for a track, regrouping multiples notes and a soundfont. Each track is unique and can be viewed either
    via config view or midi view.
    Notes and soundfont are defined via a parameter encoding model alongside loaded data.
    """
    newid = itertools.count()

    def __init__(self):
        #Data
        self.id = next(Track.newid)
        sfl = SoundfontLoader.get_instance()
        self.soundfont = sfl.get()  # soundfont selected by user, <=< instrument

        self.filter = FilterModule() #Filter module linked to the column, dictating which row in data is used to generate notes
        self.data = Data().getInstance()
        self.filter.column = self.data.get_variables()[0]
        self.gain = 100 #Volume of the current track, between 0 and 100
        self.muted = False
        self.offset = 0
        self.music = Models.music_model.Music.getInstance() #Needed to backtrack and remove itself upon deletion, among other things

        #Other models
        self.pencodings = {}
        for pe in ENCODING_OPTIONS:
            self.pencodings[pe] = ParameterEncoding(encoded_var=pe)

        #Ctrls
        self.ctrl = TrackCtrl(self)

        #Views
        self.midiView = None
        self.configView = None

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["data"]
        del state["music"]
        del state["midiView"]
        del state["configView"]
        del state["ctrl"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.data = Data.getInstance()
        self.ctrl = TrackCtrl(self)
        self.music = Models.music_model.Music.getInstance()
        #elf.music.ctrl.add_track(self)
        self.configView = None
        self.midiView = None

    def serialize(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)
            self.music.sonification_view.add_log_line("Track saved to {}".format(f.name))

    def unserialize(self, path):
        with open(path, 'rb') as f:
            oldid = self.id
            var = pickle.load(f)
            self.__dict__.update(var.__dict__)
            self.id = oldid
            self.music.sonification_view.add_log_line("Track loaded to id {}".format(self.id))

    def generate_notes(self, batch):
        """
        Generate notes for the current track, based on main variable, parameter encoding and filters.
        :param batch: pandas Dataframe,
            a subset of the dataset regardless the considered filter
        :return list of notes
        """
        notes = [] #Container for the next batch of data
        for idx, row in self.filter_batch(batch).iterrows():  # iterate over index and row
            notes.append(TNote(tfactor=self.music.timeSettings.get_temporal_position(row, self.offset),
                                    channel=self.id,
                                    value=self.pencodings["value"].get_parameter(row),
                                    velocity=self.pencodings["velocity"].get_parameter(row),
                                    duration=self.pencodings["duration"].get_parameter(row),
                                    id=row['id']))
        return notes

    def filter_batch(self, batch):
        for encoding in self.pencodings.values():
            batch = encoding.filter.eval_batch(batch)
        return self.filter.eval_batch(batch)

    def set_main_var(self, variable : str):
        self.filter.assign_column(variable)

    def set_soundfont(self, soundfont):
        self.soundfont = soundfont

    def remove(self):
        self.music.ctrl.remove_track(track=self)
