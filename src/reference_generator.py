import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.validation import add_range_validation

from .settings import (
    DEFAULT_OPTIONS_START,
    DEFAULT_OPTIONS_NUMBER_ITERATIONS,
    REFGEN_MAX_START_VALUE,
    REFGEN_MAX_ITERATIONS,
)
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
        self.rowconfigure(1, weight=3)
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
        self.controller = ControllerReferenceGenerator(
            self.refgen_model, 
            self.wrapper_refgen_options.view_frame, 
            self.wrapper_refgen_fields.view_frame.view_refgen_fields,
        )
        self.wrapper_refgen_options.view_frame.controller = self.controller
        self.wrapper_refgen_fields.view_frame.view_refgen_fields.controller = self.controller
        self.controller.initialise_mvc()

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
        #self._gui_show_layout()

    def setup_view_variables(self):
        if self.controller is None:
            raise Exception("Error: controller not set for ViewRefGenOptions")

        # Default to "Report"
        self.vars_options_doctype_dropdown = ttk.StringVar(self, value=list(DROPDOWN_REFERENCE_TYPES.keys())[0])
        self.vars_options_doctype_dropdown.trace_add("write", self.controller.handle_doctype_updated)

        self.vars_options_iteration_start_entry = ttk.IntVar(self, value=DEFAULT_OPTIONS_START)
        self.vars_options_iteration_start_entry.trace_add("write", self.controller.handle_start_value_updated)
        
        self.vars_options_iteration_step_entry = ttk.IntVar(self, value=DEFAULT_OPTIONS_NUMBER_ITERATIONS)
        self.vars_options_iteration_step_entry.trace_add("write", self.controller.handle_step_value_updated)

        self.vars_options_index_reference_in_view = ttk.IntVar(self, value=DEFAULT_OPTIONS_START)

        self.vars_options_number_iterations_label = ttk.StringVar(self, value=f"1 / {DEFAULT_OPTIONS_NUMBER_ITERATIONS}")
        self.vars_options_end_value_label = ttk.IntVar(value=(DEFAULT_OPTIONS_START + DEFAULT_OPTIONS_NUMBER_ITERATIONS))
 
    def gui_setup_grid_layout(self):
        # Create 4x4 layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

    def gui_setup_frames(self):
        if not self.controller:
            raise Exception("Error: controller not set for ViewRefGenOptions")
        self.ui_options_header_iteration_settings = ttk.Label(self, text="Iteration settings")

        self.ui_widget_separator = ttk.Separator(self, orient=tk.HORIZONTAL, bootstyle="secondary")

        self.ui_options_doctype_label = ttk.Label(self, text="Document type")
        self.ui_options_doctype_dropdown = ttk.Combobox(self, values=list(DROPDOWN_REFERENCE_TYPES.keys()), textvariable=self.vars_options_doctype_dropdown)

        self.ui_options_start_label = ttk.Label(self, text="Start")
        self.ui_options_start_entry = ttk.Spinbox(
            self, 
            width=15,
            from_=0, 
            to=REFGEN_MAX_START_VALUE, 
            textvariable=self.vars_options_iteration_start_entry, 
            wrap=False,
        )
        add_range_validation(self.ui_options_start_entry, 0, REFGEN_MAX_START_VALUE, when="key")

        self.ui_options_step_label = ttk.Label(self, text="N° of iterations") 
        self.ui_options_step_entry = ttk.Spinbox(
            self, 
            width=15,
            from_=1, 
            to=REFGEN_MAX_ITERATIONS, 
            textvariable=self.vars_options_iteration_step_entry, 
            wrap=False,
        )
        add_range_validation(self.ui_options_step_entry, 1, REFGEN_MAX_ITERATIONS, when="key")

        self.ui_options_end_label = ttk.Label(self, text="End")
        self.ui_options_end_value_label = ttk.Label(self, textvariable=self.vars_options_end_value_label)

        self.ui_options_header_preview_label = ttk.Label(self, text="Preview references")

        self.ui_options_generate_button = ttk.Button(self, width=15, text="Generate entries", command=self.controller.handle_generate_button_clicked)
        self.ui_options_clear_fields_button = ttk.Button(self, width=15, text="Clear fields", command=self.controller.handle_clear_fields_button_clicked)

        self.ui_options_delete_iteration_button = ttk.Button(self, width=15, text="Delete iteration", command=self.controller.handle_delete_iteration_button_clicked)

        self.ui_options_number_iterations_label = ttk.Label(self, textvariable=self.vars_options_number_iterations_label)

        self.ui_options_previous_iteration_button = ttk.Button(self, width=15, text="Previous", command=self.controller.handle_previous_button_clicked)
        self.ui_options_next_iteration_button = ttk.Button(self, width=15, text="Next", command=self.controller.handle_next_button_clicked)

        # Place objects in RefGenOptions frame
        self.ui_widget_separator.grid(column=0, row=4, columnspan=4, sticky="sew")
        self.ui_options_header_iteration_settings.grid(column=0, row=0, sticky="nsew", columnspan=2, padx=(15, 0))
        self.ui_options_doctype_label.grid(column=0, row=1, sticky="nsew", padx=(15, 0))
        self.ui_options_doctype_dropdown.grid(column=1, row=1)
        self.ui_options_start_label.grid(column=0, row=2, sticky="nsew", padx=(15, 0))
        self.ui_options_start_entry.grid(column=1, row=2)
        self.ui_options_step_label.grid(column=0, row=3, sticky="nsew", padx=(15, 0))
        self.ui_options_step_entry.grid(column=1, row=3)
        self.ui_options_end_label.grid(column=0, row=4, padx=(15, 0))
        self.ui_options_end_value_label.grid(column=1, row=4)

        self.ui_options_header_preview_label.grid(column=2, row=0, sticky="nsew", columnspan=2)
        self.ui_options_generate_button.grid(column=2, row=1, columnspan=2)
        self.ui_options_clear_fields_button.grid(column=2, row=2)
        self.ui_options_delete_iteration_button.grid(column=3, row=2)
        self.ui_options_number_iterations_label.grid(column=2, row=3, columnspan=2)
        self.ui_options_previous_iteration_button.grid(column=2, row=4)
        self.ui_options_next_iteration_button.grid(column=3, row=4)

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
        self.parent = container
        self.controller: ControllerReferenceGenerator | None = None
        self.gui_setup_canvas_layout()
        #self._gui_show_layout()

    def gui_setup_canvas_layout(self):
        self.view_refgen_fields = ViewRefGenFields(self)
        self.view_refgen_fields.pack(expand=True, fill=tk.BOTH)

    def _gui_show_layout(self):
        self.test = ttk.Label(self, text="Hello!", background="blue", anchor="center")
        self.test.pack(expand=True, fill=tk.BOTH)
        self.test2 = ttk.Label(self, text="Goodbye!", background="blue", anchor="center")
        self.test2.pack(expand=True, fill=tk.BOTH)
 

