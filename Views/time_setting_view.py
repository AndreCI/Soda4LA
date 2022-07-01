from tkinter import ttk


class TimeSettingView(ttk.Frame):
    '''
    Presents options relative to time to the user, enabling them to configure time settings
    Future
    '''

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.create_widgets()
        self.setup_widgets()

    def create_widgets(self):
        pass

    def setup_widgets(self):
        pass

    def setup_controller(self, controller):
        pass
