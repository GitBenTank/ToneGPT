import os
import json

def load_all_genres(tones_dir='tones'):
    genres = {}
    for filename in os.listdir(tones_dir):
        if filename.endswith('.json'):
            genre_name = filename.replace('.json', '')
            filepath = os.path.join(tones_dir, filename)
            with open(filepath, 'r') as f:
                genres[genre_name] = json.load(f)
    return genres
