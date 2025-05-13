from tonegpt.core.recommend import recommend_tone
from tonegpt.core.tone_loader import load_all_genres
from rapidfuzz import process

def list_available_genres():
    genres = load_all_genres()
    return list(genres.keys())

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
