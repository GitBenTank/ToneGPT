#!/usr/bin/env python3
"""
Update Golden Presets Script

Regenerates all golden preset files with current deterministic, clamped outputs.
This ensures test fixtures match the current engine behavior.

Usage:
    python tools/update_goldens.py
"""

from pathlib import Path
import json
import sys

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tonegpt.core.clean_ai_tone_generator import CleanAIToneGenerator
from tonegpt.core.canonicalize import canonicalize_preset
from tonegpt.core.validate_and_clamp import enforce_ref_ranges

GOLDEN_DIR = Path("tests/data/golden_presets")
QUERIES = {
    # Core genre presets
    "marshall_jcm800_metal.json": "Marshall JCM800 metal tone with high gain and tight bass",
    "mesa_rectifier_modern.json": "Mesa Boogie Rectifier modern high gain tone",
    "fender_twin_clean.json": "Fender Twin Reverb clean tone with reverb",
    "vox_ac30_crunch.json": "Vox AC30 crunch tone with overdrive",
    "marshall_plexi_complex.json": "Marshall Plexi with Tube Screamer, delay, and reverb for classic rock",
    
    # Expanded genre coverage
    "u2_edge_delay.json": "U2 Edge delay tone with dotted eighth note delay and shimmer reverb",
    "gilmour_ambient.json": "Gilmour ambient tone with long reverb and delay for atmospheric sound",
    "srv_blues.json": "Stevie Ray Vaughan blues tone with Tube Screamer and Fender amp",
    "metalcore_modern.json": "Modern metalcore tone with high gain amp and tight bass response",
    "funk_clean.json": "Funk clean tone with bright Fender amp and compression",
    "jazz_fusion.json": "Jazz fusion tone with clean amp and chorus for smooth leads",
    "shoegaze_wall.json": "Shoegaze wall of sound with multiple delays and reverb",
    "country_twang.json": "Country twang tone with Telecaster and bright amp settings",
}

def main():
    """Regenerate all golden preset files with current engine output."""
    print("🔄 Regenerating golden presets with current deterministic, clamped outputs...")
    
    gen = CleanAIToneGenerator()
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)

    for filename, query in QUERIES.items():
        print(f"  Generating: {filename}")
        result = gen.generate_tone_from_query(query)
        result = canonicalize_preset(result)
        result = enforce_ref_ranges(result)
        
        out_path = GOLDEN_DIR / filename
        with out_path.open("w") as f:
            json.dump(result, f, indent=2, sort_keys=True)
        print(f"  ✅ Updated {out_path}")
    
    print(f"\n🎉 Successfully updated {len(QUERIES)} golden preset files!")
    print("   All presets now use deterministic, clamped parameter values.")

if __name__ == "__main__":
    main()
