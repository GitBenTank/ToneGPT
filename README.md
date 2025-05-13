# 🎛️ ToneGPT for Fractal FM9

> **Current Version:** v2 — Cleaned JSON, Organized Structure, UI Bypass Ready

ToneGPT is an AI assistant designed to help guitarists create tone presets for the **Fractal FM9**. It uses structured JSON data to dynamically generate tone chains based on **genre**, **band**, or **effect tags**, with an interactive UI for tone building.

---

## 🚀 Features
- ✅ Genre-based tone search (e.g. metal, ambient, funk)
- ✅ Band & tag-based refinement (e.g. Deftones, ambient lead, fuzz)
- ✅ Fully cleaned amps & cabs lists from Fractal Wiki
- ✅ Streamlit UI with Bypass Toggles for each block
- ✅ Visual signal path display
- ✅ Ready for Scenes & Controllers expansion (v3-dev branch)

---

## 📂 Project Structure

ToneGPT-FM9-V2/
├── data/                # Cleaned amps and cabs JSON lists
│   ├── amps_list.json
│   └── cabs_list.json
├── tonegpt/             # Core logic, config, interface, tests
│   ├── core/
│   ├── interface/
│   ├── config.py
│   └── aliases.json
├── tones/               # Genre-based tone preset JSON files
│   ├── metal.json
│   ├── ambient.json
│   └── etc…
├── ui/                  # Streamlit UI files
│   └── frontend_v3_blocks.py
├── fractalaudio_scraper.py # Scraping utility for amps/cabs data
├── ToneSync.py          # Core tone chain manager (future v3 expansions)
├── run.sh               # Shell script to launch UI
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── LICENSE
└── venv/                # Virtual environment (local)

---

## 🧠 How It Works
1. User inputs band, genre, or tags.
2. JSON preset templates (from `/tones/`) are matched.
3. Amp & Cab models pulled from cleaned `/data/` lists.
4. UI allows block selection, bypass toggles, and visual signal chain.
5. Outputs a reference chain for FM9 tone building.

---

## 🛠️ Installation
```bash
# Clone repo
git clone https://github.com/GitBenTank/ToneGPT-FM9-V2.git
cd ToneGPT-FM9-V2

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the UI
bash run.sh

---

🎯 Roadmap
	•	v2 - Data cleaned, UI Bypass Toggle complete
	•	v3 - Scenes & Controllers UI
	•	Export helper for .syx FM9 files
	•	Real-time assistant (chatbot / tone suggester)
	•	Full signal path designer with Scenes, X/Y, and Blocks export

⸻

🙌 Contributing

PRs, forks, and suggestions are welcome. The goal is to make ToneGPT a helpful, clean tool for FM9 users.

⸻

📄 License

MIT License
