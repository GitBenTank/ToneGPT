import json
import os

def load_blocks():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "blocks", "blocks.json")
    with open(path, "r") as f:
        return json.load(f)

def describe_block(block_key, block_data):
    if block_key not in block_data:
        print(f"No data found for block: {block_key}")
        return

    block = block_data[block_key]
    print(f"🔧 {block['name']}")
    print(block["description"])
    print("Required:", "Yes" if block["required"] else "No")
    
    if "key_parameters" in block:
        print("Key Parameters:", ", ".join(block["key_parameters"]))
    else:
        print("Key Parameters: N/A")
    
    print()
