from datetime import datetime
import pandas as pd
from dateutil.parser import parse

import Ctrls.data_controller
from Utils.constants import DATA_PATH
from Utils.sound_setup import MAX_SAMPLE
from Utils.sound_setup import SAMPLE_PER_TIME_LENGTH


class Data:
    """
    Data csv wrapper, offers additional information such as a list of all instances of a variable
    """
    _instance = None

    def __init__(self):
        """
            header      : list,
                        column of the dataframe
            df          : Pandas.Dataframe,
                        Our dataset
            batch_size  : int,
                        the buffer size
        """
        if Data._instance is None:
            self.df = None
            self.header = None
            self.timing_span = None
            self.set_data_timespan = None
            self.index = None
            self.first_date = None
            self.last_date = None
            self.batch_size = None
            self.date_column = None
            #self.timestamp_columns = [] # List of all columns that look like a date one
            self.view = None
            self.ctrl = Ctrls.data_controller.DataCtrl(self)
            Data._instance = self

    @staticmethod
    def getInstance():
        if not Data._instance:
            Data()
        return Data._instance

    def retrieve_data(self, path):
        """
        Regarding the file extension, this file calls the right method to retrieve data
        :param path: str,
                The file path
        """
        if '.csv' in path:
            self.df = pd.read_csv(path)
        elif '.json' in path:
            self.df = pd.read_json(path)
        else:
            self.df = pd.read_excel(path)

    def read_data(self, path):
        """
        :param path: str
        """
        self.retrieve_data(path)
        self.header = list(self.df.columns)
        self.timing_span = MAX_SAMPLE
        self.set_data_timespan = None
        self.index = 0
        self.first_date = None
        self.last_date = None
        self.batch_size = SAMPLE_PER_TIME_LENGTH
        #self.get_timestamp_column()  # self.date_column value is modified here
        #self.df['timestamp'] = self.df[self.date_column].apply(lambda x: self.get_datetime(x).timestamp())

    @staticmethod
    def is_date(string, fuzzy=False):
        """
        Return whether the string can be interpreted as a date.
        :param string: str, string to check for date
        :param fuzzy: bool, ignore unknown tokens in string if True
        """
        try:
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False
        except TypeError:
            return False

    def get_candidates_timestamp_columns(self):
        """
        find and return all columns that looks like a timestamp
        """
        candidates = [c for c in self.header if self.is_date(self.df[c].loc[self.df[c].first_valid_index()])]
        return candidates

    def get_variables(cls):
        """
        Get the columns (header) of our dataset
        :return:
            header: list,
                The columns of the csv file
        """
        return cls.header

    def get_variables_instances(cls, column):
        """
        Get unique instances from a column
        :param
            column: str,
                the target column
        :return: list,
                unique value from the target column
        """
        return pd.unique(cls.df[column])

    def get_first_and_last(cls):
        data = cls.df[0: + cls.batch_size]
        return data

    def get_next(cls):
        """
        This method send a batch of samples at a same time
        :return:
            data: pd.Dataframe,
                data buffered
        """
        data = cls.df[cls.index: cls.index + cls.batch_size]
        cls.index += cls.batch_size
        return data

    @staticmethod
    def get_datetime(d):
        """
        :param
            d: str,
                date to convert
        :return:
            date: str,
                converted date
        """
        date = datetime.strptime(d, '%d/%m/%Y %H:%M:%S')
        return date

    def assign_timestamps(self):
        """
        Method to assign timestamp to a new column
        """
        self.df['timestamp'] = self.df[self.date_column].apply(lambda x: self.get_datetime(x).timestamp())
        # let's set first and last date here
        self.first_date = self.get_datetime(self.df.loc[0, self.date_column])
        self.last_date = self.get_datetime(self.df.loc[self.df.__len__()-1, self.date_column])
        # now, the computation
        self.timing_span = self.first_date - self.last_date
        # first and last date into seconds
        self.first_date = self.first_date.timestamp()
        self.last_date = self.last_date.timestamp()

    def get_insight(self, col):
        """
        This function helps to have an overview of our data with respect to the type of feature
        :param col:
        :return: dict
        """
        insight = {}

        if col in self.df.select_dtypes(exclude='object'):  # if col is continious
            return {'mode': self.df[col].mode(), 'mean': self.df[col].mean(), 'min': self.df[col].min(),
                    'max': self.df[col].max(), 'median': self.df[col].median()}

        else:  # col is an object/categorical
            return self.df[col].value_counts().to_dict()
