import json

with open("blocks/blocks.json") as f:
    BLOCKS = json.load(f)

def get_block_insights(effects):
    insights = []
    for effect in effects:
        try:
            match = next((b for b in BLOCKS if b.get("name", "").lower() == effect.lower()), None)
            if match:
                insights.append({
                    "name": match.get("name", "Unknown"),
                    "description": match.get("description", "No description provided."),
                    "required": match.get("required", False),
                    "key_parameters": match.get("key_parameters", [])
                })
            else:
                insights.append({
                    "name": effect,
                    "description": "⚠️ No block data found for this effect.",
                    "required": False,
                    "key_parameters": []
                })
        except Exception as e:
            insights.append({
                "name": effect,
                "description": f"⚠️ Error loading block: {str(e)}",
                "required": False,
                "key_parameters": []
            })
    return insights

