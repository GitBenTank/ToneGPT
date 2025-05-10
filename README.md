# ToneGPT for Fractal FM9 🎸

ToneGPT is an AI-assisted tool designed to help guitarists create and explore custom tone presets for the Fractal FM9. Select a genre, get suggested amps, cabs, and effects, and see detailed insights for each block.

---

## 🚀 Features

- Genre-based tone preset selector
- Amp and cab recommendations
- Suggested effects chain
- Summary description of tone
- Detailed block insights from `blocks.json`

---

## 📁 Project Structure

ToneGPT-FM9/
├── frontend.py
├── core/
│ └── tone_loader.py
├── interface/
│ └── block_insights.py
├── tones/
│ ├── ambient.json
│ ├── metal.json
│ ├── funk.json
│ └── ...etc
├── blocks/
│ └── blocks.json
├── README.md
└── requirements.txt


---

## ▶️ How to Run

```bash
# Install requirements
pip install -r requirements.txt

# Run the app
streamlit run frontend.py

---

Then open the browser at http://localhost:8501

---
## 📦 Requirements
pip install streamlit json5

---

## 🧠 Future Plans
Export to FM9 preset formats

Upload your own tone files

PDF tone sheet generation

Genre/tag-based search
