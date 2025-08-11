#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# run.sh — activate venv and launch the UI
# ──────────────────────────────────────────────────────────────────────────────

# move to the script’s directory (repo root)
cd "$(dirname "$0")"

# activate the virtualenv
source .venv/bin/activate

# run Streamlit
streamlit run ui/frontend_v3_blocks.py

