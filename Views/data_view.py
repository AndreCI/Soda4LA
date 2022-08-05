from tkinter import ttk, Toplevel, Button, Label
from tkinter.ttk import Frame, Combobox

from Utils.constants import DEFAULT_PADDING, TFRAME_STYLE, DEFAULT_PADY, DEFAULT_PADX
from Utils.tktable_table import Table


class DataView(Toplevel):
    """
    View to display and interact with user selected data.
    """

    def __init__(self, ctrl, model, **kwargs):
        Toplevel.__init__(self, **kwargs)
        #Ctrl and model
        self.ctrl = ctrl
        self.model = model

        #View data

        #View setup
        self.table = Table(self, data=self.model.get_first_and_last().to_dict('records'))

        self.infoFrame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.timestampLabel = Label(self.infoFrame, text="timestamp column: undefined")
        self.timestampAssignButton = Button(self.infoFrame, text="Assign", command=self.assign_col)

        self.exit_frame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.validateButton = Button(self.exit_frame, text="Validate", command=self.ctrl.validate)
        self.cancelButton = Button(self.exit_frame, text="Cancel", command=self.destroy)

        self.setup_widgets()

    def setup_widgets(self):
        self.table.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

        #INFO FRAME
        self.infoFrame.grid(column=0, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.timestampLabel.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.timestampAssignButton.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        #END INFO FRAME

        #EXIT FRAME
        self.exit_frame.grid(column=0, row=3, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.validateButton.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.cancelButton.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        #END EXIT FRAME

    def assign_col(self):
        if(self.table.selected_cell != None):
            self.timestampLabel.config(text=("timestamp column:{}").format(self.table.headers[self.table.selected_cell._pos[0]]))

    def destroy(self) -> None:
        self.ctrl.remove_window()
        super().destroy()