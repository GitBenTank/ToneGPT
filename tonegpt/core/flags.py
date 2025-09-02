"""
Feature flags for ToneGPT system

This module defines feature flags for future functionality while maintaining
the current single-mode FM9-focused architecture.
"""

# Future multi-device support flag
# When enabled, allows support for devices other than FM9
# Currently disabled to maintain single-mode FM9 focus
FEATURE_MULTI_DEVICE: bool = False  # reserved for future; do not use in core

# Future advanced features flag (if ever needed)
# Currently disabled as per Cursor Rules - single-mode only
FEATURE_ADVANCED_MODE = False

# Advanced parameter control flag
# Enables advanced parameter manipulation features
FEATURE_ADVANCED_PARAMETERS = True

# Real-time analysis flag
# Enables real-time frequency analysis and visualization
FEATURE_REAL_TIME_ANALYSIS = True

# Export integration flag
# Enables export to various formats (FM9 presets, etc.)
FEATURE_EXPORT_INTEGRATION = True
