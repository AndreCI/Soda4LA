import itertools
import time
from queue import PriorityQueue

import pandas as pd
from midiutil.MidiFile import MIDIFile

from Ctrls.music_controller import MusicCtrl
from Models import note_model
from Models.data_model import Data
from Models.time_settings_model import TimeSettings
from Models.track_model import Track
from Utils.constants import BATCH_NBR_PLANNED


class Music:
    """
    Model class for music. Music is defined as the end product of the sonification process, regardless of esthetic.
    A music can be played via its music view or displayed via midi view.
    """
    _instance = None
    track_newid = itertools.count()

    def generate_track_id(self):
        id = next(self.track_newid)
        while(str(id) in self.tracks.keys()):
            id = next(self.track_newid)
        return id

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
            self.timescale = 1000  # ticks per seconds
            self.muted = False

            # Other models
            self.tracks = {}  # List of track model created by user
            self.tracks_note = {}

            self.timeSettings = TimeSettings(self)
            self.data = Data.getInstance()
            self.queue_capacity = self.timeSettings.batchPlanned * self.timeSettings.batchSize
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

    def generate_midi(self, filename="output"):

        """
        Generate and populate a midi file based on current parameters and data.
        :param filename:
        :return:
        """
        # setup
        bpm = self.timeSettings.get_bpm()
        self.data.reset_playing_index()
        self.ctrl.setup_general_attribute()
        self.ctrl.load_soundfonts()
        mf = MIDIFile(len(self.tracks), eventtime_is_ticks=False)  # declare midi file
        for key in self.tracks:
            mf.addTrackName(int(key), 0, str(self.tracks[key].id))
            mf.addTempo(int(key), 0, bpm)
        # iterate over data
        while not self.data.get_next().empty:
            current_data = self.data.get_next(iterate=True)
            for t in self.tracks.values():
                for note in t.generate_notes(current_data):
                    mf.addNote(track=t.id, channel=t.id, pitch=note.value,
                               time=note_model.convert_seconds_to_quarter(
                                   float(self.get_absolute_note_timing(note.tfactor)) / self.timescale, bpm),
                               duration=note_model.convert_seconds_to_quarter(float(note.duration) / self.timescale,
                                                                              bpm),
                               volume=note.velocity)
        with open(filename + ".mid", "wb") as outf:
            mf.writeFile(outf)

    def write_fluidsynth_config(self, filename):
        # TODO add more options
        """
        Automatically write a config file for fluidsynth, containg info about soundfonts, gain, etc.
        """
        with open(filename + "-fluidsynth_midi_to_wav.config", "w") as f:
            lines = ["set player.reset-synth 0\n"]  # prevent fluidsynth to override settings
            for t in self.tracks.values():
                lines.append("load \"{}\"\n".format(t.soundfont))  # load soundfonts
            for key in self.tracks:
                lines.append("select {} {} 0 0\n".format(int(key), int(key) + 1))  # assign soundfonts to tracks
            for key in self.tracks:
                lines.append("cc {} 7 {}\n".format(key, self.tracks[key].gain * 1.27))  # update gain
            f.writelines(lines)

    def generate_dataframe(self):
        """Pre compute all notes into a dataframe"""
        t1 = time.perf_counter()
        for track in self.tracks.values():
            evaluated_data = track.filter_batch(self.data.df, False)
            notes = evaluated_data.apply(lambda x: track.build_note2(x), axis=1)
            self.tracks_note[str(track.id)] = notes
        print("done in {} for {} lines".format(time.perf_counter() - t1, len(self.tracks_note["0"])))

    def generate(self): 
        """
        Threaded.
        Produce at regular intervals a note, based on data and tracks configuration and put it into self.notes
        Uses notes as a PriorityQueue, which is concurently used by music_view (consumer) and various semaphores to
        get access. In theory, each row in the dataset can be converted into multiples notes (1 note/track).
        """
        while True:  # This thread never stops
            self.ctrl.playingEvent.wait()  # wait if we are stopped
            self.ctrl.pausedEvent.wait()  # wait if we are paused
            # with self.ctrl.trackSemaphore:
            max_note_nbr = len(self.tracks) * self.data.batch_size  # Acquire queue as if each row will become a note
            note_nbr = 0  # track how many row actually become notes
            self.ctrl.emptySemaphore.acquire(n=max_note_nbr)  # Check if the queue is not full
            # Usually hang on this ^^^
            if not self.ctrl.playing:  # Check if semaphore was acquired while stop was pressed
                self.ctrl.emptySemaphore.release(n=max_note_nbr)  # Release if so, and return to start of loop to wait
            elif(not self.data.get_next().empty):
                current_data = self.data.get_next(iterate=True)  # get the next batch
                self.ctrl.push_data_to_table(current_data)  # display
                self.ctrl.queueSemaphore.acquire()  # Check if the queue is unused - can hang here
                if not self.ctrl.playing:  # if music stopped during acquirement of queueSemaphore, release everything
                    self.ctrl.queueSemaphore.release()
                    self.ctrl.emptySemaphore.release(n=max_note_nbr)
                else:
                    for t in self.tracks.values():
                        for note in t.generate_notes(current_data):
                            self.notes.put_nowait(note)
                            self.ctrl.graphSemaphore.acquire()
                            self.sonification_view.visualisationView.futureNotes.append(note)
                            self.ctrl.graphSemaphore.release()
                            note_nbr += 1  # keep track of how many note are actually generated
                    self.ctrl.queueSemaphore.release()  # Release queue
                    self.ctrl.emptySemaphore.release(
                        n=max_note_nbr - note_nbr)  # If not all rows become note, release empty accordingly
                    self.ctrl.fullSemaphore.release(n=note_nbr)  # Inform consumer that queue is not empty
            else:  # If we have no more data, we are at the end of the music
                print("sleeping...")
                self.ctrl.finished = True
                time.sleep(0.5)

    def get_absolute_note_timing(self, tfactor):
        """
        Compute and return the absolute timing in sec of a tfactor, depending on music duration.
        :param tfactor: a value between 0 and 1
        """
        return int(tfactor * self.timeSettings.get_music_duration() * 1000)

    def add_track(self, track, generate_view=False):
        # with self.ctrl.trackSemaphore:
        self.tracks[str(track.id)] = track
        if generate_view:
            self.sonification_view.trackView.add_track(track)

    def remove_track(self, track : Track) -> None:

        # with self.ctrl.trackSemaphore:
        del self.tracks[str(track.id)]
