
DATA_PATH= "data/tamagocours/Tamagocours.csv"
soundfont_path = "data/soundfonts/"

SF_Default = soundfont_path + "Jazz_Guitar.sf2"#"FluidR3_GM2-2.sf2"
SF_Chemclarinet = soundfont_path + "Chemical_Clarinet_MDX7.sf2"
SF_Soprano = soundfont_path + "Recorder_Soprano.sf2"
SF_Warmlead = soundfont_path + "Warm_Lead_MDX7.sf2"
SF_Cleanguitar = soundfont_path + "Clean_Guitar.sf2"
SF_Jazzguitar = soundfont_path + "Jazz_Guitar.sf2"


ENCODING_OPTIONS =  ["value", "duration", "velocity"]
SOUNDFONT =  ["Guitar", "Piano", "Drum"]
MOCKUP_VARS =  ["timestamp", "user_id", "action", "item_id"]

DEFAULT_PADDING = (5, 5, 5, 5)
DEFAULT_PADX = (5, 5)
DEFAULT_PADY = (5, 5)
DEFAULT_BGCOLOR = 'blue'

TFRAME_STYLE = {"DEFAULT" : ["TFrame", "green"],
                "TRACK": ["Trackframe.TFrame", "grey"],
                "CONFIG": ["Configframe.TFrame", "grey"],
                "TRACK_COLLECTION": ["TCollection.TFrame", "cyan"],
                "NOTE": ["TNote.TFrame", "grey"],
                "PARAMETER_MAPPING": ["TPMapping.TFrame", "grey"]
                }