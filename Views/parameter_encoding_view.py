from tkinter import Toplevel, Button, Listbox, END, Entry, Label
from tkinter.ttk import Frame, Combobox

from Utils.constants import DEFAULT_PADDING, TFRAME_STYLE, DEFAULT_PADY, DEFAULT_PADX, MOCKUP_VARS


class ParameterEncodingView(Toplevel):
    """"
    View for encoding variables. started from track_config_view, and linked to a specific parameter of a note (value, duration, velocity)
    """

    def __init__(self, ctrl, model, **kwargs):
        Toplevel.__init__(self, **kwargs)
        #ctrl and model
        self.ctrl = ctrl
        self.model = model

        #View data
        self.fmode = False
        self.title("Encoding for {}".format(self.model.encoded_var))
        #self.geometry('450x400')

        #setup view
        self.create_widgets()
        self.setup_widgets()

    def select_variable(self, event):
        self.ctrl.assign_main_var(self.selectVarCB.get())
        for var, val in zip(self.variableList, self.valueList):
            var.destroy()
            val.destroy()
        self.variableList = []
        self.valueList = []
        #self.parameterListBox.delete(0, END)
        #self.valueListBox.delete(0, END)
        for i, item in enumerate(self.model.get_variables_instances()):
            self.variableList.append(Label(self.handpick_frame, text=item))
            self.valueList.append(Entry(self.handpick_frame))
            self.valueList[-1].insert(0, str(i*10))
            #self.parameterListBox.insert(END, item)
            #self.valueListBox.insert(END, i)
        for i, tk_m in enumerate(zip(self.variableList, self.valueList)):
            tk_m[0].grid(column=0, row=i, pady=0, padx=DEFAULT_PADX, sticky="ew")
            tk_m[1].grid(column=1, row=i, pady=0, padx=0, sticky="ew")

    def create_widgets(self):
        self.main_frame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])

        self.varlistLabel = Label(self.main_frame, text="Select variable")
        self.selectVarCB = Combobox(self.main_frame, values=self.model.datas.get_variables())
        self.selectVarCB.bind('<<ComboboxSelected>>', self.select_variable)
        self.selectVarCB.current(0)
        self.ctrl.assign_main_var(self.selectVarCB.get())

        self.filterEntry = Entry(self.main_frame)
        self.filterLabel = Label(self.main_frame, text="Filter")

        self.switvhModeLabel = Label(self.main_frame, text="Change mode")
        self.switchModeButton = Button(self.main_frame, text="Function Mode", command=self.switch_mode)

        self.function_frame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.selectFunctionCombobox = Combobox(self.function_frame, values=MOCKUP_VARS)
        self.selectVarCB.current(0)

        self.handpick_frame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        #self.parameterListBox = Listbox(self.handpick_frame)
        #self.valueListBox = Listbox(self.handpick_frame)
        self.variableList = []
        self.valueList = []
        for i, item in enumerate(self.model.get_variables_instances()):
            #self.parameterListBox.insert(END, item)
            self.variableList.append(Label(self.handpick_frame, text=item))
            self.valueList.append(Entry(self.handpick_frame))#.insert(END, i)
            self.valueList[i].insert(0, str(i*10))

        self.exit_frame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.validateButton = Button(self.exit_frame, text="Validate", command=self.ctrl.validate)
        self.cancelButton = Button(self.exit_frame, text="Cancel", command=self.destroy)

    def setup_widgets(self):
        self.main_frame.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

        self.varlistLabel.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.selectVarCB.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")

        self.filterLabel.grid(column=0, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.filterEntry.grid(column=1, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")

        self.switvhModeLabel.grid(column=0, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.switchModeButton.grid(column=1, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")

        self.handpick_frame.grid(column=0, row=3, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.selectFunctionCombobox.grid(column=0, row=3, pady=DEFAULT_PADY, padx=DEFAULT_PADX)


        #self.parameterListBox.grid(column=0, row=0, rowspan=len(self.valueList)+1, pady=DEFAULT_PADY, padx=0)
        #self.valueListBox.grid(column=1, row=0, pady=DEFAULT_PADY, padx=0)
        for i, tk_m in enumerate(zip(self.variableList, self.valueList)):
            tk_m[0].grid(column=0, row=i, pady=0, padx=DEFAULT_PADX, sticky="ew")
            tk_m[1].grid(column=1, row=i, pady=0, padx=0, sticky="ew")

        self.exit_frame.grid(column=0, row=4, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.validateButton.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.cancelButton.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")

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
