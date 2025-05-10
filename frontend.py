import streamlit as st
import json
from core.tone_loader import load_all_genres
from interface.block_insights import get_block_insights

# Load all tone data
genres = load_all_genres()
genre_names = list(genres.keys())

st.set_page_config(page_title="ToneGPT for FM9", layout="wide")
st.title("🎸 ToneGPT for Fractal FM9")

# Sidebar genre selection
selected_genre = st.sidebar.selectbox("Select a Genre", genre_names)
genre_data = genres[selected_genre]

# Show tone preset info
st.subheader(f"🎵 Band: {genre_data['band']}")
st.write(f"**🎚️ Preset Name:** {genre_data['preset_name']}")
st.write(f"**📦 Genre:** {genre_data['genre']}")
st.write(f"**🔊 Amp Model:** {genre_data['amp_model']}")
st.write(f"**🧱 Cab IR:** {genre_data['cab_ir']}")

# Effects chain
st.markdown("**🎛️ Effects Chain:**")
effects = genre_data.get("effects", [])
st.write(", ".join(effects))

# Summary
st.markdown("**📝 Summary:**")
st.info(genre_data["summary"])

# Block insights
st.markdown("---")
st.subheader("🔍 Block Insights")
block_insights = get_block_insights(effects)

for insight in block_insights:
    st.markdown(f"### 🔧 {insight['name']}")
    st.write(insight['description'])
    st.write(f"**Required:** {'Yes' if insight['required'] else 'No'}")
    st.write(f"**Key Parameters:** {', '.join(insight['key_parameters'])}")
