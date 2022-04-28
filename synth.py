import fluidsynth
import time

from app_setup import SOUNDFONT1, SOUNDFONT2


class FluidSynth(object):

    def __init__(self, track=0, soundfont=None, *a, **k):
        super(FluidSynth, *a, **k)
        self._soundfont = soundfont if soundfont is not None else SOUNDFONT2
        self.track = track

    def load_misc(self):

        self.fs = fluidsynth.Synth()
        self.fs.start()

        self.sfid = self.fs.sfload(self._soundfont)
        self.fs.program_select(self.track, self.sfid, 0, 0)

    def play_note_loaded(self, note):
        self.fs.noteon(self.track, note.value, note.velocity)
        time.sleep(note.duration)

        self.fs.noteoff(self.track, note.value)
        time.sleep(0.1)

    def play_note_legacy(self, note):
        fs = fluidsynth.Synth()
        fs.start()

        sfid = fs.sfload(self._soundfont)
        fs.program_select(0, sfid, 0, 0)

        fs.noteon(0, note.value, note.velocity)
        time.sleep(note.duration)

        fs.noteoff(0, note.value)
        time.sleep(0.1)

        fs.delete()


def test_playing():
    fs = fluidsynth.Synth()
    fs.start()

    sfid = fs.sfload("FluidR3_GM2-2.SF2")
    fs.program_select(0, sfid, 0, 0)

    fs.noteon(0, 60, 30)
    fs.noteon(0, 67, 30)
    fs.noteon(0, 76, 30)
    time.sleep(1.0)

    fs.noteoff(0, 60)
    fs.noteoff(0, 67)
    fs.noteoff(0, 76)
    time.sleep(1.0)

    fs.delete()


def test_returning_data():
    fs = fluidsynth.Synth()
    sfid = fs.sfload("FluidR3_GM2-2.SF2")
    fs.program_select(0, sfid, 0, 0)

    fs.noteon(0, 60, 30)
    fs.noteon(0, 67, 30)
    fs.noteon(0, 76, 30)
    time.sleep(1.0)

    fs.noteoff(0, 60)
    fs.noteoff(0, 67)
    fs.noteoff(0, 76)
    time.sleep(1.0)

    samples = fs.get_samples(1024)
    fs.delete()
    return fluidsynth.raw_audio_string(samples)


if __name__ == '__main__':
    test_playing()
