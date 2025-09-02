"""
Feature flags for ToneGPT system

TL;DR: Feature flags for future expansion while maintaining FM9 single-mode focus.
- FEATURE_MULTI_DEVICE: Reserved for future multi-device support (adapters only)
- All flags default to False to maintain current single-mode architecture
- No advanced mode flags (single-mode only per Cursor Rules)
- Feature flags only used in adapters, never in core modules

Constraints:
- FM9 single-mode only (docs/ground-truth.md#Invariants)
- Feature flags in adapters only (docs/ground-truth.md#Future-proofing)
- No advanced mode logic (docs/ground-truth.md#Invariants)
"""

# Future multi-device support flag
# When enabled, allows support for devices other than FM9
# Currently disabled to maintain single-mode FM9 focus
# TODO: Enable when FM9 → other Fractal devices are supported
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
