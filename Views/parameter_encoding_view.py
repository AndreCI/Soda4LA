from tkinter import Toplevel, Button, Listbox, END
from tkinter.ttk import Frame, Combobox

from Utils.constants import DEFAULT_PADDING, TFRAME_STYLE, DEFAULT_PADY, DEFAULT_PADX, MOCKUP_VARS


class ParameterEncodingView(Toplevel):
    """"
    View for encoding variables to an encoding. started from track_config_view, and linked to a specific parameter of a note (value, duration, velocity)
    """

    def __init__(self, ctrl, **kwargs):
        Toplevel.__init__(self, **kwargs)
        self.ctrl = ctrl #TODO: should not use ctrl but give it command. Should use model to get data
        self.fmode = False
        self.title("Encoding+ for {}".format(self.ctrl.var))
        self.geometry('450x400')
        self.create_widgets()
        self.setup_widgets()

    def select_variable(self, event):
        self.ctrl.selectedVar = self.selectVarCB.get()
        self.parameterListBox.delete(0, END)
        self.valueListBox.delete(0, END)
        for i, item in enumerate(self.ctrl.get_variables_instances()): #TODO should use model rather than ctrl
            self.parameterListBox.insert(END, item)
            self.valueListBox.insert(END, i)

    def create_widgets(self):
        self.main_frame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.selectVarCB = Combobox(self.main_frame, values=self.ctrl.db.get_variables())
        self.selectVarCB.bind('<<ComboboxSelected>>', self.select_variable)
        self.selectVarCB.current(0)
        self.ctrl.selectedVar = self.selectVarCB.get()
        self.selectFilterButton = Button(self.main_frame, text="Select Filter")
        self.switchModeButton = Button(self.main_frame, text="Function Mode", command=self.switch_mode)

        self.function_frame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.selectFunctionCombobox = Combobox(self.function_frame, values=MOCKUP_VARS)
        self.selectVarCB.current(0)

        self.handpick_frame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.parameterListBox = Listbox(self.handpick_frame)
        self.valueListBox = Listbox(self.handpick_frame)
        for i, item in enumerate(self.ctrl.get_variables_instances()):
            self.parameterListBox.insert(END, item)
            self.valueListBox.insert(END, i)

        self.exit_frame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.validateButton = Button(self.exit_frame, text="Validate", command=self.ctrl.validate)
        self.cancelButton = Button(self.exit_frame, text="Cancel", command=self.destroy)

    def setup_widgets(self):
        self.main_frame.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.selectVarCB.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.selectFilterButton.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.switchModeButton.grid(column=2, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

        self.handpick_frame.grid(column=0, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.selectFunctionCombobox.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

        self.parameterListBox.grid(column=0, row=0, pady=DEFAULT_PADY, padx=0)
        self.valueListBox.grid(column=1, row=0, pady=DEFAULT_PADY, padx=0)

        self.exit_frame.grid(column=0, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.validateButton.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.cancelButton.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

    def switch_mode(self):
        self.fmode = not self.fmode
        self.switchModeButton.configure(text=("Handpick Mode" if self.fmode else "Function Mode"))
        if (self.fmode):
            self.handpick_frame.grid_forget()
            self.function_frame.grid(column=0, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        else:
            self.function_frame.grid_forget()
            self.handpick_frame.grid(column=0, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

    def destroy(self) -> None:
        self.ctrl.remove_window()
        super().destroy()
