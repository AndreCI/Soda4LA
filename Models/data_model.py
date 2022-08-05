from datetime import datetime
import pandas as pd

from Ctrls.data_controller import DataCtrl
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
            self.view = None
            self.ctrl = DataCtrl(self)
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
        self.get_timestamp_column()# self.date_column value is modified here
        self.assign_timestamp()

    def get_timestamp_column(self):
        """
        This method search the timestamp column
        """
        for col in self.header:
            if isinstance(self.get_datetime(self.df[col].loc[self.df[col].first_valid_index()]), datetime): # if the first notNa element in the column looks like a timestamp
                self.date_column = col
            break

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

    def set_timing_span(self):
        self.timing_span, _ = self.get_deltatime()

    def assign_timestamp(self):
        """
        Method to assign timestamp to a new column
        """
        self.df['timestamp'] = self.df[self.date_column].apply(lambda x: self.get_datetime(x).timestamp())

        # We call method here to init all the attributes
        self.set_timing_span()

