import fluidsynth
import threading

from Models.data_model import Data
from Models.track_model import Track
from Utils.sound_setup import SAMPLE_PER_TIME_LENGTH
from Views.music_view import MusicView


class MusicCtrl:
    """
    Controller for final music model. <=> sonification ctrl
    """

    def __init__(self, model):
        #Other data
        self.playing = False  # True if the music has started, regardless of wheter its paused. False when the music is stopped or ended.
        self.paused = False
        self.CAPACITY =6*SAMPLE_PER_TIME_LENGTH
        self.mutex = threading.Semaphore()
        self.empty = threading.Semaphore(self.CAPACITY)
        self.full = threading.Semaphore(0)
        self.playingCV = threading.Event()
        self.pausedEvent = threading.Event()
        #Model
        self.model = model #Music model
        self.view = MusicView(model, self)

    def create_track(self):
        """
        Create a track and adds it to the model
        """
        self.model.add_track(track=Track(self.model))

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
        self.view.play()
        self.playing = True
        self.paused = False
        self.playingCV.set()
        self.pausedEvent.set()

    def pause(self):
        self.view.pause()
        self.paused = True
        self.playingCV.clear()
        self.pausedEvent.clear()

    def stop(self):
        print("Stopping {}, {}, {}".format(self.empty._value, self.full._value, self.mutex._value))
        #self.mutex.acquire()
        self.view.stop()
        self.playing = False
        self.paused = False
        d = Data.getInstance()
        d.reset_playing_index()
        self.model.notes.clear()
        self.empty.release()
        #self.empty = threading.Semaphore(self.CAPACITY)
        #self.full = threading.Semaphore(0)
        self.playingCV.clear()
        #self.mutex.release()
        self.mutex = threading.Semaphore(1)
        #self.model.data.reset_playing_index()

    def open_time_settings(self):
        self.model.timeSettings.ctrl.show_window()