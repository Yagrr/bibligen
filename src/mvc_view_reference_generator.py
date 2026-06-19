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
from .mvc_controller import Controller
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
        self.controller: Controller | None = None
        self.gui_setup_grid_layout()
        #self._gui_show_layout()

    def setup_view_variables(self) -> None:
        if self.controller is None:
            raise ValueError("Error: controller not set for ViewRefGenOptions")

        # NOTE: Default to "Report"
        self.vars_options_doctype_dropdown = ttk.StringVar(self, value=list(DROPDOWN_REFERENCE_TYPES.keys())[0])
        self.vars_options_doctype_dropdown.trace_add("write", self.controller.handle_doctype_updated)

        self.vars_options_iteration_start_entry = ttk.IntVar(self, value=DEFAULT_OPTIONS_START)
        self.vars_options_iteration_start_entry.trace_add("write", self.controller.handle_start_value_updated)
        
        self.vars_options_iteration_step_entry = ttk.IntVar(self, value=DEFAULT_OPTIONS_NUMBER_ITERATIONS)
        self.vars_options_iteration_step_entry.trace_add("write", self.controller.handle_step_value_updated)

        self.vars_options_index_reference_in_view = ttk.IntVar(self, value=DEFAULT_OPTIONS_START)

        self.vars_options_number_iterations_label = ttk.StringVar(self, value=f"1 / {DEFAULT_OPTIONS_NUMBER_ITERATIONS}")
        self.vars_options_end_value_label = ttk.IntVar(value=(DEFAULT_OPTIONS_START + DEFAULT_OPTIONS_NUMBER_ITERATIONS))
 
    def gui_setup_grid_layout(self) -> None:
        # NOTE: Create 4x4 layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

    def gui_setup_frames(self) -> None:
        """
        Invoke widgets and place them on the grid.
        Requires controller to be set as widgets are tied to controller.
        """
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

        self.ui_options_step_label = ttk.Label(self, text="N° of steps") 
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
        self.ui_options_reset_fields_button = ttk.Button(self, width=15, text="Reset fields", command=self.controller.handle_reset_fields_button_clicked)
        self.ui_options_generate_button = ttk.Button(self, width=15, text="Generate entries", command=self.controller.handle_generate_button_clicked)
        self.ui_options_clear_fields_button = ttk.Button(self, width=15, text="Clear fields", command=self.controller.handle_clear_fields_button_clicked)
        self.ui_options_delete_iteration_button = ttk.Button(self, width=15, text="Delete iteration", command=self.controller.handle_delete_iteration_button_clicked)
        self.ui_options_number_iterations_label = ttk.Label(self, textvariable=self.vars_options_number_iterations_label)
        self.ui_options_previous_iteration_button = ttk.Button(self, width=15, text="Previous", command=self.controller.handle_previous_button_clicked)
        self.ui_options_next_iteration_button = ttk.Button(self, width=15, text="Next", command=self.controller.handle_next_button_clicked)

        self.ui_widget_separator.grid(column=0, row=4, columnspan=4, sticky="sew")
        self.ui_options_header_iteration_settings.grid(column=0, row=1, sticky="nsew", padx=(15, 0))
        self.ui_options_doctype_label.grid(column=0, row=1, sticky="nsew", padx=(15, 0))
        self.ui_options_doctype_dropdown.grid(column=1, row=1)
        self.ui_options_start_label.grid(column=0, row=2, sticky="nsew", padx=(15, 0))
        self.ui_options_start_entry.grid(column=1, row=2)
        self.ui_options_step_label.grid(column=0, row=3, sticky="nsew", padx=(15, 0))
        self.ui_options_step_entry.grid(column=1, row=3)
        self.ui_options_end_label.grid(column=0, row=4, padx=(15, 0))
        self.ui_options_end_value_label.grid(column=1, row=4)

        self.ui_options_header_preview_label.grid(column=2, row=0, sticky="nsew", columnspan=2)
        self.ui_options_reset_fields_button.grid(column=2, row=1)
        self.ui_options_generate_button.grid(column=3, row=1)
        self.ui_options_clear_fields_button.grid(column=2, row=2)
        self.ui_options_delete_iteration_button.grid(column=3, row=2)
        self.ui_options_number_iterations_label.grid(column=2, row=3, columnspan=2)
        self.ui_options_previous_iteration_button.grid(column=2, row=4)
        self.ui_options_next_iteration_button.grid(column=3, row=4)

    def _gui_show_layout(self) -> None:
        """
        Private function for development for showing the frame's current layout
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
        self.ui_layout_number_iterations_label = ttk.Label(self, text="[first step value / last step value]", background="pink", anchor="center")
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
        self.controller: Controller | None = None
        self.gui_setup_layout()
        #self._gui_show_layout()

    def gui_setup_layout(self) -> None:
        self.view_refgen_fields = ViewRefGenFields(self, autohide=True)
        self.view_refgen_fields.pack(expand=True, fill=tk.BOTH)

    def _gui_show_layout(self) -> None:
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
        self.controller: Controller | None = None
        self.fields: list[ViewReferenceField | ViewReferenceFieldList] = []
        #self._gui_show_layout()

    def _gui_show_layout(self) -> None:
        for i in range(5):
            field_label = ttk.Label(self, text="Fields", background="blue", anchor="center", font=("Arial", 12))
            field_label.pack(expand=True, fill=tk.BOTH, padx=0, pady=20, anchor="n")

    def gui_generate_reference_in_view(self, model_fields_dict: dict) -> None:
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
        
    def gui_delete_reference_in_view(self) -> None:
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

        self.pack(side=tk.TOP, fill=tk.X, padx=0, pady=8, anchor="n")

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
        if field_name in ["url", "doi", "issn"]:
            self.label_field_name = ttk.Label(self, text=f"{field_name}")
        elif field_name == "booktitle":
            self.label_field_name = ttk.Label(self, text="Book title")
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
        self.pack(side=tk.TOP, fill=tk.X, padx=0, pady=10, anchor="n")

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

        self.refresh_list_element_index(self.list_values)
        return

    def gui_move_element_down(self, index_element: int) -> None:
        if self.parent.controller is None:
            raise ValueError("Error - ViewReferenceFieldList - move field list element down: controller not set for ViewRefGenFields")

        if index_element >= len(self.list_values) - 1:
            # Check if it's last element, cannot move element further down
            raise IndexError(f"Error - ViewReferenceFieldList - move field list element down: index out of bounds {index_element}, number of elements: {len(self.list_values) - 1}")

        target_field: str = self.field_name
        self.parent.controller.handle_field_list_move_element_down_button_clicked(target_field, index_element)
        self.refresh_list_element_index(self.list_values)

        return

    def handle_field_value_updated(self, index_element: int, new_value: str) -> None:
        if self.parent.controller is None:
            raise ValueError("Error - ViewReferenceFieldList - update field list element: controller not set for ViewRefGenFields")

        target_field: str = self.field_name
        # Send data to controller and model
        self.parent.controller.handle_field_list_element_value_updated(target_field, index_element, new_value)

        # Update list elements - no need to refresh the View
        self.list_values[index_element] = new_value
        return

    def gui_add_element_below(self, index_element: int) -> None:
        if self.parent.controller is None:
            raise ValueError("Error - ViewReferenceFieldList - add field list element: controller not set for ViewRefGenFields")

        target_field: str = self.field_name
        self.parent.controller.handle_field_list_add_element_below_button_clicked(target_field, index_element)

        # Add element below given index with empty string.
        self.refresh_list_element_index(self.list_values)

        return

    def gui_delete_element(self, index_element: int) -> None:
        if self.parent.controller is None:
            raise ValueError("Error - ViewReferenceFieldList - delete field list element: controller not set for ViewRefGenFields")

        if len(self.list_values) <= 1:
            # Check if list_element is not empty or only one element
            # The list cannot be empty.
            raise ValueError("Error - ViewReferenceFieldList - delete field list element: list_values is empty or only has one value")

        if index_element >= len(self.list_values):
            raise IndexError(f"Error - ViewReferenceFieldList - delete field list element: index out of bounds {index_element}, number of elements: {len(self.list_values) - 1}")

        target_field: str = self.field_name
        self.parent.controller.handle_field_list_delete_element_button_clicked(target_field, index_element)

        # Update list_values
        self.refresh_list_element_index(self.list_values)
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

    def gui_create_widgets(self, field_name) -> None:
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
        self.parent.gui_move_element_up(self.index)
        return

    def handle_move_element_down(self) -> None:
        self.parent.gui_move_element_down(self.index)
        return

    def handle_add_element_below(self) -> None:
        self.parent.gui_add_element_below(self.index)
        return

    def handle_delete_element(self) -> None:
        self.parent.gui_delete_element(self.index)
        return

    def handle_field_value_updated(self, variable_name: str, index: str, mode: str) -> None:
        new_value: str = self.vars_field_value.get()
        self.parent.handle_field_value_updated(self.index, new_value)
        return
