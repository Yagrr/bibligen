import tkinter as tk
import ttkbootstrap as ttk

from .settings import (
    FONT,
    FONT_SIZE,
    DEFAULT_OPTIONS_START,
    DEFAULT_OPTIONS_NUMBER_ITERATIONS,
    REFGEN_MAX_ITERATIONS,
    REFGEN_MAX_FIELDS,
)
from .utils import ScrollBar
from .reference_model import ModelReferenceDatabase
from .reference_type import LIST_REFERENCE_TYPES


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
        """
            Creating model and linking model and views to controller
        """
        self.refgen_model = ModelReferenceDatabase()
        self.controller_refgen = ControllerReferenceGenerator(
            self.refgen_model, 
            self.wrapper_refgen_options.view_frame, 
            self.wrapper_refgen_fields.view_frame,
        )
        self.wrapper_refgen_options.view_frame.controller = self.controller_refgen
        self.wrapper_refgen_options.view_frame.controller = self.controller_refgen

class WrapperRefGenOptions(ttk.Frame):
    """
        Wrapper for RefGenOptions for placement in parent frame, and to avoid
        pack() / grid() conflicts.
    """
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent = container
        self.view_frame = ViewRefGenOptions(self)
        self.view_frame.pack(expand=True, fill=tk.BOTH)

class ViewRefGenOptions(ttk.Frame):
    """
        View frame with buttons and entry objects for the user to change how
        many references the system should create, and how many values to
        iterate.
    """
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent = container
        self.controller: ControllerReferenceGenerator | None = None
        self.gui_setup_grid_layout()
        self._gui_show_layout()
        #self.gui_setup_frames()

 
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

    def setup_view_variables(self):
        #TODO: Figure out what values to keep inside of View, and what to keep in model
        # Probably will need to delete this function if we're storing everything in the model
        # Need to be careful and match these to the model, or make the model match these instead.
        self.vars_options_start = ttk.StringVar(self)
        self.vars_options_number_iterations = ttk.StringVar()

    def gui_setup_frames(self):
        if not self.controller:
            raise Exception("Error: controller not set for ViewRefGenOptions")
        self.ui_options_header_iteration_settings = ttk.Label(self, text="Iteration settings")
        self.ui_options_doctype_label = ttk.Label(self, text="Document type")
        self.ui_options_doctype_dropdown = ttk.Combobox(self, values=LIST_REFERENCE_TYPES)
        self.ui_options_start_label = ttk.Label(self, text="Start")

        #TODO: Add objects and figure out their variables
        self.ui_options_start_entry = ttk.Entry(self, textvariable=self.vars_options_start_entry)

        self.ui_options_step_label = ttk.Label(self, text="N° of iterations") 

        # TODO: Need to figure out how to listen to variable updates.
        # On update, -> need stringVar() set
        self.ui_options_step_entry = ttk.Spinbox(
            self, 
            from_=DEFAULT_OPTIONS_NUMBER_ITERATIONS, 
            to=REFGEN_MAX_ITERATIONS, 
            textvariable=self.vars_options_step_entry, 
            wrap=False,
        )

        self.ui_options_end_label = ttk.Label(self, text="End")

        #TODO: This needs to update when ui_start_entry is modified or ui_step_entry is modified
        # Need to init the value based on default start value
        self.ui_options_end_value_label = ttk.Label(self, textvariable=self.vars_options_end_value_label)

        self.ui_options_header_preview_label = ttk.Label(self, text="Preview references", background="grey", anchor="center")

        self.ui_options_generate_button = ttk.Button(self, text="Generate entries", command=self.controller.handle_generate_button_clicked)
        self.ui_options_clear_fields_button = ttk.Button(self, text="Clear fields", command=self.controller.handle_clear_fields_button_clicked)

        self.ui_options_delete_iteration_button = ttk.Button(self, text="Delete iteration", command=self.controller.handle_delete_iteration_button_clicked)

        # TODO: This needs to update when either 
        # current reference in view index is modified or
        # ui_step_entry is modified.
        # To create function Update step/start
        # Example display: 1/6 iterations
        self.ui_options_number_iterations_label = ttk.Label(self, textvariable=self.vars_options_number_iterations_label)

        self.ui_options_previous_iteration_button = ttk.Button(self, text="Previous", command=self.controller.handle_previous_button_clicked)
        self.ui_options_next_iteration_button = ttk.Button(self, text="Next", command=self.controller.handle_next_button_clicked)

        # Place objects in RefGenOptions frame
        self.ui_options_header_iteration_settings.grid(column=0, row=0, sticky="nsew", columnspan=2)
        self.ui_options_doctype_label.grid(column=0, row=1, sticky="nsew")
        self.ui_options_doctype_dropdown.grid(column=1, row=1, sticky="nsew")
        self.ui_options_start_label.grid(column=0, row=2, sticky="nsew")
        self.ui_options_start_entry.grid(column=1, row=2, sticky="nsew")
        self.ui_options_step_label.grid(column=0, row=3, sticky="nsew")
        self.ui_options_step_entry.grid(column=1, row=3, sticky="nsew")
        self.ui_options_end_label.grid(column=0, row=4, sticky="nsew")
        self.ui_options_end_value_label.grid(column=1, row=4, sticky="nsew")

        self.ui_options_header_preview_label.grid(column=2, row=0, sticky="nsew", columnspan=2)
        self.ui_options_generate_button.grid(column=2, row=1, sticky="nsew", columnspan=2)
        self.ui_options_clear_fields_button.grid(column=2, row=2, sticky="nsew")
        self.ui_options_delete_iteration_button.grid(column=3, row=2, sticky="nsew")
        self.ui_options_number_iterations_label.grid(column=2, row=3, sticky="nsew", columnspan=2)
        self.ui_options_previous_iteration_button.grid(column=2, row=4, sticky="nsew")
        self.ui_options_next_iteration_button.grid(column=3, row=4, sticky="nsew")

    def _gui_show_layout(self):
        """
            Private function for development for showing how the frame's current layout
        """
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
        self.ui_layout_number_iterations_label = ttk.Label(self, text="[first step value 1 / last step value 6]", background="pink", anchor="center")
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
        self.view_frame = ViewRefGenFields(self)
        self.view_frame.pack(expand=True, fill=tk.BOTH)


