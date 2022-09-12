from collections import namedtuple

_note_dict = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
TNote = namedtuple('TNote', ['tfactor', 'channel', 'value', 'velocity', 'duration', 'id'])
CNote = namedtuple('CNote', ['channel', 'value', 'velocity', 'duration'])

def CNote_to_TNote(note, tfactor):
    return TNote(tfactor=tfactor, channel=note.channel, value=note.value, velocity=note.velocity, duration=note.duration)


def Note_to_TNote(note, tfactor, channel):
    return TNote(tfactor=tfactor, channel=channel, value=note.value, velocity=note.velocity, duration=note.duration)

def TNote_to_QNote(note, time_ms, track_id, bpm):
    return (track_id, track_id, convert_seconds_to_quarter(time_ms, bpm),
            convert_seconds_to_quarter(note.duration, bpm),
            convert_seconds_to_quarter(note.velocity, bpm))

def is_valid_note(note):
    """Return True if note is in a recognised format. False if not."""
    if note[0] not in _note_dict:
        return False
    for post in note[1:]:
        if post != "b" and post != "#":
            return False
    return True

def note_to_int(note, octave):
    """Convert notes in the form of C, C#, Cb, C##, etc. to an integer in the
    range of 0-11.
    Throw a ValueError exception if the note format is not recognised.
    """
    if is_valid_note(note):
        val = _note_dict[note[0]]
    else:
        raise ValueError("Unknown note format '%s'" % note)

    # Check for '#' and 'b' postfixes
    for post in note[1:]:
        if post == "b":
            val -= 1
        elif post == "#":
            val += 1
    return val % 12 + octave * 12

def int_to_note(note_int, accidentals="#"):
    """Convert integers in the range of 0-11 to notes in the form of C or C#
    or Db.
    Throw a RangeError exception if the note_int is not in the range 0-11.
    If not specified, sharps will be used.
    """
    if note_int not in range(12):
        note_int = note_int % 12
    ns = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    nf = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    if accidentals == "#":
        return ns[note_int]
    elif accidentals == "b":
        return nf[note_int]
    else:
        raise ValueError("'%s' not valid as accidental" % accidentals)


def convert_seconds_to_quarter(time_in_sec, bpm):
    """
    Util function
    :param time_in_sec:
    :param bpm:
    :return:
    """
    quarter_per_second = (bpm/60)
    time_in_quarter = time_in_sec * quarter_per_second
    return time_in_quarter
