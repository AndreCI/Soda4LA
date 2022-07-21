from Models.data_model import Data
from Views.parameter_encoding_view import ParameterEncodingView


class ParameterEncodingCtrl:
    """
    Controller for the encoding view
    """

    def __init__(self, model):
        #Model
        self.model = model

    def assign_main_var(self, main_var):
        self.model.set_main_var(main_var)

    def show_window(self):
        if (self.model.peView == None):
            self.model.peView = ParameterEncodingView(self, self.model)
        self.model.peView.focus_set()

    def validate(self):
        variable = []
        values = []
        for var, val in zip(self.model.peView.variableList, self.model.peView.valueList):
            variable.append(var.cget("text"))
            values.append(val.get())
        self.model.assign_encoding(variable, values)

        self.model.filter.assign(self.model.peView.filterEntry.get())
        self.model.peView.destroy()

    def destroy(self):
        if (self.model.peView != None):
            self.model.peView.destroy()

    def remove_window(self):
        self.model.peView = None
