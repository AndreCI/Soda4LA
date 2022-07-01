from tkinter import ttk


class NoteView(ttk.Frame):
    """
    View of a single note, reprensented as a rectangle on a grid. Each instance must be linked to a specific note
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
