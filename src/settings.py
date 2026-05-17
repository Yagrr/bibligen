from .reference_model import ReferenceType

""" App settings and configurations """

WINDOW_TITLE = "bibligen"
WIDTH_WINDOW = 1500
HEIGHT_WINDOW = 1000

THEME = "darkly"
FONT = "TkFixedFont"
FONT_SIZE = 14

DEFAULT_REFERENCE_TYPE = ReferenceType.REPORT
DEFAULT_START = 0
DEFAULT_ITERATIONS = 1
# Double square brackets, only capturing digit inside
DEFAULT_PATTERN = r"(?:\[\[)\d+(?:\]\])"

REFGEN_MAX_ITERATIONS = 50
REFGEN_MAX_FIELDS = 15
