"""
Parameter validation and clamping for FM9 parameters

TL;DR: Ensures all parameters are within valid FM9 ranges and normalizes common mistakes.
- Clamps parameters to min/max ranges from FM9 reference
- Converts obvious ms→% mistakes for attack/release parameters
- Rounds values to reasonable precision
- Maintains FM9 accuracy and prevents out-of-range errors

Constraints:
- FM9 single-mode only (docs/ground-truth.md#Invariants)
- Parameters from data/fm9_comprehensive_reference.json
- No parameter invention - only clamping and normalization
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any

# Load FM9 reference data
_REF = json.loads(Path("data/fm9_comprehensive_reference.json").read_text(encoding="utf-8"))

# Map canonical block types to reference keys
_BLOCK_REF = {
    "amp": "amp_block", 
    "cab": "cab_block", 
    "drv": "drive_block", 
    "dly": "delay_block",
    "rev": "reverb_block", 
    "modulation": "modulation_block", 
    "pitch": "pitch_block",
    "dynamics": "dynamics_block", 
    "eq": "eq_block", 
    "utility": "utility_block",
}


def _ms_to_percent(v_ms: float, full_scale_ms: float = 2000.0) -> float:
    """
    Convert milliseconds to percentage (0-100).
    
    Args:
        v_ms: Value in milliseconds
        full_scale_ms: Full scale in milliseconds (default 2000ms)
        
    Returns:
        Percentage value (0-100)
    """
    return max(0.0, min(100.0, (float(v_ms) / full_scale_ms) * 100.0))


def _normalize(block_type: str, param: str, value: float, spec: Dict[str, Any]) -> float:
    """
    Normalize parameter values, handling common mistakes.
    
    Args:
        block_type: Block type (e.g., 'dynamics')
        param: Parameter name (e.g., 'attack')
        value: Current parameter value
        spec: Parameter specification from FM9 reference
        
    Returns:
        Normalized parameter value
    """
    p = param.lower()
    
    # Handle attack/release parameters that might be in milliseconds instead of percentage
    if p in ("attack", "release") and spec.get("max") == 100.0 and value > 120.0:
        return _ms_to_percent(value)
    
    return value


def clamp_range(value: float, spec: Dict[str, Any]) -> float:
    """
    Clamp a single parameter value to its valid range.
    
    Args:
        value: Parameter value to clamp
        spec: Parameter specification from FM9 reference
        
    Returns:
        Clamped parameter value within valid range
    """
    if not isinstance(value, (int, float)):
        return value
    
    if "min" in spec and "max" in spec:
        lo, hi = float(spec["min"]), float(spec["max"])
        clamped = max(lo, min(hi, float(value)))
        
        # Round to reasonable precision
        if "step" in spec:
            step = float(spec["step"])
            if step > 0:
                clamped = round(clamped / step) * step
        
        return round(clamped, 1)
    
    return float(value)


def enforce_ref_ranges(preset: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enforce FM9 parameter ranges and normalize values.
    
    Args:
        preset: Tone preset dictionary with 'blocks' key
        
    Returns:
        Preset with clamped and normalized parameters
    """
    blocks = preset.get("blocks", [])
    fixed = []
    
    for blk in blocks:
        bkey = blk["type"].lower()
        ref_key = _BLOCK_REF.get(bkey, f"{bkey}_block")
        spec = _REF.get(ref_key, {}).get("key_parameters", {})
        params = dict(blk.get("parameters", {}))
        
        for k, v in list(params.items()):
            ps = spec.get(k)
            if ps and isinstance(v, (int, float)) and "min" in ps and "max" in ps:
                # Normalize the value first
                v = _normalize(bkey, k, float(v), ps)
                
                # Clamp to valid range
                lo, hi = float(ps["min"]), float(ps["max"])
                if v < lo: 
                    v = lo
                if v > hi: 
                    v = hi
                
                # Round to reasonable precision
                params[k] = round(v, 1)
        
        fixed.append({**blk, "parameters": params})
    
    return {**preset, "blocks": fixed}
