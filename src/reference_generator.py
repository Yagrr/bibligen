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
                                                ->ViewRefGenFields (pack, connected to controller)
                                                    ->ViewReferenceField
                                                        ->Widgets and user interactions
                                                    ->ViewReferenceField
                                                        ->Widgets and user interactions
                                                    ->ViewReferenceFieldList
                                                        ->ViewReferenceFieldListElement
                                                            -> Widgets and user interactions
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
            raise ValueError("Error: controller not set for ViewRefGenOptions")

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
    
    View object hierarchy:
    WrapperRefGenfields -> ViewRefGenFields -> ViewReferenceField
                                                    -> ViewReferenceField
                                                    -> ViewReferenceFieldList
                                                        -> ViewReferenceFieldListElement
                                                        -> ViewReferenceFieldListElement
                                                        ...
                                                    -> ViewReferenceField
                                                    ...
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
        self.gui_setup_layout()
        #self._gui_show_layout()

    def gui_setup_layout(self):
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
        self.fields: list[ViewReferenceField | ViewReferenceFieldList] = []
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
        if self.controller is None:
            raise ValueError("Error: controller not set for ViewRefGenFields")

        for field_name, field_value in model_fields_dict.items():
            if field_name == "item_type":
                continue
            elif isinstance(field_value, list):
                self.fields.append(ViewReferenceFieldList(self, field_name, field_value))
            else:
                self.fields.append(ViewReferenceField(self, field_name, field_value))
        
    def gui_delete_reference_in_view(self):
        """
            Destroys all children within the ViewRefGenFields frame.
            This assumes that all of the frame's children are ViewReferenceField.
        """
        for field in self.winfo_children():
            field.destroy()


