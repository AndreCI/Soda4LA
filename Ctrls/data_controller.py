import csv
from datetime import datetime

from Utils.constants import MOCKUP_KEYS
from app_setup import MAX_SAMPLE, DATA_PATH


class DataCtrl():
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        instantiation, unique
        """
        if (cls._instance is None):
            cls._instance = super(DataCtrl, cls).__new__(cls, *args, **kwargs)
            cls.init = False
        return cls._instance

    def setup(cls, path):
        cls.init = True
        cls.csvfile = open(path)
        cls.reader = csv.reader(cls.csvfile)
        cls.header = cls.reader.__next__()
        cls.data = []
        for d in cls.reader:
            cls.data.append(d)
        cls.index = 0
        cls.set_data_timespan(MAX_SAMPLE)

    def get_variables(self):
        if(not self.init):
            return MOCKUP_KEYS
        return self.header

    def get_variables_instances(self, variable):
        idx = self.header.index(variable)
        instances = []
        for d in self.data:
            if(d[idx] not in instances):
                instances.append(d[idx])
        return instances

    def get_next(self):
        d = self.data[self.index]
        self.index += 1
        return d

    def get_data_timespan(self, data):
        min_t = self.get_datetime(data[0][4])
        max_t = self.get_datetime(data[-1][4])
        timedelta = max_t - min_t
        return timedelta.total_seconds()

    def set_data_timespan(self, max_sample):
        min_t = self.get_datetime(self.data[0][4])
        max_t = self.get_datetime(self.data[max_sample][4])
        timedelta = max_t - min_t
        self.timing_span = timedelta.total_seconds()

    def get_deltatime(self, current_date, min_date=None):
        if (min_date == None):
            min_t = self.get_datetime(self.data[0][4])
        else:
            min_t = self.get_datetime(min_date)
        current_t = self.get_datetime(current_date)
        timedelta = current_t - min_t
        return timedelta

    @staticmethod
    def get_datetime(d):
        date = datetime.strptime(d, '%d/%m/%Y %H:%M:%S')
        return date


if __name__ == '__main__':
    db = DataCtrl()
    db.setup(DATA_PATH)
    print(db.get_variables())
    print(db.get_variables_instances("actionType"))
    for i in range(10):
        print(db.get_next())
    db.csvfile.close()
