import json
from pathlib import Path

GENRES_PATH = Path("./tones")
BLOCKS_FILE = Path("./core/blocks.json")

def load_blocks():
    with open(BLOCKS_FILE, "r") as f:
        return {b["name"].lower() for b in json.load(f)}

def sync_tone_files():
    valid_blocks = load_blocks()
    print(f"✅ Loaded {len(valid_blocks)} valid blocks from blocks.json\n")

    for tone_file in GENRES_PATH.glob("*.json"):
        print(f"🎸 Checking {tone_file.name}...")
        with open(tone_file, "r") as f:
            presets = json.load(f)

        updated = False
        for preset in presets:
            corrected_effects = []
            for effect in preset.get("effects", []):
                effect_clean = effect.lower().strip()
                if effect_clean in valid_blocks:
                    corrected_effects.append(effect)
                else:
                    print(f"⚠️  Effect '{effect}' in preset '{preset.get('preset_name')}' not found in blocks.json")
                    # For now, keep it but highlight for manual review
                    corrected_effects.append(effect + " ❓")
                    updated = True
            preset["effects"] = corrected_effects

        if updated:
            with open(tone_file, "w") as f:
                json.dump(presets, f, indent=2)
            print(f"✅ Updated {tone_file.name} with corrections.\n")
        else:
            print(f"✅ No issues found in {tone_file.name}.\n")

if __name__ == "__main__":
    sync_tone_files()
