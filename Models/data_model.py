from datetime import datetime

import numpy as np
import pandas as pd
from Utils.constants import DATA_PATH, SAMPLE_PER_TIME_LENGTH_S


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
            self.df = pd.read_csv(DATA_PATH)
            self.header = list(self.df.columns)
            self.timing_span = None
            self.set_data_timespan = None
            self.index = 0
            self.first_date = None
            self.last_date = None
            self.batch_size = SAMPLE_PER_TIME_LENGTH_S
            self.date_column = 'date'
            self.assign_timestamp()
            Data._instance = self

    @staticmethod
    def getInstance():
        if not Data._instance:
            Data()
        return Data._instance

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

    def get_next(cls, iterate=False):
        """
        This method send a batch of samples at a same time
        :return:
            data: pd.Dataframe,
                data buffered
        """
        data = cls.df[cls.index: cls.index + cls.batch_size]
        if(iterate):
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

    def get_deltatime(self):
        """
        Calculate the time span between the end and the beginning
        :param
            column: str,
                The date column of our dataset
        :return:
            time_date: datetime.timedelta,
                date representation of the time span
            time_sec: datetime.timedelta,
                time span in seconds
        """
        # let's set first and last date here
        self.first_date = self.get_datetime(self.df.loc[0, self.date_column])
        self.last_date = self.get_datetime(self.df.loc[self.df.__len__()-1, self.date_column])
        # now, the computation
        time_date = self.first_date - self.last_date
        time_sec = time_date.total_seconds()
        # first and last date into seconds
        self.first_date = self.first_date.timestamp()
        self.last_date = self.last_date.timestamp()

        return time_date, time_sec

    def assign_timestamp(self):
        """
        Method to assign timestamp to a new column
        """
        self.df['timestamp'] = self.df[self.date_column].apply(lambda x: self.get_datetime(x).timestamp())
        self.df['id'] = np.arange(1, self.df.shape[0] + 1)
        # We call method here to init all the attributes
        self.timing_span, _ = self.get_deltatime()

    def reset_playing_index(self):
        self.index = 0
