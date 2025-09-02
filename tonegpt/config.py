"""
ToneGPT Configuration

TL;DR: Central configuration for FM9 single-mode system.
- Defines file paths for FM9 data sources
- BLOCKS_FILE: Main FM9 blocks data (1,631 blocks)
- FM9_CONFIG_FILE: Primary parameter source
- All paths relative to tonegpt package root

Constraints:
- FM9 single-mode only (docs/ground-truth.md#Invariants)
- Data sources are read-only (docs/ground-truth.md#Safety Constraints)
- No network paths or external URLs
"""

import pathlib

BASE_DIR = pathlib.Path(__file__).parent.resolve()

BLOCKS_FILE = BASE_DIR / "core" / "blocks_with_footswitch.json"
ALIASES_FILE = BASE_DIR / "aliases.json"
# TONES_DIR removed - AI generates tones dynamically
FM9_CONFIG_FILE = BASE_DIR / "core" / "fm9_config.json"
