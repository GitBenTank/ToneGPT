"""
🎸 ToneGPT AI - AI-Powered FM9 Tone Generation Platform

A cutting-edge, AI-powered tone generation platform designed specifically for 
Fractal Audio's FM9 hardware. This project demonstrates advanced AI implementation, 
real-time audio analysis, and professional-grade software architecture.

Author: Ben Tankersley
License: MIT
Repository: https://github.com/GitBenTank/ToneGPT-FM9-V3
"""

__version__ = "1.0.0"
__author__ = "Ben Tankersley"
__email__ = "your.email@example.com"
__license__ = "MIT"
__url__ = "https://github.com/GitBenTank/ToneGPT-FM9-V3"

# Version info for production release
VERSION_INFO = {
    "major": 1,
    "minor": 0,
    "patch": 0,
    "release": "production",
    "build_date": "2025-01-27",
    "fm9_compatibility": "Firmware 3.x+",
    "python_version": "3.8+"
}

def get_version():
    """Get the full version string"""
    return f"{VERSION_INFO['major']}.{VERSION_INFO['minor']}.{VERSION_INFO['patch']}"

def get_version_info():
    """Get detailed version information"""
    return VERSION_INFO.copy()

def is_production():
    """Check if this is a production release"""
    return VERSION_INFO['release'] == 'production'

def get_fm9_compatibility():
    """Get FM9 compatibility information"""
    return VERSION_INFO['fm9_compatibility']
