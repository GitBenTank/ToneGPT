#!/usr/bin/env python3
"""
ToneGPT - AI-Powered Guitar Tone Generation
Streamlit Cloud Entry Point
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the main Streamlit app
from ui.frontend_interactive import main

if __name__ == "__main__":
    main()
