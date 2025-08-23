import streamlit as st
import json
from pathlib import Path
import sys
import os

# Add the parent directory to the path so we can import tonegpt modules
sys.path.append(str(Path(__file__).parent.parent))

from tonegpt.core.ai_tone_generator import AIToneGenerator

# ──────────────────────────────────────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ToneGPT AI - FM9 Tone Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────────────────────
# Initialize AI Tone Generator
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_ai_generator():
    """Initialize the AI tone generator"""
    return AIToneGenerator()

ai_generator = get_ai_generator()

# ──────────────────────────────────────────────────────────────────────────────
# Load Data
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
AMPS_FILE = DATA_DIR / "amps_list.json"
CABS_FILE = DATA_DIR / "cabs_list.json"

@st.cache_data(show_spinner=False)
def load_list(path: Path, key: str):
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        st.error(f"Failed to load {path.name}: {e}")
        return []

    if isinstance(raw, list) and (not raw or isinstance(raw[0], str)):
        return [s.strip() for s in raw if isinstance(s, str)]

    out = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict) and key in item and item[key]:
                out.append(str(item[key]).strip())
    return out

# Build dropdown arrays
amp_models = ["None"] + sorted(load_list(AMPS_FILE, "Model"), key=str.upper)
cab_models = ["None"] + sorted(load_list(CABS_FILE, "Cab"), key=str.upper)

# ──────────────────────────────────────────────────────────────────────────────
# Session State Management
# ──────────────────────────────────────────────────────────────────────────────
if 'current_tone' not in st.session_state:
    st.session_state.current_tone = None
if 'tone_history' not in st.session_state:
    st.session_state.tone_history = []
if 'ai_query' not in st.session_state:
    st.session_state.ai_query = ""

# ──────────────────────────────────────────────────────────────────────────────
# Main UI Layout
# ──────────────────────────────────────────────────────────────────────────────
st.title("🎛️ ToneGPT AI - FM9 Tone Generator")
st.markdown("**AI-powered tone creation for Fractal FM9 - Create tones with natural language!**")

# ──────────────────────────────────────────────────────────────────────────────
# AI Tone Generation Section
# ──────────────────────────────────────────────────────────────────────────────
st.header("🤖 AI Tone Generation")

# AI Query Input
col1, col2 = st.columns([3, 1])
with col1:
    ai_query = st.text_input(
        "Describe the tone you want:",
        placeholder="e.g., 'Give me a Deftones-style metal tone' or 'Clean ambient lead with delay'",
        value=st.session_state.ai_query,
        key="ai_query_input"
    )

with col2:
    if st.button("🎯 Generate Tone", type="primary", use_container_width=True):
        if ai_query.strip():
            st.session_state.ai_query = ai_query
            with st.spinner("🤖 AI is crafting your perfect tone..."):
                try:
                    # Generate the tone
                    generated_tone = ai_generator.generate_tone_from_query(ai_query)
                    st.session_state.current_tone = generated_tone
                    st.session_state.tone_history.append(generated_tone)
                    st.success("✨ AI tone generated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating tone: {e}")
        else:
            st.warning("Please enter a tone description!")

# Display generated tone info
if st.session_state.current_tone:
    tone = st.session_state.current_tone
    
    st.subheader("🎵 Generated Tone")
    
    # Tone description and details
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Description:** {tone['description']}")
        st.markdown(f"**Genre:** {tone['intent']['genre'].title()}")
        if tone['intent']['characteristics']:
            st.markdown(f"**Characteristics:** {', '.join(tone['intent']['characteristics']).title()}")
    
    with col2:
        if st.button("🔄 Generate Variation", use_container_width=True):
            with st.spinner("Creating variation..."):
                variation = ai_generator.generate_tone_from_query(ai_query)
                variation['variation'] = len(st.session_state.tone_history) + 1
                st.session_state.current_tone = variation
                st.session_state.tone_history.append(variation)
                st.rerun()
    
    st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# FM9 Edit-like Interface
# ──────────────────────────────────────────────────────────────────────────────
st.header("🎛️ FM9 Tone Builder")

