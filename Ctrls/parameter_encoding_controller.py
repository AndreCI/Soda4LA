from Ctrls.data_controller import DataCtrl
from Views.parameter_encoding_view import ParameterEncodingView


class ParameterEncodingCtrl:
    """
    Controller for the encoding view
    """

    def __init__(self, var):
        self.db = DataCtrl()
        self.var = var
        self.view = None
        self.selectedVar = None

    def get_variables_instances(self):
        return self.db.get_variables_instances(self.selectedVar)

    def show_window(self):
        if (self.view == None):
            self.view = ParameterEncodingView(self)
        self.view.focus_set()

    def validate(self):
        self.view.destroy()

    def destroy(self):
        if (self.view != None):
            self.view.destroy()

    def remove_window(self):
        self.view = None
