import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

from Models.data_model import Data
from Models.music_model import Music
from Utils.constants import DATA_PATH
from Utils.constants import DEFAULT_PADDING, TFRAME_STYLE
from Views.data_view import DataView
from Views.sonification_view import SonificationView


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

        self.db = Data.getInstance()

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
        filename = askopenfilename(filetypes=[("csv file", "*.csv")])#, (" file",'*.png'), ("All files", " *.* "),))
        self.db.read_data(filename)
        self.show_data()
        Music.getInstance().timeSettings.set_attribute(self.db.first_date, self.db.last_date)

        print(filename)

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
