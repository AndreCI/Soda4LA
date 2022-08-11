import math
import threading

from Views.time_settings_view import TimeSettingsView


class TimeSettingsCtrl():

    """
    Ctrl for the time settings model
    """
    def __init__(self, model):
        self.model = model #TimeSettings Model

    def change_batch_size(self, size):
        if self.model.music.ctrl.playing:
            self.model.music.ctrl.stoppedEvent.wait()
        self.model.batchSize = size
        self.model.data.batch_size = math.ceil(size / 2)
        self.model.music.ctrl.change_queue_size(size)

    def validate(self):
        """
        Validate time settings entered by user and update models accordingly
        """
        size = self.model.tsView.batchSizeValue.get()
        threading.Thread(target=self.change_batch_size, args=[size], daemon=True).start()

        self.model.musicDuration = self.model.tsView.musicLengthValue.get()
        self.model.timeBuffer = self.model.tsView.bufferSizeValue.get()
        self.model.set_type(self.model.tsView.selectedTimeType.get())

        self.model.tsView.destroy()

    def show_window(self):
        if (self.model.tsView == None):
            self.model.tsView = TimeSettingsView(self, self.model)
        self.model.tsView.focus_set()

    def destroy(self):
        if (self.model.tsView != None):
            self.model.tsView.destroy()

    def remove_window(self):
        self.model.tsView = None
