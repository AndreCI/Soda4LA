from Views.data_view import DataView
from Views.parameter_encoding_view import ParameterEncodingView


class DataCtrl:
    """
    Controller for the data view
    """

    def __init__(self, model):
        #Model
        self.model = model


    def show_window(self):
        if (self.model.view == None):
            self.model.view = DataView(self, self.model)
        self.model.view.focus_set()

    def validate(self):

        self.model.view.destroy()

    def destroy(self):
        if (self.model.view != None):
            self.model.view.destroy()

    def remove_window(self):
        self.model.view = None
