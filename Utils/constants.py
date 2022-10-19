#PARAMETERS
TIME_BUFFER = 1000 #ms, time used to plan future notes.
BATCH_SIZE = 1
BATCH_NBR_PLANNED=5

#OPTIONS
TIME_SETTINGS_OPTIONS = ["linear", "tempo-basic"]
TIME_SETTINGS_OPTIONS_TOOLTIP = \
    ["Linear: Each row is processed at constant interval. The interval is always #rows/song length",
     "tempo-basic: Ratios of temporal distance between rows are preserved."]
FUNCTION_OPTIONS = ["linear"]  # isomorphisms
ENCODING_OPTIONS = ["value", "duration", "velocity"]
MOCKUP_VARS = ["timestamp", "user_id", "action", "item_id"]

#UI
DEFAULT_PADDING = (5, 5, 5, 5)
DEFAULT_PADX = (5, 5)
DEFAULT_PADY = (5, 5)
DEFAULT_BGCOLOR = 'blue'

TFRAME_STYLE = {"DEFAULT": ["TFrame", "green"],
                "TRACK": ["Trackframe.TFrame", "grey"],
                "CONFIG": ["Configframe.TFrame", "grey"],
                "TRACK_COLLECTION": ["TCollection.TFrame", "darkred"],
                "NOTE": ["TNote.TFrame", "grey"],
                "PARAMETER_MAPPING": ["TPMapping.TFrame", "grey"],
                "TIMESETTINGS": ["Timesettings.TFrame", "grey"]
                }

#PATHS
DATA_PATH= "data/sequential_data/Tamagocours.csv"
#DATA_PATH= "data/sequential_data/AL2049.csv"
FILE_PATH= "data/savefiles"
soundfont_path = "data/soundfonts"


def rgb_hack(r, g, b):
    rgb = (r, g, b)
    return "#%02x%02x%02x" % rgb

LIGHTRED = rgb_hack(205, 100, 100)
