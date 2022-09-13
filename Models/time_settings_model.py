from Ctrls.time_settings_controller import TimeSettingsCtrl


#TODO add other time settings
from Models.data_model import Data
from Utils.constants import TIME_SETTINGS_OPTIONS, BATCH_SIZE, TIME_BUFFER


class TimeSettings():
    """
    Model class for time settings. It informs track/music models about the way to compute temporal distance between 2 notes based on their
    respective data lignes.
    """
    def __init__(self, music):
        #Data
        self.possible_types = TIME_SETTINGS_OPTIONS
        self.minVal = None
        self.maxVal = None
        self.idMax = None
        self.batchSize = BATCH_SIZE
        self.timeBuffer = TIME_BUFFER
        self.autoload = False
        self.autoloadDataPath = ""
        self.autoloadTimestampcol = ""
        self.debugVerbose = False

        self.type = self.possible_types[1]
        #Other models
        self.music = music
        self.data = Data.getInstance()
        self.musicDuration = self.data.size #1 row per seconds

        #Ctrl
        self.ctrl = TimeSettingsCtrl(self)
        #View
        self.tsView = None

        try:
            with open("settings.ini", "r") as settingsFile:
                for line in settingsFile.readlines():
                    identifier = line.split("=")[0]
                    value = line.split("=")[1]
                    if(identifier == "autoload"):
                        self.autoload = eval(value)
                    elif(identifier == "datapath"):
                        self.autoloadDataPath = eval(value)
                    elif(identifier == "timestampcol"):
                        self.autoloadTimestampcol = eval(value)
                    elif(identifier == "debugverbose"):
                        self.debugVerbose = eval(value)

        except FileNotFoundError:
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
        self.ctrl = TimeSettingsCtrl(self)
        self.tsView = None
        self.data = Data.getInstance()


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
            raise ValueError("Max val {} must be > at min val {}".format(maxVal, minVal))
        self.minVal = minVal
        self.maxVal = maxVal
        self.idMax = idMax
        if not self.musicDuration:
            self.musicDuration = idMax

    def get_temporal_position(self, current, offset=0):
        """
        Return the temporal position of a data point, based on the minimum and maximum and the current selected type.
        Regardless of type, if min=current, then this will return 0. if max=current, then this will return 1.
        :param current: a data point with features timestamp and id
        :param offset: change the temporal position by offset, in ms
        :return: a temporal position between 0 and 1.
        """
        return_value = None
        if self.maxVal < current["internal_timestamp"] < self.minVal:
            raise ValueError("current{} must be in range [min; max] : [{};{}]".format(current.internal_timestamp, self.minVal, self.maxVal))
        distance = self.maxVal - self.minVal
        offset = float(offset)/float(1000*self.musicDuration)
        #ratio = float(distance)/float(max)
        if self.type == self.possible_types[0]:
            return_value = offset + (current["internal_timestamp"] - self.minVal)/float(distance)#(ratio - min) * current
        elif self.type == self.possible_types[1]:
            return_value = offset + float(current["internal_id"])/float(self.idMax)
        else:
            raise NotImplementedError()
        if(return_value <0 or return_value>1):
            raise ValueError("absolute temporal position computation ended up with a non valid value ({}). "
                             "the current timestamp {} is between the maximun {} and the minimum {}"
                             .format(return_value, current.internal_timestamp, self.maxVal, self.minVal))
        return return_value
