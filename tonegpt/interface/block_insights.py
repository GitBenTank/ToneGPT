import json
from tonegpt.config import BLOCKS_FILE

with open(BLOCKS_FILE, "r") as f:
    BLOCKS = json.load(f)

def get_block_insights(effects):
    insights = []
    for effect in effects:
        match = next((b for b in BLOCKS if b.get("name", "").lower() == effect.lower()), None)
        if match:
            insights.append({
                "name": match.get("name", "Unknown"),
                "description": match.get("description", "No description provided."),
                "required": match.get("required", False),
                "key_parameters": match.get("key_parameters", []),
                "category": match.get("category", "Uncategorized"),
                "tags": match.get("tags", [])
            })
        else:
            insights.append({
                "name": effect,
                "description": "⚠️ No block data found for this effect.",
                "required": False,
                "key_parameters": [],
                "category": "Uncategorized",
                "tags": []
            })
    return insights
