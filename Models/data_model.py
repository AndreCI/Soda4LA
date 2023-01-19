import logging
import os.path
from datetime import datetime

import dateutil
import numpy as np
import pandas as pd
from dateutil.parser import parse, ParserError
from pandas import DataFrame

import Models.music_model as music_model
from Utils.error_manager import ErrorManager


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
            self.current_dataset = None
            self.df = []
            self.data_index = 0
            self.header = None
            self.timing_span = None
            self.set_data_timespan = None
            self.index = None
            self.first_date = None
            self.last_date = None
            self.primary_data_path = None
            self.batch_size = None
            self.date_column = None
            self.size = None
            self.view = None
            self.formats = None
            self.sample_size = None
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
                self.df.append(pd.read_csv(path, sep=";"))
            except:
                self.df.append(pd.read_csv(path))
        elif '.json' in path:
            self.df.append(pd.read_json(path))
        elif '.xsl' in path:
            self.df.append(pd.read_excel(path))
        else:
            raise FileNotFoundError("Specified data file has not been found at location: {}".format(path))

    def read_primary_data(self, path:str):
        """
        :param path: str
        """
        if len(self.df) > 0:
            raise ValueError("There is already primary data loaded!")
        self.primary_data_path = path
        self.retrieve_data(path)
        self.header = list(self.df[0].columns)
        self.timing_span = None
        self.set_data_timespan = None
        self.index = 0
        self.first_date = None
        self.last_date = None
        music = music_model.Music.getInstance()
        self.batch_size = music.settings.batchSize
        self.sample_size = music.settings.sampleSize
        self.size = self.df[0].shape[0] + 1
        music.settings.reset_music_duration()
        self.current_dataset = self.df[0]

    def read_additional_data(self, path:str):
        self.data_index+=1
        self.retrieve_data(path)

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
        candidates = [c for c in self.header if self.is_date(self.current_dataset[c].loc[self.current_dataset[c].first_valid_index()])]
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
        return pd.unique(self.df[0][column])

    def get_max(self, column:str)->float:
        return max([float(x) for x in self.current_dataset[column]])

    def get_min(self, column:str)->float:
        return min([float(x) for x in self.current_dataset[column]])

    def get_first(self):
        return self.current_dataset.iloc[range(0, self.sample_size)]

    def get_second(self):
        return self.current_dataset.iloc[range(self.sample_size - 1, self.sample_size*2)]

    def get_next(self, iterate=False) -> DataFrame:
        """
        This method send a batch of samples at a same time
        :return:
            data: pd.Dataframe,
                data buffered
        """
        data = self.current_dataset[self.index: self.index + self.batch_size]
        if (iterate):
            self.index += self.batch_size
        return data

    def get_timestamp_formats(self, additional_format:str="")-> [str]:
        """
        Read, write and returns currently used formats for timestamp. Formats are stored on disk and regenerated to default if the file is deleted.
        :param additional_format: an additional timestamp format that will be saved to disk.
        :return: a list of str of formats for the timestamp column.
        """
        if self.formats != None and (additional_format=="" or additional_format in self.formats):
            return self.formats
        if(not os.path.exists("timestamp_formats.ini")):
            with open("timestamp_formats.ini", "w") as file:
                file.writelines(['%d/%m/%Y %H:%M:%S\n',
                   '%d/%m/%y %H:%M:%S\n',
                   '%Y-%m-%d %H:%M:%S\n', #2014-03-31 13:28:25
                   '%y-%m-%d %H:%M:%S\n', #14-03-31 13:28:25
                   '%H:%M:%S PM'] #1:20:21 PM
                   )
        formats = []
        with open('timestamp_formats.ini', "r+") as file:
            for line in file.readlines():
                formats.append(line.removesuffix("\n"))
            if(additional_format != "" and additional_format not in formats):
                formats.insert(0, additional_format)
                logging.info(logging.INFO, "Additional format added : {}".format(additional_format))
                file.write('\n' + additional_format)
        self.formats = formats
        return self.formats

    @staticmethod
    def get_datetime(d, formats) -> datetime:
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

        for f in formats:
            try:
                date = datetime.strptime(d, f)
                if(date.year <= 1970): #years before 1970-01-02 02:00:00 or beyond 3001-01-19 07:59:59 will raise oserror
                    date = date.replace(year=1971)
                    ErrorManager.getInstance().datetime_replacement_warning()
                return date
            except ValueError:
                pass
        try:
            yourdate = dateutil.parser.parse(d)
            return yourdate
        except ParserError:
            raise ValueError("No format found for this timestamp: {}".format(d))


    def assign_timestamps(self, additional_format="") -> None:
        """
        Method to assign timestamp to a new column
        """
        self.df[self.data_index]['internal_timestamp'] = self.df[self.data_index][self.date_column].apply(lambda x: self.get_datetime(x, self.get_timestamp_formats(additional_format)).timestamp())
        if not self.df[self.data_index]['internal_timestamp'].is_monotonic_increasing:
            sort_data = ErrorManager.getInstance().sorted_data_warning()
            if(sort_data):
                self.df[self.data_index] = self.df[self.data_index].sort_values(by='internal_timestamp', axis=0)
            else:
                exit()
        self.df[self.data_index]['internal_id'] = np.arange(1, self.df[self.data_index].shape[0] + 1)
        self.df[self.data_index]['internal_filter'] = True
        # set first and last date here
        first_date = self.get_datetime(self.df[self.data_index].iloc[0][self.date_column], self.get_timestamp_formats(additional_format))
        last_date = self.get_datetime(self.df[self.data_index].iloc[len(self.df[self.data_index]) - 1][self.date_column], self.get_timestamp_formats(additional_format))
        self.timing_span = first_date - last_date
        # first and last date into seconds
        self.first_date = first_date.timestamp()
        self.last_date = last_date.timestamp()

    def set_data_index(self, index)->None:
        self.data_index = index
        self.current_dataset = self.df[self.data_index]

    def reset_playing_index(self) -> None:
        self.index = 0

    def get_insight(self, col):
        """
        This function helps to have an overview of our data with respect to the type of feature
        :param col:
        :return: dict
        """
        insight = {}

        if col in self.df[self.data_index].select_dtypes(exclude='object'):  # if col is continious
            return {'mode': self.df[self.data_index][col].mode(), 'mean': self.df[self.data_index][col].mean(), 'min': self.df[self.data_index][col].min(),
                    'max': self.df[self.data_index][col].max(), 'median': self.df[self.data_index][col].median()}

        else:  # col is an object/categorical
            return self.df[self.data_index][col].value_counts().to_dict()
