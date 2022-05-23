import time
import itertools
from collections import deque

import fluidsynth

from Ctrls.MIDI_controller import MIDICtrl
from app_setup import SF_Chemclarinet, SF_Warmlead, SF_Default

import numpy as np
from pyaudio import PyAudio, paContinue, paInt16

from midi import hz_to_midi, RTNote
from synth import FluidSynth

class StreamProcessor(object):

    FREQS_BUF_SIZE = 11

    def __init__(self):
        self.controller = MIDICtrl()
        self._synth = FluidSynth(track=0, soundfont= SF_Default)
        self.synth3 = fluidsynth.Synth()
        self._synth2 = FluidSynth(track=1, soundfont=SF_Default)
        self._synth.load_misc()
        self._synth2.load_misc()
        seq = fluidsynth.Sequencer()
        self.id1 = seq.register_fluidsynth(self.synth3)
        seq.note_on(time=500, absolute=False, channel=0, key=60, velocity=80, dest=self.id1)
        seq.process(1000)
        time.sleep(1.0)

    def run(self):
        for i in range(10):
            note = self.controller.get_next_note()
            self._synth.play_note_loaded(note)
            note = self.controller.get_next_note()
            self._synth2.play_note_loaded(note)

if __name__ == '__main__':
    stream_proc = StreamProcessor()
    #stream_proc.run()
