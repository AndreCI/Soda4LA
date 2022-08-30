import logging

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename

except:
    logging.debug("tjk==jubter")

try:
    import Models.data_model #import Data
except:
    logging.debug("model dataimport")
try:
    import Models.music_model
except:
    logging.debug("model music import")
try:
    from Utils.constants import DEFAULT_PADDING, TFRAME_STYLE
except:
    logging.debug("other inport cibs")
try:
    from Views.sonification_view import SonificationView
    import logging
except:
    logging.debug("other inport sonview")

class MainView(tk.Tk):
    """"
    Main view, contains all the others modules and submodules. Progam starts here.
    Modules: sonification view, menubar
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Soda4LA")
        self.geometry('1500x1000')
        s = ttk.Style()
        for v in TFRAME_STYLE.values():
            s.configure(v[0], background=v[1])

        self.db = Models.data_model.Data.getInstance()

        self.setup_menu()
        self.create_widgets()
        self.setup_widgets()
        self.config(menu=self.menubar)
        self.load_data()


    def setup_menu(self):
        self.menubar = tk.Menu(self)
        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Load data", command=self.load_data)
        filemenu.add_command(label="Show data", command=self.show_data)
        # filemenu.add_command(label="Save")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="About")
        self.menubar.add_cascade(label="Help", menu=helpmenu)

    def load_data(self):
        #TODO add other filetype
        m = Models.music_model.Music.getInstance()
        if(m.timeSettings.autoload):
            self.db.read_data(m.timeSettings.autoloadDataPath)
            self.db.date_column = m.timeSettings.autoloadTimestampcol
            self.db.assign_timestamps()
            m.sonification_view.dataTable.set_data(self.db.get_first_and_last().to_dict('records'))
        else:
            filename = askopenfilename(filetypes=[("csv file", "*.csv")])#, (" file",'*.png'), ("All files", " *.* "),))
            self.db.read_data(filename)
            self.show_data()
#        Music.getInstance().timeSettings.set_attribute(self.db.first_date, self.db.last_date)

    def show_data(self):
        self.db.ctrl.show_window()

    def create_widgets(self):
        # self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.sonificationView = SonificationView(self, padding=DEFAULT_PADDING, style=TFRAME_STYLE["CONFIG"][0])

        # self.sonificationView.create_widgets()

    def setup_widgets(self):
        # self.mainframe.grid(column=0, row=0)
        # self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)
        self.sonificationView.grid(column=0, row=0)

    def setup_controller(self, controller):
        pass


if __name__ == "__main__":
    mv = MainView()
    mv.mainloop()
