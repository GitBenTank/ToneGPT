import os
from rapidfuzz import process
from core.recommend import recommend_tone

def list_available_genres():
    tones_dir = os.path.join(os.path.dirname(__file__), "..", "tones")
    return [f.replace(".json", "") for f in os.listdir(tones_dir) if f.endswith(".json")]

def main():
    print("\n🎛️  Welcome to ToneGPT for FM9\n")
    genre_input = input("Enter a genre (e.g., grunge, psychedelic, classic_rock): ").strip().lower()

    available_genres = list_available_genres()
    best_match, score, _ = process.extractOne(genre_input, available_genres)

    if score < 70:
        print(f"\n⚠️ No close match found for genre: {genre_input}")
        print("📂 Available genres:", ", ".join(available_genres))
        return

    recommend_tone(best_match)

if __name__ == "__main__":
    main()
