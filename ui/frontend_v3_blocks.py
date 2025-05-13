import streamlit as st
import json

# Load amps and cabs data
with open('data/amps_list.json', 'r') as f:
    amps_data = json.load(f)

with open('data/cabs_list.json', 'r') as f:
    cabs_data = json.load(f)

# Example block options
drive_blocks = ["None", "FAS Boost", "TS808 Mod", "Klon", "Rat Distortion"]
delay_blocks = ["None", "Digital Stereo Delay", "Tape Delay", "Ping Pong Delay"]
reverb_blocks = ["None", "Medium Plate", "Large Hall", "Spring Reverb"]
eq_blocks = ["None", "5 Band EQ", "10 Band EQ", "Parametric EQ"]

# Extract amp & cab names
amp_models = [amp['Model'] for amp in amps_data]
cab_models = [cab['Cab'] for cab in cabs_data]

# Streamlit Config
st.set_page_config(page_title="ToneGPT - FM9 Blocks", layout="wide")
st.title("🎛️ ToneGPT - FM9 Blocks (Bypass Toggles Added)")

# Layout Grid - Mimic FM9 Edit
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Drive 1")
    bypass_drive1 = st.checkbox("Bypass Drive 1", value=False, key="bypass_drive1")
    selected_drive1 = st.selectbox("Select Drive 1", drive_blocks, key="drive1_select")
    if selected_drive1 != "None" and not bypass_drive1:
        drive1_gain = st.slider("Gain", 0.0, 10.0, 5.0, key="drive1_gain")
        drive1_level = st.slider("Level", 0.0, 10.0, 5.0, key="drive1_level")

with col2:
    st.header("Drive 2")
    bypass_drive2 = st.checkbox("Bypass Drive 2", value=False, key="bypass_drive2")
    selected_drive2 = st.selectbox("Select Drive 2", drive_blocks, key="drive2_select")
    if selected_drive2 != "None" and not bypass_drive2:
        drive2_gain = st.slider("Gain", 0.0, 10.0, 5.0, key="drive2_gain")
        drive2_level = st.slider("Level", 0.0, 10.0, 5.0, key="drive2_level")

with col3:
    st.header("Amp & Cab")
    bypass_amp = st.checkbox("Bypass Amp", value=False, key="bypass_amp")
    selected_amp = st.selectbox("Select Amp", amp_models, key="amp_select")
    amp_gain = st.slider("Amp Gain", 0.0, 10.0, 5.0, key="amp_gain")
    amp_master = st.slider("Master Volume", 0.0, 10.0, 5.0, key="amp_master")

    bypass_cab = st.checkbox("Bypass Cab", value=False, key="bypass_cab")
    selected_cab = st.selectbox("Select Cab IR", cab_models, key="cab_select")

# Second row grid for EQ, Delay, Reverb
col4, col5, col6 = st.columns(3)

with col4:
    st.header("EQ Block")
    bypass_eq = st.checkbox("Bypass EQ", value=False, key="bypass_eq")
    selected_eq = st.selectbox("Select EQ", eq_blocks, key="eq_select")
    if selected_eq != "None" and not bypass_eq:
        eq_low = st.slider("Low Freq", -12.0, 12.0, 0.0, key="eq_low")
        eq_mid = st.slider("Mid Freq", -12.0, 12.0, 0.0, key="eq_mid")
        eq_high = st.slider("High Freq", -12.0, 12.0, 0.0, key="eq_high")

with col5:
    st.header("Delay Block")
    bypass_delay = st.checkbox("Bypass Delay", value=False, key="bypass_delay")
    selected_delay = st.selectbox("Select Delay", delay_blocks, key="delay_select")
    if selected_delay != "None" and not bypass_delay:
        delay_time = st.slider("Delay Time (ms)", 0, 2000, 500, key="delay_time")
        delay_mix = st.slider("Mix", 0.0, 100.0, 30.0, key="delay_mix")

with col6:
    st.header("Reverb Block")
    bypass_reverb = st.checkbox("Bypass Reverb", value=False, key="bypass_reverb")
    selected_reverb = st.selectbox("Select Reverb", reverb_blocks, key="reverb_select")
    if selected_reverb != "None" and not bypass_reverb:
        reverb_size = st.slider("Room Size", 0.0, 10.0, 5.0, key="reverb_size")
        reverb_mix = st.slider("Mix", 0.0, 100.0, 30.0, key="reverb_mix")

# Signal Path Visual
st.subheader("🧩 Signal Path Chain")
signal_path = ["Input"]

if selected_drive1 != "None" and not bypass_drive1:
    signal_path.append(selected_drive1)
if selected_drive2 != "None" and not bypass_drive2:
    signal_path.append(selected_drive2)
if selected_amp != "None" and not bypass_amp:
    signal_path.append(selected_amp)
if selected_cab != "None" and not bypass_cab:
    signal_path.append(selected_cab)
if selected_eq != "None" and not bypass_eq:
    signal_path.append(selected_eq)
if selected_delay != "None" and not bypass_delay:
    signal_path.append(selected_delay)
if selected_reverb != "None" and not bypass_reverb:
    signal_path.append(selected_reverb)

signal_path.append("Output")

path_display = " ➔ ".join(signal_path)
st.success(path_display)

st.caption("ToneGPT | Fractal FM9 Companion UI with Bypass Toggles")