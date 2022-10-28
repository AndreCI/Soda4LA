import logging
from datetime import datetime

import numpy as np
import pandas as pd
from dateutil.parser import parse
from pandas import DataFrame

import Ctrls.data_controller
from Utils.constants import BATCH_SIZE


class Data:
    """
    Data csv wrapper, offers additional information such as a list of all instances of a variable
    """
    _instance = None

    @staticmethod
    def getInstance():
        if not Data._instance:
            Data()
        return Data._instance

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
            self.path = None
            self.batch_size = None
            self.date_column = None
            self.size = None
            self.view = None
            #self.ctrl = Ctrls.data_controller.DataCtrl(self)
            Data._instance = self

    def retrieve_data(self, path:str):
        """
        Regarding the file extension, this file calls the right method to retrieve data
        :param path: str,
                The file path
        """
        if '.csv' in path:
            try:
                self.df = pd.read_csv(path, sep=";")
            except:
                self.df = pd.read_csv(path)
        elif '.json' in path:
            self.df = pd.read_json(path)
        elif '.xsl' in path:
            self.df = pd.read_excel(path)
        else:
            raise FileNotFoundError("Specified data file has not been found at location: {}".format(path))

    def read_data(self, path:str):
        """
        :param path: str
        """
        self.path = path
        self.retrieve_data(path)
        self.header = list(self.df.columns)
        self.timing_span = None
        self.set_data_timespan = None
        self.index = 0
        self.first_date = None
        self.last_date = None
        self.batch_size = BATCH_SIZE
        self.size = self.df.shape[0] + 1

    @staticmethod
    def is_date(string:str, fuzzy=False) ->bool:
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

    def get_candidates_timestamp_columns(self) -> [str]:
        """
        find and return all columns that looks like a timestamp
        """
        candidates = [c for c in self.header if self.is_date(self.df[c].loc[self.df[c].first_valid_index()])]
        return candidates

    def get_best_guess_variable(self) -> str:
        lower = self.header[0]
        for header in self.header:
            varins = [str(x) for x in self.get_variables_instances(header)]
            if (len(self.get_variables_instances(lower)) > len(varins) > 5 and "nan" not in varins):
                lower = header
        return lower

    def get_variables(self) -> [str]:
        """
        Get the columns (header) of our dataset
        :return:
            header: list,
                The columns of the csv file
        """
        return self.header

    def get_variables_instances(self, column:str) -> [str]:
        """
        Get unique instances from a column
        :param
            column: str,
                the target column
        :return: list,
                unique value from the target column
        """
        return pd.unique(self.df[column])

    def get_max(self, column:str)->float:
        return max([float(x) for x in self.df[column]])

    def get_min(self, column:str)->float:
        return min([float(x) for x in self.df[column]])

    def get_first(self):
        return self.df.iloc[range(0, 10)]

    def get_second(self):
        return self.df.iloc[range(9, 20)]

    def get_first_and_last(self):
        data = self.df.iloc[[0, 1, 2, 3, 4, -5, -4, -3, -2, -1]]
        return data

    def get_next(self, iterate=False) -> DataFrame:
        """
        This method send a batch of samples at a same time
        :return:
            data: pd.Dataframe,
                data buffered
        """
        data = self.df[self.index: self.index + self.batch_size]
        if (iterate):
            self.index += self.batch_size
        return data

    @staticmethod
    def get_datetime(d, additional_format:str) -> datetime:
        """
        :param
            d: str,
                date to convert
            additional_format: str,
                format to try
        :return:
            date: str,
                converted date
        """

        formats = ['%d/%m/%Y %H:%M:%S',
                   '%d/%m/%y %H:%M:%S',
                   '%H:%M:%S PM'  #1:20:21 PM
                   ]
        if additional_format != "":
            formats.insert(0, additional_format)
            logging.info(logging.INFO, "Additional format added : {}".format(additional_format))
        for f in formats:
            try:
                date = datetime.strptime(d, f)
                if(date.year == 1900): #years before 1970-01-02 02:00:00 or beyond 3001-01-19 07:59:59 will raise oserror
                    date = date.replace(year=1986)
                return date
            except ValueError:
                pass
        raise ValueError("No format found for this timestamp.")


    def assign_timestamps(self, additional_format="") -> None:
        """
        Method to assign timestamp to a new column
        """
        self.df['internal_timestamp'] = self.df[self.date_column].apply(lambda x: self.get_datetime(x, additional_format).timestamp())
        #self.df = self.df.sort_values(by='internal_timestamp',
        #                              axis=0)  # TODO message to user telling them that data were sorted
        self.df['internal_id'] = np.arange(1, self.df.shape[0] + 1)
        self.df['internal_filter'] = True
        # set first and last date here
        first_date = self.get_datetime(self.df.iloc[0][self.date_column], additional_format)
        last_date = self.get_datetime(self.df.iloc[len(self.df) - 1][self.date_column], additional_format)
        self.timing_span = first_date - last_date
        # first and last date into seconds
        self.first_date = first_date.timestamp()
        self.last_date = last_date.timestamp()

    def reset_playing_index(self) -> None:
        self.index = 0

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
