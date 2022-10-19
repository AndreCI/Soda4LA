# PARAMETERS
TIME_BUFFER = 1000  # ms, time used to plan future notes.
BATCH_SIZE = 1
BATCH_NBR_PLANNED = 5
MAX_NOTE_GRAPH = 100

# OPTIONS
TIME_SETTINGS_OPTIONS = ["tempo-basic", "linear"]
TIME_SETTINGS_OPTIONS_TOOLTIP = \
    ["tempo-basic: Ratios of temporal distance between rows are preserved.",
     "Linear: Each row is processed at constant interval. The interval is always #rows/song length. Experimental."]
FUNCTION_OPTIONS = ["linear"]  # isomorphisms
ENCODING_OPTIONS = ["value", "duration", "velocity"]
MOCKUP_VARS = ["timestamp", "user_id", "action", "item_id"]

# UI
DEFAULT_PADDING = (5, 5, 5, 5)
DEFAULT_PADX = (5, 5)
DEFAULT_PADY = (5, 5)
DEFAULT_BGCOLOR = 'blue'

# PATHS
FILE_PATH = "data/savefiles"
soundfont_path = "data/soundfonts"
