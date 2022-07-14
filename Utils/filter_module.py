

#TODO complexify with other filter options, such as str filters.
class FilterModule():
    """
    Module to use as a filter when needed, providing an interface between what users entered into the filter box and data
    """
    def __init__(self):
        self.variable=None
        self.filter=None
        self.filter_mode = ["None", "Single", "Range", "Multiple"]
        self.mode = self.filter_mode[0]

    def evaluate(self, value):
        '''
        Determines whether a value in a row should be converted as a note, based on filter.
        :param value: current value to evaluate
        :return: True if value follows the filter, False otherwise.
        '''
        if(self.mode == "None"):
            return True
        if(self.mode == "Single" and self.filter == value):
            return True
        if(self.mode == "Range" and value in self.filter):
            return True
        if(self.mode == "Multiple" and value in self.filter):
            return True
        return False
    
    def assign_variable(self, variable : str):
        """
        Setup the main variable to which the filter will be applied
        :param variable: name of a colomun in data
        """
        self.variable = variable

    def assign(self, filter):
        """
        Setup a filter, based on implemented options
        :param filter: str representation of a filter, entered by user
        :return: True if the filter entered is accepted, otherwise False
        """
        if(filter.isnumeric()):
            self.mode = self.filter_mode[1]
            self.filter = eval(filter)
            return True
        if(len(filter) > 0 and filter[0] == "["):
            self.mode = self.filter_mode[2]
            tab_f = eval(filter)
            self.filter = range(tab_f[0], tab_f[1])
            return True
        if(len(filter.split(";")) > 1):
            self.mode = self.filter_mode[3]
            self.filter = [eval(v) for v in filter.split(";")]
            return True
        self.filter = None
        return False


