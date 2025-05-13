from tonegpt.core.tone_loader import load_all_genres
from tonegpt.interface.block_insights import get_block_insights

def test_all_genres():
    genres = load_all_genres()
    print(f"\n✅ Loaded genres: {list(genres.keys())}")

    total_genres = len(genres)
    warnings = []

    for genre_name, genre_data in genres.items():
        print(f"\n🎸 Testing genre: {genre_name}")
        print(f"🎵 Band: {genre_data['band']}")
        print(f"🎚️  Preset Name: {genre_data['preset_name']}")
        print(f"🎛️  Effects: {', '.join(genre_data['effects'])}")

        block_insights = get_block_insights(genre_data['effects'])

        for block in block_insights:
            print(f"🔧 {block['name']}")
            print(f"{block['description']}")
            print(f"Required: {'Yes' if block.get('required') else 'No'}")
            print(f"Key Parameters: {', '.join(block.get('key_parameters', [])) if block.get('key_parameters') else 'N/A'}\n")

            if "⚠️" in block['description']:
                warnings.append((genre_name, block['name']))

        print(f"✅ {genre_name} tested.\n")

    print(f"\n🎯 Test Summary: {total_genres} genres tested.")
    if warnings:
        print(f"⚠️ Warnings in {len(warnings)} blocks:")
        for genre, block in warnings:
            print(f" - {genre}: Issue with {block}")
    else:
        print("✅ All blocks matched successfully!")

if __name__ == "__main__":
    test_all_genres()
