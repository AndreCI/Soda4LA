from tkinter import ttk


class TemplateView(ttk.Frame):
    """

    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        #Ctrl and model

        #View data

        #View setup
        self.create_widgets()
        self.setup_widgets()

    def create_widgets(self):
        pass

    def setup_widgets(self):
        pass

    def setup_controller(self, controller):
        pass
