from Views.parameter_mapping_view import ParameterMappingView


class ParameterMappingCtrl:
    def __init__(self, key):
        self.key = key
        self.view = None

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