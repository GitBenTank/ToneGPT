#!/bin/bash
# ToneGPT Complete System Launcher

echo "🎸 ToneGPT Complete System - Launching..."
echo "=========================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if required files exist
if [ ! -f "tonegpt/core/blocks_with_footswitch.json" ]; then
    echo "❌ Core blocks file not found. Please run complete_system_integration.py first."
    exit 1
fi

# Launch the enhanced UI
echo "🚀 Launching ToneGPT Production UI..."
echo "🌐 Open your browser to: http://localhost:8506"
echo "🔀 Use the sidebar to switch between modes!"
echo ""
echo "Press Ctrl+C to stop the system"
echo ""

streamlit run ui/frontend_production_enhanced.py --server.port 8506
