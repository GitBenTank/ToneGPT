import pathlib

# Base directory of the project (ToneGPT-FM9-V3 root)
BASE_DIR = pathlib.Path(__file__).parent.resolve()

# Paths to core files & folders
BLOCKS_FILE = BASE_DIR / "core" / "blocks.json"
ALIASES_FILE = BASE_DIR / "aliases.json"
TONES_DIR = BASE_DIR / "tones"

# Debug print (optional, remove in prod)
if __name__ == "__main__":
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"BLOCKS_FILE: {BLOCKS_FILE}")
    print(f"ALIASES_FILE: {ALIASES_FILE}")
    print(f"TONES_DIR: {TONES_DIR}")
