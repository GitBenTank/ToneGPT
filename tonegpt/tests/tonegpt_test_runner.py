import json
from pathlib import Path

GENRES_PATH = Path(__file__).parent.parent / "tones"
BLOCKS_FILE = Path(__file__).parent.parent / "core" / "blocks.json"

def load_genres():
    genres = {}
    for file in GENRES_PATH.glob("*.json"):
        with open(file, "r") as f:
            genre_data = json.load(f)
            genres[file.stem] = genre_data
    return genres

def load_blocks():
    with open(BLOCKS_FILE, "r") as f:
        return json.load(f)

def batch_preset_test():
    genres = load_genres()
    blocks = load_blocks()
    print(f"✅ Loaded {len(genres)} genres and {len(blocks)} blocks.\n")

    for genre_name, presets in genres.items():
        print(f"🎸 Genre: {genre_name}")
        if not isinstance(presets, list):
            print(f"❌ Error: Preset data for genre '{genre_name}' is not a list.\n")
            continue

        for preset in presets:
            print(f"🔧 Preset: {preset.get('preset_name', 'Unnamed')}")
            print(f"Band: {preset.get('band', 'Unknown')}")
            print(f"Effects: {', '.join(preset.get('effects', []))}")

            for effect in preset.get('effects', []):
                matching_blocks = [b for b in blocks if b['name'].lower() == effect.lower()]
                if not matching_blocks:
                    print(f"⚠️ Warning: Effect '{effect}' not found in blocks.json\n")
                else:
                    print(f"✅ Block '{effect}' validated.\n")
            print("-" * 40)

if __name__ == "__main__":
    batch_preset_test()