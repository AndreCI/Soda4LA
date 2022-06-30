#!/usr/bin/env python3
import struct
import time
import fluidsynth
from ctypes import *

from app_setup import SF_Chemclarinet, SF_Warmlead, SF_Default, SF_Soprano

seqduration = 1000


def schedule_next_callback2():
    callbackdate = int(now + seqduration)
    sequencer.timer(callbackdate, dest=mySeqID2)


def schedule_next_callback():
    # I want to be called back before the end of the next sequence
    callbackdate = int(now + seqduration)
    sequencer.timer(callbackdate, dest=mySeqID)


def schedule_next_sequence2():
    note_duration = int(seqduration / 16)
    note_velocity = 80
    sequencer.note(int(now + seqduration * 1 / 4), 0, 30, duration=note_duration, velocity=note_velocity,
                   dest=synthSeqID)
    sequencer.note(int(now + seqduration * 2 / 2), 0, 65, duration=note_duration, velocity=note_velocity,
                   dest=synthSeqID)
    sequencer.note(int(now + seqduration * 3 / 4), 0, 30, duration=note_duration, velocity=note_velocity,
                   dest=synthSeqID)
    sequencer.note(int(now + seqduration * 4 / 4), 0, 65, duration=note_duration, velocity=note_velocity,
                   dest=synthSeqID)
    schedule_next_callback2()

def schedule_next_sequence():
    global now
    # the sequence to play
    # the beat : 2 beats per sequence
    note_duration = int(seqduration/16)
    note_velocity = 80
    sequencer.note(int(now + seqduration * 1 / 4), 0, 60, duration=note_duration, velocity=note_velocity, dest=synthSeqID)
    sequencer.note(int(now + seqduration * 2 / 4), 0, 65, duration=note_duration, velocity=note_velocity, dest=synthSeqID)
    sequencer.note(int(now + seqduration * 3 / 4), 0, 60, duration=note_duration, velocity=note_velocity, dest=synthSeqID)
    sequencer.note(int(now + seqduration * 4 / 4), 0, 65, duration=note_duration, velocity=note_velocity, dest=synthSeqID)
    # melody
    sequencer.note(int(now + seqduration * 1 / 10), 1, 45, duration=250, velocity=int(127 * 2 / 3), dest=synthSeqID)
    sequencer.note(int(now + seqduration * 4 / 10), 1, 50, duration=50, velocity=int(127 * 2 / 3), dest=synthSeqID)
    sequencer.note(int(now + seqduration * 8 / 10), 1, 55, duration=200, velocity=int(127 * 3 / 3), dest=synthSeqID)
    #sequencer.note(int(now + seqduration * 8 / 10), 1, 55, duration=200, velocity=int(127 * 3 / 3), dest=synthSeqID)
    #sequencer.note(int(now + seqduration * 8 / 10), 1, 55, duration=200, velocity=int(127 * 3 / 3), dest=synthSeqID)
    # so that we are called back early enough to schedule the next sequence
    schedule_next_callback()

    now = now + seqduration


def seq_callback2(time, event, seq, data):
    print(time)
    schedule_next_sequence2()

def seq_callback(time, event, seq, data):
    print(time)
    print(data)
    print(seq)
    print(event)
    print('------')
    schedule_next_sequence()


if __name__ == "__main__":

    global sequencer, fs, mySeqID, mySeqID2, synthSeqID, now
    fs = fluidsynth.Synth()
    fs.start()
    # you might have to use other drivers:
    # fs.start(driver="alsa", midi_driver="alsa_seq")

    sfid = fs.sfload(SF_Default)
    sfid2 = fs.sfload(SF_Soprano)
    fs.program_select(0, sfid, 0, 0)
    fs.program_select(1, sfid2, 0, 0)  # use the same program for channel 2 for cheapness

    sequencer = fluidsynth.Sequencer()
    now = sequencer.get_tick()
    synthSeqID = sequencer.register_fluidsynth(fs)
    mySeqID = sequencer.register_client("mycallback", seq_callback)
    mySeqID2 = sequencer.register_client("mycallback", seq_callback2)
    schedule_next_sequence()
    schedule_next_sequence2()

    time.sleep(20)

    sequencer.delete()
    fs.delete()