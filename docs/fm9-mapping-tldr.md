# FM9 Mapping TL;DR (Authoritative)

## 🎸 **Quick Reference**

### **Data Sources (Priority Order)**
1. `/data/fm9_config.json` - Primary parameter source
2. `/data/fm9_comprehensive_reference.json` - Fallback reference
3. **NEVER synthesize values** - if missing, raise ValueError with file+key

### **Parameter Rules**
- **ALWAYS read from data/fm9_config.json first**
- **FALLBACK to data/fm9_comprehensive_reference.json**
- **NEVER invent parameters** - if missing, raise ValueError with exact file+key
- **VALIDATE against hardware** - ensure accuracy to real FM9

## 🔧 **Canonical Block Categories**

### **AMP - Amplifiers**
- **Source**: `data/fm9_config.json` → `AMP` section
- **Fallback**: `data/fm9_comprehensive_reference.json` → `amp_block`
- **Key Parameters**: gain, bass, mid, treble, presence, master, level

### **CAB - Cabinets**
- **Source**: `data/fm9_config.json` → `CAB` section
- **Fallback**: `data/fm9_comprehensive_reference.json` → `cab_block`
- **Key Parameters**: low_cut, high_cut, level, mic_type, mic_distance

### **DRV - Drive Effects**
- **Source**: `data/fm9_config.json` → `DRV` section
- **Fallback**: `data/fm9_comprehensive_reference.json` → `drive_block`
- **Key Parameters**: drive, tone, level, mix

### **MOD - Modulation Effects**
- **Source**: `data/fm9_config.json` → `MOD` section
- **Fallback**: `data/fm9_comprehensive_reference.json` → `modulation_block`
- **Key Parameters**: rate, depth, mix, level

### **DLY - Delay Effects**
- **Source**: `data/fm9_config.json` → `DLY` section
- **Fallback**: `data/fm9_comprehensive_reference.json` → `delay_block`
- **Key Parameters**: time, feedback, mix, level

### **REV - Reverb Effects**
- **Source**: `data/fm9_config.json` → `REV` section
- **Fallback**: `data/fm9_comprehensive_reference.json` → `reverb_block`
- **Key Parameters**: room_size, decay, mix, level

## 🎯 **Mapping Rules**

### **Gear Matching**
```python
# Marshall JCM800 → "BRIT 800 2204 HIGH"
# Mesa Rectifier → "Recto Pro", "RECTO1 ORANGE MODERN"
# Fender Twin → "TWIN REVERB", "TWIN REVERB NORMAL"
# Vox AC30 → "AC30", "AC30 TOP BOOST"
```

### **Parameter Validation**
```python
# Always validate against official ranges
if gain < 0.0 or gain > 10.0:
    raise ValueError("Gain must be 0.0-10.0 per FM9 specs")
```

## ⚠️ **Common Pitfalls**

### **DON'T**
- Invent parameter values
- Use generic ranges
- Assume parameter behavior
- Skip validation

### **DO**
- Cite exact file+section for missing data
- Use official FM9 parameter ranges
- Validate all inputs
- Document constraints

## 🔍 **Quick Checks**

### **Before Coding**
1. Is parameter in `fm9_comprehensive_reference.json`?
2. What's the official range?
3. Are there any constraints?
4. Do I need to cite missing data?

### **After Coding**
1. All parameters validated?
2. Ranges match FM9 specs?
3. No invented values?
4. Constraints documented?
