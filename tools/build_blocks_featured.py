#!/usr/bin/env python3
"""
Build blocks_featured.json from existing blocks data.

This script transforms the current blocks_with_footswitch.json into a clean,
featured-parameters-only format with real-world mappings.
"""

import json
import csv
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
SRC_BLOCKS = ROOT / "tonegpt" / "core" / "blocks_with_footswitch.json"
DEFAULTS = ROOT / "data" / "blocks_featured.defaults.json"
MAP_CSV = ROOT / "data" / "fm9_model_map.csv"
OUT = ROOT / "data" / "blocks_featured.json"


def load_defaults():
    """Load featured parameters defaults."""
    defaults = json.loads(DEFAULTS.read_text(encoding="utf-8"))
    return {b["block"]: b["featured_parameters"] for b in defaults["blocks"]}


def load_map():
    """Load real-world mappings from CSV."""
    mapping = defaultdict(dict)
    if MAP_CSV.exists():
        with MAP_CSV.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                block = row["block"].strip()
                fm9 = row["fm9_name"].strip()
                real = (row.get("real_world") or "").strip() or None
                aliases = [a.strip() for a in (row.get("aliases") or "").split(";") if a.strip()]
                mapping[(block, fm9)] = {"real_world": real, "aliases": aliases}
    return mapping


def main():
    """Transform blocks data into featured format."""
    print("Loading source blocks data...")
    src_blocks = json.loads(SRC_BLOCKS.read_text(encoding="utf-8"))
    
    print("Loading featured parameters defaults...")
    featured = load_defaults()
    
    print("Loading real-world mappings...")
    mapping = load_map()
    
    # Group blocks by category
    blocks_by_category = defaultdict(list)
    for block in src_blocks:
        category = block["category"].upper()
        blocks_by_category[category].append(block)
    
    print(f"Found {len(blocks_by_category)} block categories:")
    for category, blocks in blocks_by_category.items():
        print(f"  {category}: {len(blocks)} models")
    
    # Build output structure
    out_blocks = []
    for category, blocks in blocks_by_category.items():
        models = []
        for block in blocks:
            fm9_name = block["name"]
            key = (category, fm9_name)
            maprow = mapping.get(key, {})
            
            # Use existing real_world from block if available, otherwise from CSV
            real_world = block.get("real_world") or maprow.get("real_world")
            
            models.append({
                "fm9_name": fm9_name,
                "real_world": real_world,
                "aliases": maprow.get("aliases", [])
            })
        
        out_blocks.append({
            "block": category,
            "featured_parameters": featured.get(category, []),
            "models": models
        })
    
    # Write output
    output_data = {"blocks": out_blocks}
    OUT.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
    
    print(f"\n✅ Wrote {OUT}")
    print(f"📊 Summary:")
    print(f"  - {len(out_blocks)} block categories")
    total_models = sum(len(b["models"]) for b in out_blocks)
    print(f"  - {total_models} total models")
    
    # Show some stats
    for block in out_blocks:
        category = block["block"]
        model_count = len(block["models"])
        param_count = len(block["featured_parameters"])
        print(f"  - {category}: {model_count} models, {param_count} featured params")


if __name__ == "__main__":
    main()
