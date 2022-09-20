from Views.data_view import DataView


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
        self.model.date_column = self.model.view.selectedCandidate
        self.model.assign_timestamps()
        self.model.view.destroy()

    def destroy(self):
        if (self.model.view != None):
            self.model.view.destroy()

    def remove_window(self):
        self.model.view = None
