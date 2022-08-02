import fluidsynth
import threading
from Models.track_model import Track
from Utils.sound_setup import SAMPLE_PER_TIME_LENGTH
from Views.music_view import MusicView


class MusicCtrl:
    """
    Controller for final music model. <=> sonification ctrl
    """

    def __init__(self, model):
        #Model
        self.model = model #Music model
        self.view = MusicView(model)
        #Other data


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

    def play(self):
        """
        Start a thread via music model to produce notes for the music view, then start the sequencer
        """
        self.note_generator_thread = threading.Thread(target=self.model.generate, args=[self.model], daemon=True)
        self.note_generator_thread.start()
        self.view.play()

    def pause(self):
        #TODO how to pause the sequencer? Hitting pley should restart where it stopped
        pass

    def stop(self):
        #TODO how to stop the sequencer?
        pass

    def open_time_settings(self):
        self.model.timeSettings.ctrl.show_window()