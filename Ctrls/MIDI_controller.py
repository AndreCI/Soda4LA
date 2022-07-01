from Ctrls.data_controller import DataCtrl
from Models.Note import CNote, CNote_to_TNote
from Utils.constants import *
from Utils.sound_setup import *


#TODO rework, this should modify a model object based on views commands
class MIDICtrl():
    """"
    Controller for midi protocols, transforming data into proper midi encoding
    """

    def __init__(self):
        self.data_ctrl = DataCtrl()
        self.data_ctrl.setup(DATA_PATH)
        self.value_encoding = VALUE_encoding
        self.timing_span = 1
        self.duration = 100
        self.velocity = 100

    def assign_time(self, data):
        """
        Return a value between [0-1], where 0 is at the start of the music and 1 at the end.
        Independant of the total duration of the end music.
        """
        current_t = self.data_ctrl.get_deltatime(data[4], self.timing_start)
        timing = (current_t.total_seconds()) / self.timing_span
        return timing

    def assign_duration(self, data):
        return self.duration

    def assign_value(self, data):
        value = self.value_encoding["default"][0]
        if (data[2] in self.value_encoding):
            value = self.value_encoding[data[2]][0]
        else:
            print("encoding not found: " + data[2])
        return value

    def assign_velocity(self, data):
        return self.velocity

    def assign_channel(self, data):
        value = self.value_encoding["default"][1]
        if (data[2] in self.value_encoding):
            value = self.value_encoding[data[2]][1]
        else:
            print("encoding not found: " + data[2])
        return value

    def process_next_notes(self, start, end):
        notes = []
        data = self.data_ctrl.data[start:end]
        self.timing_span = self.data_ctrl.get_data_timespan(data)
        self.timing_start = self.data_ctrl.data[start][4]
        for d in data:
            notes.append(self.process_next_note_timed(d))
        return notes

    def process_next_note(self, data):
        return CNote(self.assign_channel(data), self.assign_value(data), self.assign_velocity(data),
                     self.assign_duration(data))

    def process_next_note_timed(self, data):
        return CNote_to_TNote(self.process_next_note(data), self.assign_time(data))

    def get_next_note(self):
        data = self.data_ctrl.get_next()
        if (TIMING == "auto"):
            return self.process_next_note(data)
        else:
            return self.process_next_note_timed(data)
