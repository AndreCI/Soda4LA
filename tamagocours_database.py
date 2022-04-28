import csv

class CSVWrapper():
    def __init__(self, path):
        self.csvfile = open(path)
        self.reader = csv.reader(self.csvfile)
        self.get_next()

    def get_next(self):
        return self.reader.__next__()


if __name__ == '__main__':
    db = CSVWrapper("data/tamagocours/TraceTamagoAvril2015_codagechat.xls - Feuille1.csv")
    for i in range(10):
        print(db.get_next())
    db.csvfile.close()


