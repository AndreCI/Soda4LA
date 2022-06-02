from tkinter import ttk
from Utils.constants import DEFAULT_BGCOLOR, DEFAULT_PADX, DEFAULT_PADY, TFRAME_STYLE


class TemplateView(ttk.Frame):
    """

    """
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