class ViewReferenceField(ttk.Frame):
    """
    Generic class object representing the label and entry field of a given reference in view.
    Automatically adds callback function for the fields that are being updated.
    Fields for dates and lists of authors/editors should be handled differently.

    No validation is added for fields like "Year" so that the user is able to
    iterate using the pattern.

    Inputs: 

    ViewRefGenFields: container with a linked controller as an input
    field_name: String for creating label
    field_value (optional): String for populating entry field.
    """
    def __init__(self, container: ViewRefGenFields, field_name: str, field_value: str="", **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent: ViewRefGenFields = container
        self.field_name: str = field_name

        self.gui_setup_grid_layout()
        self.setup_view_variables(field_value)
        self.gui_create_widgets(field_name)

        self.pack(side=tk.TOP, fill=tk.X, padx=0, pady=25, anchor="n")

    def get_field_value(self) -> str:
        return self.vars_field_value.get()
    
    def gui_setup_grid_layout(self) -> None:
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def setup_view_variables(self, field_value) -> None:
        if self.parent is None:
            raise Exception(f"Error - unable to setup reference fields view variables: Inaccessible controller - no parent set for ViewReferenceField '{self}'")
        if self.parent.controller is None:
            raise Exception(f"Error - unable to setup reference fields view variables: Inaccessible controller - no controller set for '{self.parent}'")

        self.vars_field_value = ttk.StringVar(self, value=field_value)
        self.vars_field_value.trace_add("write", self.handle_field_value_updated)

        return

    def gui_create_widgets(self, field_name: str) -> None:
        if field_name == "url":
            self.label_field_name = ttk.Label(self, text=f"{field_name}")
        else:
            self.label_field_name = ttk.Label(self, text=f"{field_name.capitalize()}")

        self.field_entry = ttk.Entry(self, textvariable=self.vars_field_value)

        self.label_field_name.grid(column=0, row=0, sticky="nsew", padx=(25, 10), pady=(0, 5))
        self.field_entry.grid(column=0, row=1, sticky="nsew", padx=(25, 35))

        return

    def handle_field_value_updated(self, variable_name: str, index: str, mode: str) -> None:
        if self.parent is None:
            raise Exception(f"Error - unable to setup reference fields view variables: Inaccessible controller - no parent set for ViewReferenceField '{self}'")
        if self.parent.controller is None:
            raise Exception(f"Error - unable to setup reference fields view variables: Inaccessible controller - no controller set for '{self.parent}'")

        self.parent.controller.handle_field_value_updated(self.field_name, self.vars_field_value.get())
        return


class ViewReferenceFieldList(ttk.Frame):
    """
    Class object representing the View model of a list field; the field data
    in a ModelReference of type list.
    Example: {"author": ["John Doe", "Jane Doe"]}

    This class tracks the list of elements in string format so that it can be
    reused to refresh the ViewReferenceFieldListElement that is displayed,
    including its ordering. This is absolutely a very hacky way of changing the
    View since it is done inplace instead of letting the controller do its
    thing, but I couldn't find a better way to change the ordering of  elements
    in ViewReferenceFieldList due to how tkinter works.
    """
    def __init__(self, container: ViewRefGenFields, field_name: str, list_values: list[str]=[""], **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent: ViewRefGenFields = container
        self.list_elements: list[ViewReferenceFieldListElement] = []
        self.list_values: list[str] = list_values
        self.field_name: str = field_name

        self.refresh_list_element_index(self.list_values)
        self.pack(side=tk.TOP, fill=tk.X, padx=0, pady=25, anchor="n")

    def gui_create_widgets(self, list_values: list[str]) -> None:
        """
        Create field element and enables/disables buttons according to a given
        element's position in index.
        """
        # Create the fields with pack and place them top to bottom
        for i, field_value in enumerate(list_values):
            list_element: ViewReferenceFieldListElement = ViewReferenceFieldListElement(self, i, self.field_name, field_value)
            self.list_elements.append(list_element)
            self.refresh_field_element_button_states(list_element)
        return

    def refresh_list_element_index(self, list_values: list[str]) -> None:
        """
        Function that corrects the index attribute of each element.
        This function should be called everytime the order of the elements are modified.
        """
        self.gui_delete_field_elements()
        self.gui_create_widgets(list_values)
        for list_element in self.list_elements:
            self.refresh_field_element_button_states(list_element)
    
    def refresh_field_element_button_states(self, list_element) -> None:
        """
        Modify field element button states based on index.
        This function is invoked here instead of being placed in the
        ViewReferenceFieldListElement class in order to access the length
        of self.list_elements.
        """
        # Activate/deactivate buttons based on index position
        print(f"refresh, list_element.index {list_element.index}")
        if list_element.index == 0:
            # Index is the first, disable move up.
            list_element.ui_button_move_element_up.config(state="disabled") 
            if len(self.list_elements) > 1:
                # More than one element, enable delete and up button
                list_element.ui_button_move_element_down.config(state="normal") 
                list_element.ui_button_delete_element.config(state="normal") 
            else:
                # Only one element, disable both move up and down buttons, and delete buttons
                list_element.ui_button_move_element_down.config(state="disabled") 
                list_element.ui_button_delete_element.config(state="disabled") 
            return

        if list_element.index == len(self.list_elements) - 1:
            # List element is the last and has more than one list element
                # More than one element, enable up button
            list_element.ui_button_move_element_up.config(state="normal") 
            list_element.ui_button_delete_element.config(state="normal") 
            list_element.ui_button_move_element_down.config(state="disabled") 
            return

        # Element is not the first nor the last
        # More than one element, enable all buttons
        list_element.ui_button_move_element_up.config(state="normal") 
        list_element.ui_button_move_element_down.config(state="normal") 
        list_element.ui_button_delete_element.config(state="normal") 
        return

    def gui_delete_field_elements(self) -> None:
        """
        Delete both at index from the list and delete the element itself
        """
        print("View Field List - Delete field elements")
        for i, field_element in enumerate(self.winfo_children()):
            field_element.destroy()
        self.list_elements = []
        return

    def gui_move_element_up(self, index_element: int) -> None:
        """
        Move the view of an element closer to 0, or the top of the list.
        Use refresh_list_element_index to redraw view.
        """
        # signature: requires target_field and index
        print(f"View Field List - Move element up {self.list_values}")
        if self.parent.controller is None:
            raise ValueError("Error - ViewReferenceFieldList - move field list element up: controller not set for ViewRefGenFields")

        if len(self.list_values) <= 1:
            # Check if list_element is not empty or only one element
            raise ValueError("Error - ViewReferenceFieldList - move field list element up: list_values is empty or only has one value")

        if index_element >= len(self.list_values):
            raise IndexError(f"Error - ViewReferenceFieldList - move field list element up: index out of bounds. Index: {index_element} ")

        target_field: str = self.field_name
        # Callback function to handle model
        self.parent.controller.handle_field_list_move_element_up_button_clicked(target_field, index_element)

        print(f"View Field List - Elements after moving up: {self.list_values}")
        self.refresh_list_element_index(self.list_values)
        return

    def gui_move_element_down(self, index_element: int) -> None:
        print(f"View Field List - Move element down {self.list_values}")
        if self.parent.controller is None:
            raise ValueError("Error - ViewReferenceFieldList - move field list element down: controller not set for ViewRefGenFields")

        if index_element >= len(self.list_values) - 1:
            # Check if it's last element, cannot move element further down
            raise IndexError(f"Error - ViewReferenceFieldList - move field list element down: index out of bounds {index_element}, number of elements: {len(self.list_values) - 1}")

        target_field: str = self.field_name
        self.parent.controller.handle_field_list_move_element_down_button_clicked(target_field, index_element)
        print(f"View Field List - Elements after moving down: {self.list_values}")
        self.refresh_list_element_index(self.list_values)

        return

    def handle_field_value_updated(self, index_element: int, new_value: str) -> None:
        print(f"View Field List - Update field value {self.list_values}")
        if self.parent.controller is None:
            raise ValueError("Error - ViewReferenceFieldList - update field list element: controller not set for ViewRefGenFields")

        target_field: str = self.field_name
        # Send data to controller and model
        self.parent.controller.handle_field_list_element_value_updated(target_field, index_element, new_value)

        # Update list elements - no need to refresh the View
        self.list_values[index_element] = new_value
        print(f"View Field List - After element update: {self.list_values}")
        return

    def gui_add_element_below(self, index_element: int) -> None:
        print(f"View Field List - Add element below {self.list_values}")
        if self.parent.controller is None:
            raise ValueError("Error - ViewReferenceFieldList - add field list element: controller not set for ViewRefGenFields")

        target_field: str = self.field_name
        self.parent.controller.handle_field_list_add_element_below_button_clicked(target_field, index_element)

        # Add element below given index with empty string.
        print(f"View Field List - After adding element below {self.list_values}")
        self.refresh_list_element_index(self.list_values)
        print(f"View Field List - After adding element below {self.list_values}")

        return

    def gui_delete_element(self, index_element: int) -> None:
        print(f"View Field List - Deleting element {self.list_values}")
        if self.parent.controller is None:
            raise ValueError("Error - ViewReferenceFieldList - delete field list element: controller not set for ViewRefGenFields")

        if len(self.list_values) <= 1:
            # Check if list_element is not empty or only one element
            # The list cannot be empty.
            raise ValueError("Error - ViewReferenceFieldList - delete field list element: list_values is empty or only has one value")

        if index_element >= len(self.list_values):
            raise IndexError(f"Error - ViewReferenceFieldList - delete field list element: index out of bounds {index_element}, number of elements: {len(self.list_values) - 1}")

        print(f"View Field List - number of elements before deletion: {len(self.list_elements)}")
        print(f"View Field List - number of values before deletion: {len(self.list_values)}")

        target_field: str = self.field_name
        self.parent.controller.handle_field_list_delete_element_button_clicked(target_field, index_element)

        # Update list_values
        print(f"View Field List - After deleting element {self.list_values}")
        self.refresh_list_element_index(self.list_values)
        print(f"View Field List - number of elements after deletion: {len(self.list_elements)}")
        print(f"View Field List - number of values after deletion: {len(self.list_values)}")
        return


class ViewReferenceFieldListElement(ttk.Frame):
    """
    Class object representing an element in a field list and its associated widgets.

    The callback functions of a given element also invokes function calls to
    its parent ViewReferenceFieldList, which is connected to the Controller.
    This effectively allows data to bubble up from the View to the Model.

    Example: Author field element with buttons to move up or down, add element
    below, or delete itself.
    """
    def __init__(self, container: ViewReferenceFieldList, index: int, field_name, field_value: str="", **kw):
        ttk.Frame.__init__(self, container, **kw)
        self.parent: ViewReferenceFieldList = container
        self.index: int = index
        self.pack(side=tk.TOP, fill=tk.X, padx=0, pady=10, anchor="n")
        self.widget_wrapper = ttk.Frame(self)
        self.widget_wrapper.pack(side=tk.TOP, fill=tk.X, padx=0, anchor="n")

        self.gui_setup_grid_layout()
        self.setup_view_variables(field_value)
        self.gui_create_widgets(field_name)

    def gui_setup_grid_layout(self) -> None:

        self.widget_wrapper.rowconfigure(0, weight=1)
        self.widget_wrapper.columnconfigure(0, weight=1)
        self.widget_wrapper.columnconfigure(1, weight=1)
        self.widget_wrapper.columnconfigure(2, weight=1)
        self.widget_wrapper.columnconfigure(3, weight=4)
        self.widget_wrapper.columnconfigure(4, weight=1)
        self.widget_wrapper.columnconfigure(5, weight=1)

    def setup_view_variables(self, field_value) -> None:
        if self.parent is None:
            raise Exception(f"Error - unable to setup reference list element view variables: Inaccessible controller - no parent set for ViewReferenceField '{self}'")

        self.vars_field_value = ttk.StringVar(self, value=field_value)
        self.vars_field_value.trace_add("write", self.handle_field_value_updated)

    def gui_create_widgets(self, field_name):
        """
        Create widgets and attach event listeners.
        """
        self.ui_button_move_element_up = ttk.Button(self.widget_wrapper, width=2, text="↑", command=self.handle_move_element_up)
        self.ui_button_move_element_down = ttk.Button(self.widget_wrapper, width=2, text="↓", command=self.handle_move_element_down)

        self.label_field_name = ttk.Label(self.widget_wrapper, text=f"{field_name.capitalize()}")

        self.field_entry = ttk.Entry(self.widget_wrapper, textvariable=self.vars_field_value)

        self.ui_button_add_element_below = ttk.Button(self.widget_wrapper, width=2, text="+", command=self.handle_add_element_below)
        self.ui_button_delete_element = ttk.Button(self.widget_wrapper, width=2, text="-", command=self.handle_delete_element)

        self.ui_button_move_element_up.grid(column=0, row=0, padx=0)
        self.ui_button_move_element_down.grid(column=1, row=0, padx=0)
        self.label_field_name.grid(column=2, row=0, padx=2)
        self.field_entry.grid(column=3, row=0, sticky="ew")
        self.ui_button_add_element_below.grid(column=4, row=0, padx=0)
        self.ui_button_delete_element.grid(column=5, row=0, padx=0)

    """
    HACK:
    Couldn't figure out how to cleanly pass View element data to
    controller callback function with tkinter, so I'm using this method of calling the
    element's parent's functions and passing attributes of an field element
    instance so the controller functions properly works.
    """

    def handle_move_element_up(self) -> None:
        print(f"Element index: {self.index}")
        self.parent.gui_move_element_up(self.index)
        return

    def handle_move_element_down(self) -> None:
        print(f"Element index: {self.index}")
        self.parent.gui_move_element_down(self.index)
        return

    def handle_add_element_below(self) -> None:
        print(f"Element index: {self.index}")
        self.parent.gui_add_element_below(self.index)
        return

    def handle_delete_element(self) -> None:
        print(f"Element index: {self.index}")
        self.parent.gui_delete_element(self.index)
        return

    def handle_field_value_updated(self, variable_name: str, index: str, mode: str) -> None:
        print(f"Element index: {self.index}")
        new_value: str = self.vars_field_value.get()
        self.parent.handle_field_value_updated(self.index, new_value)
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

        # self.view_fields.gui_setup_frames()

        # Disable buttons as there is only one reference on initialisaiton
        self.refresh_view_options_reference_in_view()
        # Show first reference and pass controller to list fields
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
                # More than one reference, enable next button
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

        # catch error if function is activated somehow even when index is the last one
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

    def handle_field_value_updated(self, target_field: str, new_value: str) -> None:
        index_reference_in_view: int = self.view_options.vars_options_index_reference_in_view.get()
        self.model.update_reference_field_at_index(target_field, index_reference_in_view, new_value) 
        return

    def handle_field_list_element_value_updated(self, target_field: str, index_list_element: int, new_value: str) -> None:
        index_reference_in_view: int = self.view_options.vars_options_index_reference_in_view.get()
        self.model.update_element_in_reference_field_list(target_field, index_reference_in_view, index_list_element, new_value)
        return

    """
    Field list element manipulation functions are located below.
    ViewReferenceFieldListElement represent things like an individual author or
    editor. They are stored within a field list, representing the ensemble of authors or editors.

    These functions are invoked from within ViewReferenceFieldList after
    bubble-up callback function in ViewReferenceFieldListElement is invoked
    upon user interaction.

    They work as follows:
    User Interaction -> ViewReferenceFieldListElement -callback function-> ViewReferenceFieldList  -calls-> Controller -calls-> Model

    Note that in this instance, the view handles itself, and is not controlled by the controller.

    Detailed explanation:
    - User interacts with the button widgets within ViewReferenceFieldListElement
      - This invokes the respective callback function (i.e., add element below)
        within the ViewReferenceFieldListElement instance.
        - These callback functions call the respective function of its parent,
          ViewReferenceFieldList (i.e., add element below)

    - ViewReferenceFieldList keeps track of all ViewReferenceFieldListElement
      in a list
        - The reason why each ViewReferenceFieldListElement instance have their
          own callback functions that calls functions within
          ViewReferenceFieldList is because I couldn't figure out how to pass
          parameter values through callback functions. We need to pass the
          position of the list element within the list to be able to modify the
          element in the model at a given reference index.

    - ViewReferenceFieldList keeps track of the state of the widgets, and
      handles the logic for when a button should be disabled or not.
        - It refreshes the widgets to reflect how the internal Model has changed.
    """

    def handle_field_list_add_element_below_button_clicked(self, target_field, index_list_element: int):
        index_reference_in_view: int = self.view_options.vars_options_index_reference_in_view.get()
        self.model.add_element_in_reference_field_list_at_index(target_field, index_reference_in_view, index_list_element)
        return

    def handle_field_list_delete_element_button_clicked(self, target_field, index_list_element: int):
        index_reference_in_view: int = self.view_options.vars_options_index_reference_in_view.get()
        self.model.delete_element_in_reference_field_list_at_index(target_field, index_reference_in_view, index_list_element)
        return

    def handle_field_list_move_element_up_button_clicked(self, target_field: str, index_list_element: int) -> None:
        """
        In list field, handle "up element up" button click event.
        """
        index_reference_in_view: int = self.view_options.vars_options_index_reference_in_view.get()
        self.model.move_element_up_in_reference_list_field(target_field, index_reference_in_view, index_list_element)
        return

    def handle_field_list_move_element_down_button_clicked(self, target_field: str, index_list_element: int) -> None:
        """
        In list field, handle "move element down" button click event.
        """
        index_reference_in_view: int = self.view_options.vars_options_index_reference_in_view.get()
        self.model.move_element_down_in_reference_list_field(target_field, index_reference_in_view, index_list_element)
        return
