import math
import threading

from Utils.constants import BATCH_NBR_PLANNED
from Utils.utils import is_int

class TimeSettingsCtrl():
    """
    Ctrl for the time settings model
    """

    def __init__(self, model):
        self.model = model  # TimeSettings Model

    def change_batch_size(self, size):
        if self.model.music.ctrl.playing:
            self.model.music.ctrl.stoppedEvent.wait()
        self.model.batchSize = size
        self.model.data.batch_size = size
        self.model.music.ctrl.change_queue_size(size * BATCH_NBR_PLANNED)

    def validate(self, batch_size, song_length, note_timing, tempo_idx, autoload):
        """
        Validate time settings entered by user and update models accordingly
        """

        if not (is_int(batch_size) and
                is_int(song_length) and
                is_int(note_timing)):
            return
        threading.Thread(target=self.change_batch_size, args=[int(batch_size)], daemon=True, name="change_batch_size").start()
        self.model.musicDuration = int(song_length)
        self.model.timeBuffer = int(note_timing)
        self.model.set_type(self.model.possible_types[tempo_idx])
        self.model.autoload = autoload
        self.model.autoloadDataPath = self.model.data.path

        self.write_to_ini()

    def write_to_ini(self):
        with open("settings.ini", "w") as settingsFile:
            line = "autoload=" + str(self.model.autoload) + "\n"
            settingsFile.write(line)
            line = "datapath=\"" + str(self.model.autoloadDataPath) + "\"\n"
            settingsFile.write(line)
            line = "timestampcol=\"" + str(self.model.data.date_column) + "\"\n"
            settingsFile.write(line)
            line = "debugverbose=" + str(self.model.debugVerbose) + "\n"
            settingsFile.write(line)

    def open_time_settings(self, view):
        self.model.view = view
        view.model = self.model
        view.update_ui()
        view.show()
