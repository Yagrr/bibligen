import tkinter as tk
import ttkbootstrap as ttk

from src.settings import (
    WINDOW_TITLE,
    WIDTH_WINDOW,
    HEIGHT_WINDOW,
    THEME,
)

from src.reference_generator import ContainerRefGen


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename=THEME)
        # Window configuration - dimensions and position
        self.title(WINDOW_TITLE)
        self.geometry(f'{WIDTH_WINDOW}x{HEIGHT_WINDOW}')
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f'+{x}+{y}')

        self.parent_frame = UserInterface(self)
        self.parent_frame.pack(fill=tk.BOTH, expand=True)


class UserInterface(ttk.Frame):
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent = container
        self.gui_setup_grid_layout()
        self.gui_create_frames()
        self._gui_show_layout()

    def gui_setup_grid_layout(self):
        # 3x2 grid layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def gui_create_frames(self):
        # Invoke containers to initialise app
        # TODO: Create the rest of the containers
        self.frame_left = ContainerRefGen(self, padding="15") 

        self.frame_left.grid(column=0, row=0, sticky="nsew", rowspan=3)
        
        ...

    def _gui_show_layout(self):
        # Visualising widget placement for testing
        self.label_refgen = ttk.Label(self, text="User inputs", background="red", anchor="center")
        self.label_bibtex_output = ttk.Label(self, text="Output display", background="green", anchor="center")
        self.label_console = ttk.Label(self, text="Console", background="orange", anchor="center")

        # self.label_refgen.grid(column=0, row=0, sticky="nsew", rowspan=3)
        self.label_bibtex_output.grid(column=1, row=0, sticky="nsew", rowspan=2)
        self.label_console.grid(column=1, row=2, sticky="nsew", rowspan=1)
