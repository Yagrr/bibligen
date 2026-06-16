from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mvc_model import ModelReferenceDatabase
    from mvc_view_reference_generator import ViewRefGenOptions, ViewRefGenFields
    from mvc_view_output_display import ViewOutputWindow

class Controller:
    """
    Controller object linking user interactions to the view component (GUI),
    and model component (internal data).
    
    Ex: If X button is clicked, then Y happens to internal data, and Z GUI
    element is updated.
    """
    def __init__(self, model: "ModelReferenceDatabase", view_options: "ViewRefGenOptions", view_fields: "ViewRefGenFields", view_output: "ViewOutputWindow"):
        self.model = model
        self.view_options = view_options
        self.view_fields = view_fields
        self.view_output = view_output
        self.old_start_value: int = 0
        self.old_step_value: int = 1

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
            # Index is the first, disable Delete, Previous and Reset Fields buttons
            self.view_options.ui_options_delete_iteration_button.config(state="disabled")
            self.view_options.ui_options_previous_iteration_button.config(state="disabled")
            self.view_options.ui_options_reset_fields_button.config(state="disabled")

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
        self.view_options.ui_options_reset_fields_button.config(state="normal")
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
        try:
            new_start_value: int = int(self.view_options.ui_options_start_entry.get())
            step_value: int = int(self.view_options.ui_options_step_entry.get())
            self.old_start_value = new_start_value
            self.old_step_value = step_value
        except ValueError:
            # Entry fields have validation, ValueError typically triggered when all characters are erased
            new_start_value = self.old_start_value
            step_value = self.old_step_value

        if len(self.model.references) == 1:
            self.view_options.vars_options_end_value_label.set(new_start_value)
        else:
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
        try:
            start_value: int = int(self.view_options.ui_options_start_entry.get())
            new_step_value: int = int(self.view_options.ui_options_step_entry.get())
            self.old_start_value = start_value
            self.old_step_value = new_step_value
        except ValueError:
            # Entry fields have validation, ValueError typically triggered when all characters are erased
            start_value = self.old_start_value
            new_step_value = self.old_step_value

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

    def handle_reset_fields_button_clicked(self) -> None:
        """
        Resets current reference in view to be equal to the first.
        Useful for when the user modified iterations other than the first.
        """
        index_reference_in_view = self.view_options.vars_options_index_reference_in_view.get()
        self.model.reset_model_reference_fields(index_reference_in_view)
        self.refresh_view_fields_reference_in_view()
        self.refresh_view_options_reference_in_view()
        return

    def handle_generate_button_clicked(self) -> None:
        """
        Call self.model.convert_refs_to_bib() function, then send output to Console window.
        """
        output_str = self.model.convert_refs_to_bib()
        self.view_output.set_output_text(output_str)
        return

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
