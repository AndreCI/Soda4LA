from Models.note_model import note_to_int, int_to_note
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

    def setDefaultValue(self, value):
        if value == "":
            return
        if (self.model.encoded_var == "value"):
            if value.isnumeric():
                try:
                    v = note_to_int(int_to_note(int(value)), int(self.model.octave))
                    self.model.defaultValue = v
                except ValueError:
                    print("Issue with value in setDefault-value {}".format(value))
            else:
                try:
                    v = note_to_int(str(value).upper(), int(self.model.octave))
                    self.model.defaultValue = v
                except ValueError:
                    print("Issue with value in setDefault-value-nonnum {}".format(value))
        elif value.isnumeric():
            self.model.defaultValue = int(value)

    def resetValue(self, variable):
        self.model.handpickEncoding.pop(variable, None)

    def setValue(self, value, variable):
        if (self.model.encoded_var == "value"):
            if value.isnumeric():
                try:
                    v = note_to_int(int_to_note(int(value)), int(self.model.octave))
                    self.model.handpickEncoding[variable] = v
                except ValueError:
                    pass
            else:
                try:
                    v = note_to_int(str(value).upper(), int(self.model.octave))
                    self.model.handpickEncoding[variable] = v
                except ValueError:
                    pass
        elif value.isnumeric():
            self.model.handpickEncoding[variable] = int(value)

    def validate(self):
        print("NONONO")
        self.model.handpicked = self.model.peView.handpicked_mode
        if self.model.handpicked:
            variable = []
            values = []
            for v in self.model.peView.variables:
                variable.append(v["variable"])
                values.append(v["value"].get())
            self.model.assign_handpicked_encoding(variable, values, self.model.peView.octaveEntryVar.get())
            self.model.filter.assign_quali_table([v["variable"] for v in self.model.peView.variables if v["checked"].get()==1])
        else:
            self.model.assign_function_encoding(function=self.model.peView.selectFunctionCB.get(), min_val=self.model.peView.fMinVar.get(), max_val=self.model.peView.fMaxVar.get())
            self.model.filter.assign(self.model.peView.filterEntry.get())
        self.model.peView.destroy()

    def destroy(self):
        if (self.model.peView != None):
            self.model.peView.destroy()

    def remove_window(self):
        self.model.peView = None
