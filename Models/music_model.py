import time
from collections import deque

import fluidsynth
from Ctrls.music_controller import MusicCtrl
from Models.data_model import Data
from Models.time_settings_model import TimeSettings
from Models.track_model import Track
from Utils.sound_setup import SAMPLE_PER_TIME_LENGTH, MUSIC_TOTAL_DURATION

import platform

from Ctrls.MIDI_controller import MIDICtrl
# Should we add a controller attribute here?
from Utils.constants import BUFFER_TIME_LENGTH

import threading
import queue

# Not really sure about how we implement MCV for Music.
from Views.music_view import MusicView


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
            #Data
            self.gain = 100
            self.muted = False
            #self.notes = queue.PriorityQueue(maxsize=6 * SAMPLE_PER_TIME_LENGTH) # Priority queue ordered by tfactor
            self.notes = deque(maxlen=6*SAMPLE_PER_TIME_LENGTH)
            #Other models
            self.tracks = [] #List of track model created by user
            self.timeSettings = TimeSettings()
            self.data = Data.getInstance()
            self.timeSettings.set_attribute(self.data.first_date, self.data.last_date, self.data.df.shape[0] + 1)

            #Ctrl
            self.ctrl = MusicCtrl(self)

            #Views
            self.sonification_view = None

            #Threads
            self.producer_thread = threading.Thread(target=self.generate, daemon=True)
            self.producer_thread.start()

    def generate(self):
        while True:  # This thread never stops
            print("waiting")
            self.ctrl.playingCV.wait() #wait if we are paused
            print("p w")
            self.ctrl.pausedEvent.wait() #wait if we are paused
            print("paused w")
            #while self.ctrl.playing is False or self.ctrl.paused:
            #    time.sleep(0.1)  # We wait if the music is paused or ended
            #time.sleep(0.5)  # Waiting a bit because it bugs when i dont
            self.ctrl.empty.acquire()
            print("e a")
            self.ctrl.mutex.acquire()
            print("m a")
            for t in self.tracks:
                self.notes.extend(t.generate_notes(self.data.get_next(
                    iterate=True)))  # We append a list of notes to queue, automatically sorted by tfactor
            print("added data with idx {} to notes".format(self.data.index))
            self.ctrl.mutex.release()
            print("m r")
            self.ctrl.full.release()
            print("f r")
            time.sleep(BUFFER_TIME_LENGTH / 2000)  # Waiting a bit to not overpopulate the queue



            #if (self.data.get_next().empty):  # If we have no more data, we are at the end of the music
            #    self.playing = False

    def generate_legacy(self):
        """
        Threaded
        Iterate over the data, generate all the notes for all the tracks, so that they can be played.
        This function is the producer of our producer-consumer design
        """
        while True: #This thread never stops
            while self.ctrl.playing and not self.ctrl.paused and self.data.get_next().empty is False: # We still have data, and its not paused
                self.ctrl.empty.acquire()
                self.ctrl.mutex.acquire()
                print("adding data with idx {} to notes".format(self.data.index))
                for t in self.tracks:
                    #self.notes.put(t.generate_notes(self.data.get_next(iterate=True))) # We append a list of notes to queue, automatically sorted by tfactor
                    self.notes.extend(t.generate_notes(self.data.get_next(iterate=True))) # We append a list of notes to queue, automatically sorted by tfactor
                self.ctrl.mutex.release()
                self.ctrl.full.release()
                time.sleep(BUFFER_TIME_LENGTH/1000) #Waiting a bit to not overpopulate the queue
            time.sleep(0.1) #If we are paused, wait a bit and try again
            if(self.data.get_next().empty): #If we have no more data, we are at the end of the music
                self.playing = False

    def add_track(self, track : Track):
        self.tracks.append(track)
        self.sonification_view.add_track(track)

    def remove_track(self, track : Track):
        self.tracks.remove(track)
        self.sonification_view.remove_track(track)

