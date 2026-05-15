import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo

from config.settings import (
    WINDOW_TITLE,
    WIDTH_WINDOW,
    HEIGHT_WINDOW,
)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title(WINDOW_TITLE)
        self.geometry(f'{WIDTH_WINDOW}x{HEIGHT_WINDOW}')
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f'+{x}+{y}')


        self.parent_frame = ContentFrame(self)
        self.parent_frame.pack(fill=tk.BOTH, expand=True)

class ContentFrame(ttk.Frame):
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent = container
        self.setup_layout()
        self.create_children()
        self._show_layout()

    def setup_layout(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

    def create_children(self):
        # Create place_holders to indicate layout
        ...

    def _show_layout(self):
        self.label = ttk.Label(self, text="User inputs", background="red", anchor="center")
        self.label.grid(column=0, row=0, sticky="nsew", rowspan=2)
        self.label_2 = ttk.Label(self, text="Console", background="orange", anchor="center")
        self.label_2.grid(column=1, row=0, sticky="nsew", rowspan=1)
        self.label_3 = ttk.Label(self, text="Output display", background="green", anchor="center")
        self.label_3.grid(column=1, row=1, sticky="nsew", rowspan=2)

    def button_clicked(self):
        showinfo(title="Information", message="Hello, user!")


class FrameCommunicationManager():
    def __init__(self):
        self.listeners = {}
    # Allow user inputs, allow self destruct.
    ...
