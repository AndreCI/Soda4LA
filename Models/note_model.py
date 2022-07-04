from collections import namedtuple

Note = namedtuple('Note', ['value', 'velocity', 'duration'])
CNote = namedtuple('CNote', ['channel', 'value', 'velocity', 'duration'])
TNote = namedtuple('TNote', ['tfactor', 'channel', 'value', 'velocity', 'duration'])


def CNote_to_TNote(note, tfactor):
    return TNote(tfactor=tfactor, channel=note.channel, value=note.value, velocity=note.velocity, duration=note.duration)


def Note_to_TNote(note, tfactor, channel):
    return TNote(tfactor=tfactor, channel=channel, value=note.value, velocity=note.velocity, duration=note.duration)