# Signal Chain Visualization
st.subheader("🔗 Signal Chain")
if st.session_state.current_tone:
    tone = st.session_state.current_tone['tone_patch']
    
    # Create signal chain visualization
    chain = ["Input"]
    for block_name, block_data in tone.items():
        if block_data.get('enabled', False):
            chain.append(f"🎛️ {block_data['type']}")
    chain.append("Output")
    
    # Display as a flow
    cols = st.columns(len(chain))
    for i, (col, block) in enumerate(zip(cols, chain)):
        if i == 0 or i == len(chain) - 1:
            col.markdown(f"**{block}**")
        else:
            col.markdown(f"**{block}**")
        
        if i < len(chain) - 1:
            col.markdown("➡️")

st.divider()

# Block Configuration Interface
st.subheader("⚙️ Block Configuration")

# Row 1: Drive Blocks
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🔥 Drive 1**")
    if st.session_state.current_tone:
        tone = st.session_state.current_tone['tone_patch']
        drive1 = tone.get('drive_1', {})
        
        bypass_d1 = st.checkbox("Bypass", value=not drive1.get('enabled', False), key="bypass_d1")
        if not bypass_d1 and drive1.get('enabled'):
            # X/Y Channel Selection
            if 'channels' in drive1:
                current_ch = drive1.get('current_channel', 'A')
                channel = st.selectbox("Channel", ["A", "B", "C", "D"], 
                                     index=ord(current_ch) - ord('A'), key="d1_channel")
                
                # Show current channel info
                ch_data = drive1['channels'][channel]
                st.selectbox("Drive Type", [ch_data['type']], index=0, key="d1_type", disabled=True)
                
                # Parameters for current channel
                params = ch_data.get('parameters', {})
                gain = st.slider("Gain", 0.0, 10.0, params.get('gain', 5.0), key="d1_gain")
                level = st.slider("Level", 0.0, 10.0, params.get('level', 5.0), key="d1_level")
                tone_param = st.slider("Tone", 0.0, 10.0, params.get('tone', 5.0), key="d1_tone")
                
                # Show all channels info
                with st.expander(f"All Channels (Current: {channel})"):
                    for ch, data in drive1['channels'].items():
                        ch_params = data['parameters']
                        st.write(f"**Ch.{ch}**: {data['type']} - Gain:{ch_params['gain']}, Level:{ch_params['level']}")
            else:
                # Legacy single channel
                sel_d1 = st.selectbox("Drive Type", ["None"] + ai_generator.blocks_data.get("gain", []), 
                                     index=0 if drive1.get('type') == "None" else 1, key="d1_type")
                
                if sel_d1 != "None":
                    params = drive1.get('parameters', {})
                    gain = st.slider("Gain", 0.0, 10.0, params.get('gain', 5.0), key="d1_gain")
                    level = st.slider("Level", 0.0, 10.0, params.get('level', 5.0), key="d1_level")
                    tone_param = st.slider("Tone", 0.0, 10.0, params.get('tone', 5.0), key="d1_tone")
        else:
            st.info("Drive 1 is bypassed")

with col2:
    st.markdown("**🔥 Drive 2**")
    if st.session_state.current_tone:
        tone = st.session_state.current_tone['tone_patch']
        drive2 = tone.get('drive_2', {})
        
        bypass_d2 = st.checkbox("Bypass", value=not drive2.get('enabled', False), key="bypass_d2")
        if not bypass_d2 and drive2.get('enabled'):
            sel_d2 = st.selectbox("Drive Type", ["None"] + ai_generator.blocks_data.get("drive", {}).get("types", []), 
                                 index=0 if drive2.get('type') == "None" else 1, key="d2_type")
            
            if sel_d2 != "None":
                params = drive2.get('parameters', {})
                gain = st.slider("Gain", 0.0, 10.0, params.get('gain', 5.0), key="d2_gain")
                level = st.slider("Level", 0.0, 10.0, params.get('level', 5.0), key="d2_level")
                tone_param = st.slider("Tone", 0.0, 10.0, params.get('tone', 5.0), key="d2_tone")
        else:
            st.info("Drive 2 is bypassed")

