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
    # REPORT is non standard but included anyways
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
        self.iteration_start = DEFAULT_START
        self.iteration_start = DEFAULT_START # add to settings, is 0 by default
        self.iteration_number = DEFAULT_ITERATIONS # add to settings, needs to be 1
        self.pattern = DEFAULT_PATTERN
        self.references: list[ModelReference] = []
        # Needs to be a dict
        # Insert position in queue
        #
    def add_model_reference(self, item_type: ReferenceType, value_iterable: int):
        ...

    def delete_model_reference(self, reference):
        ...

    def update_iteration_start(self, value: int):
        self.iteration_start = value

    def update_iteration_number(self, value: int):
        self.iteration_start = value

    def convert_refs_to_bib(self):
        ...
        

class ModelReference:
    def __init__(self, item_type: ReferenceType, value_iterable: int):
        self.item_type = item_type
        self.value_iterable = value_iterable
        self.fields = item_type.value

    def update_value_iterable(self):
        ...

    def update_field(self, input_value: str, target_field: str) -> None:
        # if author
        # if authors
        ...

    def convert_fields_to_bib(self) -> str:
        ...

