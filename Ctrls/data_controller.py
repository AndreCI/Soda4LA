import csv
from datetime import datetime

from app_setup import MAX_SAMPLE


class data_ctrl():
    def __init__(self, path):
        self.csvfile = open(path)
        self.reader = csv.reader(self.csvfile)
        self.header = self.reader.__next__()
        self.data = []
        for d in self.reader:
            self.data.append(d)
        self.index = 0
        self.set_data_timespan(MAX_SAMPLE)

    def get_next(self):
        d = self.data[self.index]
        self.index+=1
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
        if(min_date==None):
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
    db = data_ctrl("data/tamagocours/TraceTamagoAvril2015_codagechat.xls - Feuille1.csv")
    for i in range(10):
        print(db.get_next())
    db.csvfile.close()