with col3:
    st.markdown("**🎸 Amp & Cab**")
    if st.session_state.current_tone:
        tone = st.session_state.current_tone['tone_patch']
        amp = tone.get('amp', {})
        cab = tone.get('cab', {})
        
        # Amp with X/Y Channels
        bypass_amp = st.checkbox("Bypass Amp", value=not amp.get('enabled', False), key="bypass_amp")
        if not bypass_amp and amp.get('enabled'):
            # X/Y Channel Selection for Amp
            if 'channels' in amp:
                current_ch = amp.get('current_channel', 'A')
                channel = st.selectbox("Amp Channel", ["A", "B", "C", "D"], 
                                     index=ord(current_ch) - ord('A'), key="amp_channel")
                
                # Show current channel info
                ch_data = amp['channels'][channel]
                st.selectbox("Amp Model", [ch_data['type']], index=0, key="amp_type", disabled=True)
                
                # Parameters for current channel
                params = ch_data.get('parameters', {})
                gain = st.slider("Amp Gain", 0.0, 10.0, params.get('gain', 5.0), key="amp_gain")
                master = st.slider("Master Vol", 0.0, 10.0, params.get('master', 5.0), key="amp_master")
                bass = st.slider("Bass", 0.0, 10.0, params.get('bass', 5.0), key="amp_bass")
                mid = st.slider("Mid", 0.0, 10.0, params.get('mid', 5.0), key="amp_mid")
                treble = st.slider("Treble", 0.0, 10.0, params.get('treble', 5.0), key="amp_treble")
                
                # Show all channels info
                with st.expander(f"All Amp Channels (Current: {channel})"):
                    for ch, data in amp['channels'].items():
                        ch_params = data['parameters']
                        gain_level = "Clean" if ch_params['gain'] < 4 else "Crunch" if ch_params['gain'] < 6 else "Lead" if ch_params['gain'] < 8 else "High Gain"
                        st.write(f"**Ch.{ch}**: {data['type']} - Gain:{ch_params['gain']} ({gain_level})")
            else:
                # Legacy single channel
                sel_amp = st.selectbox("Amp Model", amp_models, 
                                     index=amp_models.index(amp.get('type', 'None')) if amp.get('type') in amp_models else 0, key="amp_type")
                
                if sel_amp != "None":
                    params = amp.get('parameters', {})
                    gain = st.slider("Amp Gain", 0.0, 10.0, params.get('gain', 5.0), key="amp_gain")
                    master = st.slider("Master Vol", 0.0, 10.0, params.get('master', 5.0), key="amp_master")
                    bass = st.slider("Bass", 0.0, 10.0, params.get('bass', 5.0), key="amp_bass")
                    mid = st.slider("Mid", 0.0, 10.0, params.get('mid', 5.0), key="amp_mid")
                    treble = st.slider("Treble", 0.0, 10.0, params.get('treble', 5.0), key="amp_treble")
        
        # Cab
        bypass_cab = st.checkbox("Bypass Cab", value=not cab.get('enabled', False), key="bypass_cab")
        if not bypass_cab and cab.get('enabled'):
            sel_cab = st.selectbox("Cab IR", cab_models, 
                                 index=cab_models.index(cab.get('type', 'None')) if cab.get('type') in cab_models else 0, key="cab_type")
            
            if sel_cab != "None":
                params = cab.get('parameters', {})
                lowcut = st.slider("Low Cut (Hz)", 20, 1000, params.get('lowcut', 80), key="cab_lowcut")
                highcut = st.slider("High Cut (Hz)", 2000, 20000, params.get('highcut', 8000), key="cab_highcut")

# Row 2: Effects
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("**🎛️ EQ Block**")
    if st.session_state.current_tone:
        tone = st.session_state.current_tone['tone_patch']
        eq = tone.get('eq', {})
        
        bypass_eq = st.checkbox("Bypass EQ", value=not eq.get('enabled', False), key="bypass_eq")
        if not bypass_eq and eq.get('enabled'):
            sel_eq = st.selectbox("EQ Type", ["None"] + ai_generator.blocks_data.get("eq", {}).get("types", []), 
                                 index=0 if eq.get('type') == "None" else 1, key="eq_type")
            
            if sel_eq != "None":
                params = eq.get('parameters', {})
                low = st.slider("Low (dB)", -12.0, 12.0, params.get('low', 0.0), key="eq_low")
                mid = st.slider("Mid (dB)", -12.0, 12.0, params.get('mid', 0.0), key="eq_mid")
                high = st.slider("High (dB)", -12.0, 12.0, params.get('high', 0.0), key="eq_high")
        else:
            st.info("EQ is bypassed")

