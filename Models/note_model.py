from __future__ import annotations

import math
from collections import namedtuple

import Models.data_model as data_model
import Models.track_model as track
from Models.parameter_encoding_model import ParameterEncoding

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from Models.track_model import Track
# Allows to use type hint while preventing cyclic imports

_note_dict = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
NNote = namedtuple('NNote', 'tfactor channel value velocity duration void id')
TNote = namedtuple('TNote', ['tfactor', 'channel', 'value', 'velocity', 'duration', 'void', 'id'])
ANote = namedtuple('TNote', ['timing', 'tfactor', 'channel', 'value', 'velocity', 'duration', 'void', 'id'])
CNote = namedtuple('CNote', ['channel', 'value', 'velocity', 'duration'])


class NoteData:
    _instance = None

    @staticmethod
    def getInstance():
        if not NoteData._instance:
            NoteData()
        return NoteData._instance

    def __init__(self):
        if NoteData._instance is None:
            self.df = None
            self.data: data_model.Data = None
            self.tracks = None
            self.tracks_note = None
            NoteData._instance = self

    def setup(self, tracks: [track.Track]):
        self.data = data_model.Data.getInstance()
        self.tracks = tracks
        self.tracks_note = []

    def create_note(self, row):
        return TNote(tfactor=0, channel=0, value=0, velocity=100, duration=100, void=False, id=-1)

    def generate(self):
        """Pre compute all notes into a dataframe"""
        raise NotImplementedError()
        notes = self.data.current_dataset.apply(lambda x: self.create_note(x), axis=1)
        for track in self.tracks:
            notes = self.data.current_dataset.apply(lambda x: self.create_note(x), axis=1)
            self.tracks_note.append(notes)

    def update(self, track_id: int, parmeter_encoding: ParameterEncoding):
        pass

    def reset(self):
        pass

    def find_index_from_time(self, tfactor: float) -> int:
        return self.df.indexof(tfactor)


def is_valid_note(note):
    """Return True if note is in a recognised format. False if not."""
    if note[0] not in _note_dict:
        return False
    for post in note[1:]:
        if post != "B" and post != "#":
            return False
    return True


def note_to_int(note, octave):
    """Convert notes in the form of C, C#, Cb, C##, etc. to an integer in the
    range of 0-11.
    Throw a ValueError exception if the note format is not recognised.
    """
    if is_valid_note(note):
        val = _note_dict[note[0]]
    else:
        raise ValueError("Unknown note format '%s'" % note)

    # Check for '#' and 'b' postfixes
    for post in note[1:]:
        if post == "B":
            val -= 1
        elif post == "#":
            val += 1
    return val % 12 + octave * 12


def int_to_note(note_int, accidentals="#"):
    """Convert integers in the range of 0-11 to notes in the form of C or C#
    or Db.
    Throw a RangeError exception if the note_int is not in the range 0-11.
    If not specified, sharps will be used.
    """
    if note_int not in range(12):
        note_int = note_int % 12
    ns = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    nf = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    if accidentals == "#":
        return ns[note_int]
    elif accidentals == "b":
        return nf[note_int]
    else:
        raise ValueError("'%s' not valid as accidental" % accidentals)


def convert_seconds_to_quarter(time_in_sec, bpm):
    """
    Util function to transform a timing in seconds into quarterticks, used to write to disk
    :param time_in_sec: a time position in seconds
    :param bpm: beats per minute
    :return: index of the beat at time_in_sec
    """
    quarter_per_second = (bpm / 60)  # <=> beat per seconds
    time_in_quarter = time_in_sec * quarter_per_second
    return time_in_quarter


def note_to_hz(value):
    power = (value - 69) / 12
    return int(440 * math.pow(2, power))
