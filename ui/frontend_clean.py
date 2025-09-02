import streamlit as st
import json
from pathlib import Path
import sys
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Add the parent directory to the path so we can import tonegpt modules
sys.path.append(str(Path(__file__).parent.parent))

from tonegpt.core.enhanced_ai_tone_generator import EnhancedAIToneGenerator
from tonegpt import __version__, VERSION_INFO, is_production, get_fm9_compatibility

def safe_float(value, default=0.0):
    """Safely convert value to float for sliders"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

# Page Configuration
st.set_page_config(
    page_title="ToneGPT AI - Clean Version",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize AI Tone Generator
@st.cache_resource
def get_ai_generator():
    """Initialize the AI tone generator"""
    return EnhancedAIToneGenerator()

ai_generator = get_ai_generator()

# Session State Management
if 'current_tone' not in st.session_state:
    st.session_state.current_tone = None
if 'tone_history' not in st.session_state:
    st.session_state.tone_history = []
if 'ai_query' not in st.session_state:
    st.session_state.ai_query = ""

# Main UI Layout
st.title("🎸 ToneGPT AI - Clean Interface")
st.markdown("**AI-powered FM9 tone generation with clean, streamlined interface**")

# System Status
st.success("🟢 **SYSTEM STATUS: RUNNING** - All systems operational")

# AI Tone Generation Section
st.header("🤖 AI Tone Generation")

# AI Query Input
col1, col2 = st.columns([3, 1])
with col1:
    ai_query = st.text_input(
        "Describe the tone you want:",
        placeholder="e.g., 'Give me a Metallica-style metal tone' or 'Clean ambient lead with delay'",
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

# Signal Chain Visualization
st.subheader("🔗 Signal Chain")
if st.session_state.current_tone:
    tone = st.session_state.current_tone['tone_patch']
    
    # Create signal chain
    chain = []
    chain.append({"name": "Input", "icon": "🎸", "type": "input"})
    
    # Add enabled blocks
    for block_name, block_data in tone.items():
        if block_data.get('enabled', False):
            block_type = block_data.get('type', 'Unknown')
            icon = "🎛️"
            
            # Determine block type and icon
            if 'drive' in block_name.lower():
                icon = "🔥"
            elif 'amp' in block_name.lower():
                icon = "⚡"
            elif 'cab' in block_name.lower():
                icon = "📻"
            elif any(effect in block_name.lower() for effect in ['delay', 'reverb', 'eq', 'chorus', 'flanger']):
                icon = "✨"
            
            chain.append({
                "name": block_type,
                "icon": icon,
                "type": block_name,
                "details": block_data
            })
    
    # Add output
    chain.append({"name": "Output", "icon": "🎧", "type": "output"})
    
    # Display signal chain
    for i, block in enumerate(chain):
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            st.markdown(f"### {block['icon']} {block['name']}")
            
            # Block parameters if available
            if 'details' in block and block['details']:
                params = block['details'].get('parameters', {})
                if params:
                    param_text = []
                    for param, value in list(params.items())[:3]:  # Show first 3 params
                        if isinstance(value, (int, float)):
                            param_text.append(f"**{param}:** {value:.1f}")
                        else:
                            param_text.append(f"**{param}:** {value}")
                    
                    if param_text:
                        st.markdown(f"*{' | '.join(param_text)}*")
            
            st.markdown("---")
        
        # Add connection indicator (except for last block)
        if i < len(chain) - 1:
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                st.markdown("⬇️")

# Tone Analysis
if st.session_state.current_tone:
    st.subheader("📊 Tone Analysis")
    
    # Analyze tone complexity
    analysis = ai_generator.analyze_tone_complexity(st.session_state.current_tone['tone_patch'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Blocks", analysis["active_blocks"])
    with col2:
        st.metric("Parameters", analysis["parameter_count"])
    with col3:
        st.metric("Complexity Score", f"{analysis['complexity_score']}/100")
    with col4:
        st.metric("Complexity Level", analysis["technical_analysis"]["complexity_level"].title())
    
    if analysis["genre_indicators"]:
        st.markdown(f"**Genre Indicators:** {', '.join(analysis['genre_indicators']).title()}")

# Quick Demo Section
st.divider()
st.header("🚀 Quick Demo")

demo_col1, demo_col2, demo_col3 = st.columns(3)

with demo_col1:
    if st.button("🎸 **Metal Tone**", use_container_width=True):
        st.session_state.ai_query = "Give me a Metallica-style metal tone with high gain and tight bass"
        st.rerun()

with demo_col2:
    if st.button("🎵 **Clean Jazz**", use_container_width=True):
        st.session_state.ai_query = "Create a clean jazz tone with warm mids and subtle reverb"
        st.rerun()

with demo_col3:
    if st.button("🎹 **Ambient Pad**", use_container_width=True):
        st.session_state.ai_query = "Generate an ambient pad tone with delay and reverb"
        st.rerun()

# Sidebar
with st.sidebar:
    st.header("🎛️ System Info")
    st.markdown(f"**Version:** {__version__}")
    st.markdown(f"**Build:** {VERSION_INFO['build_date']}")
    st.markdown(f"**FM9:** {get_fm9_compatibility()}")
    
    if is_production():
        st.success("**🟢 PRODUCTION**")
    else:
        st.warning("**🟡 DEVELOPMENT**")
    
    st.divider()
    
    st.header("📊 Cache Stats")
    cache_stats = ai_generator.get_cache_stats()
    st.metric("Cache Size", f"{cache_stats['cache_size']}/{cache_stats['cache_max_size']}")
    st.metric("Utilization", f"{cache_stats['cache_utilization']:.1f}%")
    
    if st.button("Clear Cache"):
        ai_generator.clear_cache()
        st.success("Cache cleared!")
        st.rerun()
    
    st.divider()
    
    st.header("📚 Tone History")
    if st.session_state.tone_history:
        for i, tone in enumerate(reversed(st.session_state.tone_history[-5:])):
            if st.button(f"Load: {tone['description'][:30]}...", key=f"load_{i}"):
                st.session_state.current_tone = tone
                st.rerun()
    else:
        st.info("No tones generated yet")

# Footer
st.divider()
st.caption("🎸 ToneGPT AI | Clean Interface | Built with ❤️ for guitarists")