with col5:
    st.markdown("**⏰ Delay Block**")
    if st.session_state.current_tone:
        tone = st.session_state.current_tone['tone_patch']
        delay = tone.get('delay', {})
        
        bypass_delay = st.checkbox("Bypass Delay", value=not delay.get('enabled', False), key="bypass_delay")
        if not bypass_delay and delay.get('enabled'):
            sel_delay = st.selectbox("Delay Type", ["None"] + ai_generator.blocks_data.get("delay", {}).get("types", []), 
                                    index=0 if delay.get('type') == "None" else 1, key="delay_type")
            
            if sel_delay != "None":
                params = delay.get('parameters', {})
                time = st.slider("Time (ms)", 0, 2000, params.get('time', 500), key="delay_time")
                mix = st.slider("Mix (%)", 0.0, 100.0, params.get('mix', 30.0), key="delay_mix")
                feedback = st.slider("Feedback (%)", 0.0, 100.0, params.get('feedback', 20.0), key="delay_feedback")
        else:
            st.info("Delay is bypassed")

with col6:
    st.markdown("**🌊 Reverb Block**")
    if st.session_state.current_tone:
        tone = st.session_state.current_tone['tone_patch']
        reverb = tone.get('reverb', {})
        
        bypass_reverb = st.checkbox("Bypass Reverb", value=not reverb.get('enabled', False), key="bypass_reverb")
        if not bypass_reverb and reverb.get('enabled'):
            sel_reverb = st.selectbox("Reverb Type", ["None"] + ai_generator.blocks_data.get("reverb", {}).get("types", []), 
                                     index=0 if reverb.get('type') == "None" else 1, key="reverb_type")
            
            if sel_reverb != "None":
                params = reverb.get('parameters', {})
                room_size = st.slider("Room Size", 0.0, 10.0, params.get('room_size', 5.0), key="reverb_size")
                mix = st.slider("Mix (%)", 0.0, 100.0, params.get('mix', 30.0), key="reverb_mix")
                decay = st.slider("Decay", 0.0, 10.0, params.get('decay', 5.0), key="reverb_decay")
        else:
            st.info("Reverb is bypassed")

# ──────────────────────────────────────────────────────────────────────────────
# Tone Management
# ──────────────────────────────────────────────────────────────────────────────
st.divider()
st.header("💾 Tone Management")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💾 Save Current Tone", use_container_width=True):
        if st.session_state.current_tone:
            # Save to session state for now (could be extended to save to file)
            st.success("Tone saved to session!")
        else:
            st.warning("No tone to save!")

with col2:
    if st.button("📋 Export to FM9", use_container_width=True):
        if st.session_state.current_tone:
            st.info("Export functionality coming soon! This will generate FM9-compatible files.")
        else:
            st.warning("No tone to export!")

with col3:
    if st.button("🔄 Reset to Default", use_container_width=True):
        st.session_state.current_tone = None
        st.rerun()

# ──────────────────────────────────────────────────────────────────────────────
# Tone History
# ──────────────────────────────────────────────────────────────────────────────
if st.session_state.tone_history:
    st.divider()
    st.header("📚 Tone History")
    
    for i, tone in enumerate(reversed(st.session_state.tone_history[-5:])):  # Show last 5
        with st.expander(f"🎵 {tone['description']} (Query: '{tone['query']}')"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**Genre:** {tone['intent']['genre'].title()}")
                if tone['intent']['characteristics']:
                    st.markdown(f"**Characteristics:** {', '.join(tone['intent']['characteristics']).title()}")
                st.markdown(f"**Generated:** {tone.get('variation', 'Original')}")
            
            with col2:
                if st.button(f"Load Tone {i+1}", key=f"load_{i}"):
                    st.session_state.current_tone = tone
                    st.rerun()

# ──────────────────────────────────────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────────────────────────────────────
st.divider()
st.caption("🎸 ToneGPT AI | AI-powered FM9 tone generation | Built with ❤️ for guitarists")

# Sidebar for additional features
with st.sidebar:
    st.header("🎛️ Quick Actions")
    
    st.subheader("🎯 Popular Tones")
    popular_queries = [
        "Deftones-style metal tone",
        "Clean ambient lead",
        "Blues rhythm tone",
        "Classic rock lead",
        "Funk rhythm groove"
    ]
    
    for query in popular_queries:
        if st.button(query, use_container_width=True):
            st.session_state.ai_query = query
            st.rerun()
    
    st.divider()
    
    st.subheader("⚙️ Settings")
    st.checkbox("Auto-save tones", value=True)
    st.checkbox("Show parameter ranges", value=True)
    
    st.divider()
    
    st.subheader("📊 Stats")
    st.metric("Tones Generated", len(st.session_state.tone_history))
    st.metric("Current Session", "Active")
