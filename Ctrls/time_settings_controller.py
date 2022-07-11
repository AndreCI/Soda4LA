from Views.time_settings_view import TimeSettingsView


class TimeSettingsCtrl():

    """
    Ctrl for the time settings model
    """
    def __init__(self, model):
        self.model = model

    def validate(self):
        self.model.set_type(self.model.tsView.selected.get())

        self.model.tsView.destroy()

    def show_window(self):
        if (self.model.tsView == None):
            self.model.tsView = TimeSettingsView(self, self.model)
        self.model.tsView.focus_set()

    def destroy(self):
        if (self.model.tsView != None):
            self.model.tsView.destroy()

    def remove_window(self):
        self.model.tsView = None
