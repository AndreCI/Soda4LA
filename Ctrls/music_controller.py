
from Models.track_model import Track


class MusicCtrl():
    """
    Controller for final music model.
    """

    def __init__(self, model):
        #Model
        self.model = model

    def create_track(self):
        self.model.add_track(self=self.model, track=Track(self.model))

    def remove_track(self, track):
        self.model.tracks.remove(track)#lambda x: x.id == track_id)
        self.model.sonification_view.remove_track(track)

    def play(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

    def generate(self):
        pass
