#!/bin/bash

# 🎸 ToneGPT AI - Deployment Script
# This script sets up and runs ToneGPT AI for production use

echo "🚀 ToneGPT AI - Production Deployment"
echo "====================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version is installed, but Python $required_version+ is required."
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Kill any existing Streamlit processes
echo "🧹 Cleaning up existing processes..."
pkill -f "streamlit run" 2>/dev/null || true

# Start the application
echo "🚀 Starting ToneGPT AI..."
echo "🌐 The application will be available at: http://localhost:8504"
echo "📱 Press Ctrl+C to stop the application"
echo ""

# Run the application
streamlit run ui/frontend_ai_v4.py --server.port 8504 --server.headless true
