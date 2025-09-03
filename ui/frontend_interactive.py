#!/usr/bin/env python3
"""
Interactive Tone Editor Frontend

Professional interactive frontend for ToneGPT with:
- Compact chain canvas (Input → [Blocks] → Output) with drag-reorder + bypass toggles
- Knob widgets for featured params only (blocks_featured spec)
- "Randomize within range" button per block (seeded from query for repeatability)
- Snapshot panel showing diff vs. golden (param deltas)

Usage:
    streamlit run ui/frontend_interactive.py
"""

import streamlit as st
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import random
import hashlib

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tonegpt.core.clean_ai_tone_generator import CleanAIToneGenerator
from tonegpt.core.canonicalize import canonicalize_preset, canonical_block, canonical_param
from tonegpt.core.validate_and_clamp import enforce_ref_ranges, clamp_range
from tonegpt.core.flags import FEATURE_MULTI_DEVICE


def _seed_from_query(query: str) -> None:
    """Generate deterministic seed from query string for consistent output."""
    h = int(hashlib.sha1(query.encode("utf-8")).hexdigest(), 16) % (2**31)
    random.seed(h)


def load_blocks_featured() -> Dict[str, Any]:
    """Load the blocks_featured.json data."""
    blocks_file = Path("data/blocks_featured.json")
    if blocks_file.exists():
        return json.loads(blocks_file.read_text())
    return {}


def load_fm9_reference() -> Dict[str, Any]:
    """Load the FM9 comprehensive reference data."""
    ref_file = Path("data/fm9_comprehensive_reference.json")
    if ref_file.exists():
        return json.loads(ref_file.read_text())
    return {}


def render_knob_widget(block_type: str, param_name: str, current_value: float, 
                      param_spec: Dict[str, Any], key: str) -> float:
    """Render a compact knob-style widget for a parameter."""
    min_val = param_spec.get("min", 0.0)
    max_val = param_spec.get("max", 100.0)
    step = param_spec.get("step", 0.1)
    
    # Compact parameter display
    param_label = param_name.replace('_', ' ').title()
    
    # Create a compact slider
    return st.slider(
        param_label,
        min_value=float(min_val),
        max_value=float(max_val),
        value=float(current_value),
        step=float(step),
        key=key,
        help=f"{min_val} - {max_val}",
        label_visibility="visible"
    )


def render_block_editor(block_type: str, block_data: Dict[str, Any], 
                       blocks_featured: Dict[str, Any], fm9_ref: Dict[str, Any], 
                       block_identifier: str = "0") -> Dict[str, Any]:
    """Render the editor for a single block."""

    
    # Compact header with enable toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{block_type.upper()}**")
    with col2:
        enabled = st.checkbox("Enabled", value=block_data.get("enabled", True), 
                             key=f"{block_identifier}_enabled")
    

    
    if not enabled:

        return {**block_data, "enabled": False}
    
    # Compact model display with tooltip
    if "type" in block_data:
        current_model = block_data["type"]
        real_world = block_data.get("real_world", current_model)
        
        # Show FM9 name with real-world name as tooltip
        if real_world != current_model:
            st.caption(f"📱 {current_model}")
            st.caption(f"💡 {real_world}", help="Real-world gear name")
        else:
            st.caption(f"📱 {current_model}")
    
    # Featured parameters - handle the list structure
    featured_params = []
    blocks_list = blocks_featured.get("blocks", [])
    for block_info in blocks_list:
        if isinstance(block_info, dict) and block_info.get("block", "").upper() == block_type.upper():
            featured_params = block_info.get("featured_parameters", [])
            break
    
    if not featured_params:
        st.info(f"No featured parameters defined for {block_type}")
        return block_data
    
    # Get parameter specifications
    ref_key = f"{block_type.lower()}_block"
    param_specs = fm9_ref.get(ref_key, {}).get("key_parameters", {})
    
    # Compact parameter layout - 2 columns
    if featured_params:
        col1, col2 = st.columns(2)
        
        updated_params = {}
        for i, param_name in enumerate(featured_params):
            if param_name in param_specs:
                current_value = block_data.get("parameters", {}).get(param_name, 0.0)
                param_spec = param_specs[param_name]
                
                # Alternate between columns
                with col1 if i % 2 == 0 else col2:
                    # Render knob widget
                    new_value = render_knob_widget(
                        block_type, param_name, current_value, param_spec,
                        f"{block_identifier}_{param_name}"
                    )
                    
                    # Clamp the value to ensure it's within range
                    clamped_value = clamp_range(new_value, param_spec)
                    updated_params[param_name] = clamped_value
        
        # Compact randomize button
        if st.button(f"🎲 Randomize", key=f"randomize_{block_identifier}", use_container_width=True):
            # Generate random values within spec ranges
            for param_name in featured_params:
                if param_name in param_specs:
                    param_spec = param_specs[param_name]
                    min_val = param_spec.get("min", 0.0)
                    max_val = param_spec.get("max", 100.0)
                    random_value = random.uniform(min_val, max_val)
                    updated_params[param_name] = clamp_range(random_value, param_spec)
            st.rerun()
    
    result = {
        **block_data,
        "enabled": enabled,
        "parameters": {**block_data.get("parameters", {}), **updated_params}
    }
    return result


