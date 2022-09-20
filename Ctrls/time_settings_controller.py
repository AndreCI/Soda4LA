import math
import threading

from Utils.constants import BATCH_NBR_PLANNED
from Utils.utils import is_int
from Views.time_settings_view import TimeSettingsView


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

    def validate(self):
        """
        Validate time settings entered by user and update models accordingly
        """

        if not (is_int(self.model.tsView.batchSizeValue.get()) and
                is_int(self.model.tsView.musicLengthValue.get()) and
                is_int(self.model.tsView.bufferSizeValue.get())):
            return
        size = self.model.tsView.batchSizeValue.get()
        threading.Thread(target=self.change_batch_size, args=[size], daemon=True).start()

        self.model.musicDuration = int(self.model.tsView.musicLengthValue.get())
        self.model.timeBuffer = self.model.tsView.bufferSizeValue.get()
        self.model.set_type(self.model.tsView.selectedTimeType.get())
        self.model.autoload = self.model.tsView.autoloadVar.get() == 1
        self.model.autoloadDataPath = self.model.data.path

        self.write_to_ini()
        self.model.tsView.destroy()

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

    def show_window(self):
        if (self.model.tsView == None):
            self.model.tsView = TimeSettingsView(self, self.model)
        self.model.tsView.focus_set()

    def destroy(self):
        if (self.model.tsView != None):
            self.model.tsView.destroy()

    def remove_window(self):
        self.model.tsView = None
