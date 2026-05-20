import tkinter as tk
import ttkbootstrap as ttk

from .settings import REFGEN_MAX_FIELDS, FONT, FONT_SIZE
from .reference_model import ModelReferenceDatabase


class WrapperRefGen(ttk.Frame):
    """
    Parent GUI Frame container to contain "reference generator options" container
    and the "reference fields" container.
    """
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent = container
        self.container_ref_gen = ContainerRefGen(self)
        self.container_ref_gen.pack(expand=True, fill=tk.BOTH)


class ContainerRefGen(ttk.Frame):
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent = container

        self.gui_setup_grid_layout()
        #self._gui_show_layout()
        self.gui_create_frames()
        self.initialise_mvc()

    def gui_setup_grid_layout(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def _gui_show_layout(self):
        # Visualise widget placement for testing
        self.label_refgen_options = ttk.Label(self, text="Reference generator options", background="blue", anchor="center") 
        self.label_refgen_fields = ttk.Label(self, text="User input fields", background="purple", anchor="center")

        self.label_refgen_options.grid(column=0, row=0, sticky="nsew")
        self.label_refgen_fields.grid(column=0, row=1, sticky="nsew")

    def gui_create_frames(self):
        self.wrapper_refgen_options = WrapperRefGenOptions(self)
        self.wrapper_refgen_fields = WrapperRefGenFields(self)

        self.wrapper_refgen_options.grid(column=0, row=0, sticky="nsew")
        self.wrapper_refgen_fields.grid(column=0, row=1, sticky="nsew")

    def initialise_mvc(self):
        self.refgen_model = ModelReferenceDatabase()
        self.view_refgen_options = ViewRefGenOptions()
        self.view_refgen_fields = ViewRefGenFields()
        self.controller_refgen = ControllerReferenceGenerator(self.refgen_model, self.view_refgen_options, self.view_refgen_fields)
        self.view_refgen_fields.controller = self.controller_refgen
        self.view_refgen_options.controller = self.controller_refgen

class WrapperRefGenOptions(ttk.Frame):
    """
        Wrapper for RefGenOptions for placement in parent frame, and to avoid
        pack() / grid() conflicts.
    """
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent = container
        self.frame_container = ViewRefGenOptions(self)
        self.frame_container.pack(expand=True, fill=tk.BOTH)

class ViewRefGenOptions(ttk.Frame):
    #TODO: Implement frame with buttons
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent = container
        self.controller: ControllerReferenceGenerator | None = None
        self.gui_setup_grid_layout()
        self._gui_show_layout()
        #self.gui_create_frames()

 
    def gui_setup_grid_layout(self):
        # Create 4x4 layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

    def gui_create_frames(self):
        ...

    def gui_setup_iteration_settings(self):
        self.ui_header_iteration_settings = ttk.Label(self, text="Iteration settings")
        self.ui_label_integer_start = ttk.Label(self, text="Start:")
        self.ui_label_number_iterations = ttk.Label(self, text="N° of iterations")
        self.ui_label_number_end = ttk.Label(self, text="End:")
        #TODO: On interaction, update end_year label. via controller

        # self.ui_start_value_entry =
        # self.ui_end_value_label =

        # self.number_iterations = tk.StringVar(self.ui_number_iterations, "1")

        # self.ui_number_iterations = ttk.Spinbox(
        #     self, 
        #     from_=1, 
        #     to=30, 
        #     textvariable=self.number_iterations, 
        #     wrap=True,
        # )

        # self.ui_button_generate_entries =
        # self.ui_button_clear_fields = 
        # self.ui_label_reference_counter = # [current reference number] out of [last ref number]
        # self.ui_button_previous_reference = # Toggles preview of next reference
        # self.ui_button_next_reference =  # Toggles preview of next reference

    def _gui_show_layout(self):
        #self.ui_header_iteration_settings = ttk.Label(self, text="Preview General", background="purple", anchor="center")
        #self.ui_header_iteration_settings.grid(column=0, row=0, sticky="nsew", columnspan=4, rowspan=4)

        self.ui_layout_iteration_settings = ttk.Label(self, text="Iteration settings", background="purple", anchor="center")
        self.ui_layout_doctype_label = ttk.Label(self, text="Document type", background="red", anchor="center")
        self.ui_layout_doctype_dropdown = ttk.Label(self, text="Dropdown here", background="red", anchor="center")
        self.ui_layout_start_label = ttk.Label(self, text="Start", background="blue", anchor="center")
        self.ui_layout_start_entry = ttk.Label(self, text="Start entry", background="red", anchor="center")
        self.ui_layout_step_label = ttk.Label(self, text="Steps", background="blue", anchor="center")
        self.ui_layout_step_entry = ttk.Label(self, text="Steps entry", background="red", anchor="center")
        self.ui_layout_end_label = ttk.Label(self, text="End", background="green", anchor="center")
        self.ui_layout_end_value = ttk.Label(self, text="End value", background="red", anchor="center")

        self.ui_layout_preview_label = ttk.Label(self, text="Preview references", background="grey", anchor="center")
        self.ui_layout_generate_button = ttk.Label(self, text="Generate button", background="green", anchor="center")
        self.ui_layout_clear_fields_button = ttk.Label(self, text="Clear fields", background="blue", anchor="center")
        self.ui_layout_delete_iteration_button = ttk.Label(self, text="Delete iteration", background="black", anchor="center")
        self.ui_layout_number_iterations_label = ttk.Label(self, text="[1/6]", background="pink", anchor="center")
        self.ui_layout_previous_iteration_button = ttk.Label(self, text="Previous button here", background="grey", anchor="center")
        self.ui_layout_next_iteration_button = ttk.Label(self, text="Next button here", background="black", anchor="center")


        self.ui_layout_iteration_settings.grid(column=0, row=0, sticky="nsew", columnspan=2)
        self.ui_layout_doctype_label.grid(column=0, row=1, sticky="nsew")
        self.ui_layout_doctype_dropdown.grid(column=1, row=1, sticky="nsew")
        self.ui_layout_start_label.grid(column=0, row=2, sticky="nsew")
        self.ui_layout_start_entry.grid(column=1, row=2, sticky="nsew")
        self.ui_layout_step_label.grid(column=0, row=3, sticky="nsew")
        self.ui_layout_step_entry.grid(column=1, row=3, sticky="nsew")
        self.ui_layout_end_label.grid(column=0, row=4, sticky="nsew")
        self.ui_layout_end_value.grid(column=1, row=4, sticky="nsew")

        self.ui_layout_preview_label.grid(column=2, row=0, sticky="nsew", columnspan=2)
        self.ui_layout_generate_button.grid(column=2, row=1, sticky="nsew", columnspan=2)
        self.ui_layout_clear_fields_button.grid(column=2, row=2, sticky="nsew")
        self.ui_layout_delete_iteration_button.grid(column=3, row=2, sticky="nsew")
        self.ui_layout_number_iterations_label.grid(column=2, row=3, sticky="nsew", columnspan=2)
        self.ui_layout_previous_iteration_button.grid(column=2, row=4, sticky="nsew")
        self.ui_layout_next_iteration_button.grid(column=3, row=4, sticky="nsew")

    def gui_reset(self):
        ...

class WrapperRefGenFields(ttk.Frame):
    """
        Wrapper for RefGenFields for placement in parent frame, and to avoid
        pack() / grid() conflicts.
    """
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent = container
        self.frame_container = ViewRefGenFields(self)
        self.frame_container.pack(expand=True, fill=tk.BOTH)


class ViewRefGenFields(ttk.Frame):
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.entries = []
        self.ref_count = 0 # Used to check for max number of fields.
        self.parent = container
        self.controller: ControllerReferenceGenerator | None = None
        self.ui_fields_canvas = ttk.Canvas(self)

        #self._gui_show_layout()
        self.gui_setup_scrollbar()
        self.gui_add_fields()

        #TODO: Need to figure out how to add widgets to Canvas (entry and button)
        # Need to create a [field_name] [entry] object

        # TODO: Setup grid for ui_canvas. Maybe place +field at the bottom of canvas
        # TODO: Create a separate frame object of fixed width for UI fields canvas.
        # The canvas is purely here to enable scrolling.
        # Arbitrary width but of fixed height. Used to place fields.
    def _gui_show_layout(self):
        self.ui_fields = ttk.Label(self, text="Fields", background="blue", anchor="center")
        #self.ui_fields.grid(column=0, row=0, sticky="nsew", columnspan=4, rowspan=4)
        self.ui_fields.pack(expand=True, fill=tk.BOTH)

    def gui_add_fields(self):
        self.test = ttk.Label(self.ui_fields_canvas, text="Hello!", background="blue", anchor="center")
        self.test.pack(expand=True, fill=tk.BOTH)
        self.ui_fields_canvas.create_window((100, 1000), window=self.test, anchor="center")

    def gui_setup_scrollbar(self):
        """ 
        Create scrollable frame with ui_canvas to contain field entries.
        This is needed as different document types will have different numbers
        of fields.
        """
        self.ui_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.ui_fields_canvas.yview)
        self.ui_fields_canvas.configure(yscrollcommand=self.ui_scrollbar.set)

        self.ui_scrollable_frame = ttk.Frame(self)

        self.ui_fields_canvas.pack(side="left", fill="both", expand=True)
        self.ui_scrollbar.pack(side="right", fill="y")

        self.ui_canvas_window = self.ui_fields_canvas.create_window((0, 0), window=self.ui_scrollable_frame, anchor="nw")
        # Bind controls for scrolling
        self.ui_scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.ui_fields_canvas.bind("<Configure>", self.on_canvas_configure)
        
    def on_frame_configure(self, event):
        self.ui_fields_canvas.configure(scrollregion=self.ui_fields_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.ui_fields_canvas.itemconfig(self.ui_canvas_window, width=canvas_width)
    
    #TODO:Add entry creation and deletion function.
    def gui_add_entry(self):
        # Check if over REFGEN_MAX_FIELDS
        # Trigger popup if that happens
        self.frame_count += 1

    def gui_delete_entry(self):
        # Check if over REFGEN_MAX_FIELDS
        self.frame_count -= 1


class ControllerReferenceGenerator:
    """
    Element linking model component to the UI state and user interactions.
    If X button is clicked, then Y happens to internal data.
    """
    def __init__(self, model: ModelReferenceDatabase, view_options: ViewRefGenOptions, view_fields: ViewRefGenFields):
        self.model = model
        self.view_options = view_options
        self.view_fields = view_fields
    # TODO: Create custom logic to setup interactions between model and view
    # Allows user interactions to bind to internal data as per MVC framework.
    # 1. Not sure if models and views should be implemented as dictionary
    # 2. Not sure if this should be placed in app.py as this will communicate between widgets
    #self.view.add_callback("get_number_iterations", self.)
        """ Register a ttk.Frame object to mediator """

    def update_options_iterations_start(self):
        ...

    def update_option_iteration_number(self):
        # If reference in database is less than iteration number, then delete.
        ...
    # def update_field(self):
