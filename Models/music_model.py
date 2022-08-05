import time
import fluidsynth
from Ctrls.music_controller import MusicCtrl
from Models.data_model import Data
from Models.time_settings_model import TimeSettings
from Models.track_model import Track
from Utils.sound_setup import SAMPLE_PER_TIME_LENGTH

import platform

from Ctrls.MIDI_controller import MIDICtrl
# Should we add a controller attribute here?
from Utils.constants import BUFFER_TIME_LENGTH

import threading
import queue

# Not really sure about how we implement MCV for Music.


class Music:
    """
    Model class for music. Music is defined as the end product of the sonification process, regardless of esthetic.
    A music can be played via its music view or displayed via midi view.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        instantiation, unique
        """
        if cls._instance is None:
            cls._instance = super(Music, cls).__new__(cls, *args, **kwargs)
            #Data
            cls.gain = 100
            cls.muted = False
            cls.notes = queue.Queue(maxsize=3*SAMPLE_PER_TIME_LENGTH) # The easiest way for Consumer-Producer design pattern is to have this as a queue

            #Other models
            cls.tracks = [] #List of track model created by user
            cls.timeSettings = TimeSettings()
            cls.data = Data.getInstance()
            cls.timeSettings.set_attribute(cls.data.first_date, cls.data.last_date)

            #Ctrl
            cls.ctrl = MusicCtrl(cls)

            #Views
            cls.sonification_view = None

            #Threads
            cls.producer_thread = threading.Thread(target=cls.generate)
            cls.consumer_thread = threading.Thread(target=cls.synthetize, daemon=True)

        return cls._instance

    def __int__(self):
        # Fluidsynth
        self.synth = fluidsynth.Synth()
        self.sequencer = fluidsynth.Sequencer()
        self.registeredSynth = self.sequencer.register_fluidsynth(self.synth)  # necessary for fluidynth, called as an arg by the sequencer

    def generate(cls):
        """
        Iterate over the data, generate all the notes for all the tracks, so that they can be played.
        This function is the producer of our producer-consumer design
        It produces notes if note.size() < 2*Batch_len
        """
        while cls.data.get_next().empty is False and cls.notes.empty() is True: # We still have sample but queue is empty
            for t in cls.tracks:
                cls.notes.put(t.generate_notes(cls.data.get_next())) # We append a list of notes to queue
                time.sleep(2)

    def play(cls):  # Equivalent of Play in Music controller.
        """
        Start the producer and the consumer threads
        and play the music
        """
        cls.producer_thread.start()
        cls.consumer_thread.start()

    def stop(self):
        self.synth.system_reset()

    def pause(self):
        NotImplementedError()

    def synthetize(self):
        """
            lorem ipsum
        """
        # Upon hitting play, register all track and soundfonts
        for track in self.tracks:
            sfid = self.synth.sfload(track.soundfont)  # Load the soundfont
            self.synth.program_select(track.id, sfid, 0, 0)  # Assign soundfont to a channel
        # ToDO finish the implementation and synthetize the notes in the queue (self.notes)
        for note in self.notes.get(block=False):
            self.sequencer.note(time=note.tfactor,
                                channel=note.channel, key=note.value, duration=note.duration, velocity=note.velocity,
                                dest=self.registeredSynth)

        # Start the synth so its ready to play notes
        if platform.system() == 'Windows':
            # Use the line below if for MS Windows driver
            self.synth.start()
        else:
            self.synth.start(driver="alsa")
            # you might have to use other drivers:
            # fs.start(driver="alsa", midi_driver="alsa_seq")

    def add_track(self, track : Track):
        self.tracks.append(track)
        self.sonification_view.add_track(track)

    def remove_track(self, track : Track):
        self.tracks.remove(track)
        self.sonification_view.remove_track(track)

    def wrap_snc(self, time, event, seq, data):
        """
        Wrapper with the right signature for schedule_next_callback. Arguments are irrelevant but necessary to respect the signature requested by fluidsynth
        :param time: irrelevant - not used
        :param event: irrelevant - not used
        :param seq: irrelevant - not used
        :param data: irrelevant - not used
        """
        self.synthetize()
