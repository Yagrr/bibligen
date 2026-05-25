from enum import Enum

""" 
List of currently supported reference types, for use by GUI
vars_options_doctype_dropdown 
"""

class ReferenceType(Enum):
    """
    Enum class to serve as document templates.
    Document types and fields based on `https://bibtex.eu/types/` and
    `https://www.bibtex.com/e/entry-types/`

    TODO: For MISC item type, allow users to add custom fields.

    Current list of document type: 
    Article, Book, Booklet, Conference, Inbook,
    Incollection, Inproceedings, Manual, Masters thesis, Misc., PhD thesis,
    Proceedings, Technical report, Report, Unpublished
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

DROPDOWN_REFERENCE_TYPES: dict[str, ReferenceType] = {
    "Report": ReferenceType.REPORT,
    "Misc.": ReferenceType.MISC,
    "Article": ReferenceType.ARTICLE,
    "Book": ReferenceType.BOOK,
    "Booklet": ReferenceType.BOOKLET,
    "Conference": ReferenceType.CONFERENCE,
    "Inbook": ReferenceType.INBOOK,
    "Incollection": ReferenceType.INCOLLECTION,
    "Inproceedings": ReferenceType.INPROCEEDINGS,
    "Manual": ReferenceType.MANUAL,
    "Master's Thesis": ReferenceType.MASTERSTHESIS,
    "PhD thesis": ReferenceType.PHDTHESIS,
    "Proceedings": ReferenceType.PROCEEDINGS,
    "Technical report": ReferenceType.TECHREPORT,
    "Unpublished": ReferenceType.UNPUBLISHED,
}
