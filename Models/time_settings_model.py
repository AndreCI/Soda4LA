from Ctrls.time_settings_controller import TimeSettingsCtrl


#TODO add other time settings
from Utils.constants import TIME_SETTINGS_OPTIONS, MUSIC_TOTAL_DURATION_S, SAMPLE_PER_TIME_LENGTH_S


class TimeSettings():
    """
    Model class for time settings. It informs track/music models about the way to compute temporal distance between 2 notes based on their
    respective data lignes.
    """
    def __init__(self):
        #Data
        self.possible_types = TIME_SETTINGS_OPTIONS
        self.minVal = None
        self.maxVal = None
        self.idMax = None
        self.musicDuration = MUSIC_TOTAL_DURATION_S
        self.SAMPLES_PER_TICK = SAMPLE_PER_TIME_LENGTH_S

        self.type = self.possible_types[1]
        #Other models
        #Ctrl
        self.ctrl = TimeSettingsCtrl(self)
        #View
        self.tsView = None

    def set_type(self, type : str):
        if(type not in self.possible_types):
            raise NotImplementedError()
        self.type = type

    def set_attribute(self, minVal, maxVal, idMax):
        """
        Setup attributes needed to compute later a temporal position
        :param minVal: float,
            the first timestamp of the dataset, i.e. the first action ever taken
        :param maxVal: float,
            the last timestamp of the dataset, i.e. the last action ever taken
        """
        if(maxVal <= minVal):
            raise ValueError()
        self.minVal = minVal
        self.maxVal = maxVal
        self.idMax = idMax

    def get_temporal_position(self, current):
        """
        Return the temporal position of a data point, based on the minimum and maximum and the current selected type.
        Regardless of type, if min=current, then this will return 0. if max=current, then this will return 1.
        :param current: a data point with features timestanp and id
        :return: a temporal position between 0 and 1.
        """
        if self.maxVal < current.timestamp < self.minVal:
            raise ValueError("current{} must be in range [min; max] : [{};{}]".format(current.timestamp, self.minVal, self.maxVal))
        distance = self.maxVal - self.minVal
        #ratio = float(distance)/float(max)
        if self.type == self.possible_types[0]:
            return (current.timestamp - self.minVal)/float(distance)#(ratio - min) * current
        elif self.type == self.possible_types[1]:
            return float(current.id)/float(self.idMax)
        else:
            raise NotImplementedError()
