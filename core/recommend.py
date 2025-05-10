import json
import os
from rapidfuzz import process
from core.tone_loader import load_tone
from core.block_data import load_blocks, describe_block

def recommend_tone(genre):
    tone = load_tone(genre)
    if not tone:
        print(f"\n⚠️ Tone preset not found for genre: {genre}")
        return

    print("\n🎸 Recommended Tone Preset\n")
    print(f"🎵 Band: {tone['band']}")
    print(f"🎚️  Preset Name: {tone['preset_name']}")
    print(f"📦 Genre: {tone['genre']}")
    print(f"🔊 Amp Model: {tone['amp_model']}")
    print(f"🧱 Cab IR: {tone['cab_ir']}")
    print(f"🎛️  Effects: {', '.join(tone['effects'])}")
    print(f"\n📝 Summary: {tone['summary']}\n")
    print("-" * 28 + "\n")
    print("🔍 Block Insights:\n")

    blocks = load_blocks()
    available_keys = list(blocks.keys())

    for effect in tone["effects"]:
        best_match, score, _ = process.extractOne(effect.lower(), available_keys)
        if score >= 75:
            describe_block(best_match, blocks)
        else:
            print(f"No data found for block: {effect}")
