""" App settings and configurations """

WINDOW_TITLE = "bibligen"
WIDTH_WINDOW = 2000
HEIGHT_WINDOW = 1000

THEME = "darkly"
FONT = "TkFixedFont"
FONT_SIZE = 14

DEFAULT_OPTIONS_START = 0
DEFAULT_OPTIONS_NUMBER_ITERATIONS = 1

# First iteration holds a special role. Any instances of [[value]] is replaced.
DEFAULT_PATTERN_FIRST_ITERATION = "[[value]]"
# Double square brackets, only capturing digit inside. This pattern is used after the first iteration.
DEFAULT_PATTERN = r"(?:\[\[)\d+(?:\]\])"

REFGEN_MAX_ITERATIONS = 50
REFGEN_MAX_FIELDS = 15
