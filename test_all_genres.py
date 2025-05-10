from core.tone_loader import load_all_genres
from interface.block_insights import get_block_insights

def test_all_genres():
    genres = load_all_genres()
    print("✅ Loaded genres:", list(genres.keys()))  # Debug print

    for genre_name, genre_data in genres.items():
        print(f"\n🎸 Testing genre: {genre_name}")
        print("\n🎸 Recommended Tone Preset")
        print(f"\n🎵 Band: {genre_data['band']}")
        print(f"🎚️  Preset Name: {genre_data['preset_name']}")
        print(f"📦 Genre: {genre_data['genre']}")
        print(f"🔊 Amp Model: {genre_data['amp_model']}")
        print(f"🧱 Cab IR: {genre_data['cab_ir']}")
        print(f"🎛️  Effects: {', '.join(genre_data['effects'])}")
        print(f"\n📝 Summary: {genre_data['summary']}")
        print("\n----------------------------\n")

        print("🔍 Block Insights:\n")
        block_insights = get_block_insights(genre_data['effects'])

        if isinstance(block_insights, list):
            for block in block_insights:
                print(f"🔧 {block['name']}")
                print(f"{block['description']}")
                print(f"Required: {'Yes' if block.get('required') else 'No'}")
                print(f"Key Parameters: {', '.join(block.get('key_parameters', [])) if block.get('key_parameters') else 'N/A'}\n")
        else:
            print(f"❌ Error with genre '{genre_name}': {block_insights}\n")

        print(f"✅ {genre_name} loaded successfully.\n")

if __name__ == "__main__":
    test_all_genres()
