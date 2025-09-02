# Allowed Overrides

This document lists the few cases where it's okay to deviate from the standard FM9 parameter sourcing rules.

## 🎯 **Override Categories**

### **1. Alias Handling**
**When:** Parameter names have multiple valid forms in FM9
**Example:** `hiCut` vs `high_cut` vs `hi_cut`
**Override:** Use canonical form from `docs/glossary.md`
**Citation:** `docs/fm9-mapping-tldr.md#Canonical Block Categories`

```python
# ALLOWED: Alias normalization
def normalize_param_name(param_name: str) -> str:
    """Normalize parameter names to canonical form"""
    aliases = {
        'hiCut': 'high_cut',
        'hi_cut': 'high_cut', 
        'lowCut': 'low_cut',
        'lo_cut': 'low_cut'
    }
    return aliases.get(param_name, param_name)
```

### **2. Missing Parameter Fallbacks**
**When:** Parameter exists in FM9 but not in reference files
**Example:** New FM9 firmware adds parameter not yet in reference
**Override:** Add to reference files, don't invent
**Citation:** `docs/ground-truth.md#Invariants`

```python
# ALLOWED: Add missing parameter to reference
def add_missing_param_to_reference(param_name: str, param_spec: dict):
    """Add missing parameter to FM9 reference files"""
    # Add to data/fm9_comprehensive_reference.json
    # Then use in code
    pass

# NOT ALLOWED: Invent parameter
def invent_parameter():
    # This violates the rules
    return {"gain": 5.0}  # DON'T DO THIS
```

### **3. Feature Flag Usage**
**When:** Future multi-device support needed
**Example:** Adding support for other Fractal devices
**Override:** Use `FEATURE_MULTI_DEVICE` flag in adapters only
**Citation:** `docs/ground-truth.md#Future-proofing`

```python
# ALLOWED: Feature flag in adapters
from tonegpt.core.flags import FEATURE_MULTI_DEVICE

def device_adapter():
    if FEATURE_MULTI_DEVICE:
        # Multi-device logic here
        pass
    else:
        # FM9-only logic
        pass

# NOT ALLOWED: Feature flag in core
def core_function():
    if FEATURE_MULTI_DEVICE:  # DON'T DO THIS IN CORE
        pass
```

### **4. Error Handling Overrides**
**When:** Graceful degradation needed for missing data
**Example:** Missing parameter in reference files
**Override:** Fail fast with clear error message
**Citation:** `docs/fm9-mapping-tldr.md#Parameter Rules`

```python
# ALLOWED: Fail fast with citation
def get_parameter(param_name: str, block_type: str):
    """Get parameter from FM9 reference"""
    if param_name not in reference:
        raise ValueError(
            f"Missing parameter '{param_name}' in "
            f"data/fm9_comprehensive_reference.json#{block_type}_block"
        )

# NOT ALLOWED: Silent fallback
def get_parameter_bad(param_name: str):
    return reference.get(param_name, 5.0)  # DON'T INVENT VALUES
```

## 🚫 **Never Allowed Overrides**

### **1. Dual-Mode Logic**
- **Never** add dual-mode logic to core modules
- **Never** use commercial/personal mode switching
- **Citation:** `docs/ground-truth.md#Invariants`

### **2. Parameter Invention**
- **Never** invent parameter values
- **Never** use estimated or guessed ranges
- **Citation:** `docs/fm9-mapping-tldr.md#Parameter Rules`

### **3. Network Calls in Core**
- **Never** make network requests in `tonegpt/core/*`
- **Never** fetch data from external sources
- **Citation:** `docs/ground-truth.md#Safety Constraints`

### **4. Hardware Modification**
- **Never** write to firmware paths
- **Never** modify hardware configurations
- **Citation:** `docs/ground-truth.md#Safety Constraints`

## 📋 **Override Request Process**

1. **Document the need** - Why is the override necessary?
2. **Cite the rule** - Which rule needs to be overridden?
3. **Propose the solution** - How will you handle it safely?
4. **Update this file** - Add the override to this document
5. **Get approval** - Ensure the override is justified

## ✅ **Validation Checklist**

Before using any override:
- [ ] Is it in the allowed categories above?
- [ ] Does it maintain FM9 single-mode focus?
- [ ] Does it preserve data integrity?
- [ ] Is it properly documented?
- [ ] Are tests updated?

Remember: **Overrides should be rare exceptions, not common practice.**
