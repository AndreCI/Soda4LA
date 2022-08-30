import pandas as pd

from Ctrls.music_controller import MusicCtrl
from Models.data_model import Data
from Models.time_settings_model import TimeSettings
from Models.track_model import Track
from Utils.visualisation import visualisation


# Should we add a controller attribute here?


class Music:
    """
    Model class for music. Music is defined as the end product of the sonification process, regardless of esthetic.
    A music can be played via its music view or displayed via midi view.
    """
    _instance = None

    def __init__(cls):
        """
        instantiation, unique
        """
        if Music._instance is None:
            Music._instance = cls
            # Data
            cls.gain = 100
            cls.muted = False

            # Other models
            cls.tracks = []  # List of track model created by user
            cls.timeSettings = TimeSettings()
            cls.data = Data.getInstance()

            # Ctrl
            cls.ctrl = MusicCtrl(cls)

            # Views
            cls.sonification_view = None

    @staticmethod
    def getInstance():
        if not Music._instance:
            Music()
        return Music._instance

    def generate(cls):
        """
        Iterate over the data, generate all the notes for all the tracks, so that they can be played
        """
        while cls.data.get_next().empty is False:
            for t in cls.tracks:
                t.generate_notes(cls.data.get_next())

    def add_track(self, track: Track):
        self.tracks.append(track)
        self.sonification_view.add_track(track)

    def remove_track(self, track: Track):
        self.tracks.remove(track)
        self.sonification_view.remove_track(track)

    def visualise(self, notes):
        """
        Method to plot a scatter.
        :param: notes: list of Tuples
        :return: matplotlib object
        """
        # Tuple args: tfactor, channel, value, velocity, duration
        # x-axis is time, y-axis is note value.
        # Notes from a track should have a same color

        # Transform batch into a dataframe. Remember to keep tracks as a column
        df = pd.DataFrame(notes, columns=['tfactor', 'channel', 'value', 'velocity', 'duration'])

        # retrieve our visualisation
        return visualisation(df)
