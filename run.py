import threading
import time

import app_setup
from Ctrls.MIDI_controller import MIDICtrl
from Models.Note import *
from app_setup import *
from Ctrls.sequencer_controller import SeqCtrl

def thread_adding(seq, mctrl):
    i=0
    while(i<MAX_SAMPLE):
        seq.setup_notes(mctrl.process_next_notes(i, i+SAMPLE_PER_DURATION))
        i+= SAMPLE_PER_DURATION
        time.sleep(2)
        mctrl.duration -= 10

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
    for k in VALUE_encoding.keys():
        app_setup.VALUE_encoding[k] = [100, 2]
    time.sleep(1000)

def legacy():
    for i in range(MAX_SAMPLE):
        if(TIMING=="auto"):
            seq.add_next_note(CNote_to_TNote(mctrl.get_next_note(), i*100/seq.seqduration))
        else:
            seq.add_next_note(mctrl.get_next_note())
    time.sleep(1000)