import time

import fluidsynth

from Models.note_model import TNote
from Utils.constants import SF_Default
from Utils.sound_setup import SAMPLE_PER_TIME_LENGTH


#TODO separate ctrl and model. should be a model?
class SeqCtrl(object):
    """
    Wrapper for fluidsynth, notes can be buffered at regular interval using threads and callbacks. can be started and paused.
    """

    def __init__(self, soundfonts, sequence_duration=1000):
        self.synth = fluidsynth.Synth()
        self.seqduration = sequence_duration
        self.soundfonts = soundfonts
        self.synth_ids = []
        self.seq_ids = []
        self.next_notes = []
        self.buffer_notes = []

        # Use the line below if for MS Windows driver
        # self.synth.start()
        self.synth.start(driver="alsa")
        # you might have to use other drivers:
        # fs.start(driver="alsa", midi_driver="alsa_seq")

        for s in soundfonts:
            sfid = self.synth.sfload(s["soundfont"])
            self.synth_ids.append(sfid)
            self.synth.program_select(s["channel"], sfid, 0, 0)

        self.sequencer = fluidsynth.Sequencer()
        self.now = self.sequencer.get_tick()
        self.synthSeq_id = self.sequencer.register_fluidsynth(self.synth)
        # for callback in callbacks:
        self.seq_ids.append(self.sequencer.register_client("callback", self.seq_callback))

    def schedule_next_callback(self):
        # I want to be called back before the end of the next sequence
        callbackdate = int(self.now + self.seqduration)
        self.sequencer.timer(callbackdate, dest=self.seq_ids[0])

    def setup_notes(self, notes):
        self.buffer_notes.extend(notes)

    def add_next_note(self, note):
        self.next_notes.append(note)

    def schedule_next_sequence(self):
        self.next_notes = self.buffer_notes[:SAMPLE_PER_TIME_LENGTH]
        self.buffer_notes = self.buffer_notes[SAMPLE_PER_TIME_LENGTH:]
        for note in self.next_notes:
            print(note)
            #TODO user absolute = True rather than cumulative?
            self.sequencer.note(int(self.now + self.seqduration * note.tfactor),
                                channel=note.channel, key=note.value, duration=note.duration, velocity=note.velocity,
                                dest=self.synthSeq_id)
        self.next_notes = []
        self.schedule_next_callback()
        self.now += self.seqduration

    def seq_callback(self, time, event, seq, data):
        print("New callback")
        self.schedule_next_sequence()

    def start(self):
        self.schedule_next_sequence()

    def __del__(self):
        self.sequencer.delete()
        self.synth.delete()


if __name__ == "__main__":
    seq = SeqCtrl([{"soundfont": SF_Default, "channel": 0}])
    seq.setup_notes([TNote(velocity=60, duration=80, tfactor=1 / 4, key=60)])
    seq.schedule_next_sequence()
    time.sleep(10)
