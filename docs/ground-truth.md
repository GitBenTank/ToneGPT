# ToneGPT Ground Truth Documentation

## 🎯 **System Purpose**
ToneGPT is a single-mode, FM9-focused AI tone generation platform that provides accurate real-world gear modeling using authentic FM9 specifications.

## 🏗️ **Architecture Principles**

### **Single-Mode Baseline**
- **FM9-only focus**: No dual-mode logic in core modules
- **Future multi-device**: Behind `FEATURE_MULTI_DEVICE` flag in adapters only
- **Clean separation**: Core logic separate from device-specific implementations
- **TODO**: Enable `FEATURE_MULTI_DEVICE` when FM9 → other Fractal devices are supported

### **Data Source Hierarchy**
1. **Primary**: `/data/fm9_comprehensive_reference.json` - Official FM9 parameters
2. **Secondary**: `/data/fm9_config.json` - Configuration overrides
3. **Fallback**: Never invent parameters - stop and cite missing data

## 📋 **Acceptance Criteria**

### **FM9 Parameter Mapping**
- [ ] All block parameters sourced from `fm9_comprehensive_reference.json`
- [ ] No invented or estimated parameter values
- [ ] Missing parameters documented with exact file+section citations
- [ ] Parameter ranges match official FM9 specifications

### **Code Quality**
- [ ] Python 3.12 with type hints
- [ ] Google-style docstrings with "Constraints" subsection
- [ ] No network calls in `tonegpt/core/*`
- [ ] All data sources are read-only

### **Architecture Compliance**
- [ ] No dual-mode logic in core modules
- [ ] Single-mode FM9 baseline maintained
- [ ] Future multi-device support behind feature flags
- [ ] Clean separation of concerns

### **Testing Requirements**
- [ ] Tests updated/added for new functionality
- [ ] FM9 parameter mapping preserved in tests
- [ ] No hidden dual-mode reintroduction
- [ ] All changes pass existing test suite

## 🔒 **Safety Constraints**

### **Data Integrity**
- Never modify firmware or hardware paths
- All FM9 data sources are read-only
- No network calls in core modules
- Parameter validation against official specs

### **System Boundaries**
- Core modules: Pure logic, no I/O
- Adapters: Device-specific implementations
- UI: Presentation layer only
- Data: Immutable reference sources

## 📊 **Quality Metrics**

### **Parameter Accuracy**
- 100% of parameters sourced from official FM9 data
- 0% invented or estimated values
- All parameter ranges validated against hardware specs

### **Code Quality**
- 100% type hint coverage
- All docstrings include "Constraints" subsection
- No network dependencies in core
- Clean architecture principles followed

### **Testing Coverage**
- All new functionality tested
- FM9 parameter mapping preserved
- No regression in existing features
- Performance benchmarks maintained
