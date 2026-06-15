import re
from copy import deepcopy

from .settings import (
    DEFAULT_OPTIONS_START,
    DEFAULT_OPTIONS_NUMBER_ITERATIONS,
    DEFAULT_PATTERN_FIRST_ITERATION,
    DEFAULT_PATTERN,
)

from .reference_type import ReferenceType, DROPDOWN_REFERENCE_TYPES

class ModelReferenceDatabase:
    """
    Model object representing the collection of references that have been
    generated in bulk. Contains data on start year, number of iterations, and
    regex pattern to substitute with iterated values.
    """
    def __init__(self):
        self.vars_iteration_start_value: int = DEFAULT_OPTIONS_START # Replace pattern with iteration_start
        self.vars_iteration_step_value: int = DEFAULT_OPTIONS_NUMBER_ITERATIONS # Iterate by iteration_step
        self.vars_iterable_string_pattern_first_iteration: str = DEFAULT_PATTERN_FIRST_ITERATION
        self.vars_iterable_string_pattern: str = DEFAULT_PATTERN
        self.references: list[ModelReference] = []
        
        # On init, default to REPORT item type
        self.initialise_database(ReferenceType.REPORT,
                                 self.vars_iteration_start_value +
                                 self.vars_iteration_step_value,
                                 self.vars_iterable_string_pattern_first_iteration)

    def initialise_database(self, item_type: ReferenceType, value_iterable: int, pattern: str):
        self.references.append(ModelReference(item_type, value_iterable, pattern))

    def add_model_reference(self) -> None:
        """
        Triggered when the step value is updated.

        Adds a new model reference to the reference database, assuming that the
        database is initialised already, where the database already has one
        reference already.

        The new model reference is a copy of the latest reference but with the
        value_iterable +1.
        """
        reference_copy = deepcopy(self.references[-1])
        if len(self.references) == 1:
            reference_copy.pattern = self.vars_iterable_string_pattern
        reference_copy.value_iterable += 1
        # Replace fields with pattern
        reference_copy.replace_pattern_in_fields_with_iterable()
        self.references.append(reference_copy)

        self.vars_iteration_step_value += 1
        return

    def delete_model_reference(self, index: int) -> None:
        # Interaction: triggered when step value is updated, 
        """
        Delete reference by index. The first reference should not be deleted.
        The only way for the first reference to be deleted is when the database is being rebuilt.
        Skip pattern replacement for the first reference.
        """
        if index == 0:
            # TODO: Log error as the first reference should not be removed.
            return

        del self.references[index]
        self.vars_iteration_step_value -= 1
        for i, reference in enumerate(self.references):
            if reference.value_iterable > 0:
                reference.value_iterable -= 1
            if i != 0:
                reference.replace_pattern_in_fields_with_iterable()
        return

    def get_reference_at_index(self, index: int):
        """
        Returns the ModelReference or None at a given index.
        Used to update field values.
        """
        if index >= len(self.references):
            # TODO: Add error logging
            raise IndexError("Error while using ModelReferenceDatabase.get_reference_at_index(), index out of range")

        return self.references[index]

    def update_reference_field_at_index(self, target_field: str, index_reference: int, new_value: str) -> None:
        """
        Updates the field value for a given index of the reference database.
        """
        reference = self.get_reference_at_index(index_reference)
        reference.update_field(target_field, new_value)
        return

    # NOTE: Field list interactions

    def update_element_in_reference_field_list(self, target_field: str, index_reference: int, index_list_element: int, new_value: str) -> None:
        reference = self.get_reference_at_index(index_reference)
        reference.update_element_in_list_field(target_field, index_list_element, new_value)
        return

    def add_element_in_reference_field_list_at_index(self, target_field: str, index_reference: int, index_list_element: int):
        reference = self.get_reference_at_index(index_reference)
        reference.add_element_to_list_field(target_field, index_list_element)
        return

    def delete_element_in_reference_field_list_at_index(self, target_field: str, index_reference: int, index_list_element: int):
        reference = self.get_reference_at_index(index_reference)
        reference.delete_element_in_list_field(target_field, index_list_element)
        return

    def move_element_up_in_reference_list_field(self, target_field: str, index_reference: int, index_list_element: int):
        reference = self.get_reference_at_index(index_reference)
        reference.move_element_up_in_list_field(target_field, index_list_element)
        return

    def move_element_down_in_reference_list_field(self, target_field: str, index_reference: int, index_list_element: int):
        reference = self.get_reference_at_index(index_reference)
        reference.move_element_down_in_list_field(target_field, index_list_element)
        return

    def clear_model_reference_fields(self, index: int) -> None:
        """
        For all fields - except fields with the pattern, author, and date -
        clear the field value.
        This should only happen if the user chooses to go over the previews
        and modify the fields of an entry after the first.
        If the first reference has no patterns, then iterations cannot happen.
        """
        reference = self.references[index]

        for field_name, field_value in reference.fields:
            if field_name in ["item_type", "author", "editor", "year"] or reference.pattern in field_value:
                continue
            else:
                reference.fields[field_name] = ""

        return

    def update_reference_doctype(self, doctype: str) -> None:
        """
        For each ModelReferenceDatabase.references (ModelReference):
            ModelReference.fields to match the dictionary signature of
            the new document type as defined in DROPDOWN_REFERENCE_TYPES
            which links the UI dropdown reference type to the
            ReferenceType enum, containing the field signature of a given
            `item_type`/ReferenceType/document type.
        """
        new_doctype_fields_template: dict = DROPDOWN_REFERENCE_TYPES[doctype].value
        # Get all field names except for "item_type" in the new document template.
        new_doctype_fields_list: list[str] = [field_name for field_name in new_doctype_fields_template.keys() if field_name != "item_type"]

        for reference in self.references:

            reference_fields = list(reference.fields.keys())

            for field_name in reference_fields:
                if field_name != "item_type" and field_name not in new_doctype_fields_list:
                    del reference.fields[field_name]

            for field_name, field_value in new_doctype_fields_template.items():
                if field_name == "item_type":
                    reference.fields[field_name] = doctype
                if field_name not in reference.fields:
                    # Create field if it does not exist, detect if field is a list or a string
                    if isinstance(field_value, list):
                        reference.fields[field_name] = []
                    else:
                        reference.fields[field_name] = field_value
        return

    def update_iteration_start(self, value: int):
        """
        Updates the iteration_start_value. This is propagated across all
        references.
        """
        self.vars_iteration_start_value = value
        for i, reference in enumerate(self.references):
            reference.value_iterable = value + i
            # Update pattern in field
            if i != 0:
                reference.replace_pattern_in_fields_with_iterable()
        return

    def update_iteration_step(self, new_step_value: int) -> None:
        """
        Triggered when Controller's handle_step_value_updated is used.
        Also triggered when handle_delete_iteration_button_clicked() is called.

        Logic:
        - If step is less than the current step: Remove references up till step.
        Update the step value.

        - If step is greater than the previous step: Add more references, the
        copy of the latest reference. The add_model_reference() function
        automatically updates the iterable in each field.
        """
        if new_step_value < self.vars_iteration_step_value:
            self.references = self.references[:new_step_value]
        if new_step_value > self.vars_iteration_step_value:
            count_new_steps = new_step_value - self.vars_iteration_step_value
            while count_new_steps > 0:
                self.add_model_reference()
                count_new_steps -= 1

        # Update field values.
        self.vars_iteration_step_value = new_step_value

    def convert_refs_to_bib(self) -> str:
        """
        Converts the references in the database to a bib string, to write to
        file or copy paste.
        """
        bib_string = []
        unique_keys = []
        for reference in self.references:
            # Create non-duplicate citation key
            citation_key = reference.generate_citation_key()

            if citation_key == "":
                citation_key = "placeholder"

            if citation_key in unique_keys:
                k = 1
                while (f"{citation_key}-{k}" in unique_keys):
                    k += 1
                citation_key = f"{citation_key}-{k}"
                unique_keys.append(citation_key)
            else:
                unique_keys.append(citation_key)

            bib_string.append(reference.convert_fields_to_bib(citation_key))

        return "\n".join(bib_string)

        

