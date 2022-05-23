from tkinter import ttk, Tk, StringVar
from tkinter.constants import N, W, E, S


class MainView():
    def __init__(self):
        pass

    def display(self):
        root = Tk()
        root.title("Soda4LA")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        root.mainloop()

if __name__ == "__main__":
    mv = MainView()
    mv.display()