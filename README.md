# 🎛️ ToneGPT for Fractal FM9
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Last Commit](https://img.shields.io/github/last-commit/GitBenTank/ToneGPT-FM9-V2)

ToneGPT is an AI assistant built to help guitarists generate tone presets for the Fractal FM9. Powered by structured JSON data, it enables genre- and tag-based searches to build effect block chains tailored to specific sounds, bands, or styles.

---

## 🚀 Features
- Genre-based tone search (e.g. `metal`, `ambient`, `funk`)
- Band-based search (e.g. `Deftones`, `Explosions in the Sky`)
- Tag-based refinement (e.g. `clean`, `lead`, `synth`)
- JSON-based preset suggestions
- Modular design to support expansion

---

## 📂 Project Structure

```
ToneGPT-FM9-V2/
├── tones/                      # JSON tone preset files organized by genre
│   ├── metal.json
│   ├── ambient.json
│   └── ...
├── blocks.json                # Master block definitions (drive, modulation, ambience, etc.)
├── main.py                    # Core logic for input parsing and tone generation
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🧠 How It Works
- The tool takes input such as `ambient lead` or `funk rhythm`
- It maps your query to preset templates in `tones/`
- Block chains are generated from `blocks.json` to match the tone type
- Returns are formatted for reference and future FM9 conversion

---

## 🔍 Genre/Tag-Based Tone Search
ToneGPT-FM9 supports a variety of input styles:
- **Band names** — e.g. `Paramore`, `Tool`, `Cocteau Twins`
- **Genres** — e.g. `math rock`, `synthwave`, `blues`
- **Tags** — e.g. `clean`, `lead`, `crunch`, `ambient`

The assistant intelligently selects a tone chain and relevant block configuration.

---

## 🛠️ Installation
1. Clone the repo:
```bash
git clone https://github.com/GitBenTank/ToneGPT-FM9-V2.git
cd ToneGPT-FM9-V2
```
2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the tool:
```bash
python main.py
```

---

## 🎥 Demo
UI in development — demo GIF coming soon!

---

## 📌 Dependencies
- [RapidFuzz](https://github.com/maxbachmann/RapidFuzz): Fuzzy string matching

---

## 📅 Roadmap
- [x] Genre/tag-based tone search
- [ ] Streamlit or Flask web interface
- [ ] Export to `.syx` format for FM9
- [ ] Real-time tone assistant chatbot

---

## 🙌 Contributing
Open to collaboration! Feel free to fork, submit PRs, or drop suggestions.

---

## ©️ License
MIT
