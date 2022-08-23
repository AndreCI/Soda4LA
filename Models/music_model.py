import threading
import time
from queue import PriorityQueue

from Ctrls.music_controller import MusicCtrl
from Models.data_model import Data
from Models.note_model import TNote
from Models.time_settings_model import TimeSettings
from Utils.constants import BATCH_NBR_PLANNED
from Models.track_model import Track



class Music:
    """
    Model class for music. Music is defined as the end product of the sonification process, regardless of esthetic.
    A music can be played via its music view or displayed via midi view.
    """
    _instance = None

    @staticmethod
    def getInstance():
        if not Music._instance:
            Music()
        return Music._instance

    def __init__(self):
        """
        instantiation, unique
        """
        if Music._instance is None:
            Music._instance = self
            # Data
            self.gain = 100
            self.muted = False

            # Other models
            self.tracks = []  # List of track model created by user
            self.timeSettings = TimeSettings(self)
            self.data = Data.getInstance()
            self.QUEUE_CAPACITY = BATCH_NBR_PLANNED * self.timeSettings.batchSize
            self.notes = PriorityQueue()  # Priority queue ordered by tfactor

            # Ctrl
            self.ctrl = MusicCtrl(self)

            # Views
            self.sonification_view = None
            self.ctrl.producer_thread.start()


    def __getstate__(self):
        state = self.__dict__.copy()
        del state["data"]
        del state["ctrl"]
        del state["sonification_view"]
        del state["notes"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.notes = PriorityQueue()
        self.sonification_view = None
        self.data = Data.getInstance()
        #self.ctrl = None#MusicCtrl(self)


    def generate(self):
        """
        Threaded.
        Produce at regular intervals a note, based on data and tracks configuration and put it into self.notes
        """
        while True:  # This thread never stops
            self.ctrl.playingEvent.wait()  # wait if we are stopped
            self.ctrl.pausedEvent.wait()  # wait if we are paused
            #with self.ctrl.trackSemaphore:
            max_note_nbr = len(self.tracks) * self.data.batch_size  #Acquire queue as if each row will become a note
            note_nbr = 0  # track how many row actually become notes
            self.ctrl.emptySemaphore.acquire(n=max_note_nbr)  # Check if the queue is not full
            # Usually hang on this ^^^
            if not self.ctrl.playing:  # Check if semaphore was acquired while stop was pressed
                self.ctrl.emptySemaphore.release(n=max_note_nbr)  # Release if so, and return to start of loop to wait
            else:
                current_data = self.data.get_next(iterate=True)
                self.ctrl.queueSemaphore.acquire()  # Check if the queue is unused
                for t in self.tracks:
                    for note in t.generate_notes(current_data):
                        self.notes.put_nowait(note)
                        note_nbr += 1  # We append a list of notes to queue, automatically sorted by tfactor
                self.ctrl.queueSemaphore.release()  # Release queue
                self.ctrl.emptySemaphore.release(n=max_note_nbr-note_nbr) # If not all rows become note, release empty accordingly
                self.ctrl.fullSemaphore.release(n=note_nbr)  # Inform consumer that queue is not empty
            #print("loop released with {}, {}".format(max_note_nbr, note_nbr))
            #time.sleep(self.timeSettings.timeBuffer / 1000)  # Waiting a bit to not overpopulate the queue. Necessary?
            if (self.data.get_next().empty):  # If we have no more data, we are at the end of the music
                self.ctrl.playing = False

    def get_absolute_note_timing(self, tfactor):
        return int(tfactor * self.timeSettings.musicDuration * 1000)

    def add_track(self, track, generate_view=False):
        #with self.ctrl.trackSemaphore:
        self.tracks.append(track)
        if generate_view:
            self.sonification_view.add_track(track)

    def remove_track(self, track):
        #with self.ctrl.trackSemaphore:
        self.tracks.remove(track)
        self.sonification_view.remove_track(track)
