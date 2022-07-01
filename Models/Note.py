from collections import namedtuple

Note = namedtuple('Note', ['key', 'velocity', 'duration'])
CNote = namedtuple('CNote', ['channel', 'key', 'velocity', 'duration'])
TNote = namedtuple('TNote', ['tfactor', 'channel', 'key', 'velocity', 'duration'])


def CNote_to_TNote(note, tfactor):
    return TNote(tfactor=tfactor, channel=note.channel, key=note.var, velocity=note.velocity, duration=note.duration)


def Note_to_TNote(note, tfactor, channel):
    return TNote(tfactor=tfactor, channel=channel, key=note.var, velocity=note.velocity, duration=note.duration)
