import json
import pathlib

def load_blocks():
    # Correct path to core/blocks.json using pathlib
    base_dir = pathlib.Path(__file__).parent.parent.resolve()
    blocks_file = base_dir / "core" / "blocks.json"

    print(f"Loading blocks.json from: {blocks_file}")

    with open(blocks_file, "r") as f:
        return json.load(f)

def describe_block(block_key, block_data):
    # Find matching block by 'name' key
    match = next((b for b in block_data if b.get("name", "").lower() == block_key.lower()), None)

    if not match:
        print(f"No data found for block: {block_key}")
        return

    print(f"🔧 {match.get('name', block_key)}")
    print(match.get("description", "No description provided."))
    print("Required:", "Yes" if match.get("required", False) else "No")

    key_params = match.get("key_parameters", [])
    if key_params:
        print("Key Parameters:", ", ".join(key_params))
    else:
        print("Key Parameters: N/A")

    print()