class ModelReference:
    def __init__(self, item_type: ReferenceType, value_iterable: int, pattern: str):
        self.item_type: ReferenceType = item_type
        self.value_iterable: int = value_iterable
        self.fields: dict = item_type.value
        self.pattern: str = pattern
  
    def replace_pattern_in_fields_with_iterable(self):
        """
        Replaces all occurences of the pattern with the iterable value for
        display purposes. Only applicable to references after the first one.
        Keeping the square brackets. Square brackets are removed when converted
        to .bib.
        This function is not called for the first reference.
        """
        for field_name, field_value in self.fields.items():
            # ignore list (author, editor) field types.
            if isinstance(field_value, list):
                continue
            # Check if this object is copied from the first reference, if it is then replace [[value]]
            # Otherwise replace [[integer]] by the value iterable, which should be updated by +1.
            if DEFAULT_PATTERN_FIRST_ITERATION in field_value:
                # Replace "[[value]]" since it's a copy of the first iterable.
                self.fields[field_name] = field_value.replace(DEFAULT_PATTERN_FIRST_ITERATION, f"[[{self.value_iterable}]]")
            else:
                self.fields[field_name] = re.sub(self.pattern, f"[[{self.value_iterable}]]", field_value)

    def update_field(self, target_field: str, input_value: str) -> None:
        """
        Updates the value of a field given the provided value.
        Provided that it is not a list type.
        """
        self.fields.update({target_field: input_value})

    # NOTE: Field list interactions

    def update_element_in_list_field(self, target_field: str, index_list_element: int, new_value: str) -> None:
        """
        Updates the value of an element in a field list (e.g., author, editor)
        given the target_field name, the index of the element to be modified,
        and the new value.
        """
        field_list = self.fields.get(target_field, None)
        if field_list is None or not isinstance(field_list, list):
            #TODO: add error logging. Passed target_field is not a field list.
            return

        try:
            field_list[index_list_element] = new_value
        except IndexError:
            raise IndexError(f"Error - updating element in list field. Target field: '{target_field}'; Index element: '{index_list_element}'; New value: '{new_value}' ")

        return
        
    def add_element_to_list_field(self, target_field: str, index_list_element: int) -> None:
        """
        Triggered when user adds a new element in a list field in
        ViewRefGenFields using the (+) button.
        ModelReferenceDatabase interacts with model in view to add author to list.
        Adds the new element after the provided index.

        List field names include:
        "author"
        "editor"
        """
        field_list = self.fields.get(target_field, None)
        if field_list is None or not isinstance(field_list, list):
            #TODO: add error logging
            return

        self.fields[target_field].insert(index_list_element + 1, "")
        return

    def delete_element_in_list_field(self, target_field: str, index_list_element: int) -> None:
        """
        Triggered when the user removes an element in a list field in
        ViewRefGenFields using the (-) button. Removes the element from the
        model at the input index value.
        """
        field_list = self.fields.get(target_field, None)
        if field_list is None or not isinstance(field_list, list):
            return

        try:
            field_list.pop(index_list_element)
        except IndexError:
            raise IndexError("Error removing")
        return

    def move_element_up_in_list_field(self, target_field: str, index_element: int) -> None:
        """
        Move an element in a field list closer to 0, or the top of the list.
        Called when the user interacts with buttons that move the field element up or down.
        """
        field_list = self.fields.get(target_field, None)

        if field_list is None or len(field_list) == 1 or index_element == 0:
            # TODO: add error logging. Index out of range, or field list does not exist
            raise ValueError(f"Error - ModelReference - unable to move element down in list field. Target field: '{target_field}'; Index: '{index_element}'")
        if index_element >= len(field_list):
            raise IndexError(f"Error - ModelReference - unable to move element down in list field. Target field: '{target_field}'; Index: '{index_element}'")

        # FIX: Check if swap works correctly
        print(f"Field list before moving up: {field_list}")
        field_list[index_element - 1], field_list[index_element] = field_list[index_element], field_list[index_element - 1]
        print(f"Field list after moving up: {field_list}")
        return

    def move_element_down_in_list_field(self, target_field: str, index_element: int) -> None:
        """
        Move an element in a field list closer to the last index of the list,
        or the bottom of the list.
        Called when the user interacts with buttons that move the field element up or down.
        """
        field_list = self.fields.get(target_field, None)

        if field_list is None or len(field_list) == 1:
            # TODO: add error logging. Index out of range, or field list does not exist
            raise ValueError(f"Error - ModelReference - unable to move element down in list field. Target field: '{target_field}'; Index: '{index_element}'")
        if index_element >= len(field_list) - 1:
            # Check if the index is the last index, and if it's outside.
            raise IndexError(f"Error - ModelReference - unable to move element down in list field - index is last element. Target field: '{target_field}'; Index: '{index_element}'")

        # FIX: Check if swap works correctly
        print(f"Field list before moving down: {field_list}")
        field_list[index_element + 1], field_list[index_element] = field_list[index_element], field_list[index_element + 1]
        print(f"Field list after moving down: {field_list}")
        return

    # NOTE:  Export functions
    
    def generate_citation_key(self):
        try:
            if self.fields["item_type"] == "@proceedings":
                author = self.fields["editor"][0]
            else:
                author = self.fields["author"][0]
        except IndexError:
            author = "citation_key"

        # Use first three words as title
        title = "".join(self.fields.get("title", "").split()[:3])
        year = self.fields.get("year", "")
        return f"{author}{title}{year}"

    def convert_fields_to_bib(self, citation_key: str) -> str:
        """
        Converts fields into .bib string.
        Creates a key given field values.
        ModelReferenceDatabase.convert_refs_to_bib() handles duplicate keys.

        Outputs string of format:
        ```
        @item_type{citation_key,
            author = {John Doe and Jane Smith},
            title = {Example reference},
            institution = {Example Institution}, 
            year = {2026},
            volume = {14},
            number = {1},
            note = {This is an example note}
        }
        ```
        """
        bib_fields = []

        last_field = list(self.fields.keys())[-1] 
        for field_name, field_value in self.fields.items():
            if field_value == "":
                # Ignore non-fist ields with no values.
                continue

            match field_name:
                case "item_type":
                    bib_fields.append(f"{field_value}{{{citation_key},\n")
                case "author" | "editor":
                    bib_fields.append(f"\t{field_name} = {{")
                    
                    # Populate field with names, separated by "and".
                    for name in field_value:
                        if name == field_value[-1]:
                            bib_fields.append(name)
                        else:
                            bib_fields.append(f"{name} and ")
                    bib_fields.append("},\n")
                case _:
                    # Replace pattern with value iterable without square brackets.
                    field_value_final = re.sub(self.pattern, str(self.value_iterable), field_value)
                    bib_fields.append(f"\t{field_name} = {{{field_value_final}}}")
                    if field_name == last_field:
                        bib_fields.append("\n")
                    else:
                        bib_fields.append(",\n")

        bib_fields.append("}\n")

        return "".join(bib_fields)

