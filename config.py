# Metadata Music Updater - Configuration

# Root music folder (leave blank to be prompted via GUI)
MUSIC_DIR = ""

# Supported file extensions
EXTENSIONS = {".flac", ".mp3", ".m4a", ".ogg", ".wma", ".mp4"}

# Delay between API requests (in seconds)
SLEEP_BETWEEN_REQUESTS = 0.5

# Dry-run mode (True = no files are modified)
DRY_RUN = False

# Overwrite existing metadata fields
OVERWRITE_GENRE = True
OVERWRITE_DATE = True
OVERWRITE_LYRICS = True
OVERWRITE_COVER = True
OVERWRITE_ALBUM = True
OVERWRITE_TRACK = True
