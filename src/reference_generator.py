import copy
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
from .utils import ScrollBar, _debug_log_fn_decorator
from .reference_model import ModelReferenceDatabase
from .reference_type import DROPDOWN_REFERENCE_TYPES


class WrapperRefGen(ttk.Frame):
    """
    Parent GUI Frame container to contain "reference generator options" container
    and the "reference fields" container.
    UI object hierarchy:
    Wrapper RefGen -> ContainerRefGen (grid)
                            -> WrapperRefGenOptions
                                    ->ViewRefGenOptions (grid, connected to controller)
                                        ->Widgets and user interactions
                            -> ContainerRefGenFields
                                    ->WrapperRefGenFields (pack)
                                            -> .ui_fields_canvasCanvas
                                                ->ViewRefGenFields (pack, connected to controller)
                                                        ->ViewReferenceField
                                                            ->Widgets and user interactions                                                   
                                                        ->ViewReferenceField
                                                            ->Widgets and user interactions                                                   
                                                        ...

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
        self.wrapper_refgen_fields = ContainerRefGenFields(self)

        self.wrapper_refgen_options.grid(column=0, row=0, sticky="nsew")
        self.wrapper_refgen_fields.grid(column=0, row=1, sticky="nsew")

    def initialise_mvc(self):
        """
            Creating model and linking model and views to controller.
            Controller links to ViewRefGenOptions and ViewRefgenFields.
            ViewRefgenFields is nested in frames for UI purposes.
        """
        self.refgen_model = ModelReferenceDatabase()
        self.controller_refgen = ControllerReferenceGenerator(
            self.refgen_model, 
            self.wrapper_refgen_options.view_frame, 
            self.wrapper_refgen_fields.view_frame.view_refgen_fields,
        )
        self.wrapper_refgen_options.view_frame.controller = self.controller_refgen
        self.wrapper_refgen_fields.view_frame.view_refgen_fields.controller = self.controller_refgen

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
        #self.setup_view_variables()
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
        if self.controller is None:
            raise Exception("Error: controller not set for ViewRefGenOptions")

        # Default to "Report"
        self.vars_options_doctype_dropdown = ttk.StringVar(self, value=list(DROPDOWN_REFERENCE_TYPES.keys())[0])
        self.vars_options_doctype_dropdown.trace_add("write", self.controller.handle_doctype_updated)

        #TODO: Figure out what values to keep inside of View, and what to keep in model
        # Probably will need to delete this function if we're storing everything in the model
        # Need to be careful and match these to the model, or make the model match these instead.
        self.vars_options_start_entry = ttk.StringVar(self, value=str(DEFAULT_OPTIONS_START))
        self.vars_options_start_entry.trace_add("write", self.controller.handle_start_value_updated)

        #TODO: To change when step value is updated, or if iteration is deleted
        # Unsure if this should be placed in ViewRefGenFields
        self.vars_options_index_reference_in_view = ttk.StringVar(self, value="1")

        self.vars_options_step_entry = ttk.StringVar(self, value=str(DEFAULT_OPTIONS_NUMBER_ITERATIONS))
        self.vars_options_step_entry.trace_add("write", self.controller.handle_step_value_updated)

        self.vars_options_number_iterations_label = ttk.StringVar(self, value=f"{self.vars_options_index_reference_in_view}/{DEFAULT_OPTIONS_NUMBER_ITERATIONS}")
        self.vars_options_end_value_label = ttk.StringVar(value=f"{DEFAULT_OPTIONS_START + DEFAULT_OPTIONS_NUMBER_ITERATIONS}")

    def gui_setup_frames(self):
        if not self.controller:
            raise Exception("Error: controller not set for ViewRefGenOptions")
        self.ui_options_header_iteration_settings = ttk.Label(self, text="Iteration settings")

        self.ui_options_doctype_label = ttk.Label(self, text="Document type")
        self.ui_options_doctype_dropdown = ttk.Combobox(self, values=list(DROPDOWN_REFERENCE_TYPES.keys()), textvariable=self.vars_options_doctype_dropdown)

        self.ui_options_start_label = ttk.Label(self, text="Start")
        self.ui_options_start_entry = ttk.Entry(self, textvariable=self.vars_options_start_entry)

        self.ui_options_step_label = ttk.Label(self, text="N° of iterations") 
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
        # ui_step_entry is modified. Or when iteration is deleted
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


class ContainerRefGenFields(ttk.Frame):
    """
        Container for RefGenFields for placement in parent frame, and to avoid
        pack() / grid() conflicts.
    """
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent = container
        self.view_frame = WrapperRefGenFields(self)
        self.view_frame.pack(expand=True, fill=tk.BOTH)


class WrapperRefGenFields(ttk.Frame):
    """
        Wrapper for RefGenFields for creating a scrollable canvas.
    """
    def __init__(self, container=None, **kw):
        ttk.Frame.__init__(self, container, **kw)

    # TODO: index_reference_in_view is used to keep track of which Reference in
    # the canvas/table is displayed
    # To implement getter and setter functions to expose to controller
    # Getter function will be used for ui_number_iterations_label in Options
        self.parent = container
        self.controller: ControllerReferenceGenerator | None = None
        self.ui_fields_canvas = ttk.Canvas(self)
        self.ui_fields_canvas_scrollbar = ScrollBar(self, self.ui_fields_canvas)
        self.view_refgen_fields = ViewRefGenFields(self.ui_fields_canvas)

        self.gui_setup_canvas_layout()

    def gui_setup_canvas_layout(self):
        self.ui_fields_canvas.create_window((100,1000), window=self.view_refgen_fields, anchor="center")

    def _gui_show_layout(self):
        self.ui_fields = ttk.Label(self, text="Fields", background="blue", anchor="center")
        #self.ui_fields.grid(column=0, row=0, sticky="nsew", columnspan=4, rowspan=4)
        self.ui_fields.pack(expand=True, fill=tk.BOTH)

        self.test = ttk.Label(self.ui_fields_canvas, text="Hello!", background="blue", anchor="center")
        self.test.pack(expand=True, fill=tk.BOTH)
        self.ui_fields_canvas.create_window((100, 1000), window=self.test, anchor="center")
        self.test2 = ttk.Label(self.ui_fields_canvas, text="Goodbye!", background="blue", anchor="center")
        self.test2.pack(expand=True, fill=tk.BOTH)
        self.ui_fields_canvas.create_window((100, 1000), window=self.test, anchor="center")
        self.ui_fields_canvas.create_window((100, 500), window=self.test2, anchor="center")
 

class ViewRefGenFields(ttk.Frame):
    """
        Represents the fields for a given Reference entry in
        ModelReferenceDatabase. Wrapper for ViewReferenceField, to be placed in
        canvas for scrolling. ViewRefGenFields objects are contained within

        TODO: Implement auto resize for adding custom fields. Need to implement regular fields first.
        #TODO: Feature: ability to add custom fields up to REFGEN_MAX_FIELDS
    """
    def __init__(self, container=None, **kw):
        
        ttk.Frame.__init__(self, container, **kw)
        self.parent = container
        self.index_reference_in_view: int = 0
        self.controller: ControllerReferenceGenerator | None = None
        self.fields: list[ViewReferenceField] = []


    def get_index_reference_in_view(self) -> int:
        return self.index_reference_in_view

    def create_reference_fields(self, model_fields_dict: dict):
        # TODO: Implement a for loop that goes through each key:values
        # that are not Author, Report or Year
        # Add conditions for Author and Editors field
        # Create a new ViewReferenceField() passing field_name and field_value.
        # TODO: Create initialise model function in model
        ...

    def delete_reference_fields(self):
        ...

    def gui_generate_reference_in_view(self, model_fields_dict: dict):
        """
            Generates ViewReferenceField UI objects inside of ViewRefGenFields
            canvas to be displayed.

            Input: 
            model_fields_dict corresponds to an input dictionary of
            dict[field_name: field_value] pairs. Special fields corresponding
            to a list like Author and Editor logic are to be handled by ViewReferenceField logic.
        """
        for field_name, field_value in model_fields_dict.items():
            self.fields.append(ViewReferenceField(self, field_name, field_value))

        # TODO: Test if scrollable area needs to be updated since the number of fields would change.
        
    def gui_delete_reference_in_view(self):
        """
            Destroys all children within the ViewRefGenFields frame.
            This assumes that all of the frame's children are ViewReferenceField.
            TODO: Check if this affects the scrollable area and check if it
            needs to be resized
        """
        for field in self.winfo_children():
            field.destroy()


class ViewReferenceField(ttk.Frame):
    """
        Generic class object representing the label and entry field of a given reference in view.
        Automatically adds callback function for the fields that are being updated.
        Fields for dates and lists of authors/editors should be handled differently.

        Inputs: 

        ViewRefGenFields: container with a linked controller as an input
        field_name: String for creating label
        field_value (optional): String for populating entry field.


        TODO: Add conditions for creating [Authors] widget, conditions for date entry widget.
        Figure out drag/drop mechanics for reordering author.
    """
    def __init__(self, container: ViewRefGenFields, field_name: str, field_value: str="", **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent: ViewRefGenFields = container

        self.gui_setup_grid_layout()
        self.setup_view_variables(field_value)
        self.gui_create_widgets(field_name)


        self.pack(side=tk.TOP, fill=tk.X)

    def get_field_value(self) -> str:
        return self.vars_field_value.get()
    
    def gui_setup_grid_layout(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

    def setup_view_variables(self, field_value):
        if self.parent is None:
            raise Exception(f"Error - unable to setup view variables: Inaccessible controller - no parent set for ViewReferenceField '{self}'")
        if self.parent.controller is None:
            raise Exception(f"Error - unable to setup view variables: Inaccessible controller - no controller set for '{self.parent}'")

        self.vars_field_value = ttk.StringVar(self, value=field_value)
        self.vars_field_value.trace_add("write", self.parent.controller.handle_field_value_updated)

        return

    def gui_create_widgets(self, field_name: str):
        self.label_field_name = ttk.Label(self, text=f"{field_name.capitalize()}")
        self.label_field_name.grid(column=0, row=0, sticky="nsew", padx=(25, 10))
        self.field_entry = ttk.Entry(self, textvariable=self.vars_field_value)
        self.field_entry.grid(column=1, row=0, sticky="nsew", padx=(25, 10))

        return

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

    @_debug_log_fn_decorator
    def handle_doctype_updated(self, variable_name: str, index: str, mode: str) -> None:
        """
            Called when ViewRefGenOptions.vars_options_doctype_dropdown is updated.
            Updates all fields in ReferenceModel in ModelReferenceDatabase to
            have the same dictionary signature as the new doctype, with the
            updated item_type. Effectively keeps all fields in the existing
            references that are in common with the new doctype. Updates the
            Reference in view to the updated document type.
            
            If field name does not exist in the refernce, then create it in the
            ReferenceModel.fields dictionary.
            If it does not exist, then add the field. Handles fields that
            corresponds to a list.

            Regenerates ViewRefGenFields to display the new fields, as
            per ViewRefGenFields.index_reference_in_view
        """
        doctype: str = self.view_options.vars_options_doctype_dropdown.get()

        new_doctype_fields_template: dict = DROPDOWN_REFERENCE_TYPES[doctype].value
        # Get all field names except for "item_type" in the new document template.
        new_doctype_fields_list: list[str] = [field_name for field_name in new_doctype_fields_template.keys() if field_name != "item_type"]

        for reference in self.model.references:
            reference_fields = list(reference.fields.keys())

            for field_name in reference_fields:
                if field_name != "item_type" and field_name not in new_doctype_fields_list:
                    del reference.fields[field_name]

            for field_name, field_value in new_doctype_fields_template.items():
                if field_name not in reference.fields:
                    # Create field if it does not exist, detect if field is a list or a string
                    if isinstance(field_value, list):
                        reference.fields[field_name] = []
                    else:
                        reference.fields[field_name] = field_value

        # Call ViewReferenceTable to display the new model.
        index_reference_in_view: int = self.view_fields.get_index_reference_in_view()
        dictionary_in_view: dict = self.model.references[index_reference_in_view].fields
        self.view_fields.gui_delete_reference_in_view()
        self.view_fields.gui_generate_reference_in_view(dictionary_in_view)
        return
        
    @_debug_log_fn_decorator
    def handle_start_value_updated(self, variable_name: str, index: str, mode: str) -> None:
        #TODO: Update ModelReferenceDatabase.iteration_start_value
        # For each ModelReference in ModelReferenceDatabase, update value_iterable.
        # GUI: update ViewRefGenOptions.ui_end_value
        #  In ViewRefGenFields: Reinitialise by calling delete_reference_fields
        #  then create_reference_fields because vars_ in ModelReferenceDatabase has been updated
        ...

    def handle_step_value_updated(self, variable_name: str, index: str, mode: str) -> None:
        # TODO:
        # Update end label value
        # If new step value is less than previous:
            # in ModelReferenceDatabase: delete all entries that exceed the new
            # step value ModelReferenceDatabase.references[:step]
            # If ViewRefGenFields.index_reference_in_view
                # is less than the new step count, then decrement reference_in_view, 
                #  in ViewRefGenFields
                    # call delete_reference_fields call create_reference_fields for
                    # the new last entry,  in
                    # ModelReferenceDatabase[index_reference_in_view].
            # Else: Leave index_reference_in_view as-is.
        # If new step value is more than previous:
            # Triggers model.add_model_reference, map new reference_model
            # fields to the last reference_model fields
        # Update vars_iteration_step_value in ModelReferenceDatabase
        # Rebuild database:
        # For all ReferenceModel in ModelReferenceDatabase:
        # 
        ...

    def handle_generate_button_clicked(self, variable_name: str, index: str, mode: str) -> None:
        # TODO: Rename to "generate_bib"?
        # Send ModelReferenceDatabase references to output window where user
        # can copy output or save to file
        ...

    def handle_clear_fields_button_clicked(self, variable_name: str, index: str, mode: str) -> None:
        # TODO: 
        # For current reference in view, update ModelReference where all fields except
        # author and date are equal to empty string
        # Clear fields button modifies model database, and then view_fields
        # Any fields that do not have the pattern are cleared and values replaced with an empty string
        # Implement controller.clear_fields function
        # Interactions:
        # - Update the fields of the reference currently in view in ModelReferenceDatabase to be empty strings if no pattern found in value
        # - Update view_fields entries for the current view.
        ...

    def handle_delete_iteration_button_clicked(self, variable_name: str, index: str, mode: str) -> None:
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

    def handle_field_value_updated(self, variable_name: str, index: str, mode: str) -> None:
        # Get field_name
        # Triggered when value is updated and clicked off
        # Updates ReferenceModel from UI interaction
        # Need to pass which reference is in view so the model
        # knows which reference to update
        # Triggers 
        ...
