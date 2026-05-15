import tkinter as tk
import ttkbootstrap as ttk

from ..config.settings import REFGEN_MAX_FIELDS

class ContainerRefGen(ttk.Frame):
    """
    Parent GUI Frame container to contain reference generator options container
    and the reference fields container.
    """
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent = container
        # Insert data here
        self.gui_setup_grid_layout()
        self._gui_show_layout()

    def gui_setup_grid_layout(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.columnconfigure(0, weight=1)
        ...

    def gui_create_frames(self):
        self.ui_refgen_fields = ViewRefGenFields(self)
        ...

    def _gui_show_layout(self):
        # Visualise widget placement for testing
        self.label_refgen_options = ttk.Label(self, text="Reference generator options", background="blue", anchor="center")
        self.label_refgen_fields = ttk.Label(self, text="User input fields", background="purple", anchor="center")

        self.label_refgen_options.grid(column=0, row=0, sticky="nsew")
        self.label_refgen_fields.grid(column=0, row=1, sticky="nsew")

class ViewRefGenOptions(ttk.Frame):
    #TODO: Implement frame with buttons
    ...

class ViewRefGenFields(ttk.Frame):
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.entries = []
        self.frame_count = 0 # Used to check for max number of fields.
        self.parent = container
        self.ui_canvas = tk.Canvas(container)

        self.gui_setup_scrollbar()

    # TODO: Setup grid for canvas. Maybe place +field at the bottom of canvas

    def gui_setup_scrollbar(self):
        """ 
        Create scrollable frame with Canvas to contain field entries.
        This is needed as different document types will have different numbers
        of fields.
        """
        self.ui_scrollbar = ttk.Scrollbar(self.parent, orient="veritcal", command=self.ui_canvas.yview)
        self.ui_scrollable_frame = ttk.Frame(self)
        self.ui_canvas.configure(yscrollcommand=self.ui_scrollbar.set)

        self.ui_canvas.pack(side="left", fill="both", expand=True)
        self.ui_scrollbar.pack(side="right", fill="y")

        self.ui_canvas_window = self.canvas.create_window((0, 0), window=self.ui_scrollable_frame, anchor="nw")
        # Bind controls for scrolling
        self.ui_scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.ui_canvas.bind("<Configure>", self.on_canvas_configure)
        
    def on_frame_configure(self, event):
        self.ui_canvas.configure(scrollregion=self.ui_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.ui_canvas.itemconfig(self.ui_canvas_window, width=canvas_width)
    
    #TODO:Add entry creation and deletion function.
    def gui_add_entry(self):
        # Check if over REFGEN_MAX_FIELDS
        # Trigger popup if that happens
        self.frame_count += 1
        pass

    def gui_delete_entry(self):
        # Check if over REFGEN_MAX_FIELDS
        self.frame_count -= 1


class ControllerReferenceGenerator:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    # TODO: Create custom logic to setup interactions between model and view
    # Allows user interactions to bind to internal data as per MVC framework.
    # 1. Not sure if models and views should be implemented as dictionary
    # 2. Not sure if this should be placed in app.py as this will communicate between widgets
