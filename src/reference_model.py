import re

from .settings import (
    DEFAULT_OPTIONS_START,
    DEFAULT_OPTIONS_NUMBER_ITERATIONS,
    DEFAULT_PATTERN,
)

from .reference_type import ReferenceType, DROPDOWN_REFERENCE_TYPES
from .utils import _debug_log_fn_decorator

class ModelReferenceDatabase:
    """
    Model object representing the collection of references that have been
    generated in bulk. Contains data on start year, number of iterations, and
    regex pattern to substitute with iterated values.
    """
    def __init__(self):
        self.vars_iteration_start_value: int = DEFAULT_OPTIONS_START # Replace pattern with iteration_start
        self.vars_iteration_step_value: int = DEFAULT_OPTIONS_NUMBER_ITERATIONS # Iterate by iteration_step
        self.vars_iterable_string_pattern: str = DEFAULT_PATTERN
        self.references: list[ModelReference] = []
        
        # On init, default to REPORT item type
        self.add_model_reference(ReferenceType.REPORT, len(self.references) + 1)

    def get_reference_fields(self, index: int):
        """
        Returns the reference fields at a given index.
        """
        return self.references[index].fields


    def update_reference_doctype(self, doctype: str):
        new_doctype_fields_template: dict = DROPDOWN_REFERENCE_TYPES[doctype].value
        # Get all field names except for "item_type" in the new document template.
        new_doctype_fields_list: list[str] = [field_name for field_name in new_doctype_fields_template.keys() if field_name != "item_type"]

        for reference in self.references:
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
        return
    def update_iteration_start(self, value: int):
        self.iteration_start = value

    def update_iteration_step(self, value: int):
        self.iteration_start = value

    def update_iteration_end(self):
        self.iteration_end = self.vars_iteration_start_value, self.vars_iteration_step_value

    def add_model_reference(self, item_type: ReferenceType, value_iterable: int):
        self.references.append(ModelReference(item_type, value_iterable, self.vars_iterable_string_pattern))

    def delete_model_reference(self, index: int):
        """
        Delete reference by index. Ideally, the first reference should not be deleted.
        The only way for the first reference to be deleted is when the database is being rebuilt.
        """
        if index == 1:
            return
        del self.references[index]

        for i in range(len(self.references)):
            if self.references[i].value_iterable > 0:
                self.references[i].value_iterable -= 1
    
    def clear_model_reference_fields(self, index: int):
        """
            Clears all fields for all iterations  except the first reference,
            and for fields author that do not have the pattern.
            This should only happen if the user chooses to go over the previews
            and modify the fields of an entry after the first.
            If the first reference has no patterns, then iterations cannot happen.
        """
        ...

        
    def rebuild_database(self, item_type: ReferenceType, value_iterable: int):
        # rebuilds self.references once button is clicked.
        # map existing key values to references then append to database
        ...
    def reset_database(self, item_type: ReferenceType, value_iterable: int):
        # reset completely, keeping the first element intact
        ...

    def convert_refs_to_bib(self):
        # For loop that goes over each references
        # Joins into a final string
        ...
        

class ModelReference:
    def __init__(self, item_type: ReferenceType, value_iterable: int, pattern: str):
        self.item_type: ReferenceType = item_type
        self.value_iterable: int = value_iterable
        #TODO: Figure out if a model reference should contain the pattern or no
        self.fields: dict = item_type.value
        #TODO: is_modified: might be useful
        self.is_modified: bool = False
        self.pattern: str = pattern
        
    def add_author(self, author_name: str) -> None:
        self.fields["author"].append(author_name)
        return

    def remove_author(self, author_name: str) -> None:
        if author_name not in self.fields["author"]:
            return
        self.fields["author"].remove(author_name)
        return

    def update_value_iterable(self, value: int) -> None:
        # updates iterable value which is used to replace all strings matching
        # pattern
        # Allow user to modify the field. Even if that could desync the value.
        # Corrects it if steps is modified
        self.value_iterable = value
        return

    def update_field(self, input_value: str, target_field: str) -> None:
        # Do we only allow the iterable to be in the first entry?
        # if authors
        # if authors
        ...

    def convert_fields_to_bib(self) -> str:
        ...

