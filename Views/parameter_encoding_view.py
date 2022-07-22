from tkinter import Toplevel, Button, Listbox, END, Entry, Label, StringVar, IntVar
from tkinter.constants import X
from tkinter.ttk import Frame, Combobox

from Utils.constants import DEFAULT_PADDING, TFRAME_STYLE, DEFAULT_PADY, DEFAULT_PADX, MOCKUP_VARS, FUNCTION_OPTIONS
from Utils.scrollable_frame import ScrollableFrame


class ParameterEncodingView(Toplevel):
    """"
    View for encoding variables. started from track_config_view, and linked to a specific parameter of a note (value, duration, velocity)
    """

    def __init__(self, ctrl, model, **kwargs):
        Toplevel.__init__(self, **kwargs)
        #ctrl and model
        self.ctrl = ctrl #PECtrl
        self.model = model #PEModel

        #View data
        self.handpicked_mode = True #Current model, function or handpicked
        self.title("Encoding for {}".format(self.model.encoded_var))
        #self.geometry('450x400')

        #setup view
        self.mainFrame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])

        self.varlistLabel = Label(self.mainFrame, text="Select variable")
        self.selectVarCB = Combobox(self.mainFrame, values=self.model.datas.get_variables())
        self.selectVarCB.bind('<<ComboboxSelected>>', self.select_variable)
        self.selectVarCB.current(0)
        self.ctrl.assign_main_var(self.selectVarCB.get())

        self.filterEntry = Entry(self.mainFrame)
        self.filterLabel = Label(self.mainFrame, text="Filter")

        self.switchModeLabel = Label(self.mainFrame, text="Change mode")
        self.switchModeButton = Button(self.mainFrame, text="Function Mode", command=self.switch_mode)

        self.functionFrame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.functionLabel = Label(self.functionFrame, text="Function applied to map")
        self.selectFunctionCB = Combobox(self.functionFrame, values=FUNCTION_OPTIONS)
        self.selectFunctionCB.current(0)
        self.fMinLabel = Label(self.functionFrame, text="Minimal value to map")
        self.fMaxLabel = Label(self.functionFrame, text="Maximal value to map")
        self.fMinVar = IntVar(self.functionFrame, value=0)
        self.fMaxVar = IntVar(self.functionFrame, value=128)
        self.fMinEntry = Entry(self.functionFrame, textvariable=self.fMinVar)
        self.fMaxEntry = Entry(self.functionFrame, textvariable=self.fMaxVar)
        #self.selectVarCB.current(0)

        self.handpickFrame = ScrollableFrame(self, orient="vertical", width=200, height=200, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        #self.parameterListBox = Listbox(self.handpick_frame)#width=150, height=450,
        #self.valueListBox = Listbox(self.handpick_frame)
        self.variableList = []
        self.valueList = []
        for i, item in enumerate(self.model.get_variables_instances()):
            self.variableList.append(Label(self.handpickFrame.scrollableFrame, text=item))
            self.valueList.append(Entry(self.handpickFrame.scrollableFrame))#.insert(END, i)
            self.valueList[i].insert(0, str(min((i*10), 127)))

        self.exit_frame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.validateButton = Button(self.exit_frame, text="Validate", command=self.ctrl.validate)
        self.cancelButton = Button(self.exit_frame, text="Cancel", command=self.destroy)

        self.setup_widgets()

    def setup_widgets(self):
        self.mainFrame.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        #MAIN FRAME
        self.varlistLabel.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.selectVarCB.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")

        self.filterLabel.grid(column=0, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.filterEntry.grid(column=1, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")

        self.switchModeLabel.grid(column=0, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.switchModeButton.grid(column=1, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        #END MAIN FRAME

        #FUNCTION FRAME
        self.functionLabel.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.selectFunctionCB.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.fMinLabel.grid(column=0, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.fMinEntry.grid(column=1, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.fMaxLabel.grid(column=0, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.fMaxEntry.grid(column=1, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        #https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter/4140988#4140988

        #END FUNCTION FRAME
        #HANDPICK FRAME
        self.handpickFrame.grid(column=0, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

        for i, tk_m in enumerate(zip(self.variableList, self.valueList)):
            tk_m[0].grid(column=0, row=i, pady=0, padx=DEFAULT_PADX, sticky="ew")
            tk_m[1].grid(column=1, row=i, columnspan=1000, pady=0, padx=0, sticky="ew")
        #END HANDPICKFRAME

        #EXIT FRAME
        self.exit_frame.grid(column=0, row=4, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.validateButton.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.cancelButton.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        #END EXIT FRAME

    def select_variable(self, event):
        self.ctrl.assign_main_var(self.selectVarCB.get())
        #Destroy objects linked to previous variable
        for var, val in zip(self.variableList, self.valueList):
            var.destroy()
            val.destroy()
        self.variableList = []
        self.valueList = []
        #Create and setup object linked to new variable
        for i, item in enumerate(self.model.get_variables_instances()):
            self.variableList.append(Label(self.handpickFrame.scrollableFrame, text=item))
            self.valueList.append(Entry(self.handpickFrame.scrollableFrame))
            self.valueList[-1].insert(0, str(min((i*10), 127)))
        for i, tk_m in enumerate(zip(self.variableList, self.valueList)):
            tk_m[0].grid(column=0, row=i, pady=0, padx=DEFAULT_PADX, sticky="ew")
            tk_m[1].grid(column=1, row=i, pady=0, padx=0, sticky="ew")
        self.geometry("")

    def switch_mode(self):
        """
        Switch the view upon user input, either handpicked of function
        """
        self.handpicked_mode = not self.handpicked_mode
        self.switchModeButton.configure(text=("Handpick Mode" if self.handpicked_mode else "Function Mode"))
        if (self.handpicked_mode):
            self.functionFrame.grid_forget()
            self.handpickFrame.grid(column=0, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        else:
            self.handpickFrame.grid_forget()
            self.functionFrame.grid(column=0, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)


    def destroy(self) -> None:
        self.ctrl.remove_window()
        super().destroy()
