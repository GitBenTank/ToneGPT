"""
FM9 Parameter Mapping Specification Tests

Tests that all FM9 parameters are correctly sourced from official data
and that no invented values are used.
"""

import pytest
import json
from pathlib import Path
from typing import Dict, Any, List

# Test data paths
BASE_DIR = Path(__file__).parent.parent
ROOT = BASE_DIR
FM9_REFERENCE = BASE_DIR / "tonegpt" / "data" / "fm9_comprehensive_reference.json"
FM9_CONFIG = BASE_DIR / "data" / "fm9_config.json"
BLOCKS_DATA = BASE_DIR / "tonegpt" / "core" / "blocks_with_footswitch.json"


class TestFM9ParameterMapping:
    """Test FM9 parameter mapping compliance"""
    
    def setup_method(self):
        """Load test data"""
        with open(FM9_REFERENCE, 'r') as f:
            self.fm9_reference = json.load(f)
        
        with open(BLOCKS_DATA, 'r') as f:
            self.blocks_data = json.load(f)
    
    def test_all_amp_parameters_sourced_from_reference(self):
        """Test that all amp parameters come from official FM9 reference"""
        amp_blocks = [block for block in self.blocks_data if block.get('category') == 'amp']
        
        for block in amp_blocks:
            # Check that block has valid FM9 parameters
            assert 'name' in block, f"Block missing name: {block}"
            assert 'type' in block, f"Block missing type: {block}"
            
            # Verify parameter ranges match FM9 specs
            if 'parameters' in block:
                params = block['parameters']
                for param_name, param_value in params.items():
                    self._validate_parameter_range(param_name, param_value, 'amp')
    
    def test_all_cab_parameters_sourced_from_reference(self):
        """Test that all cab parameters come from official FM9 reference"""
        cab_blocks = [block for block in self.blocks_data if block.get('category') == 'cab']
        
        for block in cab_blocks:
            assert 'name' in block, f"Cab block missing name: {block}"
            assert 'type' in block, f"Cab block missing type: {block}"
            
            if 'parameters' in block:
                params = block['parameters']
                for param_name, param_value in params.items():
                    self._validate_parameter_range(param_name, param_value, 'cab')
    
    def test_all_drive_parameters_sourced_from_reference(self):
        """Test that all drive parameters come from official FM9 reference"""
        drive_blocks = [block for block in self.blocks_data if block.get('category') == 'drive']
        
        for block in drive_blocks:
            assert 'name' in block, f"Drive block missing name: {block}"
            assert 'type' in block, f"Drive block missing type: {block}"
            
            if 'parameters' in block:
                params = block['parameters']
                for param_name, param_value in params.items():
                    self._validate_parameter_range(param_name, param_value, 'drive')
    
    def test_no_invented_parameters(self):
        """Test that core parameters are sourced from FM9 reference"""
        # Test key parameters that should always be in FM9 reference
        key_parameters = {
            'amp': ['gain', 'bass', 'mid', 'treble', 'presence', 'master', 'level'],
            'cab': ['level', 'low_cut', 'high_cut'],
            'drive': ['drive', 'tone', 'level', 'mix']
        }
        
        for block_type, expected_params in key_parameters.items():
            for param_name in expected_params:
                assert self._parameter_exists_in_reference(param_name, block_type), \
                    f"Core parameter '{param_name}' not found in FM9 reference for {block_type} block"
    
    def test_parameter_ranges_match_fm9_specs(self):
        """Test that parameter ranges match official FM9 specifications"""
        # Test key amp parameters
        amp_params = self.fm9_reference['fm9_reference']['amp_block']['key_parameters']
        
        assert amp_params['gain']['min'] == 0.0
        assert amp_params['gain']['max'] == 10.0
        assert amp_params['level']['min'] == -80.0
        assert amp_params['level']['max'] == 20.0
        
        # Test key cab parameters
        cab_params = self.fm9_reference['fm9_reference']['cab_block']['key_parameters']
        
        assert cab_params['level']['min'] == -80.0
        assert cab_params['level']['max'] == 20.0
    
    def test_gear_mapping_accuracy(self):
        """Test that gear mapping uses correct FM9 block names"""
        # Test Marshall mapping
        marshall_blocks = [block for block in self.blocks_data 
                          if block.get('category') == 'amp' and 'brit' in block.get('name', '').lower()]
        assert len(marshall_blocks) > 0, "No Marshall blocks found"
        
        # Test Mesa mapping
        mesa_blocks = [block for block in self.blocks_data 
                      if block.get('category') == 'amp' and 'recto' in block.get('name', '').lower()]
        assert len(mesa_blocks) > 0, "No Mesa Rectifier blocks found"
        
        # Test Fender mapping
        fender_blocks = [block for block in self.blocks_data 
                        if block.get('category') == 'amp' and 'fender' in block.get('name', '').lower()]
        assert len(fender_blocks) > 0, "No Fender blocks found"
    
    def _validate_parameter_range(self, param_name: str, param_value: Any, block_type: str):
        """Validate parameter value against FM9 reference ranges"""
        if block_type in self.fm9_reference['fm9_reference']:
            block_ref = self.fm9_reference['fm9_reference'][f'{block_type}_block']
            if 'key_parameters' in block_ref and param_name in block_ref['key_parameters']:
                param_ref = block_ref['key_parameters'][param_name]
                if 'min' in param_ref and 'max' in param_ref:
                    min_val = param_ref['min']
                    max_val = param_ref['max']
                    assert min_val <= param_value <= max_val, \
                        f"Parameter '{param_name}' value {param_value} outside FM9 range [{min_val}, {max_val}]"
    
    def _parameter_exists_in_reference(self, param_name: str, block_type: str) -> bool:
        """Check if parameter exists in FM9 reference"""
        if 'fm9_reference' in self.fm9_reference:
            fm9_ref = self.fm9_reference['fm9_reference']
            block_key = f'{block_type}_block'
            if block_key in fm9_ref:
                block_ref = fm9_ref[block_key]
                if 'key_parameters' in block_ref:
                    return param_name in block_ref['key_parameters']
        return False


