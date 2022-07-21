from Ctrls.music_controller import MusicCtrl
from Models.data_model import Data
from Models.time_settings_model import TimeSettings
from Models.track_model import Track

from Ctrls.MIDI_controller import MIDICtrl
# Should we add a controller attribute here?


class Music:
    """
    Model class for music. Music is defined as the end product of the sonification process, regardless of esthetic.
    A music can be played via its music view or displayed via midi view.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        instantiation, unique
        """
        if (cls._instance is None):
            cls._instance = super(Music, cls).__new__(cls, *args, **kwargs)
            #Data
            cls.gain = 100
            cls.muted = False

            #Other models
            cls.tracks = [] #List of track model created by user
            cls.timeSettings = TimeSettings()
            cls.data = Data.getInstance()

            #Ctrl
            cls.ctrl = MusicCtrl(cls)

            #Views
            cls.sonification_view = None
        return cls._instance

    def generate(cls):
        """
        Iterate over the data, generate all the notes for all the tracks, so that they can be played
        """
        while cls.data.empty is False:
            for t in cls.tracks:
                t.generate_notes(cls.data.get_next())


    def add_track(self, track : Track):
        self.tracks.append(track)
        self.sonification_view.add_track(track)

    def remove_track(self, track : Track):
        self.tracks.remove(track)
        self.sonification_view.remove_track(track)