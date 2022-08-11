import time
from tkinter.constants import DISABLED, NORMAL

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
        # Other data
        self.sonification_view = None
        self.playing = False  # True if the music has started, regardless of wheter its paused. False when the music is stopped or ended.
        self.paused = False
        self.queueSemaphore = ISemaphore()  # Could be seomething else ig
        self.trackSemaphore = threading.Lock()  # Could be seomething else ig
        self.emptySemaphore = IBoundedSemaphore(model.QUEUE_CAPACITY)
        self.fullSemaphore = IBoundedSemaphore(model.QUEUE_CAPACITY)
        self.fullSemaphore.acquire(n=model.QUEUE_CAPACITY)  # Set semaphore to 0
        self.playingEvent = threading.Event()
        self.stoppedEvent = threading.Event()
        self.pausedEvent = threading.Event()
        # Model
        self.model = model  # Music model
        self.view = MusicView(model, self)
        self.datas = Data.getInstance()

    def create_track(self):
        """
        Create a track and adds it to the model
        """
        prev_track_nbr = len(self.model.tracks)
        t = Track(self.model)
        threading.Thread(target=self.model.add_track, args=[t], daemon=True).start()
       # if prev_track_nbr == 0 and len(self.model.tracks) == 1:
       #     self.sonification_view.playButton.config(state=NORMAL)

    def remove_track(self, track: Track):
        """
        Remove a track from the model
        :param track: a Track model
        """
        threading.Thread(target=self.model.remove_track, args=[track], daemon=True).start()
       # if len(self.model.tracks) == 0:
       #     self.sonification_view.playButton.config(state=DISABLED)

    def play(self):
        """
        Start a thread via music model to produce notes for the music view, then start the sequencer
        """
        self.sonification_view.playButton.config(state=DISABLED)
        self.sonification_view.pauseButton.config(state=NORMAL)
        self.sonification_view.stopButton.config(state=NORMAL)

        self.load_soundfonts()
        self.view.save_play_time()
        self.playing = True
        self.paused = False
        self.playingEvent.set()
        self.pausedEvent.set()
        self.stoppedEvent.clear()

    def pause(self):
        self.sonification_view.playButton.config(state=NORMAL)
        self.sonification_view.pauseButton.config(state=DISABLED)
        self.view.save_pause_time()
        self.paused = True
        self.playingEvent.clear()
        self.pausedEvent.clear()

    def stop(self):
        self.sonification_view.pauseButton.config(state=DISABLED)
        self.sonification_view.stopButton.config(state=DISABLED)
        self.sonification_view.playButton.config(state=NORMAL)

        print("Stopping at {} with {} notes in queue . empty:{}/{}, full:{}/{}, mutex:{}".format(
            self.view.sequencer.get_tick(), self.model.notes.qsize(),
            self.emptySemaphore._value,
            self.emptySemaphore._initial_value,
            self.fullSemaphore._value,
            self.fullSemaphore._initial_value,
            self.queueSemaphore._value))
        self.view.synth.system_reset()  # Reset synth to prevent future note from being played
        self.playingEvent.clear()  # Send stop event
        self.stoppedEvent.set()
        # Update bools
        self.playing = False
        self.paused = False
        # Update data
        self.datas.reset_playing_index()
        # Reset semaphores
        # self.emptySemaphore.release(n=len(self.model.notes))
        # self.fullSemaphore.acquire(n=len(self.model.notes))
        # Reset queue
        while (not self.model.notes.empty()):
            self.emptySemaphore.release()
            self.fullSemaphore.acquire()
            self.model.notes.get_nowait()
        # self.model.notes.clear()
        time.sleep(0.1)
        print("semaphore: {}/{}, {}/{}, {}".format(self.emptySemaphore._value,
                                                   self.emptySemaphore._initial_value,
                                                   self.fullSemaphore._value,
                                                   self.fullSemaphore._initial_value,
                                                   self.queueSemaphore._value))

    def change_queue_size(self, size):
        self.emptySemaphore.update_size(size, True)
        self.fullSemaphore.update_size(size)

    def open_time_settings(self):
        self.model.timeSettings.ctrl.show_window()

    def change_gain(self, track, value):
        self.view.synth.cc(track, 7, int(value * 1.27))  # 7 volume command, accepting value between 1-127

    def load_soundfonts(self):
        """
        Assign soundfonts to channel inside fluidsynth.
        """
        # Upon hitting play, register all track and soundfonts.
        for track in self.model.tracks:
            soundfont_fid = self.view.synth.sfload(track.soundfont)  # Load the soundfont
            self.view.synth.program_select(track.id, soundfont_fid, 0, 0)  # Assign soundfont to a channel
