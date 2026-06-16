import tkinter as tk
import ttkbootstrap as ttk

from src.settings import (
    WINDOW_TITLE,
    WIDTH_WINDOW,
    HEIGHT_WINDOW,
    THEME,
)

from src.mvc_view_reference_generator import WrapperRefGen
from src.mvc_view_output_display import WrapperOutputWindow
from src.mvc_controller import Controller
from src.mvc_model import ModelReferenceDatabase


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

class UserInterface(ttk.Frame):
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent = container
        self.pack(expand=True, fill=tk.BOTH)

        self.gui_setup_grid_layout()
        self.gui_create_frames()
        self.initialise_mvc()
        #self._gui_show_layout()

    def gui_setup_grid_layout(self):
        # 3x2 grid layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)

    def gui_create_frames(self):
        # Invoke containers to initialise app
        self.frame_left = WrapperRefGen(self) 
        self.frame_left.grid(column=0, row=0, sticky="nsew", rowspan=3, pady=10)
        self.frame_right = WrapperOutputWindow(self)
        self.frame_right.grid(column=1, row=0, sticky="nsew", rowspan=3, padx=(0, 10), pady=10)

    def _gui_show_layout(self):
        # Visualising widget placement for testing
        #self.label_refgen = ttk.Label(self, text="User inputs", background="red", anchor="center")
        self.label_bibtex_output = ttk.Label(self, text="Output display", background="green", anchor="center")
        self.label_console = ttk.Label(self, text="Console", background="orange", anchor="center")

        #self.label_refgen.grid(column=0, row=0, sticky="nsew", rowspan=3)
        self.label_bibtex_output.grid(column=1, row=0, sticky="nsew", rowspan=2)
        self.label_console.grid(column=1, row=2, sticky="nsew", rowspan=1)

    def initialise_mvc(self):
        # Get wrapper_refgen_options.view_frame
        # Get wrapper refgenFields.view_frame
        self.refgen_model = ModelReferenceDatabase()
        self.refgen_options = self.frame_left.container_ref_gen.wrapper_refgen_options.view_frame
        self.refgen_fields = self.frame_left.container_ref_gen.wrapper_refgen_fields.view_frame.view_refgen_fields
        self.refgen_output = self.frame_right.output_window
        self.controller = Controller(
            self.refgen_model, 
            self.refgen_options, 
            self.refgen_fields,
            self.refgen_output
        )
        self.refgen_options.controller = self.controller
        self.refgen_fields.controller = self.controller
        self.controller.initialise_mvc()