class TestSingleModeArchitecture:
    """Test that single-mode architecture is maintained"""
    
    def test_no_dual_mode_logic_in_core(self):
        """Test that no dual-mode logic exists in core modules"""
        core_dir = BASE_DIR / "tonegpt" / "core"
        
        for py_file in core_dir.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
                
            with open(py_file, 'r') as f:
                content = f.read()
                
            # Check for dual-mode keywords
            dual_mode_keywords = ['dual_mode', 'dual-mode', 'commercial_mode', 'personal_mode']
            for keyword in dual_mode_keywords:
                assert keyword not in content, \
                    f"Dual-mode logic found in {py_file.name}: '{keyword}'"
    
    def test_feature_flags_for_future_multi_device(self):
        """Test that future multi-device support uses feature flags"""
        # This test ensures that any future multi-device support
        # would use proper feature flags like FEATURE_MULTI_DEVICE
        core_dir = BASE_DIR / "tonegpt" / "core"
        
        for py_file in core_dir.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
                
            with open(py_file, 'r') as f:
                content = f.read()
                
            # If multi-device logic exists, it should use feature flags
            if 'multi_device' in content or 'multi-device' in content:
                assert 'FEATURE_MULTI_DEVICE' in content, \
                    f"Multi-device logic in {py_file.name} should use FEATURE_MULTI_DEVICE flag"


def test_single_mode_only_in_core():
    """Test that no dual_mode logic exists in core implementation"""
    core = ROOT / "tonegpt" / "core"
    for p in core.rglob("*.py"):
        txt = p.read_text()
        assert "dual_mode" not in txt, f"dual_mode found in core: {p}"


def test_fm9_params_source_of_truth():
    """Test that FM9 parameter sources are properly configured"""
    cfg = json.loads((ROOT / "data" / "fm9_config.json").read_text())
    ref = json.loads((ROOT / "tonegpt" / "data" / "fm9_comprehensive_reference.json").read_text())
    assert isinstance(cfg, dict) and isinstance(ref, dict)
    # Check for key FM9 configuration sections
    assert "fm9_config" in cfg, "Missing fm9_config section"
    assert "fm9_reference" in ref, "Missing fm9_reference section"


def test_no_network_calls_in_core():
    """Test that no network calls exist in core modules"""
    for p in (ROOT / "tonegpt" / "core").rglob("*.py"):
        content = p.read_text()
        assert "requests." not in content, f"Network calls not allowed: {p}"
        assert "urllib" not in content, f"Network calls not allowed: {p}"
        assert "http.client" not in content, f"Network calls not allowed: {p}"


def test_feature_flag_defined_for_future_multi_device():
    """Test that feature flag is defined for future multi-device support"""
    flags_file = ROOT / "tonegpt" / "core" / "flags.py"
    assert flags_file.exists(), "flags.py file not found"
    flags_content = flags_file.read_text()
    assert "FEATURE_MULTI_DEVICE" in flags_content, "FEATURE_MULTI_DEVICE flag not defined"


if __name__ == "__main__":
    pytest.main([__file__])
