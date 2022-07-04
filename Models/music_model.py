from Ctrls.music_controller import MusicCtrl


class Music():
    """
    Model class for music. Music is defined as the end product of the sonification process, regardless of esthetic.
    A music can be played via its music view or displayed via midi view.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        instantiation, unique
        """
        print("new")
        if (cls._instance is None):
            cls._instance = super(Music, cls).__new__(cls, *args, **kwargs)
            #Data
            cls.gain = 100
            cls.muted = False

            #Other models
            cls.tracks = []

            #Ctrl
            cls.ctrl = MusicCtrl(cls)

            #Views
            cls.sonification_view = None
            print(cls.gain)
        return cls._instance


    def add_track(self, track):
        self.tracks.append(track)
        self.sonification_view.add_track(track)

    def remove_track(self, track):
        self.tracks.remove(track)