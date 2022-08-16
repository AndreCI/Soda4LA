# TODO complexify with other filter options, such as str filters.
from enum import Enum

from Models.data_model import Data
import pandas as pd

class FilterType(Enum):
    NONE = 1,
    SINGLE = 2,
    RANGE = 3,
    MULTIPLE = 4

class FilterModule:
    """
    Module to use as a filter when needed, providing an interface between what users entered into the filter box and data
    """

    def __init__(self):
        self.filter = {}
        self.column = None #Data().getInstance().get_variables()[0] # column on which to apply the filter
        self.mode = {}

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def eval_batch(self, batch):
        """
        Determines which rows of a batch should be converted as notes, based on filter. A row can be converted as a note
        if the values found in the column corresponding to self.column are validated by the filter
        :param batch: pandas Dataframe,
            a subset of the dataset
        :return: pandas Dataframe,
            Dataframe w.r.t the filter
        """
        # create a new df using batch
        df = batch.copy()
        # Create a new column and fill it with True or False value after eval
        df['new'] = df[self.column].apply(lambda y: 'True' if self.evaluate(y) is True else 'False')
        # We return row where 'new' is True and we remove the created column
        d = df[df['new'] == 'True'].drop('new', axis=1)
        return d

    def get_filtered_data(self, header : [], data : [[]]):
        """
        Filter all of data based on the user selected filter
        :param header: list of names of each column in data
        :param data: all of data, as a list of list (row per row)
        :return: an iterable with filtered data, using lazy eval
        """
        #TODO
        raise NotImplementedError()
        idx = header.index(self.variable)
        return filter(self.evaluate, data)


    def evaluate(self, value):
        """
        Determines whether a row should be converted as a note, based on filter and the selected value. Value must comes
        from the column corresponding to self.column
        :param value: int,
            current value to evaluate
        :return: bool,
            True if value follows the filter, False otherwise.
        """
        #print("Evaluating {} with mode {}. filter is {}".format(value, self.mode, self.filter))
        if self.column not in self.mode or self.mode[self.column] is FilterType.NONE:
            return True
        if self.mode[self.column] is FilterType.SINGLE and self.filter[self.column] == value:
            return True
        if self.mode[self.column] is FilterType.RANGE and value in self.filter[self.column]:
            return True
        if self.mode[self.column] is FilterType.MULTIPLE and value in self.filter[self.column]:
            return True
        return False

    def assign_column(self, column):
        self.column = column
        if(column not in self.mode):
            self.mode[self.column] = FilterType.NONE

    def assign(self, filter):
        """
        Setup a filter, based on implemented options
        :param filter: str,
            representation of a filter, entered by user
        :return: bool,
            True if the filter entered is legal, otherwise False
        """
        if (filter.isnumeric()):
            self.mode[self.column] = FilterType.SINGLE
            self.filter[self.column] = eval(filter)
            return True
        if (len(filter) > 0 and filter[0] == "["):
            self.mode[self.column] = FilterType.RANGE
            tab_f = eval(filter)
            self.filter[self.column] = range(tab_f[0], tab_f[1])
            return True
        if (len(filter.split(";")) > 1):
            self.mode[self.column] = FilterType.MULTIPLE
            self.filter[self.column] = [eval(v) for v in filter.split(";")]
            return True
        self.mode[self.column] = FilterType.NONE
        self.filter[self.column] = None
        return False

    def assign_quali_table(self, values: []):
        """
        Assign a list of qualitatives variable as a filter.
        :param values: a list of string variable
        :return: True if the assignation was successful, else False
        """
        self.mode[self.column] = FilterType.MULTIPLE
        self.filter[self.column] = values
        return True

    def get_current_filter(self):
        if(self.column in self.filter):
            return "[" + ";".join([str(v) for v in self.filter[self.column]]) + "]"
        return ""

