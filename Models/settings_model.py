from __future__ import annotations

import os.path

import numpy

from Ctrls.settings_controller import SettingsCtrl

# TODO add other time settings
import Models.data_model as data_model
import Models.music_model as music
from Utils.constants import TIME_SETTINGS_OPTIONS, BATCH_SIZE, TIME_BUFFER, BATCH_NBR_PLANNED, SAMPLE_SIZE


class GeneralSettings:
    """
    Model class for time settings. It informs track/music models about the way to compute temporal distance between 2 notes based on their
    respective data lignes.
    """

    def __init__(self, music : music.Music):
        # Other models
        self.music = music
        self.data = data_model.Data.getInstance()

        # Data
        self.musicDuration = None  # in sec. 1 row per seconds is default
        self.possible_types = TIME_SETTINGS_OPTIONS
        self.minVal = None
        self.maxVal = None
        self.idMax = None
        self.tempoNValue = 4
        self.tempoDurValue = 100
        self.tempoOffsetValue = 0
        self.batchSize = BATCH_SIZE
        self.batchPlanned = BATCH_NBR_PLANNED
        self.timeBuffer = TIME_BUFFER
        self.sampleSize = SAMPLE_SIZE
        self.autoload = False
        self.autoloadDataPath = ""
        self.autoloadTimestampcol = ""
        self.debugVerbose = False
        self.type = self.possible_types[0]
        self.graphicalBarPercentage = 0.2
        self.graphicalLength = 10000

        # Ctrl
        self.ctrl = SettingsCtrl(self)
        # View
        self.tsView = None

        if os.path.exists("settings.ini"):
            with open("settings.ini", "r") as settingsFile:
                for line in settingsFile.readlines():
                    identifier = line.split("=")[0]
                    value = line.split("=")[1]
                    if (identifier == "autoload"):
                        self.autoload = eval(value)
                    elif (identifier == "datapath"):
                        self.autoloadDataPath = eval(value)
                    elif (identifier == "timestampcol"):
                        self.autoloadTimestampcol = eval(value)
                    elif (identifier == "debugverbose"):
                        self.debugVerbose = eval(value)
                    elif (identifier == "graphicalLength"):
                        self.graphicalLength = eval(value)
                    elif (identifier == "graphicalBarPercentage"):
                        self.graphicalBarPercentage = eval(value)
                    elif (identifier == "batchSize"):
                        self.batchSize = eval(value)
                    elif (identifier == "batchPlanned"):
                        self.batchPlanned = eval(value)
                    elif (identifier == "timeBuffer"):
                        self.timeBuffer = eval(value)
                    elif (identifier == "sampleSize"):
                        self.sampleSize = eval(value)
        else:
            self.ctrl.write_to_ini()


    def __getstate__(self):
        state = self.__dict__.copy()
        del state["data"]
        del state["music"]
        del state["ctrl"]
        del state["tsView"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.ctrl = SettingsCtrl(self)
        self.tsView = None
        self.data = data_model.Data.getInstance()
        self.possible_types = TIME_SETTINGS_OPTIONS
        self.type = self.possible_types[0]

    def get_music_duration(self) -> int:
        md = int(float(self.data.get_size())/1.5) if self.musicDuration is None else self.musicDuration
        if(self.type == self.possible_types[1]):
            bpm = int(round(60 * float(self.data.get_size()) / md))
            aoffset = float(self.tempoDurValue) / (100 * bpm / 60)  # [0-100] to s
            aoffset = numpy.trunc((self.data.get_size() + (self.tempoNValue-1 + self.tempoOffsetValue)) / self.tempoNValue) * float(aoffset)
            md += aoffset
        return md
    def reset_music_duration(self) -> None:
        self.musicDuration = int(float(self.data.get_size())/1.5)

    def get_bpm(self) ->float: #bpm = size/length
        return int(round(60 * float(self.data.get_size()) / self.get_music_duration()))

    def set_bpm(self, bpm): #length = size/bpm
        self.musicDuration = int(round(60 * float(self.data.get_size())/float(bpm)))

    def set_type(self, type: str)->None:
        if (type not in self.possible_types):
            raise NotImplementedError()
        self.type = type

    def set_attribute(self, minVal:float, maxVal:float, idMax:int)->None:
        """
        Setup attributes needed to compute later a temporal position
        :param minVal: float,
            the first timestamp of the dataset, i.e. the first action ever taken
        :param maxVal: float,
            the last timestamp of the dataset, i.e. the last action ever taken
        """
        if (maxVal <= minVal):
            raise ValueError("Max val {} must be > at min val {}".format(maxVal, minVal))
        self.minVal = minVal
        self.maxVal = maxVal
        self.idMax = idMax
        if not self.musicDuration:
            self.musicDuration = int(float(idMax)/1.5)

    def get_temporal_position(self, current, offset=0) -> float:
        """
        Return the temporal position of a data point, based on the minimum and maximum and the current selected type.
        Regardless of type, if min=current, then this will return 0. if max=current, then this will return 1.
        :param current: a data point with features timestamp and id
        :param offset: between 0-100, in %, change the temporal position relative to bpm
        :return: a temporal position between 0 and 1.
        """
        return_value = None
        if self.maxVal < current["internal_timestamp"] < self.minVal:
            raise ValueError(
                "current{} must be in range [min; max] : [{};{}]".format(current.internal_timestamp, self.minVal,
                                                                         self.maxVal))
        distance = self.maxVal - self.minVal

        offset = float(offset)/(100*self.get_bpm()/60) #[0-100] to s
        offset = float(offset) / float(self.get_music_duration()) #s to tfactor

        if self.type == self.possible_types[2]:
            return_value = offset + (current["internal_timestamp"] - self.minVal) / float(
                distance)  # (ratio - min) * current
        elif self.type == self.possible_types[1]:
            aoffset = float(self.tempoDurValue) / (100 * self.get_bpm() / 60)  # [0-100] to s
            aoffset = numpy.trunc((current["internal_id"] + (self.tempoNValue-1 + self.tempoOffsetValue)) / self.tempoNValue) * float(aoffset) / float(self.get_music_duration())  # s to tfactor
            return_value =aoffset + offset + float(current["internal_id"]) / float(self.idMax)
        elif self.type == self.possible_types[0]:
            return_value = offset + float(current["internal_id"]) / float(self.idMax)
        else:
            raise NotImplementedError()
        # if (return_value < 0 or return_value > 1):
        #     raise ValueError("absolute temporal position computation ended up with a non valid value ({}). "
        #                      "the current timestamp {} is between the maximun {} and the minimum {}"
        #                      .format(return_value, current.internal_timestamp, self.maxVal, self.minVal))
        return return_value
