from Ctrls.data_controller import DataCtrl
from Views.parameter_mapping_view import ParameterMappingView


class ParameterEncodingCtrl:
    """
    Controller for the encoding view
    """
    def __init__(self, key):
        self.db = DataCtrl()
        self.key = key
        self.view = None
        self.selectedVar = None

    def get_variables_instances(self):
        return self.db.get_variables_instances(self.selectedVar)

    def show_window(self):
        if(self.view == None):
            self.view = ParameterMappingView(self)
        self.view.focus_set()

    def validate(self):
        self.view.destroy()

    def destroy(self):
        if(self.view != None):
            self.view.destroy()

    def remove_window(self):
        self.view = None