import tamagocours_database
from app_setup import DATA_PATH
from midi import hz_to_midi, RTNote


class MIDIController():
    def __init__(self):
        self.datas = tamagocours_database.CSVWrapper(DATA_PATH)


    def get_next_note(self):
        data = self.datas.get_next()
        value, velocity, duration = 85, 100, 1
        print(data)
        if(data[2] == "showItemCUPBOARD"):
            value = 100
        return RTNote(value, velocity, duration) #value velocity duration