class ViewRefGenFields(ScrolledFrame):
    """
    Represents the fields for a given Reference entry in
    ModelReferenceDatabase. Wrapper for ViewReferenceField, to be placed in
    canvas for scrolling. ViewRefGenFields objects are contained within

    """
    def __init__(self, container=None, **kw):
        ScrolledFrame.__init__(self, container, **kw)
        self.parent = container
        self.controller: ControllerReferenceGenerator | None = None
        self.fields: list[ViewReferenceField] = []
        #self._gui_show_layout()

    def _gui_show_layout(self):
        for i in range(5):
            field_label = ttk.Label(self, text="Fields", background="blue", anchor="center", font=("Arial", 12))
            field_label.pack(expand=True, fill=tk.BOTH, padx=0, pady=20, anchor="n")

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
            if field_name == "item_type":
                continue
            view_reference = ViewReferenceField(self, field_name, field_value)
            self.fields.append(view_reference)

        
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
    """
    def __init__(self, container: ViewRefGenFields, field_name: str, field_value: str="", **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent: ViewRefGenFields = container

        self.gui_setup_grid_layout()
        self.setup_view_variables(field_value)
        self.gui_create_widgets(field_name)

        self.pack(side=tk.TOP, fill=tk.X, padx=0, pady=25, anchor="n")

    def get_field_value(self) -> str:
        return self.vars_field_value.get()
    
    def gui_setup_grid_layout(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

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
    def gui_create_widgets(self, field_name: str) -> None:
        if field_name == "url":
            self.label_field_name = ttk.Label(self, text=f"{field_name}")
        else:
            self.label_field_name = ttk.Label(self, text=f"{field_name.capitalize()}")
        self.label_field_name.grid(column=0, row=0, sticky="nsew", padx=(25, 10), pady=(0, 5))
        self.field_entry = ttk.Entry(self, textvariable=self.vars_field_value)
        self.field_entry.grid(column=0, row=1, sticky="nsew", padx=(25, 35))

        return

class ControllerReferenceGenerator:
    """
    Controller object linking user interactions to the view component (GUI),
    and model component (internal data).
    
    Ex: If X button is clicked, then Y happens to internal data, and Z GUI
    element is updated.
    """
    def __init__(self, model: ModelReferenceDatabase, view_options: ViewRefGenOptions, view_fields: ViewRefGenFields):
        self.model = model
        self.view_options = view_options
        self.view_fields = view_fields

    def initialise_mvc(self):
        if self.view_options.controller is None:
            self.view_options.controller = self

        if self.view_fields.controller is None:
            self.view_fields.controller = self
        self.view_options.setup_view_variables()
        self.view_options.gui_setup_frames()

        # Disable buttons as there is only one reference on initialisaiton
        self.refresh_view_options_reference_in_view()
        # Show first reference
        self.refresh_view_fields_reference_in_view()

    def refresh_view_fields_reference_in_view(self) -> None:
        """
        Called whenever the model is updated so the view component is kept up
        to date.

        Behaviour:
            Refreshes the current reference in view. Called when references are
            updated in ModelReferenceDatabase.

        Logic:
            If the reference in view is the first one:
            Disable the following buttons:
                - Delete iteration: the first reference shouldn't be deleted
                - Previous button: no reference to go back on.
            Otherwise, keep it enabled.

            If the reference is the last:
                - Next button: no more reference to view.
       """
        # Call ViewReferenceTable to display the new model.
        index_reference_in_view: int = self.view_options.vars_options_index_reference_in_view.get()
        dictionary_in_view: dict = self.model.references[index_reference_in_view].fields
        self.view_fields.gui_delete_reference_in_view()
        self.view_fields.gui_generate_reference_in_view(dictionary_in_view)
        return

    def refresh_view_options_reference_in_view(self) -> None:
        """
        Triggered when a function that would modify the number of references in
        the database, or the reference in view.

        Behaviour:
            Disable or enable buttons depending on whether the reference in
            view is first or last.
        """
        index_reference_in_view: int = self.view_options.vars_options_index_reference_in_view.get()
        last_index = len(self.model.references) - 1

        if index_reference_in_view == 0:
            # Index is the first, disable Delete and Previous button
            self.view_options.ui_options_delete_iteration_button.config(state="disabled")
            self.view_options.ui_options_previous_iteration_button.config(state="disabled")

            if len(self.model.references) > 1:
                # More than one one reference, enable next button
                self.view_options.ui_options_next_iteration_button.config(state="normal")
            else:
                # Only one reference, disable next button
                self.view_options.ui_options_next_iteration_button.config(state="disabled")
            return

        if index_reference_in_view == last_index:
            if len(self.model.references) > 1:
                # More than one one reference, enable previous and delete button
                self.view_options.ui_options_delete_iteration_button.config(state="normal")
                self.view_options.ui_options_previous_iteration_button.config(state="normal")
            self.view_options.ui_options_next_iteration_button.config(state="disabled")
            return

        # Index is not first, and it's not the last.
        self.view_options.ui_options_delete_iteration_button.config(state="normal")
        self.view_options.ui_options_previous_iteration_button.config(state="normal")
        self.view_options.ui_options_next_iteration_button.config(state="normal")
        return

    def handle_doctype_updated(self, variable_name: str, index: str, mode: str) -> None:
        """
        Called when ViewRefGenOptions.vars_options_doctype_dropdown is
        updated following user interaction with
        ViewRefGenOptions.ui_options_doctype_dropdown.

        Function holds (variable_name, index, mode) signature as it is called
        everytime a variable is updated.

        Behaviour:
        Modifies the "item_type" field in all ModelReference using
        ModelReferenceDatabase.update_reference_doctype()
            - For each ModelReferenceDatabase.references of type ModelReference
                - ModelReference.fields to match the dictionary signature of
                    the new document type as defined in DROPDOWN_REFERENCE_TYPES
                    which links the UI dropdown reference type to the
                    ReferenceType enum, containing the field signature of a given
                    `item_type`/ReferenceType/document type.
            - Rebuilds the reference in view in RefGenFields to reflect the new
                internal changes.

        Logic:
            - If field name does not exist in the reference, then create it with
            an empty field value in the ModelReference.fields dictionary.
            - If the field name does exist, then leave it as-is.
        """
        doctype: str = self.view_options.vars_options_doctype_dropdown.get()
        self.model.update_reference_doctype(doctype)
        self.refresh_view_fields_reference_in_view()
        return
        
    def handle_start_value_updated(self, variable_name: str, index: str, mode: str) -> None:
        """
        Called when ViewRefGenOptions.vars_options_iteration_start_entry is
        updated following user interaction with ViewRefGenOptions.ui_options_start_entry.

        Function holds (variable_name, index, mode) signature as it is called
        everytime a variable is updated.

        Behaviour:
            - Updates ModelReferenceDatabase.iteration_start_value to be equal
              to the new value.
            - For each reference, update the value_iterable to be equal to the
              new value plus their position in index.
            - Updates ViewRefGenOptions.vars_options_end_value_label

        Logic:
            - Fetch value from ViewRefGenOptions.vars_options_iteration_start_entry
            - Update end-value label ViewRefGenOptions.vars_options_end_value_label
            - Propagate updated start value to all
              ModelReference.value_iterable in ModelReferenceDatabase using
              ModelReferenceDatabase.update_iteration_start()
            - Refresh reference in view to reflect new changes.
        """
        new_start_value: int = self.view_options.vars_options_iteration_start_entry.get()
        step_value: int = self.view_options.vars_options_iteration_step_entry.get()
        self.view_options.vars_options_end_value_label.set(new_start_value + step_value)

        self.model.update_iteration_start(new_start_value)
        self.refresh_view_fields_reference_in_view()
        self.refresh_view_options_reference_in_view()
        return

    def handle_step_value_updated(self, variable_name: str, index: str, mode: str) -> None:
        """
        Called when ViewRefGenOptions.vars_options_step_entry is updated
        following user interaction with ViewRefGenOptions.ui_options_step_entry.

        Function holds (variable_name, index, mode) signature as it is called
        everytime a variable is updated.

        Behaviour:
        - Updates GUI: vars_options_iteration_start_entry
        - Updates ModelReferenceDatabase.vars_iteration_step_value
        - Cull excess references if the step value is less than before, or
            add new references if the step value is greater. Adds copies of
            the first reference but with the value iterated by the step
            value. 

            Functionality is designed as such, as the user can modify the
            fields and even delete the pattern string for any number of iterations.
            Using the first value as a copy ensures more stable usage.


        Logic:
            Use self.model.update_iteration_step() 
            - If new step value is less than the previous:
                - Delete all entries that exceed the new step value in
                    ModelReferenceDatabase.references[: new_step_value]
            - If new step value is more than the previous:
                - Append new ModelReference where the value_iterable is 
                For each reference in ModelReferenceDatabase: 
                - Update value_iterable
                - Except for the first reference, replace the pattern in
                    each field value in the reference with the value_iterable
                    (if pattern is present).
            ViewOptions
            - If ViewRefGenFields.index_reference_in_view is greater than the
                new step count, then reference in view decrement to the step
                count, and ViewRefGenFields.refresh_view_fields_reference_in_view().
                Otherwise, leave the reference in view as-is.
        """
        start_value: int = int(self.view_options.ui_options_start_entry.get())
        new_step_value: int = int(self.view_options.ui_options_step_entry.get())

        # If step is less than previous and the reference in view is at a
        # greater index than the new step, then set the last reference (new step value - 1) as the
        # new reference in view.
        # If step is greater than previous, leave as-is.
        index_reference_in_view = self.view_options.vars_options_index_reference_in_view.get()

        # Updating model and index in view.
        self.model.update_iteration_step(new_step_value)

        if index_reference_in_view > (new_step_value - 1):
            self.view_options.vars_options_index_reference_in_view.set(new_step_value - 1)
            index_reference_in_view = new_step_value - 1

        # Updating labels, end value
        self.view_options.vars_options_end_value_label.set(start_value + new_step_value)
        self.view_options.vars_options_number_iterations_label.set(f"{index_reference_in_view + 1} / {new_step_value}")

        self.refresh_view_fields_reference_in_view()
        # Disable buttons depending on index in view.
        self.refresh_view_options_reference_in_view()
        return

    def handle_generate_button_clicked(self) -> None:
        """
        Call self.model.convert_refs_to_bib() function, then send output to Console window.
        TODO: Create console window first. To determine how it can be handled.
        """
        output_str = self.model.convert_refs_to_bib()
        # Send output to output window.

    def handle_clear_fields_button_clicked(self) -> None:
        """
        For the current reference in view, update ModelReference where all
        fields - except fields with the pattern, author, and date - are equal to an empty string.
        The button should deactivate if the reference in view is the first.
        """
        index_reference_in_view = self.view_options.vars_options_index_reference_in_view.get()
        self.model.clear_model_reference_fields(index_reference_in_view)
        self.refresh_view_fields_reference_in_view()
        return

    def handle_delete_iteration_button_clicked(self) -> None:
        """
        Called when ViewRefGenOptions.ui_options_delete_iteration_button is
        clicked.

        Behaviour:
        - If the current reference in view is not the first, then delete the
          reference in view, and switch the reference in view to the previous
          reference.
        - Use self.refresh_view_options_reference_in_view() to check if the
          reference in view is the last one to disable the appropriate buttons
          (e.g., deactivate delete iteration button for the first reference and
          disable the Previous button). Then update labels.
        """
        index_reference_in_view: int = self.view_options.vars_options_index_reference_in_view.get()
        start_value: int = self.view_options.vars_options_iteration_start_entry.get()
        step_value: int = self.view_options.vars_options_iteration_step_entry.get()
        last_index: int = len(self.model.references) - 1

        if index_reference_in_view == 0:
            # First reference should not be deleted.
            # TODO: Log error, find better logging implementation
            return

        self.model.delete_model_reference(index_reference_in_view)

        if index_reference_in_view == last_index:
            # If the reference in view is the last index, then decrement alongside the step value
            index_reference_in_view -= 1
        step_value -= 1

        # Update variables
        self.view_options.vars_options_index_reference_in_view.set(index_reference_in_view)
        self.view_options.vars_options_iteration_step_entry.set(step_value)

        # Updating labels, end value
        self.view_options.vars_options_number_iterations_label.set(f"{index_reference_in_view + 1} / {step_value}")
        self.view_options.vars_options_end_value_label.set(start_value + step_value)

        self.refresh_view_options_reference_in_view()
        self.refresh_view_fields_reference_in_view()

    def handle_previous_button_clicked(self) -> None:
        index_reference_in_view: int = self.view_options.vars_options_index_reference_in_view.get()

        # catch error if function is activated somehow even when index is 0
        if index_reference_in_view == 0:
            # TODO: log error
            return

        index_reference_in_view -= 1
        self.view_options.vars_options_index_reference_in_view.set(index_reference_in_view)
        # Update label
        step_value: int = int(self.view_options.ui_options_step_entry.get())
        self.view_options.vars_options_number_iterations_label.set(f"{index_reference_in_view + 1} / {step_value}")
        # Deactivate previous button if current reference in view is 0
        self.refresh_view_options_reference_in_view()
        # Generate previous reference in view
        self.refresh_view_fields_reference_in_view()
        return

    def handle_next_button_clicked(self) -> None:
        """
        Triggered when ViewRefGenOptions.ui_options_next_iteration_button is clicked.

        Behaviour:
        - Get the current index, and check if it's the last reference. If it is
          then something has gone wrong, as the Next button should be
          deactivated if it's the last reference in view.
        - Subtract one from the index_reference_in_view, then refresh the frames to show the new reference_in_view.
        """
        index_reference_in_view: int = self.view_options.vars_options_index_reference_in_view.get()

        # catch error if function is activated somehow even when index is the last
        last_index = len(self.model.references) - 1
        if index_reference_in_view == last_index:
            # TODO: log error
            return

        index_reference_in_view += 1

        self.view_options.vars_options_index_reference_in_view.set(index_reference_in_view)
        # Update label
        step_value: int = int(self.view_options.ui_options_step_entry.get())
        self.view_options.vars_options_number_iterations_label.set(f"{index_reference_in_view + 1} / {step_value}")
        # Deactivate next button if current reference in view is the last
        self.refresh_view_options_reference_in_view()
        # Generate next reference in view
        self.refresh_view_fields_reference_in_view()
        return

    def handle_field_value_updated(self, variable_name: str, index: str, mode: str) -> None:
        # Pass field_name.
        # Triggered when value is updated and clicked off
        # Updates ReferenceModel from UI interaction
        # Need to pass which reference is in view so the model
        # knows which reference to update
        # Triggers 
        ...
