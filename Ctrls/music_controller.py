import fluidsynth
import threading

from Models.data_model import Data
from Models.track_model import Track
from Utils.IterableSemaphore import ISemaphore, IBoundedSemaphore
from Views.music_view import MusicView


class MusicCtrl:
    """
    Controller for final music model. <=> sonification ctrl
    """

    def __init__(self, model):
        #Other data
        self.playing = False  # True if the music has started, regardless of wheter its paused. False when the music is stopped or ended.
        self.paused = False
        self.queueSemaphore = ISemaphore() #Could be seomething else ig
        self.emptySemaphore = IBoundedSemaphore(model.QUEUE_CAPACITY)
        self.fullSemaphore = IBoundedSemaphore(model.QUEUE_CAPACITY)
        self.fullSemaphore.acquire(n=model.QUEUE_CAPACITY) #Set semaphore to 0
        self.playingEvent = threading.Event()
        self.pausedEvent = threading.Event()
        #Model
        self.model = model #Music model
        self.view = MusicView(model, self)
        self.datas = Data.getInstance()


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
        self.playingEvent.set()
        self.pausedEvent.set()

    def pause(self):
        self.view.pause()
        self.paused = True
        self.playingEvent.clear()
        self.pausedEvent.clear()

    def stop(self):
        print("Stopping at {} with {} notes in queue . empty:{}, full:{}, mutex:{}".format(self.view.sequencer.get_tick(), self.model.notes.qsize(),
                                                                                           self.emptySemaphore._value, self.fullSemaphore._value, self.queueSemaphore._value))
        self.view.synth.system_reset() #Reset synth to prevent future note from being played
        self.playingEvent.clear() # Send stop event
        #Update bools
        self.playing = False
        self.paused = False
        #Update data
        self.datas.reset_playing_index()
        #Reset semaphores
        #self.emptySemaphore.release(n=len(self.model.notes))
        #self.fullSemaphore.acquire(n=len(self.model.notes))
        #Reset queue
        while(not self.model.notes.empty()):
            self.emptySemaphore.release()
            self.fullSemaphore.acquire()
            self.model.notes.get_nowait()
        #self.model.notes.clear()

    def open_time_settings(self):
        self.model.timeSettings.ctrl.show_window()