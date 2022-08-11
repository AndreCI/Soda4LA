# TODO complexify with other filter options, such as str filters.
from Models.data_model import Data
import pandas as pd


class FilterModule:
    """
    Module to use as a filter when needed, providing an interface between what users entered into the filter box and data
    """

    def __init__(self):
        self.filter = None
        self.column = None #Data().getInstance().get_variables()[0] # column on which to apply the filter
        self.filter_mode = ["None", "Single", "Range", "Multiple"]
        self.mode = self.filter_mode[0]

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
        return df[df['new'] == 'True'].drop('new', axis=1)

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
        if self.mode == "None":
            return True
        if self.mode == "Single" and self.filter == value:
            return True
        if self.mode == "Range" and value in self.filter:
            return True
        if self.mode == "Multiple" and value in self.filter:
            return True
        return False

    def assign(self, filter):
        """
        Setup a filter, based on implemented options
        :param filter: str,
            representation of a filter, entered by user
        :return: bool,
            True if the filter entered is legal, otherwise False
        """
        if (filter.isnumeric()):
            self.mode = self.filter_mode[1]
            self.filter = eval(filter)
            return True
        if (len(filter) > 0 and filter[0] == "["):
            self.mode = self.filter_mode[2]
            tab_f = eval(filter)
            self.filter = range(tab_f[0], tab_f[1])
            return True
        if (len(filter.split(";")) > 1):
            self.mode = self.filter_mode[3]
            self.filter = [eval(v) for v in filter.split(";")]
            return True
        self.filter = None
        return False
