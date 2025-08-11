#!/usr/bin/env python3
import json
import pathlib
import sys

def load_blocks():
    # Now blocks.json lives in the same folder as this script:
    script_dir   = pathlib.Path(__file__).parent.resolve()
    blocks_file  = script_dir / "blocks.json"
    if not blocks_file.exists():
        sys.exit(f"❌ blocks.json not found at {blocks_file}")
    print(f"🔍 Loading blocks.json from: {blocks_file}")
    with open(blocks_file, "r") as f:
        return json.load(f)

def describe_block(block_key, block_data):
    match = next(
        (b for b in block_data if b.get("name", "").lower() == block_key.lower()),
        None
    )
    if not match:
        print(f"❓ No data found for block: {block_key!r}")
        return

    print(f"\n🔧 {match['name']}")
    print(match.get("description", "No description provided."))
    print("Required:", "Yes" if match.get("required", False) else "No")
    kp = match.get("key_parameters", [])
    print("Key Parameters:", ", ".join(kp) if kp else "N/A")
    print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python core/inspect_blocks.py <block_name>")
        sys.exit(1)

    block_name = sys.argv[1]
    blocks     = load_blocks()
    describe_block(block_name, blocks)