def render_chain_canvas(blocks: List[Dict[str, Any]], tone_patch: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """Render a compact signal chain canvas with actual model names."""
    st.markdown("### 🔗 Signal Chain")
    
    # Create a compact horizontal chain
    chain_elements = ["🎸 Input"]
    
    # Define the order of blocks in the signal chain
    block_order = [
        "drive_1", "drive_2", "amp", "cab", "eq", 
        "delay", "reverb", "modulation", "pitch", "dynamics", "utility"
    ]
    
    # Iterate through tone_patch in the correct order
    if tone_patch:
        for block_key in block_order:
            if block_key in tone_patch:
                block_data = tone_patch[block_key]
                model_name = block_data.get("type", "Unknown")
                enabled = block_data.get("enabled", True)
                
                if enabled:
                    chain_elements.append(f"🔧 {model_name}")
                else:
                    chain_elements.append(f"❌ {model_name}")
    
    chain_elements.append("🔊 Output")
    
    # Display as a compact chain
    chain_display = " → ".join(chain_elements)
    st.markdown(f"<div style='text-align: center; font-family: monospace; font-size: 14px; color: #666; padding: 10px; background: #f8f9fa; border-radius: 5px;'>{chain_display}</div>", unsafe_allow_html=True)
    
    # Return blocks as-is for now (reordering can be added later)
    reordered_blocks = blocks
    return reordered_blocks


def render_snapshot_panel(current_tone: Dict[str, Any], golden_tone: Optional[Dict[str, Any]] = None):
    """Render a compact snapshot panel."""
    st.markdown("### 📸 Snapshot")
    
    # Compact tone summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Query", current_tone.get("query", "Unknown")[:20] + "..." if len(current_tone.get("query", "")) > 20 else current_tone.get("query", "Unknown"))
    with col2:
        st.metric("Blocks", len(current_tone.get("blocks", [])))
    with col3:
        enabled_count = len([b for b in current_tone.get("blocks", []) if b.get("enabled", True)])
        st.metric("Active", enabled_count)
    
    # Diff view if golden tone provided
    if golden_tone:
        st.markdown("**Diff vs. Golden:**")
        
        # Simple parameter comparison
        current_params = {}
        golden_params = {}
        
        for block in current_tone.get("blocks", []):
            block_type = block.get("type", "UNKNOWN")
            for param, value in block.get("parameters", {}).items():
                current_params[f"{block_type}.{param}"] = value
        
        for block in golden_tone.get("blocks", []):
            block_type = block.get("type", "UNKNOWN")
            for param, value in block.get("parameters", {}).items():
                golden_params[f"{block_type}.{param}"] = value
        
        # Find differences
        all_keys = set(current_params.keys()) | set(golden_params.keys())
        differences = []
        
        for key in all_keys:
            current_val = current_params.get(key)
            golden_val = golden_params.get(key)
            
            if current_val != golden_val:
                differences.append({
                    "parameter": key,
                    "current": current_val,
                    "golden": golden_val,
                    "delta": current_val - golden_val if isinstance(current_val, (int, float)) and isinstance(golden_val, (int, float)) else "N/A"
                })
        
        if differences:
            st.markdown(f"**{len(differences)} parameters changed:**")
            for diff in differences[:10]:  # Show first 10 differences
                st.text(f"{diff['parameter']}: {diff['current']} (was {diff['golden']}, Δ{diff['delta']})")
        else:
            st.success("✅ No differences from golden preset")


def render_signal_chain_tab(tone_data: Dict[str, Any], blocks_featured: Dict[str, Any], fm9_ref: Dict[str, Any]):
    """Render the Signal Chain tab with visual flow and block management."""
    st.markdown("### 🔗 Signal Chain Overview")
    
    blocks = tone_data.get("blocks", [])
    tone_patch = tone_data.get("tone_patch", {})
    
    if blocks:
        # Visual signal chain
        reordered_blocks = render_chain_canvas(blocks, tone_patch)
        
        # Block management section
        st.markdown("### 🎛️ Block Management")
        
        # Create a grid of block cards
        cols = st.columns(3)
        for i, (block_name, block_data) in enumerate(tone_patch.items()):
            with cols[i % 3]:
                block_type = block_name.split("_")[0].upper() if "_" in block_name else block_name.upper()
                model_name = block_data.get("type", "Unknown")
                enabled = block_data.get("enabled", True)
                
                # Block card
                with st.container():
                    st.markdown(f"""
                    <div style="
                        border: 2px solid {'#ff4444' if enabled else '#666'};
                        border-radius: 8px;
                        padding: 15px;
                        margin: 10px 0;
                        background: {'#1a1a1a' if enabled else '#2a2a2a'};
                    ">
                        <h4 style="color: {'#ff4444' if enabled else '#666'}; margin: 0 0 10px 0;">{block_type}</h4>
                        <p style="color: #ccc; margin: 0; font-size: 14px;">{model_name}</p>
                        <p style="color: {'#4CAF50' if enabled else '#f44336'}; margin: 5px 0 0 0; font-size: 12px;">
                            {'● Active' if enabled else '○ Bypassed'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Quick toggle
                    if st.button(f"{'Disable' if enabled else 'Enable'} {block_type}", 
                               key=f"toggle_{block_name}", use_container_width=True):
                        tone_patch[block_name]["enabled"] = not enabled
                        st.session_state.tone_data["tone_patch"] = tone_patch
                        st.rerun()
        
        # Update session state
        tone_data["blocks"] = reordered_blocks
        tone_data["tone_patch"] = tone_patch
        st.session_state.tone_data = tone_data
    else:
        st.warning("No blocks found in tone data")


def render_block_editors_tab(tone_data: Dict[str, Any], blocks_featured: Dict[str, Any], fm9_ref: Dict[str, Any]):
    """Render the Block Editors tab with organized parameter controls."""
    st.markdown("### 🔧 Block Parameter Editors")
    
    tone_patch = tone_data.get("tone_patch", {})
    block_names = list(tone_patch.keys())
    
    if not block_names:
        st.warning("No blocks available for editing")
        return
    
    # Render each block directly without grouping
    for i, block_name in enumerate(block_names):
        block_data = tone_patch.get(block_name, {})
        if "_" in block_name:
            block_type = block_name.split("_")[0].lower()
        else:
            block_type = block_name.lower()
        
        # Always show blocks in tone_patch, regardless of blocks array enabled status
        is_enabled = block_data.get('enabled', True)
        # Use block_name in the title to make it unique
        expander_title = f"{block_type.upper()} Block {i+1} ({block_name})"
        
        with st.expander(expander_title, expanded=is_enabled):
            try:
                # Use block_name as unique identifier for widget keys
                updated_block = render_block_editor(
                    block_type, block_data, blocks_featured, fm9_ref, block_name
                )
                tone_patch[block_name] = updated_block
            except Exception as e:
                import traceback
                st.error(f"Error rendering {block_name}: {str(e)}")
                st.error(f"Full traceback: {traceback.format_exc()}")
                # Continue with the loop even if one block fails
                continue
    
    # Update session state
    tone_data["tone_patch"] = tone_patch
    st.session_state.tone_data = tone_data


def render_presets_tab(tone_data: Dict[str, Any]):
    """Render the Presets tab with tone suggestions and management."""
    st.markdown("### 🎵 Tone Presets & Suggestions")
    
    # Current tone info
    st.markdown("#### Current Tone")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info(f"**{tone_data.get('query', 'Unknown')}**")
    with col2:
        if st.button("🔄 Regenerate", use_container_width=True):
            # Trigger regeneration
            st.session_state.regenerate = True
            st.rerun()
    
    # Tone suggestions
    st.markdown("#### Quick Tone Suggestions")
    
    suggestions = [
        "Marshall JCM800 metal tone with high gain and tight bass",
        "U2 Edge delay tone with dotted eighth note delay and shimmer reverb",
        "Stevie Ray Vaughan blues tone with Tube Screamer and Fender amp",
        "Pink Floyd ambient tone with long reverb and delay",
        "Funk clean tone with bright Fender amp and compression",
        "Jazz fusion tone with clean amp and chorus"
    ]
    
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"suggestion_{i}", use_container_width=True):
                # Generate new tone based on suggestion
                with st.spinner("Generating tone..."):
                    generator = CleanAIToneGenerator()
                    result = generator.generate_tone_from_query(suggestion)
                    result = canonicalize_preset(result)
                    result = enforce_ref_ranges(result)
                    st.session_state.tone_data = result
                    st.session_state.original_query = suggestion
                    st.success("✅ Tone generated successfully!")
                    st.rerun()


def render_export_tab(tone_data: Dict[str, Any]):
    """Render the Export tab for downloading and sharing tones."""
    st.markdown("### 📤 Export & Share")
    
    # Tone summary
    st.markdown("#### Tone Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Query", tone_data.get('query', 'Unknown'))
    with col2:
        st.metric("Blocks", len(tone_data.get('tone_patch', {})))
    with col3:
        active_blocks = len([b for b in tone_data.get('tone_patch', {}).values() if b.get('enabled', False)])
        st.metric("Active", active_blocks)
    
    # Export options
    st.markdown("#### Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📄 JSON Export**")
        if st.button("💾 Download JSON", use_container_width=True):
            json_str = json.dumps(tone_data, indent=2)
            st.download_button(
                label="Download Tone JSON",
                data=json_str,
                file_name=f"tone_{tone_data.get('query', 'unknown').replace(' ', '_')}.json",
                mime="application/json"
            )
    
    with col2:
        st.markdown("**📋 Copy to Clipboard**")
        if st.button("📋 Copy JSON", use_container_width=True):
            json_str = json.dumps(tone_data, indent=2)
            st.code(json_str, language="json")
    
    # Tone preview
    st.markdown("#### Tone Preview")
    with st.expander("View Full Tone Data", expanded=False):
        st.json(tone_data)


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="ToneGPT",
        page_icon="🎸",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for compact, professional styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ff4444;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .subtitle {
        font-size: 1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .block-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    .parameter-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 0.5rem;
        align-items: center;
    }
    .parameter-label {
        min-width: 80px;
        font-weight: 500;
        color: #555;
    }
    .stExpander > div > div {
        padding: 0.5rem 1rem;
    }
    .stSlider > div > div > div {
        background-color: #ff4444;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 0.5rem;
        border-left: 3px solid #ff4444;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Compact header
    st.markdown('<h1 class="main-header">🎸 ToneGPT</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Professional Tone Editor</p>', unsafe_allow_html=True)
    
    # Initialize session state
    if "tone_data" not in st.session_state:
        st.session_state.tone_data = None
    if "original_query" not in st.session_state:
        st.session_state.original_query = ""
    
    # Load data
    blocks_featured = load_blocks_featured()
    fm9_ref = load_fm9_reference()
    
    if not blocks_featured:
        st.error("❌ Could not load blocks_featured.json")
        return
    
    if not fm9_ref:
        st.error("❌ Could not load fm9_comprehensive_reference.json")
        return
    
    # Compact sidebar for tone generation
    with st.sidebar:
        st.markdown("### 🎵 Generate Tone")
        
        query = st.text_input(
            "Describe your tone:",
            placeholder="e.g., 'Marshall JCM800 metal tone'",
            value=st.session_state.original_query,
            label_visibility="collapsed"
        )
        
        if st.button("🎸 Generate", type="primary", use_container_width=True):
            if query:
                with st.spinner("Generating tone..."):
                    generator = CleanAIToneGenerator()
                    result = generator.generate_tone_from_query(query)
                    result = canonicalize_preset(result)
                    result = enforce_ref_ranges(result)
                    
                    st.session_state.tone_data = result
                    st.session_state.original_query = query
                    st.success("✅ Tone generated successfully!")
                    st.rerun()
            else:
                st.error("Please enter a tone description")
        
        # System Info Section
        st.markdown("---")
        st.markdown("### 📊 System Info")
        
        # Initialize session state for stats if not exists
        if 'total_tones_generated' not in st.session_state:
            st.session_state.total_tones_generated = 0
        if 'total_tones_generated' in st.session_state and st.session_state.tone_data:
            # Increment counter when new tone is generated
            if 'last_query' not in st.session_state or st.session_state.last_query != query:
                st.session_state.total_tones_generated += 1
                st.session_state.last_query = query
        
        # Load system stats
        try:
            generator = CleanAIToneGenerator()
            total_blocks = len(generator.blocks_data)
            total_amps = len(generator.amp_models)
            total_drives = len(generator.drive_models)
            total_cabs = len(generator.cab_models)
            total_effects = sum(len(models) for models in generator.effect_models.values())
        except:
            total_blocks = total_amps = total_drives = total_cabs = total_effects = 0
        
        # Display stats
        st.metric("🎵 Tones Generated", st.session_state.total_tones_generated)
        st.metric("🔧 FM9 Blocks", f"{total_blocks:,}")
        st.metric("🎸 Amp Models", f"{total_amps:,}")
        st.metric("⚡ Drive Models", f"{total_drives:,}")
        st.metric("📦 Cab Models", f"{total_cabs:,}")
        st.metric("🎛️ Effect Models", f"{total_effects:,}")
        
        # Additional cool stats
        st.markdown("#### 🎯 Quick Stats")
        if st.session_state.tone_data:
            current_tone = st.session_state.tone_data
            active_blocks = len([b for b in current_tone.get('tone_patch', {}).values() if b.get('enabled', False)])
            st.metric("Active Blocks", active_blocks)
            
            # Show current tone complexity
            complexity = "Simple" if active_blocks <= 3 else "Moderate" if active_blocks <= 6 else "Complex"
            st.metric("Complexity", complexity)
        else:
            st.metric("Active Blocks", "0")
            st.metric("Complexity", "None")
    
    # Main content area with professional tabbed interface
    if st.session_state.tone_data:
        tone_data = st.session_state.tone_data
        
        # Compact header with tone info
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.markdown(f"**Current Tone:** {tone_data.get('query', 'Unknown')}")
        with col2:
            st.metric("Blocks", len([b for b in tone_data.get('tone_patch', {}).values() if b.get('enabled', False)]))
        with col3:
            st.metric("Effects", len([b for k, b in tone_data.get('tone_patch', {}).items() if b.get('enabled', False) and k not in ['amp', 'cab']]))
        with col4:
            st.metric("Active", len([b for b in tone_data.get('tone_patch', {}).values() if b.get('enabled', False)]))
        
        # Professional tabbed interface
        tab1, tab2, tab3, tab4 = st.tabs(["🔗 Signal Chain", "🔧 Block Editors", "🎵 Presets", "📤 Export"])
        
        with tab1:
            render_signal_chain_tab(tone_data, blocks_featured, fm9_ref)
        
        with tab2:
            render_block_editors_tab(tone_data, blocks_featured, fm9_ref)
        
        with tab3:
            render_presets_tab(tone_data)
        
        with tab4:
            render_export_tab(tone_data)
    
    else:
        # Clean welcome screen
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px;">
            <h2 style="color: #ff4444; margin-bottom: 20px;">🎸 Welcome to ToneGPT</h2>
            <p style="color: #666; font-size: 18px; margin-bottom: 40px;">
                Professional AI-powered guitar tone generation and editing
            </p>
            <div style="background: #1a1a1a; border-radius: 10px; padding: 30px; margin: 20px auto; max-width: 600px;">
                <h3 style="color: #ff4444; margin-bottom: 20px;">🚀 Get Started</h3>
                <p style="color: #ccc; margin-bottom: 20px;">
                    Enter a tone description in the sidebar to generate your first tone
                </p>
                <p style="color: #888; font-size: 14px;">
                    Try: "Marshall JCM800 metal tone", "U2 Edge delay tone", or "Stevie Ray Vaughan blues tone"
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
