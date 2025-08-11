import streamlit as st
import json
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# 0) Page config (must be first Streamlit call)
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="ToneGPT – FM9 Blocks", layout="wide")

# ──────────────────────────────────────────────────────────────────────────────
# 1) Locate your JSON files (repo root is parent of /ui)
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).resolve().parent.parent
DATA_DIR  = BASE_DIR / "data"
AMPS_FILE = DATA_DIR / "amps_list.json"
CABS_FILE = DATA_DIR / "cabs_list.json"

# ──────────────────────────────────────────────────────────────────────────────
# 2) Load & normalize flat lists (strings) or keyed objects
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_list(path: Path, key: str):
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        st.error(f"Failed to load {path.name}: {e}")
        return []

    # If it's already a flat list of strings, return it
    if isinstance(raw, list) and (not raw or isinstance(raw[0], str)):
        return [s.strip() for s in raw if isinstance(s, str)]

    # Otherwise expect list of dicts and pull out `key`
    out = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict) and key in item and item[key]:
                out.append(str(item[key]).strip())
    return out

# Build dropdown arrays (sorted for sanity)
amp_models = ["None"] + sorted(load_list(AMPS_FILE, "Model"), key=str.upper)
cab_models = ["None"] + sorted(load_list(CABS_FILE, "Cab"),   key=str.upper)

# Tiny debug readout so you know it worked
st.caption(f"Loaded {max(0, len(amp_models)-1)} amps • {max(0, len(cab_models)-1)} cabs")

# ──────────────────────────────────────────────────────────────────────────────
# 3) Hard-coded FM9 block lists
# ──────────────────────────────────────────────────────────────────────────────
drive_blocks  = ["None", "FAS Boost", "TS808 Mod", "Klon", "Rat Distortion"]
eq_blocks     = ["None", "5 Band EQ", "10 Band EQ", "Parametric EQ"]
delay_blocks  = ["None", "Digital Stereo Delay", "Tape Delay", "Ping Pong Delay"]
reverb_blocks = ["None", "Medium Plate", "Large Hall", "Spring Reverb"]

# ──────────────────────────────────────────────────────────────────────────────
# 4) Streamlit UI layout
# ──────────────────────────────────────────────────────────────────────────────
st.title("🎛️ ToneGPT – FM9 Blocks (Bypass Toggles)")

# First row
c1, c2, c3 = st.columns(3)

with c1:
    st.header("Drive 1")
    bypass_d1 = st.checkbox("Bypass Drive 1", key="bypass_d1")
    sel_d1    = st.selectbox("Select Drive 1", drive_blocks, key="d1")
    if sel_d1 != "None" and not bypass_d1:
        st.slider("Gain",  0.0, 10.0, 5.0, key="d1_gain")
        st.slider("Level", 0.0, 10.0, 5.0, key="d1_lvl")

with c2:
    st.header("Drive 2")
    bypass_d2 = st.checkbox("Bypass Drive 2", key="bypass_d2")
    sel_d2    = st.selectbox("Select Drive 2", drive_blocks, key="d2")
    if sel_d2 != "None" and not bypass_d2:
        st.slider("Gain",  0.0, 10.0, 5.0, key="d2_gain")
        st.slider("Level", 0.0, 10.0, 5.0, key="d2_lvl")

with c3:
    st.header("Amp & Cab")
    bypass_amp = st.checkbox("Bypass Amp", key="bypass_amp")
    sel_amp    = st.selectbox("Select Amp", amp_models, key="amp")
    if sel_amp != "None" and not bypass_amp:
        st.slider("Amp Gain",   0.0, 10.0, 5.0, key="amp_gain")
        st.slider("Master Vol", 0.0, 10.0, 5.0, key="amp_master")

    bypass_cab = st.checkbox("Bypass Cab", key="bypass_cab")
    sel_cab    = st.selectbox("Select Cab IR", cab_models, key="cab")

# Second row
c4, c5, c6 = st.columns(3)

with c4:
    st.header("EQ Block")
    bypass_eq = st.checkbox("Bypass EQ", key="bypass_eq")
    sel_eq    = st.selectbox("Select EQ", eq_blocks, key="eq")
    if sel_eq != "None" and not bypass_eq:
        st.slider("Low (dB)",  -12.0, 12.0, 0.0, key="eq_low")
        st.slider("Mid (dB)",  -12.0, 12.0, 0.0, key="eq_mid")
        st.slider("High (dB)", -12.0, 12.0, 0.0, key="eq_high")

with c5:
    st.header("Delay Block")
    bypass_dl = st.checkbox("Bypass Delay", key="bypass_dl")
    sel_dl    = st.selectbox("Select Delay", delay_blocks, key="dl")
    if sel_dl != "None" and not bypass_dl:
        st.slider("Time (ms)",  0,   2000, 500,   key="dl_time")
        st.slider("Mix (%)",    0.0, 100.0,30.0, key="dl_mix")

with c6:
    st.header("Reverb Block")
    bypass_rv = st.checkbox("Bypass Reverb", key="bypass_rv")
    sel_rv    = st.selectbox("Select Reverb", reverb_blocks, key="rv")
    if sel_rv != "None" and not bypass_rv:
        st.slider("Room Size",  0.0, 10.0, 5.0, key="rv_size")
        st.slider("Mix (%)",    0.0, 100.0,30.0, key="rv_mix")

# ──────────────────────────────────────────────────────────────────────────────
# 5) Signal-chain summary
# ──────────────────────────────────────────────────────────────────────────────
path = ["Input"]
for name, bypass, sel in [
    ("Drive 1", bypass_d1, sel_d1),
    ("Drive 2", bypass_d2, sel_d2),
    ("Amp",     bypass_amp, sel_amp),
    ("Cab",     bypass_cab, sel_cab),
    ("EQ",      bypass_eq, sel_eq),
    ("Delay",   bypass_dl, sel_dl),
    ("Reverb",  bypass_rv, sel_rv),
]:
    if sel != "None" and not bypass:
        path.append(sel)
path.append("Output")

st.subheader("🧩 Signal Path")
st.success(" ➔ ".join(path))
st.caption("ToneGPT | Fractal FM9 Companion UI")