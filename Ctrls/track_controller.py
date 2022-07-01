from Ctrls.parameter_encoding_controller import ParameterEncodingCtrl
from Models.Track import Track
from Utils.constants import ENCODING_OPTIONS


#TODO move data to model object
class TrackCtrl():
    """
    Controller for a track. each track have its own ctrl and its own views.
    """

    def __init__(self, sonification_ctrl):
        self.sonification_ctrl = sonification_ctrl
        self.track = Track()
        self.midi_view = None
        self.config_view = None
        self.muted = False
        self.encoding_windows = {}
        for k in ENCODING_OPTIONS:
            self.encoding_windows[k] = ParameterEncodingCtrl(var=k)

    def setup(self, config_view, midi_view):
        self.config_view = config_view
        self.midi_view = midi_view
        self.change_gain(100)

    def change_gain(self, gain):
        self.local_gain = gain
        if (self.midi_view.local_gain_slider.get() != gain):
            self.midi_view.local_gain_slider.set(gain)
        if (self.config_view.local_gain_slider.get() != gain):
            self.config_view.local_gain_slider.set(gain)

    def mute_track(self):
        self.muted = not self.muted

    def remove(self):
        for winctrl in self.encoding_windows.values():
            winctrl.destroy()
        self.sonification_ctrl.remove_track(self)

    def open_mapping(self, var):
        self.encoding_windows[var].show_window()
