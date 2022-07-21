import fluidsynth

from Models.track_model import Track
from Utils.sound_setup import SAMPLE_PER_TIME_LENGTH


class MusicCtrl():
    """
    Controller for final music model. <=> sonification ctrl
    """

    def __init__(self, model):
        #Model
        self.model = model #Music model

        #Other data
        self.synth = fluidsynth.Synth()
        self.synthIds = []
        self.sequencer = fluidsynth.Sequencer()
        self.registeredSynth = self.sequencer.register_fluidsynth(self.synth)
        self.now = None
        self.buffer_time_length = 2000
        self.next_notes = []
        self.buffer_notes = []
        self.seqIds = self.sequencer.register_client("callback", self.sequencer_callback)


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

    #TODO
    def play(self):
        self.now = self.sequencer.get_tick()
        self.schedule_next_sequence()
        # Use the line below if for MS Windows driver
        #self.synth.start()
        self.synth.start(driver="alsa")
        # you might have to use other drivers:
        # fs.start(driver="alsa", midi_driver="alsa_seq")

    def pause(self):
        pass

    def stop(self):
        pass

    def generate(self):
        self.model.generate(cls=self.model)
        for track in self.model.tracks:
            sfid = self.synth.sfload(track.soundfont)
            self.synthIds.append(sfid)
            self.synth.program_select(track.id, sfid, 0, 0)
        self.buffer_notes.extend(self.model.tracks[0].notes) #TODO proper and not just the first track

    def schedule_next_sequence(self):
        self.next_notes = self.buffer_notes[:SAMPLE_PER_TIME_LENGTH]
        self.buffer_notes = self.buffer_notes[SAMPLE_PER_TIME_LENGTH:]
        for note in self.next_notes:
            print(note)
            # TODO user absolute = True rather than cumulative?
            self.sequencer.note(int(self.now + self.buffer_time_length * note.tfactor),
                                channel=note.channel, key=note.value, duration=note.duration, velocity=note.velocity,
                                dest=self.registeredSynth)
        self.next_notes = []
        self.schedule_next_callback()
        self.now += self.buffer_time_length

    def schedule_next_callback(self):
        # I want to be called back before the end of the next sequence
        callbackdate = int(self.now + self.buffer_time_length)
        self.sequencer.timer(callbackdate, dest=self.seqIds)

    def sequencer_callback(self, time, event, seq, data):
        self.schedule_next_sequence()

    def open_time_settings(self):
        self.model.timeSettings.ctrl.show_window()