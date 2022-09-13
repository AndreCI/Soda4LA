from tkinter import Toplevel, Button, Listbox, END, Entry, Label, StringVar, IntVar, Checkbutton
from tkinter.constants import X, DISABLED, NORMAL
from tkinter.ttk import Frame, Combobox

from Models.note_model import note_to_int, int_to_note
from Utils.constants import DEFAULT_PADDING, TFRAME_STYLE, DEFAULT_PADY, DEFAULT_PADX, MOCKUP_VARS, FUNCTION_OPTIONS
from Utils.scrollable_frame import ScrollableFrame


class ParameterEncodingView(Toplevel):
    """"
    View for encoding variables. started from track_config_view, and linked to a specific parameter of a note (value, duration, velocity)
    """

    def __init__(self, ctrl, model, **kwargs):
        #  TODO: bigger window with a bigger space dedicated to filter. displauing on/off box buttons for
        #  categorical data. maybe range for num val. also display graphs and indicator on the selected variable
        Toplevel.__init__(self, **kwargs)
        #ctrl and model
        self.ctrl = ctrl #PECtrl
        self.model = model #PEModel

        #View data
        self.handpicked_mode = True #Current model, function or handpicked
        self.checkbuttons_toggle = True
        self.variables = []
        self.title("Encoding for {}".format(self.model.filter.column))
        #self.geometry('450x400')

        #setup view
        #frames
        self.mainFrame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.filterFrame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.functionFrame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.handpickFrame = ScrollableFrame(self, orient="vertical", width=400, height=400, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])
        self.exit_frame = Frame(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])

        #Main frame
        self.varlistLabel = Label(self.mainFrame, text="Select variable")
        self.selectVarCB = Combobox(self.mainFrame, values=self.model.data.get_variables(), state='readonly')
        self.selectVarCB.bind('<<ComboboxSelected>>', self.select_variable)
        if(self.model.initialized):
            self.selectVarCB.set(self.model.filter.column)
            self.ctrl.assign_main_var(self.selectVarCB.get())
        self.switchModeLabel = Label(self.mainFrame, text="Change mode")
        self.switchModeButton = Button(self.mainFrame, text="Function Mode", command=self.switch_mode)
        self.octaveLabel = Label(self.mainFrame, text="Octave (between 0 and 9)")
        self.octaveEntryVar = StringVar(self.mainFrame, value=self.model.octave)
        self.octaveEntry = Entry(self.mainFrame, textvariable=self.octaveEntryVar)

        #Filter
        self.filterVar = StringVar()
        self.filterEntry = Entry(self.filterFrame, textvariable=self.filterVar, width=40)
        self.filterLabel = Label(self.filterFrame, text="Filter")

        #Function frame
        self.functionLabel = Label(self.functionFrame, text="Function applied to map")
        self.selectFunctionCB = Combobox(self.functionFrame, values=FUNCTION_OPTIONS, state='readonly')
        self.selectFunctionCB.current(0)
        self.fMinLabel = Label(self.functionFrame, text="Minimal value to map")
        self.fMaxLabel = Label(self.functionFrame, text="Maximal value to map")
        self.fMinVar = IntVar(self.functionFrame, value=(self.model.functionEncoding["min"] if "min" in self.model.functionEncoding else 0))
        self.fMaxVar = IntVar(self.functionFrame, value=(self.model.functionEncoding["max"] if "max" in self.model.functionEncoding else 127))
        self.fMinEntry = Entry(self.functionFrame, textvariable=self.fMinVar)
        self.fMaxEntry = Entry(self.functionFrame, textvariable=self.fMaxVar)

        #Handpick frame
        self.toggle_checkbox = Button(self.handpickFrame.scrollableFrame, text="Uncheck all", command=self.filter_toggle_all_checkbuttons)

        #Exit frame
        self.validateButton = Button(self.exit_frame, text="Validate", command=self.ctrl.validate, state=NORMAL if self.model.initialized else DISABLED)
        self.cancelButton = Button(self.exit_frame, text="Cancel", command=self.destroy)

        self.setup_widgets()
        if(self.model.handpicked != self.handpicked_mode):
            self.switch_mode()

    def setup_widgets(self):
        self.mainFrame.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.filterFrame.grid(column=0, row=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        #No function frame gridded yet, wait for button press
        self.handpickFrame.grid(column=1, row=0, rowspan=1000, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        self.exit_frame.grid(column=1, row=1001, pady=DEFAULT_PADY, padx=DEFAULT_PADX)

        #MAIN FRAME
        self.varlistLabel.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.selectVarCB.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")


        self.switchModeLabel.grid(column=0, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.switchModeButton.grid(column=1, row=2, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")

        if(self.model.encoded_var == "value"):
            self.octaveLabel.grid(column=0, row=3, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
            self.octaveEntry.grid(column=1, row=3, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")

        #END MAIN FRAME

        #FILTER FRAME
        self.filterLabel.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.filterEntry.grid(column=1, row=0, ipady=60, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")

        #END FILTER FRAME

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
        if self.model.initialized:
            self.select_variable(None)
        # #END HANDPICKFRAME

        #EXIT FRAME
        self.validateButton.grid(column=0, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        self.cancelButton.grid(column=1, row=0, pady=DEFAULT_PADY, padx=DEFAULT_PADX, sticky="ew")
        #END EXIT FRAME

    def filter_toggle_all_checkbuttons(self):
        self.checkbuttons_toggle = not self.checkbuttons_toggle
        self.toggle_checkbox.configure(text=("Uncheck all" if self.checkbuttons_toggle else "Check all"))
        for v in self.variables:
            v["checked"].set(1 if self.checkbuttons_toggle else 0)

    def select_variable(self, event):
        self.validateButton.config(state=NORMAL)
        self.ctrl.assign_main_var(self.selectVarCB.get())
        #Destroy objects linked to previous variable
        for var in self.variables:
            var["checkbutton"].destroy()
            var["value"].destroy()
        self.variables = []
        #Create and setup object linked to new variable
        for i, variable in enumerate(self.model.get_variables_instances()):
            iv = IntVar(value=1 if self.model.filter.evaluate(variable) else 0)
            d_object = {"variable": variable,
                        "checked": iv,
                        "checkbutton":Checkbutton(self.handpickFrame.scrollableFrame, text=variable, variable=iv),
                        "value":Entry(self.handpickFrame.scrollableFrame)}
            value = (self.model.handpickEncoding[
                         variable] if variable in self.model.handpickEncoding else self.model.defaultValue)
            if(self.model.encoded_var == "value"):
                value = int_to_note(value)#min((i*10), 127)
            d_object["value"].insert(0, str(value))
            self.variables.append(d_object)

        for i, v in enumerate(self.variables):
            v["checkbutton"].grid(column=0, row=i, pady=0, padx=DEFAULT_PADX, sticky="ew")
            v["value"].grid(column=1, row=i, pady=0, padx=0, sticky="ew")

        self.toggle_checkbox.grid(column=0, row=len(self.variables) + 1, columnspan=1000,  pady=5, padx=5, sticky="ew")

        self.filterVar.set(self.model.filter.get_current_filter())
        self.geometry("")

    def switch_mode(self):
        """
        Switch the view upon user input, either handpicked of function
        """
        self.handpicked_mode = not self.handpicked_mode
        self.switchModeButton.configure(text=("Handpick Mode" if self.handpicked_mode else "Function Mode"))
        if (self.handpicked_mode):
            self.functionFrame.grid_forget()
            self.handpickFrame.grid(column=1, row=0, rowspan=1000, pady=DEFAULT_PADY, padx=DEFAULT_PADX)
        else:
            self.handpickFrame.grid_forget()
            self.functionFrame.grid(column=1, row=0, rowspan=1, pady=DEFAULT_PADY, padx=DEFAULT_PADX)


    def destroy(self) -> None:
        self.ctrl.remove_window()
        super().destroy()
