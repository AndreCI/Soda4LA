from Ctrls.data_controller import DataCtrl
from Views.parameter_encoding_view import ParameterEncodingView


class ParameterEncodingCtrl:
    """
    Controller for the encoding view
    """

    def __init__(self, model):
        #Model
        self.model = model

    def assign_main_var(self, main_var):
        self.model.main_var = main_var

    def show_window(self):
        if (self.model.pe_view == None):
            self.model.pe_view = ParameterEncodingView(self, self.model)
        self.model.pe_view.focus_set()

    def validate(self):
        self.model.pe_view.destroy()

    def destroy(self):
        if (self.model.pe_view != None):
            self.model.pe_view.destroy()

    def remove_window(self):
        self.model.pe_view = None
