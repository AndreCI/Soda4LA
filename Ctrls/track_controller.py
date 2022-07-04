from Ctrls.parameter_encoding_controller import ParameterEncodingCtrl
from Utils.constants import ENCODING_OPTIONS


class TrackCtrl():
    """
    Controller for a track. each track have its own ctrl and its own views.
    """

    def __init__(self, model):
        #Model
        self.model = model


    def setup(self, config_view, midi_view):
        self.model.config_view = config_view
        self.model.midi_view = midi_view
        self.change_gain(100)

    def change_gain(self, gain):
        self.model.gain = gain
        if (self.model.midi_view.local_gain_slider.get() != gain):
            self.model.midi_view.local_gain_slider.set(gain)
        if (self.model.config_view.local_gain_slider.get() != gain):
            self.model.config_view.local_gain_slider.set(gain)

    def mute_track(self):
        self.model.muted = not self.model.muted

    def remove(self):
        for pencoding_model in self.model.pencodings:
            pencoding_model.ctrl.destroy()

        self.model.remove()

    def open_encoding(self, encoded_var):
        [x for x in self.model.pencodings if x.encoded_var == encoded_var][0].ctrl.show_window()
