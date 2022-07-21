import csv
from datetime import datetime
import pandas as pd
from Utils.constants import DATA_PATH
from Utils.constants import MOCKUP_VARS
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
                        Our dataset with the row included
            batch_size  : int,
                        the buffer size
        """
        self.timing_span = MAX_SAMPLE
        self.df = pd.DataFrame(columns=MOCKUP_VARS)
        self.header = None
        self.set_data_timespan = None
        self.index = 0
        self.first_date = None
        self.last_date = None
        self.batch_size = SAMPLE_PER_TIME_LENGTH
        self.path = DATA_PATH
        self.assign_timestamp()
        self.date_column = 'date'

    def __new__(cls, *args, **kwargs):
        """
        instantiation, unique
        """
        if cls._instance is None:
            cls._instance = super(Data, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def setup(cls):
        """
        Method to retrieve data from the CSV file
        :param
            path: str,
                relative path to the file
        """
        cls.df = pd.read_csv(cls.path)
        cls.header = list(cls.df.columns)
        cls.index = 0

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
        self.first_date = self.df[self.date_column][0]
        self.last_date = self.df[self.date_column][-1]
        # now, the computation
        time_date = self.get_datetime(self.first_date) - self.get_datetime(self.last_date)
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
        self.df['timestamp'] = self.df[self.date_column].apply(lambda x: x.timestamp())

