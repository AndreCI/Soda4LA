# PARAMETERS
TIME_BUFFER = 1000  # ms, time used to plan future notes.
BATCH_SIZE = 10
BATCH_NBR_PLANNED = 20
MAX_NOTE_GRAPH = 100
SAMPLE_SIZE = 10

# OPTIONS
TIME_SETTINGS_OPTIONS = ["tempo-basic", "tempo-4-notes", "linear"]
TIME_SETTINGS_OPTIONS_TOOLTIP = \
    ["tempo-basic: Each row is processed at constant interval. The interval is always #rows/song length.",
     "Linear: Ratios of temporal distance between rows are preserved. Experimental."]
FUNCTION_OPTIONS = ["linear"]  # isomorphisms
ENCODING_OPTIONS = ["value", "filter", "duration", "velocity"]
MOCKUP_VARS = ["timestamp", "user_id", "action", "item_id"]

# PATHS
FILE_PATH = "data/savefiles"
soundfont_path = "data/soundfonts"
