import itertools

from Models.Note import TNote


class Track():
    """"
    """
    newid = itertools.count()
    def __init__(self):
        self.soundfont=None
        self.id = next(Track.newid)
        self.notes = [TNote(0, 0, 55, 100, 100), TNote(0.5, 0, 55, 100, 100)]

    def setSoundfont(self, soundfont):
        self.soundfont=soundfont