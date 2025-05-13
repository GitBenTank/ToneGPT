import json
from tonegpt.config import TONES_DIR, ALIASES_FILE

def load_all_genres():
    genres = {}
    for file in TONES_DIR.glob('*.json'):
        genre_name = file.stem
        with open(file, 'r') as f:
            genres[genre_name] = json.load(f)
    return genres

def load_tone(genre_name):
    genres = load_all_genres()
    return genres.get(genre_name)

def load_aliases():
    with open(ALIASES_FILE, 'r') as f:
        return json.load(f)
