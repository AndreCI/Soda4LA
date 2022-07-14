from Ctrls.time_settings_controller import TimeSettingsCtrl


#TODO add other time settings
class TimeSettings():
    """
    Model class for time settings. It informs track/music models about the way to compute temporal distance between 2 notes based on their
    respective data lignes.
    """
    def __init__(self):
        #Data
        self.possible_types = ["linear projection"]#, "log projection"]
        self.type = self.possible_types[0]
        #Other models
        #Ctrl
        self.ctrl = TimeSettingsCtrl(self)
        #View
        self.tsView = None

    def set_type(self, type : str):
        if(type not in self.possible_types):
            raise NotImplementedError()
        self.type = type

    def get_temporal_position(self, min, max, current):
        """
        Return the temporal position of a data point, based on the minimum and maximum and the current selected type.
        Regardless of type, if min=current, then this will return 0. if max=current, then this will return 1.
        :param min: the first timestamp of the data in which a and b comes from
        :param max: the last timestamp
        :param current: timestamp of data point
        :return: a temporal position between 0 and 1.
        """
        if(max<=min or max<current<min or max==0):
            raise ValueError("current{} must be in range [min; max] : [{};{}]".format(current, min, max))
        distance = max - min
        ratio = float(distance)/float(max)
        if(self.type == self.possible_types[0]):
            return (current - min)/float(distance)#(ratio - min) * current
        else:
            raise NotImplementedError()