class ViewRefGenFields(ttk.Frame):
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.entries = []
    # TODO: Used to keep track of which Reference in the canvas is displayed
    # To implement getter and setter functions to expose to controller
    # Getter function will be used for ui_number_iterations_label in Options
        self.index_reference_in_view = 0
        self.parent = container
        self.controller: ControllerReferenceGenerator | None = None
        self.ui_fields_canvas = ttk.Canvas(self)
        self.ui_fields_canvas_scrollbar = ScrollBar(self, self.ui_fields_canvas)

        #self._gui_show_layout()
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
        """ 
        TODO: Create a ViewReference object that will be placed in ViewRefGenFields canvas
        The ViewRef object should contain its own way of adding/deleting view fields

        ViewRefGenFields -parent of-> ViewReference
        ModelReferenceDatabase -parent of-> ModelReference
        """
        self.test = ttk.Label(self.ui_fields_canvas, text="Hello!", background="blue", anchor="center")
        self.test.pack(expand=True, fill=tk.BOTH)
        self.test2 = ttk.Label(self.ui_fields_canvas, text="Goodbye!", background="blue", anchor="center")
        self.test2.pack(expand=True, fill=tk.BOTH)
        self.ui_fields_canvas.create_window((100, 1000), window=self.test, anchor="center")
        self.ui_fields_canvas.create_window((100, 500), window=self.test2, anchor="center")
 
    #TODO:Add entry creation and deletion function.
    # This should keep track of how many references there are
    def gui_add_entry(self):
        # Check if over REFGEN_MAX_FIELDS
        # Trigger popup if that happens
        self.ref_count += 1

    def gui_delete_entry(self):
        # Check if over REFGEN_MAX_FIELDS
        self.ref_count -= 1


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

    def generate_entries(self):
        ...

    def handle_doctype_updated(self) -> None:
        ...

    def handle_start_value_updated(self) -> None:
        #TODO: Update ModelReferenceDatabase.iteration_start_value
        # For each ModelReference, update value_iterable
        # GUI: update ViewRefGenOptions.ui_end_value
        ...
    def handle_step_value_updated(self) -> None:
        # TODO:
        # Update end label value
        # If ViewRefGenFields.index_reference_in_view
        # is less than the new step count, then decrement it
            # Then delete reference view object in ViewRefGenFields
            # Then delete reference model entry in Reference_Database list
        # Update vars_iteration_step_value in ModelReferenceDatabase
        # Rebuild database:
            # For all ReferenceModel in ModelReferenceDatabase:
            # 
            
        #
        ...

    def handle_generate_button_clicked(self) -> None:
        # TODO: Rename to "generate_bib"?
        # This button is probably poorly named. Should be update references,
        # will have to see how well functions perform if we're constantly updating
        # Actually, generate button should be used if we want to actually output the .bib file
        ...

    def handle_clear_fields_button_clicked(self) -> None:
        # TODO: Clears all fields in the reference that's currently in view
        # that does not have the pattern. Except for date and author.
        # TODO: Clear fields button modifies model database, and then view_fields
        # Any fields that do not have the pattern are cleared and values replaced with an empty string
        # Implement controller.clear_fields function
        # Interactions:
        # - Update the fields of the reference currently in view in ModelReferenceDatabase to be empty strings if no pattern found in value
        # - Update view_fields entries for the current view.
        ...

    def handle_delete_iteration_button_clicked(self) -> None:
    # Rules:
        # Deactivate button if there is only one reference in list left.
        # TODO:  Need to set as deactivate if there's only one iteration left.
        # To implement controller.delete_iteration.
        # Need to fetch index value of current iteration that's in view.
        # To implement index value in view that's in the ViewRefGenFields.
        # Figure out how to draw/redraw fields. Need to figure out how to cache
        # it for performance and not redrawing everytime
        # Interactions:
        # - Decrement step entry value
        # - Update number_iterations value
        # - Update model references index
        ...

    def handle_previous_button_clicked(self) -> None:
    # Rules: reference count cannot be zero. There should always be at least one 
        # Count cannot be zero.

        # Decrement ViewRefGenFields.index_reference_in_view
        # Hides buttons in view, ViewCanvas needs to rebuild based on
        # ReferenceModel thats in view

        # If the index in view is the first, then deactivate the previous button
        # This should also handle the case where there is only one reference.
        
        # TODO: Updates the fields that's in view.
        # Redraws field to be the next or previous one.
        # Previous is disabled if current field in view is the first
        # To implement view_next/previous iteration functions.
        # These are mainly visual but provides user
        # access to which reference can be
        # modified at any given moment.
        ...

    def handle_next_button_clicked(self) -> None:
        # Increments ViewRefGenFields.index_reference_in_view
        # Hides buttons in view, rebuilds them from ReferenceModel

        # If index in view is the last, then deactivate next button
        # This should also handle the case where there is only one reference.
        ...

    def handle_field_value_updated(self, field_name: str) -> None:
        # Triggered when value is updated and clicked off
        # Updates ReferenceModel from UI interaction
        # Need to pass which reference is in view so the model
        # knows which reference to update
        # Triggers 
        ...

    # Functions below are to be removed, they're just placeholders.
    # Better suited if they were in the View/Model
        # def fetch_model_iteration_start_value(self) -> int:
        #     return self.model.vars_iteration_start_value

        # def update_model_iteration_start_value(self, value: int):
        #     self.model.vars_iteration_start_value = value

        # def fetch_model_iteration_step_value(self) -> int:
        #     # THis should update the view
        #     return self.model.vars_iteration_step_value

        # def update_model_iteration_step_value(self, value: int):
        #     self.model.vars_iteration_step_value = value


        # def update_view(self, view, model):
        #     ...

        # def update_options_iterations_start(self):
        #     ...

        # def update_option_iteration_number(self):
        # If reference in database is less than iteration number, then delete.
        ...
    # def update_field(self):
