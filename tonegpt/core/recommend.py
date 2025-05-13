import json
import pathlib
from tonegpt.config import BLOCKS_FILE

def load_blocks():
    print(f"Loading blocks.json from: {BLOCKS_FILE}")
    with open(BLOCKS_FILE, "r") as f:
        return json.load(f)

def describe_block(block_key, block_data):
    block = block_data.get(block_key.lower())
    if not block:
        print(f"No data found for block: {block_key}")
        return

    print(f"🔧 {block['name']}")
    print(block.get("description", "No description provided."))
    print("Required:", "Yes" if block.get("required", False) else "No")

    key_params = block.get("key_parameters", [])
    if key_params:
        print("Key Parameters:", ", ".join(key_params))
    else:
        print("Key Parameters: N/A")

    print()

