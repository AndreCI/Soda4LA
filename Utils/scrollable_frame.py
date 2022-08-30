import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    """
    Scrollframe module, used in place of a frame. can be horizontal or vertical. Automatically generate a scrollbar on
    the right or the bottom
    """
    def __init__(self, container, orient="vertical", *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        if('width' not in kwargs.keys()):
            pass
        canvas = tk.Canvas(self, width=kwargs['width'], height=kwargs['height'])
        self.scrollbar = ttk.Scrollbar(self, orient=orient, command=(canvas.yview if orient=="vertical" else canvas.xview))
        self.scrollableFrame = ttk.Frame(canvas, padding=kwargs['padding'], style=kwargs['style'])

        self.scrollableFrame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollableFrame, anchor="center")

        if(orient=="vertical"):
            canvas.configure(yscrollcommand=self.scrollbar.set)
        else:
            canvas.configure(xscrollcommand=self.scrollbar.set)

        canvas.pack(side=("left" if orient=="vertical" else "top"), fill="both", expand=True)
        self.scrollbar.pack(side=("right" if orient=="vertical" else "bottom"), fill=("y" if orient=="vertical" else "x"))
