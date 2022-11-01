class DataCtrl:
    """
    Controller for the data view
    """

    def __init__(self, model):
        # Model
        self.model = model

    def validate(self):
        self.model.date_column = self.model.view.selectedCandidate
        self.model.assign_timestamps()
        self.model.view.destroy()
