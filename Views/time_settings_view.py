from tkinter import Toplevel, Button, Listbox, END, Entry, Label, StringVar, Radiobutton, W
from tkinter.ttk import Frame, Combobox

from Utils.constants import DEFAULT_PADDING, TFRAME_STYLE, DEFAULT_PADY, DEFAULT_PADX


class TimeSettingsView(Toplevel):
    '''
    Presents options relative to time to the user, enabling them to configure time settings
    Future
    '''

    def __init__(self, ctrl, model, **kwargs):
        Toplevel.__init__(self, **kwargs)
        # ctrl and model
        self.ctrl = ctrl
        self.model = model

        # View data
        self.title("Time Settings")
        # self.geometry('450x400')

        # setup view
        self.optionsFrame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["TIMESETTINGS"][0])
        self.options = []
        self.selected = StringVar()
        self.selected.set(self.model.type)
        for t in self.model.possible_types:
            self.options.append(Radiobutton(self.optionsFrame, text=t, variable=self.selected, value=t, indicatoron=False))

        self.exitFrame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.validateButton = Button(self.exitFrame, text="Validate", command=self.ctrl.validate)
        self.cancelButton = Button(self.exitFrame, text="Cancel", command=self.destroy)

        self.setup_widgets()

    def setup_widgets(self):
        self.optionsFrame.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        for i, t in enumerate(self.options):
            t.grid(column=0, row=i, pady=0, padx=0)

        self.exitFrame.grid(column=0, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.validateButton.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.cancelButton.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

    def destroy(self) -> None:
        self.ctrl.remove_window()
        super().destroy()

