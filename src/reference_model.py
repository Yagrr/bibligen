from enum import Enum

from .settings import (
    DEFAULT_START,
    DEFAULT_ITERATIONS,
    DEFAULT_PATTERN,
)

class ReferenceType(Enum):
    """
    Enum class to serve as document templates.
    Document types and fields based on `https://bibtex.eu/types/` and
    `https://www.bibtex.com/e/entry-types/`

    TODO: For MISC item type, allow users to add custom fields.
    """
    ARTICLE = {
        "key": "",
        "item_type": "@article",
        "author": [],
        "title": "",
        "journal": "",
        "year": "",

        "publisher": "",
        "volume": "",
        "number": "",
        "pages": "",
        "issn": "",
        "doi": "",
        "url": "",
        "note": "",
    }
    BOOK = {
        "key": "",
        "item_type": "@book",
        "author": [],
        "title": "",
        "publisher": "",
        "address": "",
        "year": "",

        "editor": [],
        "series": "",
        "volume": "",
        "number": "",
        "edition": "",
        "note": "",
        # Non standard
        "doi": "",
        "issn": "",
        "isbn": "",
        "url": "",
    }
    BOOKLET = {
        "key": "",
        "item_type": "@book",
        "author": [],
        "title": "",
        "howpublished": "",
        "address": "",
        "year": "",

        "editor": [],
        "series": "",
        "volume": "",
        "number": "",
        "organization": "",
        "monthy": "",
        "note": "",

        "url": "",
    }
    CONFERENCE = {
        "key": "",
        "item_type": "@conference",
        "author": [],
        "title": "",
        "booktitle": "",
        "year": "",

        "editor": "",
        "series": "",
        "volume": "",
        "number": "",
        "pages": "",
        "address": "",
        "month": "",
        "organization": "",
        "publisher": "",
        "note": "",

        "url": "",
    }
    INBOOK = {
        "key": "",
        "item_type": "@inbook",
        "author": [],
        "title": "",
        "booktitle": "",
        "publisher": "",
        "year": "",

        "editor": [],
        "series": "",
        "volume": "",
        "number": "",
        "address": "",
        "edition": "",
        "month": "",
        "pages": "",
        "note": "",

        "url": "",
    }
    INCOLLECTION = {
        "key": "",
        "item_type": "@incollection",
        "author": [],
        "title": "",
        "booktitle": "",
        "publisher": "",
        "year": "",

        "editor": [],
        "series": "",
        "volume": "",
        "number": "",
        "edition": "",
        "address": "",
        "month": "",
        "pages": "",
        "note": "",

        "url": "",
    }
    INPROCEEDINGS = {
        "key": "",
        "item_type": "@inproceedings",
        "author": [],
        "title": "",
        "booktitle": "",
        "year": "",

        "editor": [],
        "series": "",
        "volume": "",
        "number": "",
        "address": "",
        "month": "",
        "organization": "",
        "publisher": "",
        "note": "",

        "url": "",
    }
    MANUAL = {
        "key": "",
        "item_type": "@manual",
        "author": [],
        "title": "",
        "booktitle": "",
        "year": "",

        "volume": "",
        "number": "",
        "edition": "",
        "address": "",
        "month": "",
        "organization": "",
        "note": "",

        "url": "",
    }
    MASTERSTHESIS = {
        "key": "",
        "item_type": "@mastersthesis",
        "author": [],
        "title": "",
        "school": "",
        "year": "",

        "type": "",
        "address": "",
        "month": "",
        "note": "",

        "url": "",
    }
    """ ALLOW USERS TO ADD CUSTOM FIELDS FOR MISC TYPE """
    MISC = {
        "key": "",
        "item_type": "@misc",
        "author": [],
        "title": "",
        "year": "",
        "howpublished": "",
        "note": "",
        "url": "",
    }
    PHDTHESIS = {
        "key": "",
        "item_type": "@mastersthesis",
        "author": [],
        "title": "",
        "school": "",
        "year": "",

        "type": "",
        "address": "",
        "month": "",
        "note": "",

        "url": "",
    }
    PROCEEDINGS = {
        "key": "",
        "item_type": "@proceedings",
        "editor": [],
        "title": "",
        "school": "",
        "year": "",

        "series": "",
        "volume": "",
        "number": "",
        "address": "",
        "month": "",
        "publisher": "",
        "note": "",

        "url": "",
    }
    TECHREPORT = {
        "key": "",
        "item_type": "@techreport",
        "author": [],
        "title": "",
        "institution": "",
        "year": "",

        "number": "",
        "address": "",
        "month": "",
        "note": "",

        "url": ""
    }
    # REPORT is non standard but included anyways because app use-case mainly applies
    # to this document type
    REPORT = {
        "key": "",
        "item_type": "@report",
        "author": [],
        "title": "",
        "institution": "",
        "year": "",

        "number": "",
        "address": "",
        "month": "",
        "note": "",

        "url": ""
    }
    UNPUBLISHED = {
        "key": "",
        "item_type": "@unpublished",
        "author": [],
        "title": "",
        "year": "",

        "note": "",

        "url": ""
    }


class ModelReferenceDatabase:
    def __init__(self):
        self.iteration_start = DEFAULT_START # Replace pattern with iteration_start
        self.iteration_step = DEFAULT_ITERATIONS # Iterate by iteration_step
        self.pattern = DEFAULT_PATTERN
        self.references: list[ModelReference] = []
        
        # On init, default to REPORT item type
        self.add_model_reference(ReferenceType.REPORT, len(self.references) + 1)

    def add_model_reference(self, item_type: ReferenceType, value_iterable: int):
        self.references.append(ModelReference(item_type, value_iterable, self.pattern))

    def delete_model_reference(self, index: int):
        """
        Delete reference by index. Ideally, the first reference should not be deleted.
        The only way for the first reference to be deleted is when the database is being rebuilt.
        The database is rebuilt when 
        """
        if index == 1:
            return
        del self.references[index]

    def update_iteration_start(self, value: int):
        self.iteration_start = value

    def update_iteration_step(self, value: int):
        self.iteration_start = value
        
    def rebuild_database(self, item_type: ReferenceType, value_iterable: int):
        # rebuilds self.references once button is clicked.
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
        self.item_type = item_type
        self.value_iterable = value_iterable
        self.fields = item_type.value
        self.pattern = pattern
        
    def add_author(self, author_name: str) -> None:
        self.fields["author"].append(author_name)
        return

    def remove_author(self, author_name: str) -> None:
        if author_name not in self.fields["author"]:
            return
        self.fields["author"].remove(author_name)
        return

    def update_value_iterable(self, value: str) -> None:
        self.value_iterable = value
        return

    def update_field(self, input_value: str, target_field: str) -> None:
        # Do we only allow the iterable to be in the first entry?
        # if authors
        # if authors
        ...

    def convert_fields_to_bib(self) -> str:
        ...

