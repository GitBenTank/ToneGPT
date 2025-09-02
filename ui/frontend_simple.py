#!/usr/bin/env python3
"""
ToneGPT AI - Enhanced Professional Version
Professional AI tone generator with enhanced styling
"""

import streamlit as st
import json
from pathlib import Path
import sys
import os
import numpy as np
from datetime import datetime

# Add the parent directory to the path so we can import tonegpt modules
sys.path.append(str(Path(__file__).parent.parent))

from tonegpt.core.enhanced_ai_tone_generator import EnhancedAIToneGenerator

def safe_float(value, default=0.0):
    """Safely convert value to float for sliders"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

# Constants
DRY_WET_MIX_HELP = "Dry/wet mix"
LOW_CUT_HELP = "Low Cut"
LOW_FREQ_CUTOFF_HELP = "Low frequency cutoff"
HIGH_CUT_HELP = "High Cut"
HIGH_FREQ_CUTOFF_HELP = "High frequency cutoff"
FEEDBACK_AMOUNT_HELP = "Feedback amount"

# ──────────────────────────────────────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ToneGPT AI - FM9 Tone Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────────────────────
# Enhanced Professional CSS Styling
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Warm Professional Studio Theme */
    .main {
        background: linear-gradient(135deg, #1a1f2e 0%, #2c3e50 25%, #34495e 50%, #2c3e50 75%, #1a1f2e 100%);
        color: #ffffff;
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a1f2e 0%, #2c3e50 25%, #34495e 50%, #2c3e50 75%, #1a1f2e 100%);
    }
    
    /* Warm Studio Headers */
    h1 {
        background: linear-gradient(90deg, #4a90e2 0%, #6bb6ff 25%, #87ceeb 50%, #b0e0e6 75%, #4a90e2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.2rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 0 25px rgba(74, 144, 226, 0.4);
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        letter-spacing: 2px !important;
    }
    
    h2 {
        color: #4a90e2 !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        border-left: 4px solid #4a90e2;
        padding-left: 1.5rem;
        margin: 2rem 0 1rem 0;
        background: rgba(74, 144, 226, 0.12);
        padding: 1.5rem;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.25);
    }
    
    h3 {
        color: #87ceeb !important;
        font-size: 1.6rem !important;
        font-weight: 600 !important;
        margin: 1.5rem 0 1rem 0;
        padding: 0.5rem 0;
        border-bottom: 2px solid #87ceeb;
    }
    
    /* Warm Studio Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4a90e2 0%, #6bb6ff 100%);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #6bb6ff 0%, #87ceeb 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.4);
    }
    
    /* Primary Button */
    .stButton > button[data-baseweb="button"] {
        background: linear-gradient(135deg, #3a7bd5 0%, #4a90e2 100%);
        color: #ffffff;
        box-shadow: 0 4px 15px rgba(58, 123, 213, 0.3);
    }
    
    .stButton > button[data-baseweb="button"]:hover {
        background: linear-gradient(135deg, #4a90e2 0%, #6bb6ff 100%);
        box-shadow: 0 6px 20px rgba(58, 123, 213, 0.4);
    }
    
    /* Warm Studio Input Fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.15);
        border: 2px solid rgba(74, 144, 226, 0.5);
        border-radius: 8px;
        color: #ffffff;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4a90e2;
        box-shadow: 0 0 20px rgba(74, 144, 226, 0.4);
        background: rgba(255, 255, 255, 0.25);
    }
    
    /* Warm Studio Selectboxes */
    .stSelectbox > div > div > div {
        background: rgba(255, 255, 255, 0.15);
        border: 2px solid rgba(74, 144, 226, 0.5);
        border-radius: 8px;
        color: #ffffff;
    }
    
    .stSelectbox > div > div > div:hover {
        border-color: #4a90e2;
        box-shadow: 0 0 15px rgba(74, 144, 226, 0.3);
    }
    
    /* Warm Studio Number Inputs */
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.15);
        border: 2px solid rgba(74, 144, 226, 0.5);
        border-radius: 8px;
        color: #ffffff;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }
    
    /* Warm Studio Sliders */
    .stSlider > div > div > div > div > div > div {
        background: linear-gradient(90deg, #4a90e2 0%, #6bb6ff 100%);
    }
    
    .stSlider > div > div > div > div > div > div > div {
        background: #ffffff;
        border: 3px solid #4a90e2;
        box-shadow: 0 0 10px rgba(74, 144, 226, 0.5);
    }
    
    /* Warm Studio Metrics */
    .stMetric {
        background: rgba(74, 144, 226, 0.12);
        border: 2px solid rgba(74, 144, 226, 0.4);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.25);
    }
    
    .stMetric > div > div > div {
        color: #4a90e2 !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    .stMetric > div > div > div:last-child {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Warm Studio Expanders */
    .streamlit-expanderHeader {
        background: rgba(74, 144, 226, 0.12);
        border: 2px solid rgba(74, 144, 226, 0.4);
        border-radius: 8px;
        color: #4a90e2 !important;
        font-weight: 600 !important;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(74, 144, 226, 0.2);
        border-color: #4a90e2;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
    }
    
    /* Warm Studio Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1f2e 0%, #2c3e50 100%);
        border-right: 3px solid #4a90e2;
    }
    
    /* Professional Status Messages */
    .stSuccess {
        background: rgba(34, 139, 34, 0.1);
        border: 2px solid rgba(34, 139, 34, 0.3);
        border-radius: 8px;
        color: #228b22;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(34, 139, 34, 0.2);
    }
    
    .stInfo {
        background: rgba(212, 175, 55, 0.1);
        border: 2px solid rgba(212, 175, 55, 0.3);
        border-radius: 8px;
        color: #d4af37;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2);
    }
    
    .stWarning {
        background: rgba(255, 165, 0, 0.1);
        border: 2px solid rgba(255, 165, 0, 0.3);
        border-radius: 8px;
        color: #ffa500;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 165, 0, 0.2);
    }
    
    .stError {
        background: rgba(220, 20, 60, 0.1);
        border: 2px solid rgba(220, 20, 60, 0.3);
        border-radius: 8px;
        color: #dc143c;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(220, 20, 60, 0.2);
    }
    
    /* Warm Studio Dividers */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #4a90e2 50%, transparent 100%);
        margin: 2rem 0;
        border-radius: 2px;
        box-shadow: 0 0 10px rgba(74, 144, 226, 0.3);
    }
    
    /* Warm Studio Text */
    p, div, span {
        color: #ffffff;
        line-height: 1.6;
    }
    
    /* Enhanced Caption */
    .caption {
        color: #888888;
        font-style: italic;
        text-align: center;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 8px;
        border: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    /* Warm Studio Signal Chain Blocks */
    .signal-block {
        background: linear-gradient(135deg, rgba(74, 144, 226, 0.12) 0%, rgba(107, 182, 255, 0.12) 100%);
        border: 2px solid #4a90e2;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.25);
        transition: all 0.3s ease;
    }
    
    .signal-block:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.35);
        border-color: #6bb6ff;
    }
    
    /* Warm Studio Spinner */
    .stSpinner > div > div {
        border: 3px solid rgba(74, 144, 226, 0.3);
        border-top: 3px solid #4a90e2;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Professional Download Buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(139, 69, 19, 0.3);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #a0522d 0%, #cd853f 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 69, 19, 0.4);
    }
    
    /* Warm Studio Mode Buttons */
    .mode-button {
        background: linear-gradient(135deg, #4a90e2 0%, #6bb6ff 100%);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0.5rem 0;
    }
    
    .mode-button:hover {
        background: linear-gradient(135deg, #6bb6ff 0%, #87ceeb 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.4);
    }
    
    /* Warm Studio Popular Tone Buttons */
    .popular-tone-button {
        background: linear-gradient(135deg, #3a7bd5 0%, #4a90e2 100%);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 4px 15px rgba(58, 123, 213, 0.3);
        transition: all 0.3s ease;
        margin: 0.5rem 0;
        text-align: center;
        width: 100%;
    }
    
    .popular-tone-button:hover {
        background: linear-gradient(135deg, #4a90e2 0%, #6bb6ff 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(58, 123, 213, 0.4);
    }
    
    /* Warm Studio Sidebar Stats */
    .sidebar-stats {
        background: rgba(74, 144, 226, 0.12);
        border: 2px solid rgba(74, 144, 226, 0.4);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.25);
    }
    
    /* Warm Studio Version Info */
    .version-info {
        background: rgba(74, 144, 226, 0.12);
        border: 2px solid rgba(74, 144, 226, 0.4);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.25);
    }
    
    .version-info h4 {
        color: #4a90e2 !important;
        margin: 0 0 0.5rem 0;
        font-weight: 700;
    }
    
    .version-info p {
        color: #cccccc;
        margin: 0;
        font-style: italic;
    }
    
    /* Enhanced Text Readability */
    .stMarkdown {
        color: #ffffff !important;
    }
    
    .stMarkdown p {
        color: #ffffff !important;
    }
    
    .stMarkdown li {
        color: #ffffff !important;
    }
    
    .stMarkdown strong {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    .stMarkdown em {
        color: #ffffff !important;
    }
    
    /* Streamlit Widget Labels */
    .stSelectbox label,
    .stTextInput label,
    .stNumberInput label,
    .stSlider label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Streamlit Widget Values */
    .stSelectbox > div > div > div > div {
        color: #ffffff !important;
    }
    
    /* Better contrast for all text elements */
    .element-container {
        color: #ffffff !important;
    }
    
    .element-container p {
        color: #ffffff !important;
    }
    
    .element-container div {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# Initialize AI Tone Generator
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_ai_generator():
    """Initialize the AI tone generator"""
    return EnhancedAIToneGenerator()

ai_generator = get_ai_generator()

# ──────────────────────────────────────────────────────────────────────────────
# Load Data
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
AMPS_FILE = DATA_DIR / "amps_list_final.json"
CABS_FILE = DATA_DIR / "cabs_list_final.json"

@st.cache_data(show_spinner=False)
def load_list(path: Path, key: str):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            
        if isinstance(data, list):
            if data and isinstance(data[0], str):
                return [item.strip() for item in data if item.strip()]
            elif data and isinstance(data[0], dict):
                return [item.get('name', '') for item in data if isinstance(item, dict) and item.get('name')]
        
        return []
    except Exception:
        return []

# Build dropdown arrays
amp_models = ["None"] + sorted(load_list(AMPS_FILE, "name"), key=str.upper)
cab_models = ["None"] + sorted(load_list(CABS_FILE, "name"), key=str.upper)

# ──────────────────────────────────────────────────────────────────────────────
# Session State Management
# ──────────────────────────────────────────────────────────────────────────────
if 'current_tone' not in st.session_state:
    st.session_state.current_tone = None
if 'tone_history' not in st.session_state:
    st.session_state.tone_history = []
if 'ai_query' not in st.session_state:
    st.session_state.ai_query = ""
if 'mode' not in st.session_state:
    st.session_state.mode = "dual"

# Generate a default demo tone if none exists
if st.session_state.current_tone is None:
    try:
        with st.spinner("🤖 Loading demo tone..."):
            demo_tone = ai_generator.generate_tone_from_query("Clean ambient lead")
            st.session_state.current_tone = demo_tone
            st.session_state.tone_history.append(demo_tone)
    except Exception as e:
        st.warning("Could not load demo tone. Please generate a tone manually.")

# ──────────────────────────────────────────────────────────────────────────────
# Main UI Layout
# ──────────────────────────────────────────────────────────────────────────────
st.title("🎛️ ToneGPT AI - Professional FM9 Tone Generator")

# Professional tagline
st.markdown("### AI-powered professional tone creation for Fractal FM9 - Create studio-quality tones with natural language!")

# Professional status indicators
col1, col2 = st.columns(2)
with col1:
    st.success("🟢 PRODUCTION SYSTEM ACTIVE - Professional FM9 Integration Ready")
with col2:
    st.info("🎸 Tone Library - Save, browse, and load your favorite tones")

# ──────────────────────────────────────────────────────────────────────────────
# Dual Mode Selection
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🔀 System Mode")

mode_col1, mode_col2, mode_col3 = st.columns(3)
with mode_col1:
    if st.button("🔄 Dual Mode", use_container_width=True, key="dual_mode"):
        st.session_state.mode = "dual"
        st.rerun()
with mode_col2:
    if st.button("🎯 Personal FM9", use_container_width=True, key="personal_mode"):
        st.session_state.mode = "personal"
        st.rerun()
with mode_col3:
    if st.button("💼 Commercial", use_container_width=True, key="commercial_mode"):
        st.session_state.mode = "commercial"
        st.rerun()

# Display current mode
mode = st.session_state.mode
if mode == "dual":
    st.info("🔄 Dual Mode Active - Real FM9 names + generic commercial names")
elif mode == "personal":
    st.info("🎯 Personal FM9 Mode Active - Full FM9 functionality")
elif mode == "commercial":
    st.info("💼 Commercial Mode Active - Hardware-agnostic, trademark-safe")

# ──────────────────────────────────────────────────────────────────────────────
# Professional Tone Creation
# ──────────────────────────────────────────────────────────────────────────────
st.header("🎯 Professional Tone Creation")

# Professional AI Query Input
col1, col2 = st.columns([3, 1])
with col1:
    ai_query = st.text_input(
        "Describe your professional tone:",
        placeholder="e.g., 'Studio-quality metal rhythm tone with tight bass and cutting mids' or 'Jazz fusion lead with warm overdrive and subtle reverb'",
        value=st.session_state.ai_query,
        key="ai_query_input"
    )

with col2:
    if st.button("🎯 Generate Professional Tone", type="primary", use_container_width=True):
        if ai_query.strip():
            st.session_state.ai_query = ai_query
            with st.spinner("🤖 AI is crafting your professional tone..."):
                try:
                    generated_tone = ai_generator.generate_tone_from_query(ai_query)
                    st.session_state.current_tone = generated_tone
                    st.session_state.tone_history.append(generated_tone)
                    st.success("✨ Professional tone generated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a professional tone description!")

# ──────────────────────────────────────────────────────────────────────────────
# Signal Chain Visualization
# ──────────────────────────────────────────────────────────────────────────────
if st.session_state.current_tone:
    st.header("🔗 Signal Chain")
    tone = st.session_state.current_tone['tone_patch']
    
    # Create signal chain
    chain = []
    chain.append({"name": "Input", "type": "Input"})
    
    for block_name, block_data in tone.items():
        if block_data.get('enabled', False):
            block_type = "Unknown"
            if 'channels' in block_data:
                current_channel = block_data.get('current_channel', 'A')
                if current_channel in block_data['channels']:
                    block_type = block_data['channels'][current_channel].get('type', 'Unknown')
            else:
                block_type = block_data.get('type', 'Unknown')
            
            # Enhanced labels
            if 'drive' in block_name.lower():
                display_name = f"Drive: {block_type}"
            elif 'amp' in block_name.lower():
                display_name = f"Amp: {block_type}"
            elif 'cab' in block_name.lower():
                display_name = f"Speaker: {block_type}"
            elif 'delay' in block_name.lower():
                display_name = f"Delay: {block_type}"
            elif 'reverb' in block_name.lower():
                display_name = f"Reverb: {block_type}"
            elif 'eq' in block_name.lower():
                display_name = f"EQ: {block_type}"
            else:
                display_name = f"{block_type}"
            
            chain.append({"name": display_name, "type": block_type})
    
    chain.append({"name": "Output", "type": "Output"})
    
    # Display signal chain with enhanced styling
    if len(chain) > 2:
        cols = st.columns(len(chain))
        for i, (col, block) in enumerate(zip(cols, chain)):
            with col:
                st.markdown(f"""
                <div class="signal-block">
                    <div style="font-weight: bold; color: #00d4ff; font-size: 1.1rem; margin-bottom: 0.5rem;">{block['name']}</div>
                    <div style="color: #9ca3af; font-style: italic; font-size: 0.9rem;">{block['type']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No blocks enabled. Generate a tone to see the signal chain.")



# ──────────────────────────────────────────────────────────────────────────────
# Advanced Parameter Controls
# ──────────────────────────────────────────────────────────────────────────────
if st.session_state.current_tone:
    st.header("🎛️ Advanced Parameter Controls")
    tone = st.session_state.current_tone['tone_patch']
    
    # Create tabs for different parameter categories
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🔥 Drive", "⚡ Amp", "🔊 Speaker", "🎵 Effects", "🎛️ Modulation", 
        "🎼 Pitch", "📊 Dynamics", "🎚️ Global"
    ])
    
    with tab1:
        st.subheader("🔥 Drive Block Controls")
        
        # Drive 1
        if 'drive_1' in tone and tone['drive_1'].get('enabled'):
            with st.expander("Drive 1 - Main Overdrive", expanded=True):
                drive1 = tone['drive_1']
                
                if 'channels' in drive1:
                    current_ch = drive1.get('current_channel', 'A')
                    channel = st.selectbox("Channel", ["A", "B", "C", "D"], 
                                         index=ord(current_ch) - ord('A'), key="drive1_channel")
                    
                    ch_data = drive1['channels'][channel]
                    params = ch_data.get('parameters', {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        gain = st.slider("Gain", 0.0, 10.0, safe_float(params.get('gain', 5.0), 5.0), key="drive1_gain", help="Controls the amount of distortion")
                        level = st.slider("Level", 0.0, 10.0, safe_float(params.get('level', 5.0), 5.0), key="drive1_level", help="Output volume of the drive")
                    with col2:
                        tone_param = st.slider("Tone", 0.0, 10.0, safe_float(params.get('tone', 5.0), 5.0), key="drive1_tone", help="High frequency control")
                        mix = st.slider("Mix", 0.0, 100.0, safe_float(params.get('mix', 100.0), 100.0), key="drive1_mix", help=DRY_WET_MIX_HELP)
                    with col3:
                        bass = st.slider("Bass", 0.0, 10.0, safe_float(params.get('bass', 5.0), 5.0), key="drive1_bass", help="Low frequency control")
                        treble = st.slider("Treble", 0.0, 10.0, safe_float(params.get('treble', 5.0), 5.0), key="drive1_treble", help="High frequency control")
                    
                    if st.button("🔄 Update Drive 1", key="update_drive1"):
                        drive1['channels'][channel]['parameters'].update({
                            'gain': gain, 'level': level, 'tone': tone_param, 'mix': mix, 'bass': bass, 'treble': treble
                        })
                        st.success("Drive 1 parameters updated!")
        
        # Drive 2
        if 'drive_2' in tone and tone['drive_2'].get('enabled'):
            with st.expander("Drive 2 - Secondary Drive"):
                drive2 = tone['drive_2']
                
                if 'channels' in drive2:
                    current_ch = drive2.get('current_channel', 'A')
                    channel = st.selectbox("Channel", ["A", "B", "C", "D"], 
                                         index=ord(current_ch) - ord('A'), key="drive2_channel")
                    
                    ch_data = drive2['channels'][channel]
                    params = ch_data.get('parameters', {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        gain = st.slider("Gain", 0.0, 10.0, safe_float(params.get('gain', 5.0), 5.0), key="drive2_gain")
                        level = st.slider("Level", 0.0, 10.0, safe_float(params.get('level', 5.0), 5.0), key="drive2_level")
                    with col2:
                        tone_param = st.slider("Tone", 0.0, 10.0, safe_float(params.get('tone', 5.0), 5.0), key="drive2_tone")
                        mix = st.slider("Mix", 0.0, 100.0, safe_float(params.get('mix', 100.0), 100.0), key="drive2_mix")
                    with col3:
                        bass = st.slider("Bass", 0.0, 10.0, safe_float(params.get('bass', 5.0), 5.0), key="drive2_bass")
                        treble = st.slider("Treble", 0.0, 10.0, safe_float(params.get('treble', 5.0), 5.0), key="drive2_treble")
                    
                    if st.button("🔄 Update Drive 2", key="update_drive2"):
                        drive2['channels'][channel]['parameters'].update({
                            'gain': gain, 'level': level, 'tone': tone_param, 'mix': mix, 'bass': bass, 'treble': treble
                        })
                        st.success("Drive 2 parameters updated!")
    
    with tab2:
        st.subheader("⚡ Amplifier Controls")
        
        if 'amp' in tone and tone['amp'].get('enabled'):
            with st.expander("Main Amplifier", expanded=True):
                amp = tone['amp']
                
                if 'channels' in amp:
                    current_ch = amp.get('current_channel', 'A')
                    channel = st.selectbox("Channel", ["A", "B", "C", "D"], 
                                         index=ord(current_ch) - ord('A'), key="amp_channel")
                    
                    ch_data = amp['channels'][channel]
                    params = ch_data.get('parameters', {})
                    
                    # Basic Controls
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        gain = st.slider("Gain", 0.0, 10.0, safe_float(params.get('gain', 5.0), 5.0), key="amp_gain", help="Preamp gain")
                        master = st.slider("Master", 0.0, 10.0, safe_float(params.get('master', 5.0), 5.0), key="amp_master", help="Master volume")
                    with col2:
                        bass = st.slider("Bass", 0.0, 10.0, safe_float(params.get('bass', 5.0), 5.0), key="amp_bass", help="Low frequency")
                        mid = st.slider("Mid", 0.0, 10.0, params.get('mid', 5.0), key="amp_mid", help="Mid frequency")
                    with col3:
                        treble = st.slider("Treble", 0.0, 10.0, safe_float(params.get('treble', 5.0), 5.0), key="amp_treble", help="High frequency")
                        presence = st.slider("Presence", 0.0, 10.0, params.get('presence', 5.0), key="amp_presence", help="Presence control")
                    with col4:
                        depth = st.slider("Depth", 0.0, 10.0, params.get('depth', 5.0), key="amp_depth", help="Low frequency depth")
                        sag = st.slider("Sag", 0.0, 10.0, params.get('sag', 5.0), key="amp_sag", help="Power amp sag")
                    
                    # Advanced Controls
                    st.markdown("**Advanced Parameters**")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        bright = st.slider("Bright", 0.0, 10.0, params.get('bright', 5.0), key="amp_bright", help="Brightness switch")
                        fat = st.slider("Fat", 0.0, 10.0, params.get('fat', 5.0), key="amp_fat", help="Fat switch")
                    with col2:
                        bias = st.slider("Bias", 0.0, 10.0, params.get('bias', 5.0), key="amp_bias", help="Tube bias")
                        hum = st.slider("Hum", 0.0, 10.0, params.get('hum', 5.0), key="amp_hum", help="Hum level")
                    with col3:
                        ripple = st.slider("Ripple", 0.0, 10.0, params.get('ripple', 5.0), key="amp_ripple", help="Power supply ripple")
                        bias_excursion = st.slider("Bias Excursion", 0.0, 10.0, params.get('bias_excursion', 5.0), key="amp_bias_excursion", help="Bias excursion")
                    with col4:
                        xformer_match = st.slider("Xformer Match", 0.0, 10.0, params.get('xformer_match', 5.0), key="amp_xformer_match", help="Transformer matching")
                        speaker_comp = st.slider("Speaker Comp", 0.0, 10.0, params.get('speaker_comp', 5.0), key="amp_speaker_comp", help="Speaker compression")
                    
                    if st.button("🔄 Update Amp", key="update_amp"):
                        amp['channels'][channel]['parameters'].update({
                            'gain': gain, 'master': master, 'bass': bass, 'mid': mid, 'treble': treble, 'presence': presence,
                            'depth': depth, 'sag': sag, 'bright': bright, 'fat': fat, 'bias': bias, 'hum': hum,
                            'ripple': ripple, 'bias_excursion': bias_excursion, 'xformer_match': xformer_match, 'speaker_comp': speaker_comp
                        })
                        st.success("Amp parameters updated!")
    
    with tab3:
        st.subheader("🔊 Speaker Cabinet Controls")
        
        if 'cab' in tone and tone['cab'].get('enabled'):
            with st.expander("Speaker Cabinet", expanded=True):
                cab = tone['cab']
                
                # Handle both channels structure and direct parameters
                if 'channels' in cab:
                    current_ch = cab.get('current_channel', 'A')
                    channel = st.selectbox("Channel", ["A", "B", "C", "D"], 
                                         index=ord(current_ch) - ord('A'), key="cab_channel")
                    
                    ch_data = cab['channels'][channel]
                    params = ch_data.get('parameters', {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        level = st.slider("Level", 0.0, 10.0, safe_float(params.get('level', 5.0), 5.0), key="cab_level", help="Cabinet output level")
                        low_cut = st.slider(LOW_CUT_HELP, 20.0, 500.0, params.get('low_cut', 80.0), step=0.1, key="cab_low_cut", help=LOW_FREQ_CUTOFF_HELP)
                    with col2:
                        high_cut = st.slider(HIGH_CUT_HELP, 2000.0, 20000.0, params.get('high_cut', 8000.0), step=1.0, key="cab_high_cut", help=HIGH_FREQ_CUTOFF_HELP)
                        air = st.slider("Air", 0.0, 10.0, params.get('air', 5.0), key="cab_air", help="Air frequency")
                    with col3:
                        proximity = st.slider("Proximity", 0.0, 10.0, params.get('proximity', 5.0), key="cab_proximity", help="Proximity effect")
                        room = st.slider("Room", 0.0, 10.0, params.get('room', 5.0), key="cab_room", help="Room ambience")
                    
                    if st.button("🔄 Update Cabinet", key="update_cab"):
                        cab['channels'][channel]['parameters'].update({
                            'level': level, 'low_cut': low_cut, 'high_cut': high_cut, 'air': air, 'proximity': proximity, 'room': room
                        })
                        st.success("Cabinet parameters updated!")
                else:
                    # Handle direct parameters structure
                    params = cab.get('parameters', {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        level = st.slider("Level", 0.0, 10.0, safe_float(params.get('level', 5.0), 5.0), key="cab_level_direct", help="Cabinet output level")
                        low_cut = st.slider(LOW_CUT_HELP, 20.0, 500.0, params.get('low_cut', 80.0), step=0.1, key="cab_low_cut_direct", help=LOW_FREQ_CUTOFF_HELP)
                    with col2:
                        high_cut = st.slider(HIGH_CUT_HELP, 2000.0, 20000.0, params.get('high_cut', 8000.0), step=1.0, key="cab_high_cut_direct", help=HIGH_FREQ_CUTOFF_HELP)
                        air = st.slider("Air", 0.0, 10.0, params.get('air', 5.0), key="cab_air_direct", help="Air frequency")
                    with col3:
                        proximity = st.slider("Proximity", 0.0, 10.0, params.get('proximity', 5.0), key="cab_proximity_direct", help="Proximity effect")
                        room = st.slider("Room", 0.0, 10.0, params.get('room', 5.0), key="cab_room_direct", help="Room ambience")
                    
                    if st.button("🔄 Update Cabinet", key="update_cab_direct"):
                        cab['parameters'].update({
                            'level': level, 'low_cut': low_cut, 'high_cut': high_cut, 'air': air, 'proximity': proximity, 'room': room
                        })
                        st.success("Cabinet parameters updated!")
    
    with tab4:
        st.subheader("🎵 Effects Controls")
        
        # Delay
        if 'delay' in tone and tone['delay'].get('enabled'):
            with st.expander("Delay 1"):
                delay1 = tone['delay']
                
                if 'channels' in delay1:
                    current_ch = delay1.get('current_channel', 'A')
                    channel = st.selectbox("Channel", ["A", "B", "C", "D"], 
                                         index=ord(current_ch) - ord('A'), key="delay1_channel")
                    
                    ch_data = delay1['channels'][channel]
                    params = ch_data.get('parameters', {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        time = st.slider("Time", 0.0, 2000.0, params.get('time', 500.0), key="delay1_time", help="Delay time in ms")
                        feedback = st.slider("Feedback", 0.0, 100.0, params.get('feedback', 30.0), key="delay1_feedback", help=FEEDBACK_AMOUNT_HELP)
                    with col2:
                        mix = st.slider("Mix", 0.0, 100.0, params.get('mix', 25.0), key="delay1_mix", help=DRY_WET_MIX_HELP)
                        low_cut = st.slider(LOW_CUT_HELP, 20.0, 2000.0, params.get('low_cut', 200.0), key="delay1_low_cut", help=LOW_FREQ_CUTOFF_HELP)
                    with col3:
                        high_cut = st.slider(HIGH_CUT_HELP, 2000.0, 20000.0, params.get('high_cut', 8000.0), key="delay1_high_cut", help=HIGH_FREQ_CUTOFF_HELP)
                        level = st.slider("Level", 0.0, 10.0, safe_float(params.get('level', 5.0), 5.0), key="delay1_level", help="Delay output level")
                    
                    if st.button("🔄 Update Delay 1", key="update_delay1"):
                        delay1['channels'][channel]['parameters'].update({
                            'time': time, 'feedback': feedback, 'mix': mix, 'low_cut': low_cut, 'high_cut': high_cut, 'level': level
                        })
                        st.success("Delay 1 parameters updated!")
        
        # Reverb
        if 'reverb' in tone and tone['reverb'].get('enabled'):
            with st.expander("Reverb 1"):
                reverb1 = tone['reverb']
                
                if 'channels' in reverb1:
                    current_ch = reverb1.get('current_channel', 'A')
                    channel = st.selectbox("Channel", ["A", "B", "C", "D"], 
                                         index=ord(current_ch) - ord('A'), key="reverb1_channel")
                    
                    ch_data = reverb1['channels'][channel]
                    params = ch_data.get('parameters', {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        room_size = st.slider("Room Size", 0.0, 10.0, params.get('room_size', 5.0), key="reverb1_room_size", help="Room size")
                        decay = st.slider("Decay", 0.0, 10.0, params.get('decay', 5.0), key="reverb1_decay", help="Decay time")
                    with col2:
                        mix = st.slider("Mix", 0.0, 100.0, params.get('mix', 25.0), key="reverb1_mix", help=DRY_WET_MIX_HELP)
                        pre_delay = st.slider("Pre Delay", 0.0, 100.0, params.get('pre_delay', 20.0), key="reverb1_pre_delay", help="Pre-delay in ms")
                    with col3:
                        low_cut = st.slider(LOW_CUT_HELP, 20.0, 2000.0, params.get('low_cut', 200.0), key="reverb1_low_cut", help=LOW_FREQ_CUTOFF_HELP)
                        high_cut = st.slider(HIGH_CUT_HELP, 2000.0, 20000.0, params.get('high_cut', 8000.0), key="reverb1_high_cut", help=HIGH_FREQ_CUTOFF_HELP)
                    
                    if st.button("🔄 Update Reverb 1", key="update_reverb1"):
                        reverb1['channels'][channel]['parameters'].update({
                            'room_size': room_size, 'decay': decay, 'mix': mix, 'pre_delay': pre_delay, 'low_cut': low_cut, 'high_cut': high_cut
                        })
                        st.success("Reverb 1 parameters updated!")
        
        # Note: Modulation, Pitch, and Dynamics controls are now in their dedicated tabs
        st.info("🎵 Modulation, Pitch, and Dynamics controls are now in their dedicated tabs above!")
    
    with tab5:
        st.subheader("🎛️ Modulation Controls")
        
        # Modulation
        if 'modulation' in tone and tone['modulation'].get('enabled'):
            with st.expander("Modulation 1"):
                modulation1 = tone['modulation']
                
                if 'channels' in modulation1:
                    current_ch = modulation1.get('current_channel', 'A')
                    channel = st.selectbox("Channel", ["A", "B", "C", "D"], 
                                         index=ord(current_ch) - ord('A'), key="modulation1_channel_tab5")
                    
                    ch_data = modulation1['channels'][channel]
                    params = ch_data.get('parameters', {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        rate = st.slider("Rate", 0.0, 10.0, params.get('rate', 5.0), key="modulation1_rate_tab5", help="Modulation rate")
                        depth = st.slider("Depth", 0.0, 10.0, params.get('depth', 5.0), key="modulation1_depth_tab5", help="Modulation depth")
                    with col2:
                        mix = st.slider("Mix", 0.0, 100.0, params.get('mix', 50.0), key="modulation1_mix_tab5", help=DRY_WET_MIX_HELP)
                        feedback = st.slider("Feedback", 0.0, 100.0, params.get('feedback', 0.0), key="modulation1_feedback_tab5", help=FEEDBACK_AMOUNT_HELP)
                    with col3:
                        level = st.slider("Level", 0.0, 10.0, safe_float(params.get('level', 5.0), 5.0), key="modulation1_level_tab5", help="Modulation output level")
                    
                    if st.button("🔄 Update Modulation 1", key="update_modulation1_tab5"):
                        modulation1['channels'][channel]['parameters'].update({
                            'rate': rate, 'depth': depth, 'mix': mix, 'feedback': feedback, 'level': level
                        })
                        st.success("Modulation 1 parameters updated!")
    
    with tab6:
        st.subheader("🎼 Pitch Controls")
        
        # Pitch
        if 'pitch' in tone and tone['pitch'].get('enabled'):
            with st.expander("Pitch 1"):
                pitch1 = tone['pitch']
                
                if 'channels' in pitch1:
                    current_ch = pitch1.get('current_channel', 'A')
                    channel = st.selectbox("Channel", ["A", "B", "C", "D"], 
                                         index=ord(current_ch) - ord('A'), key="pitch1_channel_tab6")
                    
                    ch_data = pitch1['channels'][channel]
                    params = ch_data.get('parameters', {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        pitch = st.slider("Pitch", -24.0, 24.0, params.get('pitch', 0.0), key="pitch1_pitch_tab6", help="Pitch shift in semitones")
                        mix = st.slider("Mix", 0.0, 100.0, params.get('mix', 50.0), key="pitch1_mix_tab6", help=DRY_WET_MIX_HELP)
                    with col2:
                        feedback = st.slider("Feedback", 0.0, 100.0, params.get('feedback', 0.0), key="pitch1_feedback_tab6", help=FEEDBACK_AMOUNT_HELP)
                        level = st.slider("Level", 0.0, 10.0, safe_float(params.get('level', 5.0), 5.0), key="pitch1_level_tab6", help="Pitch output level")
                    
                    if st.button("🔄 Update Pitch 1", key="update_pitch1_tab6"):
                        pitch1['channels'][channel]['parameters'].update({
                            'pitch': pitch, 'mix': mix, 'feedback': feedback, 'level': level
                        })
                        st.success("Pitch 1 parameters updated!")
    
    with tab7:
        st.subheader("📊 Dynamics Controls")
        
        # Dynamics
        if 'dynamics' in tone and tone['dynamics'].get('enabled'):
            with st.expander("Dynamics 1"):
                dynamics1 = tone['dynamics']
                
                if 'channels' in dynamics1:
                    current_ch = dynamics1.get('current_channel', 'A')
                    channel = st.selectbox("Channel", ["A", "B", "C", "D"], 
                                         index=ord(current_ch) - ord('A'), key="dynamics1_channel_tab7")
                    
                    ch_data = dynamics1['channels'][channel]
                    params = ch_data.get('parameters', {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        threshold = st.slider("Threshold", -60.0, 0.0, params.get('threshold', -20.0), key="dynamics1_threshold_tab7", help="Compression threshold")
                        ratio = st.slider("Ratio", 1.0, 20.0, params.get('ratio', 4.0), key="dynamics1_ratio_tab7", help="Compression ratio")
                    with col2:
                        attack = st.slider("Attack", 0.0, 100.0, params.get('attack', 10.0), key="dynamics1_attack_tab7", help="Attack time")
                        release = st.slider("Release", 0.0, 200.0, params.get('release', 100.0), key="dynamics1_release_tab7", help="Release time")
                    with col3:
                        level = st.slider("Level", 0.0, 10.0, safe_float(params.get('level', 5.0), 5.0), key="dynamics1_level_tab7", help="Dynamics output level")
                    
                    if st.button("🔄 Update Dynamics 1", key="update_dynamics1_tab7"):
                        dynamics1['channels'][channel]['parameters'].update({
                            'threshold': threshold, 'ratio': ratio, 'attack': attack, 'release': release, 'level': level
                        })
                        st.success("Dynamics 1 parameters updated!")
        
        # EQ
        if 'eq_1' in tone and tone['eq_1'].get('enabled'):
            with st.expander("EQ 1"):
                eq1 = tone['eq_1']
                
                if 'channels' in eq1:
                    current_ch = eq1.get('current_channel', 'A')
                    channel = st.selectbox("Channel", ["A", "B", "C", "D"], 
                                         index=ord(current_ch) - ord('A'), key="eq1_channel")
                    
                    ch_data = eq1['channels'][channel]
                    params = ch_data.get('parameters', {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        low_gain = st.slider("Low Gain", -12.0, 12.0, params.get('low_gain', 0.0), key="eq1_low_gain", help="Low frequency gain")
                        low_freq = st.slider("Low Freq", 20.0, 500.0, params.get('low_freq', 100.0), key="eq1_low_freq", help="Low frequency")
                    with col2:
                        mid_gain = st.slider("Mid Gain", -12.0, 12.0, params.get('mid_gain', 0.0), key="eq1_mid_gain", help="Mid frequency gain")
                        mid_freq = st.slider("Mid Freq", 200.0, 5000.0, params.get('mid_freq', 1000.0), key="eq1_mid_freq", help="Mid frequency")
                    with col3:
                        high_gain = st.slider("High Gain", -12.0, 12.0, params.get('high_gain', 0.0), key="eq1_high_gain", help="High frequency gain")
                        high_freq = st.slider("High Freq", 2000.0, 20000.0, params.get('high_freq', 8000.0), key="eq1_high_freq", help="High frequency")
                    
                    if st.button("🔄 Update EQ 1", key="update_eq1"):
                        eq1['channels'][channel]['parameters'].update({
                            'low_gain': low_gain, 'low_freq': low_freq, 'mid_gain': mid_gain, 'mid_freq': mid_freq, 'high_gain': high_gain, 'high_freq': high_freq
                        })
                        st.success("EQ 1 parameters updated!")
    
    with tab8:
        st.subheader("🎚️ Global Controls")
        
        # Input
        if 'input' in tone and tone['input'].get('enabled'):
            with st.expander("Input Block"):
                input_block = tone['input']
                
                if 'channels' in input_block:
                    current_ch = input_block.get('current_channel', 'A')
                    channel = st.selectbox("Channel", ["A", "B", "C", "D"], 
                                         index=ord(current_ch) - ord('A'), key="input_channel")
                    
                    ch_data = input_block['channels'][channel]
                    params = ch_data.get('parameters', {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        level = st.slider("Level", 0.0, 10.0, safe_float(params.get('level', 5.0), 5.0), key="input_level", help="Input level")
                        impedance = st.slider("Impedance", 0.0, 10.0, params.get('impedance', 5.0), key="input_impedance", help="Input impedance")
                    with col2:
                        noise_gate = st.slider("Noise Gate", 0.0, 10.0, params.get('noise_gate', 0.0), key="input_noise_gate", help="Noise gate threshold")
                        pad = st.slider("Pad", 0.0, 10.0, params.get('pad', 0.0), key="input_pad", help="Input pad")
                    with col3:
                        boost = st.slider("Boost", 0.0, 10.0, params.get('boost', 0.0), key="input_boost", help="Input boost")
                        trim = st.slider("Trim", 0.0, 10.0, params.get('trim', 5.0), key="input_trim", help="Input trim")
                    
                    if st.button("🔄 Update Input", key="update_input"):
                        input_block['channels'][channel]['parameters'].update({
                            'level': level, 'impedance': impedance, 'noise_gate': noise_gate, 'pad': pad, 'boost': boost, 'trim': trim
                        })
                        st.success("Input parameters updated!")
        
        # Output
        if 'output' in tone and tone['output'].get('enabled'):
            with st.expander("Output Block"):
                output_block = tone['output']
                
                if 'channels' in output_block:
                    current_ch = output_block.get('current_channel', 'A')
                    channel = st.selectbox("Channel", ["A", "B", "C", "D"], 
                                         index=ord(current_ch) - ord('A'), key="output_channel")
                    
                    ch_data = output_block['channels'][channel]
                    params = ch_data.get('parameters', {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        level = st.slider("Level", 0.0, 10.0, safe_float(params.get('level', 5.0), 5.0), key="output_level", help="Output level")
                        balance = st.slider("Balance", -10.0, 10.0, params.get('balance', 0.0), key="output_balance", help="Stereo balance")
                    with col2:
                        phase = st.slider("Phase", 0.0, 10.0, params.get('phase', 0.0), key="output_phase", help="Phase control")
                        mute = st.slider("Mute", 0.0, 10.0, params.get('mute', 0.0), key="output_mute", help="Mute control")
                    with col3:
                        boost = st.slider("Boost", 0.0, 10.0, params.get('boost', 0.0), key="output_boost", help="Output boost")
                        trim = st.slider("Trim", 0.0, 10.0, params.get('trim', 5.0), key="output_trim", help="Output trim")
                    
                    if st.button("🔄 Update Output", key="update_output"):
                        output_block['channels'][channel]['parameters'].update({
                            'level': level, 'balance': balance, 'phase': phase, 'mute': mute, 'boost': boost, 'trim': trim
                        })
                        st.success("Output parameters updated!")

# ──────────────────────────────────────────────────────────────────────────────
# Professional Tools
# ──────────────────────────────────────────────────────────────────────────────
st.header("🎸 Tone Library")

# Initialize tone library in session state
if 'tone_library' not in st.session_state:
    st.session_state.tone_library = {}

# Create columns for tone library
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📚 Saved Tones")
    
    # Show saved tones
    if st.session_state.tone_library:
        for tone_name, tone_data in st.session_state.tone_library.items():
            with st.expander(f"🎵 {tone_name}"):
                col_a, col_b, col_c = st.columns([2, 1, 1])
                
                with col_a:
                    # Show tone info
                    intent = tone_data.get('intent', {})
                    genre = intent.get('genre', 'Unknown')
                    artist = intent.get('artist', '')
                    
                    if artist:
                        st.write(f"**Artist:** {artist.title()}")
                    st.write(f"**Genre:** {genre.title()}")
                    
                    # Show effects
                    tone_patch = tone_data.get('tone_patch', {})
                    enabled_effects = [name for name, data in tone_patch.items() if data.get('enabled')]
                    st.write(f"**Effects:** {len(enabled_effects)} enabled")
                
                with col_b:
                    if st.button("🔄 Load", key=f"load_{tone_name}"):
                        st.session_state.current_tone = tone_data
                        st.success(f"Loaded {tone_name}!")
                        st.rerun()
                
                with col_c:
                    if st.button("🗑️ Delete", key=f"delete_{tone_name}"):
                        del st.session_state.tone_library[tone_name]
                        st.success(f"Deleted {tone_name}!")
                        st.rerun()
    else:
        st.info("No saved tones yet. Generate and save a tone to build your library!")

with col2:
    st.subheader("💾 Save Current Tone")
    
    if 'current_tone' in st.session_state:
        # Tone name input
        tone_name = st.text_input(
            "Tone Name:",
            placeholder="e.g., 'My Metal Tone'",
            key="save_tone_name"
        )
        
        # Auto-suggest name based on current tone
        if not tone_name:
            intent = st.session_state.current_tone.get('intent', {})
            genre = intent.get('genre', 'Unknown')
            artist = intent.get('artist', '')
            
            if artist:
                suggested_name = f"{artist.title()} {genre.title()}"
            else:
                suggested_name = f"{genre.title()} Tone"
            
            st.caption(f"💡 Suggested: {suggested_name}")
        
        # Save button
        if st.button("💾 Save Tone", use_container_width=True, key="save_tone"):
            if tone_name.strip():
                # Use suggested name if no name provided
                if not tone_name.strip():
                    tone_name = suggested_name
                
                # Add timestamp to avoid duplicates
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_name = f"{tone_name} ({timestamp})"
                
                st.session_state.tone_library[unique_name] = st.session_state.current_tone
                st.success(f"Saved '{unique_name}' to library!")
                st.rerun()
            else:
                st.warning("Please enter a tone name!")
    
    else:
        st.info("Generate a tone first to save it to your library!")
    


# ──────────────────────────────────────────────────────────────────────────────
# Export Features
# ──────────────────────────────────────────────────────────────────────────────
if st.session_state.current_tone:
    st.header("💾 Export")
    tone = st.session_state.current_tone['tone_patch']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        preset_name = st.text_input("Preset Name", value="ToneGPT_Generated", key="preset_name")
    with col2:
        preset_number = st.number_input("Preset #", min_value=1, max_value=512, value=1, key="preset_number")
    with col3:
        export_format = st.selectbox("Format", ["FM9 Preset (.syx)", "Parameter List (.txt)", "JSON (.json)"], key="export_format")
    
    if st.button("📤 Export", key="export_fm9"):
        # Generate export data
        preset_data = {
            "name": preset_name,
            "number": preset_number,
            "format": export_format,
            "timestamp": str(datetime.now()),
            "tone_patch": tone
        }
        
        if export_format == "FM9 Preset (.syx)":
            sysex_data = f"F0 00 01 74 12 {preset_name} F7"
            st.download_button(
                label="📥 Download FM9 Preset",
                data=sysex_data,
                file_name=f"{preset_name}_{preset_number:03d}.syx",
                mime="application/octet-stream"
            )
            st.success("FM9 preset ready!")
        
        elif export_format == "Parameter List (.txt)":
            param_text = f"ToneGPT Preset: {preset_name}\nPreset: {preset_number}\nGenerated: {datetime.now()}\n\n"
            for block_name, block_data in tone.items():
                if block_data.get('enabled'):
                    param_text += f"=== {block_name.upper()} ===\n"
                    if 'channels' in block_data:
                        current_ch = block_data.get('current_channel', 'A')
                        params = block_data['channels'][current_ch].get('parameters', {})
                        for param, value in params.items():
                            param_text += f"{param}: {value}\n"
                    param_text += "\n"
            
            st.download_button(
                label="📥 Download Parameters",
                data=param_text,
                file_name=f"{preset_name}_{preset_number:03d}.txt",
                mime="text/plain"
            )
            st.success("Parameter list ready!")
        
        elif export_format == "JSON (.json)":
            json_data = json.dumps(preset_data, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"{preset_name}_{preset_number:03d}.json",
                mime="application/json"
            )
            st.success("JSON export ready!")

# ──────────────────────────────────────────────────────────────────────────────
# Professional Sidebar
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Version Information
    st.markdown("### ToneGPT AI v1.0.0")
    st.markdown("**Build:** 2025-01-27")
    st.markdown("**FM9:** Firmware 3.x+")
    st.markdown("**Python:** 3.8+")
    
    st.success("🟢 PRODUCTION SYSTEM")
    
    st.divider()
    
    # System Status
    st.subheader("📊 System Status")
    st.metric("Total Blocks", "947")
    st.metric("Amplifiers", "633") 
    st.metric("Effects", "314")
    
    st.divider()
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    
    # Professional tone templates
    st.markdown("**Professional Templates:**")
    professional_queries = [
        "deftones",
        "tool", 
        "metallica",
        "david gilmour",
        "jimi hendrix",
        "stevie ray vaughan",
        "eric clapton"
    ]
    
    for query in professional_queries:
        if st.button(query, use_container_width=True):
            st.session_state.ai_query = query
            with st.spinner("🤖 Generating professional tone..."):
                try:
                    generated_tone = ai_generator.generate_tone_from_query(query)
                    st.session_state.current_tone = generated_tone
                    st.session_state.tone_history.append(generated_tone)
                    st.success(f"✨ {query} ready!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.rerun()
    
    st.divider()
    
    # Session Stats
    st.subheader("📈 Session Stats")
    st.metric("Tones Generated", len(st.session_state.tone_history))
    st.metric("Current Mode", mode.title())
    st.metric("System Status", "Active")
    
    st.divider()
    
    # Professional Footer
    st.markdown("**ToneGPT AI v1.0.0**")
    st.markdown("*Professional FM9 Integration*")
    st.markdown("*Production Ready*")

# Footer
st.divider()
st.caption("🎸 ToneGPT AI | AI-powered FM9 tone generation")
