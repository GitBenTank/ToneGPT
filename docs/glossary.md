# FM9 Glossary (Canonical Names)

This document defines canonical FM9 names and abbreviations to ensure consistency across the codebase. Cursor and contributors should use these exact terms.

## 🎸 **Block Categories (Canonical)**

### **AMP - Amplifiers**
- **Canonical:** `AMP`
- **Aliases:** `amp`, `amplifier`, `amp_block`
- **Use:** Always use `AMP` in data structures

### **CAB - Cabinets**
- **Canonical:** `CAB`
- **Aliases:** `cab`, `cabinet`, `cab_block`
- **Use:** Always use `CAB` in data structures

### **DRV - Drive Effects**
- **Canonical:** `DRV`
- **Aliases:** `drive`, `overdrive`, `distortion`, `drive_block`
- **Use:** Always use `DRV` in data structures

### **MOD - Modulation Effects**
- **Canonical:** `MOD`
- **Aliases:** `modulation`, `mod`, `mod_block`
- **Use:** Always use `MOD` in data structures

### **DLY - Delay Effects**
- **Canonical:** `DLY`
- **Aliases:** `delay`, `delay_block`
- **Use:** Always use `DLY` in data structures

### **REV - Reverb Effects**
- **Canonical:** `REV`
- **Aliases:** `reverb`, `reverb_block`
- **Use:** Always use `REV` in data structures

## 🔧 **Parameter Names (Canonical)**

### **Amplifier Parameters**
- **gain** (not `drive`, `input_gain`, `preamp_gain`)
- **bass** (not `low`, `low_freq`, `bass_freq`)
- **mid** (not `middle`, `mid_freq`, `midrange`)
- **treble** (not `high`, `high_freq`, `treble_freq`)
- **presence** (not `pres`, `presence_freq`)
- **master** (not `master_vol`, `master_volume`, `output`)
- **level** (not `output_level`, `volume`, `vol`)

### **Cabinet Parameters**
- **low_cut** (not `hiCut`, `hi_cut`, `lowcut`)
- **high_cut** (not `loCut`, `lo_cut`, `highcut`)
- **mic_type** (not `mic`, `microphone`, `mic_model`)
- **mic_distance** (not `distance`, `mic_dist`, `proximity`)

### **Drive Parameters**
- **drive** (not `gain`, `distortion`, `overdrive`)
- **tone** (not `tone_control`, `filter`, `eq`)
- **level** (not `output`, `volume`, `vol`)
- **mix** (not `wet_dry`, `blend`, `balance`)

### **Time Effect Parameters**
- **time** (not `delay_time`, `delay`, `ms`)
- **feedback** (not `fb`, `regeneration`, `repeat`)
- **mix** (not `wet_dry`, `blend`, `balance`)

## 🎛️ **FM9 Block Names (Canonical)**

### **Marshall Models**
- **BRIT 800 2204 HIGH** (not `Brit 800`, `JCM800`, `Marshall 800`)
- **BRIT 800 2203 HIGH** (not `Brit 800 2203`, `JCM800 2203`)
- **BRIT PLEXI** (not `Plexi`, `Marshall Plexi`, `Super Lead`)

### **Mesa Boogie Models**
- **Recto Pro** (not `Rectifier`, `Dual Rectifier`, `Mesa Recto`)
- **RECTO1 ORANGE MODERN** (not `Recto Orange`, `Mesa Orange`)
- **Mesa Mark IIC+** (not `Mark 2C+`, `IIC+`, `Mesa Mark`)

### **Fender Models**
- **5F1 TWEED** (not `Tweed`, `Fender Tweed`, `Champ`)
- **DELUXE VERB** (not `Deluxe Reverb`, `Fender Deluxe`)
- **TWIN REVERB** (not `Twin`, `Fender Twin`)

### **Vox Models**
- **AC30** (not `Vox AC30`, `AC-30`, `Vox`)
- **AC30 TOP BOOST** (not `AC30TB`, `Vox Top Boost`)

## 📁 **File Paths (Canonical)**

### **Data Files**
- **data/fm9_config.json** (not `fm9_config.json`, `config.json`)
- **data/fm9_comprehensive_reference.json** (not `reference.json`, `fm9_ref.json`)
- **tonegpt/core/blocks_with_footswitch.json** (not `blocks.json`, `fm9_blocks.json`)

### **Documentation Files**
- **docs/ground-truth.md** (not `ground_truth.md`, `groundtruth.md`)
- **docs/fm9-mapping-tldr.md** (not `mapping.md`, `fm9_mapping.md`)
- **docs/glossary.md** (not `terms.md`, `definitions.md`)

## 🏗️ **Architecture Terms (Canonical)**

### **Core Concepts**
- **single-mode** (not `single_mode`, `single mode`, `unimode`)
- **FM9-focused** (not `FM9_focused`, `fm9_focused`, `FM9 focused`)
- **dual_mode** (not `dual-mode`, `dual mode`) - **NEVER USE IN CORE**

### **Feature Flags**
- **FEATURE_MULTI_DEVICE** (not `MULTI_DEVICE`, `multi_device`, `MULTI_DEVICE_FLAG`)
- **FEATURE_ADVANCED_PARAMETERS** (not `ADVANCED_PARAMS`, `advanced_params`)

## 🚫 **Deprecated Terms (Never Use)**

### **Dual-Mode Terms**
- `dual_mode` - **NEVER USE IN CORE**
- `commercial_mode` - **NEVER USE IN CORE**
- `personal_mode` - **NEVER USE IN CORE**
- `generic_name` - **NEVER USE IN CORE**

### **Generic Terms**
- `generic` - Use specific FM9 terms instead
- `fallback` - Use `default` or specific error handling
- `invent` - Use `source from reference` or `fail fast`

## ✅ **Usage Guidelines**

1. **Always use canonical terms** from this glossary
2. **Never abbreviate** unless the abbreviation is listed here
3. **Check this file** before creating new terms
4. **Update this file** when adding new canonical terms
5. **Use exact case** as specified (e.g., `AMP` not `amp`)

## 🔍 **Quick Reference**

| Category | Canonical | Never Use |
|----------|-----------|-----------|
| Block Types | `AMP`, `CAB`, `DRV`, `MOD`, `DLY`, `REV` | `amp`, `cabinet`, `drive` |
| Parameters | `gain`, `bass`, `mid`, `treble`, `level` | `drive`, `low`, `high`, `vol` |
| File Paths | `data/fm9_config.json` | `config.json`, `fm9_config.json` |
| Architecture | `single-mode`, `FM9-focused` | `dual_mode`, `generic` |

This glossary ensures consistency and prevents Cursor from renaming things incorrectly.
