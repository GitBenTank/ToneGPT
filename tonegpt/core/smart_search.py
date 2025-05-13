import json
import pathlib
from rapidfuzz import process

# Load aliases from aliases.json
def load_aliases():
    base_dir = pathlib.Path(__file__).parent.parent.resolve()
    aliases_file = base_dir / "aliases.json"

    print(f"Loading aliases.json from: {aliases_file}")

    with open(aliases_file, "r") as f:
        return json.load(f)

# Smart search function
def smart_search(query, genres_data):
    aliases = load_aliases()

    bands_alias = aliases.get("bands", {})
    genres_alias = aliases.get("genres", {})
    tags_alias = aliases.get("tags", [])

    normalized_query = query.lower()

    # Direct alias band match
    for alias, band in bands_alias.items():
        if alias in normalized_query:
            return ("band", band, [])

    # Direct alias genre match
    for alias, genre in genres_alias.items():
        if alias in normalized_query:
            return ("genre", genre, [])

    # Tag matches (collect multiple)
    matched_tags = [tag for tag in tags_alias if tag in normalized_query]

    # Fuzzy fallback for bands
    band_names = list(set(bands_alias.values()))
    best_band, band_score, _ = process.extractOne(normalized_query, band_names)
    if band_score >= 75:
        return ("band", best_band, matched_tags)

    # Fuzzy fallback for genres
    genre_names = list(set(genres_alias.values()))
    best_genre, genre_score, _ = process.extractOne(normalized_query, genre_names)
    if genre_score >= 75:
        return ("genre", best_genre, matched_tags)

    # If nothing matches strong, return suggestions
    suggested_bands = [b for b, s, _ in process.extract(normalized_query, band_names, limit=5) if s >= 50]
    suggested_genres = [g for g, s, _ in process.extract(normalized_query, genre_names, limit=5) if s >= 50]
    suggested_tags = [t for t in tags_alias if t in normalized_query]

    return ("suggestions", {"bands": suggested_bands, "genres": suggested_genres, "tags": suggested_tags}, matched_tags)
