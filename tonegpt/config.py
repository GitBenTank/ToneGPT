import pathlib

BASE_DIR = pathlib.Path(__file__).parent.resolve()

BLOCKS_FILE = BASE_DIR / "core" / "blocks.json"
ALIASES_FILE = BASE_DIR / "aliases.json"
TONES_DIR = BASE_DIR / "tones"
