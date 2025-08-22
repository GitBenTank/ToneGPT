# 🎛️ ToneGPT for Fractal FM9

> **Current Version:** v3 — Cleaned JSON, Organized Structure, UI Bypass Ready

ToneGPT is an AI assistant designed to help guitarists create tone presets for the **Fractal FM9**. It uses structured JSON data to dynamically generate tone chains based on **genre**, **band**, or **effect tags**, with an interactive UI for tone building.

[![GitHub release](https://img.shields.io/github/v/release/GitBenTank/ToneGPT-FM9-V3?style=flat-square)](https://github.com/GitBenTank/ToneGPT-FM9-V3/releases)
[![GitHub issues](https://img.shields.io/github/issues/GitBenTank/ToneGPT-FM9-V3?style=flat-square)](https://github.com/GitBenTank/ToneGPT-FM9-V3/issues)
[![GitHub stars](https://img.shields.io/github/stars/GitBenTank/ToneGPT-FM9-V3?style=flat-square)](https://github.com/GitBenTank/ToneGPT-FM9-V3/stargazers)
[![License](https://img.shields.io/github/license/GitBenTank/ToneGPT-FM9-V3?style=flat-square)](LICENSE)

---

## 🚀 Features

- ✅ **Genre-based tone search** (metal, ambient, funk, blues, etc.)
- ✅ **Band & tag-based refinement** (Deftones, ambient lead, fuzz)
- ✅ **Fully cleaned amps & cabs lists** from Fractal Wiki
- ✅ **Streamlit UI** with Bypass Toggles for each block
- ✅ **Visual signal path display**
- ✅ **Ready for Scenes & Controllers expansion** (v3-dev branch)

---

## 📂 Project Structure

```
ToneGPT-FM9-V3/
├── data/                    # Cleaned amps and cabs JSON lists
│   ├── amps_list.json
│   └── cabs_list.json
├── tonegpt/                 # Core logic, config, interface, tests
│   ├── core/               # Core functionality
│   ├── interface/          # UI interface components
│   ├── config.py           # Configuration settings
│   └── aliases.json        # Block aliases and mappings
├── tones/                   # Genre-based tone preset JSON files
│   ├── metal.json
│   ├── ambient.json
│   ├── blues.json
│   └── ... (other genres)
├── ui/                      # Streamlit UI files
│   └── frontend_v3_blocks.py
├── fractalaudio_scraper.py  # Scraping utility for amps/cabs data
├── ToneSync.py              # Core tone chain manager
├── run.sh                   # Shell script to launch UI
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## 🧠 How It Works

1. **User Input**: Enter band, genre, or effect tags
2. **Template Matching**: JSON preset templates are matched from `/tones/`
3. **Model Selection**: Amp & Cab models pulled from cleaned `/data/` lists
4. **UI Interaction**: Select blocks, toggle bypass, view signal chain
5. **Output**: Reference chain for FM9 tone building

---

## 🛠️ Installation

```bash
# Clone repository
git clone https://github.com/GitBenTank/ToneGPT-FM9-V3.git
cd ToneGPT-FM9-V3

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the UI
bash run.sh  # On Windows: python -m streamlit run ui/frontend_v3_blocks.py
```

---

## 🎯 Roadmap

- **v3 (Current)**: UI refactor, branding cleanup, dropdown loader integration
- **v3-dev**: Scenes & Controllers UI expansion
- **Future**: Export helper for .syx FM9 files, real-time assistant chatbot
- **Long-term**: Full signal path designer with Scenes, X/Y, and Blocks export

---

## 🤝 Contributing

PRs, forks, and suggestions are welcome! The goal is to make ToneGPT a helpful, clean tool for FM9 users.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📋 Changelog

### v3 (Current)
- UI refactor and branding cleanup
- Dropdown loader integration
- Repository rename for clarity
- New `v3-dev` branch for staging features

### v2
- Cleaned tone data and organized structure
- UI bypass toggle functionality

### v1
- Initial release with core JSON data and basic backend
