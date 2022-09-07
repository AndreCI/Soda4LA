
from Views.parameter_encoding_view import ParameterEncodingView


class ParameterEncodingCtrl:
    """
    Controller for the encoding view
    """

    def __init__(self, model):
        #Model
        self.model = model

    def assign_main_var(self, main_var):
        self.model.filter.assign_column(main_var)
        self.model.initialized = True

    def show_window(self):
        if (self.model.peView == None):
            self.model.peView = ParameterEncodingView(self, self.model)
        self.model.peView.focus_set()

    def validate(self):
        self.model.handpicked = self.model.peView.handpicked_mode
        variable = []
        values = []
        for v in self.model.peView.variables:
            variable.append(v["variable"])
            values.append(v["value"].get())
        self.model.assign_handpicked_encoding(variable, values, self.model.peView.octaveEntryVar.get())
        self.model.assign_function_encoding(function=self.model.peView.selectFunctionCB.get(), min_val=self.model.peView.fMinVar.get(), max_val=self.model.peView.fMaxVar.get())

        if(self.model.handpicked):
            self.model.filter.assign_quali_table([v["variable"] for v in self.model.peView.variables if v["checked"].get()==1])
        else:
            self.model.filter.assign(self.model.peView.filterEntry.get())
        self.model.peView.destroy()

    def destroy(self):
        if (self.model.peView != None):
            self.model.peView.destroy()

    def remove_window(self):
        self.model.peView = None
