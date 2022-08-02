import fluidsynth # The view should not import fluidsynth since this will be used in Music_model only
from Utils.constants import BUFFER_TIME_LENGTH

# import Music_controller here
## kindly find the implementation of the Producer-Consumer in Music_Model

class MusicView:
    """
    Wrapper for fluidsynth and its sequencer, so that music can be "viewed" i.e. listen to.
    """

    def __init__(self, model):
        self.model = model
        self.synth = fluidsynth.Synth()
        self.sequencer = fluidsynth.Sequencer()
        self.registeredSynth = self.sequencer.register_fluidsynth(self.synth) # kindly explain this line
        self.seqIds = self.sequencer.register_client("callback", self.wrap_snc)  # I don't really understand wrap_snc and why we call it here.
        self.batch_starting_time = None # timestamp updated regulary by music_view
        self.next_batch_notes = [] # current notes to consumed to the sequencer
        self.buffer_notes = [] # next batch of notes to be comsumed the sequencer

        # Start the synth so its ready to play notes
        # Use the line below if for MS Windows driver
        # self.synth.start()
        self.synth.start(driver="alsa")
        # you might have to use other drivers:
        # fs.start(driver="alsa", midi_driver="alsa_seq")

    def play(self):
        # Upon hitting play, register all track and soundfonts
        for track in self.model.tracks:
            sfid = self.synth.sfload(track.soundfont) # Load the soundfont
            self.synth.program_select(track.id, sfid, 0, 0) # Assign soundfont to a channel
        self.batch_starting_time = self.sequencer.get_tick() # Get starting time
        self.schedule_next_sequence() # start the music

    def pause(self):

        NotImplementedError()

    def stop(self):
        self.synth.system_reset()

    def schedule_next_sequence(self):
        """
        Sends the next batch of notes to the sequencer, then schedule the next callback and update self.batch_starting_time
        This is called every BUFFER_TIME_LENGTH by schedule_next_sequence
        """

        # Below is unfinished code
        # TODO: better implement the producer-consumer pattern between music_nodel (producer) and music_view (consumer)
        # see https://dzone.com/articles/producer-consumer-design
        # https://en.wikipedia.org/wiki/Producer%E2%80%93consumer_problem

        # TODO: iterate over the buffer and stock notes into self.next_batch_notes IF they should be played during the
        # next BUFFER_TIME_LENGTH. compare tfactors?

        self.buffer_notes.extend(self.model.notes) # TODO Should only add notes that are not already in the buffer.
        # Notes should be removed from self.model.notes upon extending buffer_notes
        for note in self.buffer_notes:
            if note.tfactor: # TODO: if the note should be played during the next time window (BUFFER_TIME_LENGTH), then add it to the list and remove it from the buffer
                self.next_batch_notes.append(note)
                self.buffer_notes.remove(note)

        for note in self.next_batch_notes:
            # TODO timing of notes is wrong
            # use absolute = True rather than cumulative time?
            # See https://github.com/nwhitehead/pyfluidsynth#using-the-sequencer
            # Maybe it is better to do time=int(self.batch_starting_time + BUFFER_TIME_LENGTH) * notes.tfactor or something similar
            self.sequencer.note(time=int(self.batch_starting_time + BUFFER_TIME_LENGTH * note.tfactor),
                                channel=note.channel, key=note.value, duration=note.duration, velocity=note.velocity,
                                dest=self.registeredSynth)
        self.next_batch_notes = [] #Reset the notes to send to the sequencer
        self.schedule_next_callback() #Prepare the next callback
        self.batch_starting_time += BUFFER_TIME_LENGTH #for the next batch, this can be used as the starting time

    def schedule_next_callback(self):
        """
        Needs to be called before the end of the next sequence.
        Planify the future callback at the end of the buffer time
        """
        callbackdate = int(self.batch_starting_time + BUFFER_TIME_LENGTH)
        self.sequencer.timer(callbackdate, dest=self.seqIds)

    def wrap_snc(self, time, event, seq, data):
        """
        Wrapper with the right signature for schedule_next_callback
        :param time: irrelevant
        :param event: irrelevant
        :param seq: irrelevant
        :param data: irrelevant

                                                                ######## Why are they all  irrelevant ?????
        """
        self.schedule_next_sequence()

