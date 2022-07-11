import threading
import time

from Ctrls.MIDI_controller import MIDICtrl
from Ctrls.sequencer_controller import SeqCtrl
from Models.note_model import *
from Utils.constants import *
from Utils.sound_setup import *


def thread_adding(seq, mctrl):
    i = 0
    while (i < MAX_SAMPLE):
        seq.setup_notes(mctrl.process_next_notes(i, i + SAMPLE_PER_TIME_LENGTH))
        i += SAMPLE_PER_TIME_LENGTH
        time.sleep(BUFFER_TIME_LENGTH)
        mctrl.duration -= SAMPLE_PER_TIME_LENGTH


if __name__ == "__main__":
    soundsetup = [
        {"soundfont": SF_Default, "channel": 0},
        {"soundfont": SF_Jazzguitar, "channel": 1},
        {"soundfont": SF_Cleanguitar, "channel": 2}
    ]
    seq = SeqCtrl(soundsetup, TOTAL_DURATION)
    mctrl = MIDICtrl()
    t_adding = threading.Thread(target=thread_adding, args=(seq, mctrl,), daemon=True)
    t_adding.start()
    seq.start()
    print("Starting")
    time.sleep(5)
    # for k in VALUE_encoding.keys():
    # app_setup.VALUE_encoding[k] = [100, 2]
    time.sleep(1000)


