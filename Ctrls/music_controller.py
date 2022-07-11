
from Models.track_model import Track


class MusicCtrl():
    """
    Controller for final music model. <=> sonification ctrl
    """

    def __init__(self, model):
        #Model
        self.model = model

    def create_track(self):
        self.model.add_track(self=self.model, track=Track(self.model))

    def remove_track(self, track):
        self.model.remove_track(self=self.model, track=track)

    def play(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

    def generate(self):
        pass

    def open_time_settings(self):
        self.model.timeSettings.ctrl.show_window()