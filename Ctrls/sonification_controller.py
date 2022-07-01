from Ctrls.track_controller import TrackCtrl


#TODO move data to model object
class SonificationCtrl():
    """
    Controller for the sonification process. It is unique and uses other ctrls. It is linked to sonification_view
    """
    _instance = None

    def __new__(cls, view=None, *args, **kwargs):
        """
        instantiation, unique
        :param view: sonification_view
        """
        if (cls._instance is None):
            cls._instance = super(SonificationCtrl, cls).__new__(cls, *args, **kwargs)
            cls.tracks = []
            cls.view = view
        return cls._instance

    def add_track(self):
        track_ctrl = TrackCtrl(self)
        self.tracks.append(track_ctrl)
        return track_ctrl

    def remove_track(self, track_ctrl):
        self.tracks.remove(track_ctrl)
        self.view.remove_track(track_ctrl.config_view, track_ctrl.midi_view)

    def play(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

    def generate(self):
        pass
