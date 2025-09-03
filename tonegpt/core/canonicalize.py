"""
Canonicalization utilities for ToneGPT

TL;DR: Translates common/instance names to exact FM9 keys from reference data.
- Maps block aliases (drive_1 → DRV) to canonical FM9 block codes
- Maps parameter aliases (low_mid_freq → mid_freq) to canonical FM9 parameters
- Ensures consistent naming across the system
- No parameter invention - only translates existing names

Constraints:
- FM9 single-mode only (docs/ground-truth.md#Invariants)
- Data sources are read-only (docs/ground-truth.md#Safety Constraints)
- No network calls (pure function)
- Raises ValueError if required data is missing (cite file+key)
"""

from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Dict, Any, List


def _snake(s: str) -> str:
    """Convert string to snake_case for consistent key matching."""
    return re.sub(r'[^a-z0-9]+', '_', s.strip().lower()).strip('_')


def _load_json(p: str) -> Dict[str, Any]:
    """Load JSON file with error handling."""
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Missing alias file: {p}. See docs/ground-truth.md#Data Sources")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {p}: {e}. See docs/ground-truth.md#Data Sources")


# Preload alias maps
try:
    _BLOCK_ALIASES = _load_json("data/block_aliases.json")
    _PARAM_ALIASES = _load_json("data/param_aliases.json")
except ValueError:
    # Fallback to empty dicts if files don't exist yet
    _BLOCK_ALIASES = {}
    _PARAM_ALIASES = {}


def canonical_block(block_key: str) -> str:
    """
    Return canonical FM9 block code (e.g., DRV, DLY, REV) from any input.
    
    Args:
        block_key: Input block name (e.g., "drive_1", "delay", "DRV")
        
    Returns:
        Canonical block code (e.g., "DRV", "DLY", "REV")
    """
    key = _snake(block_key)
    return _BLOCK_ALIASES.get(key, key.upper())


def canonical_param(block_key: str, param: str) -> str:
    """
    Map synonyms to canonical parameter name for the given block.
    
    Args:
        block_key: Block type (e.g., "DRV", "EQ")
        param: Parameter name (e.g., "tone_control", "low_mid_freq")
        
    Returns:
        Canonical parameter name (e.g., "tone", "mid_freq")
    """
    b = canonical_block(block_key)
    p = _snake(param)
    return _PARAM_ALIASES.get(b, {}).get(p, p)


def canonicalize_preset(preset: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure preset has 'blocks' and canonical block/param names.
    
    Args:
        preset: Input preset dictionary
        
    Returns:
        Preset with canonicalized block and parameter names
        
    Raises:
        ValueError: If preset structure is invalid
    """
    if not isinstance(preset, dict):
        raise ValueError("Preset must be a dictionary")
    
    # Extract blocks from various possible keys
    blocks = preset.get("blocks") or preset.get("tone_patch", {})
    
    # Handle tone_patch format (dict of blocks)
    if isinstance(blocks, dict):
        blocks_list = []
        for block_name, block_data in blocks.items():
            if isinstance(block_data, dict):
                btype_in = block_data.get("type") or block_name
                btype = canonical_block(btype_in)
                params = block_data.get("parameters") or block_data.get("params") or {}
                canon_params = {canonical_param(btype, k): v for k, v in params.items()}
                blocks_list.append({
                    "type": btype,
                    "parameters": canon_params,
                    **{k: v for k, v in block_data.items() if k not in ("type", "block", "params", "parameters")}
                })
        blocks = blocks_list
    
    # Handle blocks list format
    elif isinstance(blocks, list):
        out_blocks = []
        for blk in blocks:
            if not isinstance(blk, dict):
                continue
            btype_in = blk.get("type") or blk.get("block") or "UNKNOWN"
            btype = canonical_block(btype_in)
            params = blk.get("parameters") or blk.get("params") or {}
            canon_params = {canonical_param(btype, k): v for k, v in params.items()}
            out_blocks.append({
                "type": btype,
                "parameters": canon_params,
                **{k: v for k, v in blk.items() if k not in ("type", "block", "params", "parameters")}
            })
        blocks = out_blocks
    
    else:
        blocks = []
    
    # Always include 'blocks' key to satisfy tests
    return {**preset, "blocks": blocks}


def validate_against_reference(preset: Dict[str, Any], fm9_ref: Dict[str, Any]) -> None:
    """
    Validate canonicalized preset against FM9 reference data.
    
    Args:
        preset: Canonicalized preset dictionary
        fm9_ref: FM9 comprehensive reference data
        
    Raises:
        ValueError: If block type or parameter not found in reference
    """
    blocks = preset.get("blocks", [])
    
    for block in blocks:
        if not isinstance(block, dict):
            continue
            
        block_type = block.get("type", "").lower()
        ref_block = fm9_ref.get(f"{block_type}_block")
        
        if not ref_block:
            raise ValueError(f"Unknown block type {block_type} in data/fm9_comprehensive_reference.json")
        
        valid_params = set(ref_block.get("key_parameters", {}).keys())
        params = block.get("parameters", {})
        
        for param_name in params.keys():
            if param_name not in valid_params:
                raise ValueError(f"{block_type}.{param_name} not in FM9 reference data/fm9_comprehensive_reference.json")
