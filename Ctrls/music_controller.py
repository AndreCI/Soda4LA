
from Models.track_model import Track


class MusicCtrl():
    """
    Controller for final music model. <=> sonification ctrl
    """

    def __init__(self, model):
        #Model
        self.model = model #Music model

    def create_track(self):
        """
        Create a track and adds it to the model
        """
        self.model.add_track(self=self.model, track=Track(self.model))

    def remove_track(self, track : Track):
        """
        Remove a track from the model
        :param track: a Track model
        """
        self.model.remove_track(self=self.model, track=track)

    #TODO
    def play(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

    def generate(self):
        self.model.generate()

    def open_time_settings(self):
        self.model.timeSettings.ctrl.show_window()