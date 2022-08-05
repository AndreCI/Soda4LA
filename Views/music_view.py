import platform
import threading
import time

import fluidsynth  # The view should not import fluidsynth since this will be used in Music_model only

from Utils.constants import BUFFER_TIME_LENGTH
# import Music_controller here
## kindly find the implementation of the Producer-Consumer in Music_Model
from Utils.sound_setup import MUSIC_TOTAL_DURATION


class MusicView:
    """
    Wrapper for fluidsynth and its sequencer, so that music can be "viewed" i.e. listen to.
    """

    def __init__(self, model, ctrl):
        self.model = model
        self.ctrl = ctrl
        self.synth = fluidsynth.Synth()
        self.sequencer = fluidsynth.Sequencer()
        self.registeredSynth = self.sequencer.register_fluidsynth(
            self.synth)  # necessary for fluidynth, called as an arg by the sequencer
        self.seqIds = self.sequencer.register_client("callback",
                                                     self.wrap_consume)  # necessary for fluidsynth, called by the sequencer with a specific signature
        self.now = None
        self.starting_time = None
        self.pause_start_time = None
        self.consumer_thread = threading.Thread(target=self.consume, daemon=True)
        self.consumer_thread.start()

        # Start the synth so its ready to play notes
        if platform.system() == 'Windows':
            # Use the line below if for MS Windows driver
            self.synth.start()
        else:
            self.synth.start()
            # you might have to use other drivers:
            # fs.start(driver="alsa", midi_driver="alsa_seq")

    def setup_soundfonts(self):
        """
        Assign soundfonts to channel inside fluidsynth.
        """
        # Upon hitting play, register all track and soundfonts. TODO Reset needed?
        for track in self.model.tracks:
            sfid = self.synth.sfload(track.soundfont)  # Load the soundfont
            self.synth.program_select(track.id, sfid, 0, 0)  # Assign soundfont to a channel

    def play(self):
        self.setup_soundfonts()
        if (not self.ctrl.playing):
            self.starting_time = self.sequencer.get_tick()
        if(self.ctrl.paused): #If the model was paused, increment starting time by pause time
            paused_time = self.sequencer.get_tick() - self.pause_start_time
            print(paused_time)
            self.starting_time += paused_time
        print("started playing")

    def pause(self):
        self.pause_start_time = self.sequencer.get_tick()

    def stop(self):
        pass
        #self.synth.system_reset()

    def consume(self):
        idx = 0
        while True: #This thread never stops
            for note in self.model.notes.get(block=True, timeout=60):  # Wait if no block is available
                note_timing_abs = note.tfactor * MUSIC_TOTAL_DURATION * 1000  # sec to ms
                current_time = self.sequencer.get_tick()
                note_timing = int(note_timing_abs - (current_time - self.starting_time)) #relative timing, indicating in how much ms a note should be played
                while (note_timing > BUFFER_TIME_LENGTH): #Check if the current note should be played soon
                    time.sleep(BUFFER_TIME_LENGTH / 1000) #if not, wait a bit
                    current_time = self.sequencer.get_tick()
                    note_timing = int(note_timing_abs - (current_time - self.starting_time))
                print("new note with idx {} scheduled in {}ms (abs: {}ms): {}. {} notes remaining in queue".format(idx,
                                                                                                                   note_timing,
                                                                                                                   note_timing_abs,
                                                                                                                   note,
                                                                                                                   self.model.notes.qsize()))
                self.sequencer.note(absolute=False, time=note_timing, channel=note.channel, key=note.value,
                                    duration=note.duration, velocity=note.velocity, dest=self.registeredSynth)
                idx += 1
                print(self.starting_time)
                while self.ctrl.playing is False or self.ctrl.paused:
                    time.sleep(0.1) #We wait if the music is paused or ended

        #self.now += BUFFER_TIME_LENGTH
        #self.schedule_next_callback()  # Prepare the next callback

    def schedule_next_callback(self):
        # I want to be called back before the end of the next sequence
        callbackdate = int(self.now + BUFFER_TIME_LENGTH)
        self.sequencer.timer(callbackdate, dest=self.seqIds)

    def wrap_consume(self, time, event, seq, data):
        """
        Wrapper with the right signature for schedule_next_callback. Arguments are irrelevant but necessary to respect the signature requested by fluidsynth
        :param time: irrelevant - not used
        :param event: irrelevant - not used
        :param seq: irrelevant - not used
        :param data: irrelevant - not used
        """
        self.consume()
