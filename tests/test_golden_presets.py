"""
Golden Tests for FM9 Presets

TL;DR: Tests that assert output JSON matches exactly for known FM9 presets.
- Validates complete tone generation accuracy
- Ensures no parameter drift or changes
- Tests real-world gear mapping (Marshall, Mesa, Fender, Vox)
- Validates FM9 single-mode architecture

Constraints:
- FM9 single-mode only (docs/ground-truth.md#Invariants)
- Params from data/fm9_config.json -> fm9_comprehensive_reference.json
- No network calls (pure function)
- Raises ValueError if required param missing (cite file+key)
"""

import json
import pytest
from pathlib import Path
from tonegpt.core.clean_ai_tone_generator import CleanAIToneGenerator

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "data" / "golden_presets"


class TestGoldenPresets:
    """Test that generated tones match known FM9 presets exactly"""
    
    @pytest.fixture
    def generator(self):
        """Create AI tone generator instance"""
        return CleanAIToneGenerator()
    
    def test_marshall_jcm800_metal_tone(self, generator):
        """Test Marshall JCM800 metal tone generation"""
        query = "Marshall JCM800 metal tone with high gain and tight bass"
        result = generator.generate_tone_from_query(query)
        
        # Load expected golden preset
        golden_file = TEST_DATA_DIR / "marshall_jcm800_metal.json"
        if golden_file.exists():
            with open(golden_file, 'r') as f:
                expected = json.load(f)
            
            # Assert exact match
            assert result == expected, f"Generated tone doesn't match golden preset: {golden_file}"
        else:
            # Create golden preset if it doesn't exist
            TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(golden_file, 'w') as f:
                json.dump(result, f, indent=2)
            pytest.skip(f"Created golden preset: {golden_file}")
    
    def test_mesa_rectifier_modern_tone(self, generator):
        """Test Mesa Rectifier modern tone generation"""
        query = "Mesa Boogie Rectifier modern high gain tone"
        result = generator.generate_tone_from_query(query)
        
        # Load expected golden preset
        golden_file = TEST_DATA_DIR / "mesa_rectifier_modern.json"
        if golden_file.exists():
            with open(golden_file, 'r') as f:
                expected = json.load(f)
            
            # Assert exact match
            assert result == expected, f"Generated tone doesn't match golden preset: {golden_file}"
        else:
            # Create golden preset if it doesn't exist
            TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(golden_file, 'w') as f:
                json.dump(result, f, indent=2)
            pytest.skip(f"Created golden preset: {golden_file}")
    
    def test_fender_twin_clean_tone(self, generator):
        """Test Fender Twin clean tone generation"""
        query = "Fender Twin Reverb clean tone with reverb"
        result = generator.generate_tone_from_query(query)
        
        # Load expected golden preset
        golden_file = TEST_DATA_DIR / "fender_twin_clean.json"
        if golden_file.exists():
            with open(golden_file, 'r') as f:
                expected = json.load(f)
            
            # Assert exact match
            assert result == expected, f"Generated tone doesn't match golden preset: {golden_file}"
        else:
            # Create golden preset if it doesn't exist
            TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(golden_file, 'w') as f:
                json.dump(result, f, indent=2)
            pytest.skip(f"Created golden preset: {golden_file}")
    
    def test_vox_ac30_crunch_tone(self, generator):
        """Test Vox AC30 crunch tone generation"""
        query = "Vox AC30 crunch tone with overdrive"
        result = generator.generate_tone_from_query(query)
        
        # Load expected golden preset
        golden_file = TEST_DATA_DIR / "vox_ac30_crunch.json"
        if golden_file.exists():
            with open(golden_file, 'r') as f:
                expected = json.load(f)
            
            # Assert exact match
            assert result == expected, f"Generated tone doesn't match golden preset: {golden_file}"
        else:
            # Create golden preset if it doesn't exist
            TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(golden_file, 'w') as f:
                json.dump(result, f, indent=2)
            pytest.skip(f"Created golden preset: {golden_file}")
    
    def test_complex_multi_effect_tone(self, generator):
        """Test complex tone with multiple effects"""
        query = "Marshall Plexi with Tube Screamer, delay, and reverb for classic rock"
        result = generator.generate_tone_from_query(query)
        
        # Load expected golden preset
        golden_file = TEST_DATA_DIR / "marshall_plexi_complex.json"
        if golden_file.exists():
            with open(golden_file, 'r') as f:
                expected = json.load(f)
            
            # Assert exact match
            assert result == expected, f"Generated tone doesn't match golden preset: {golden_file}"
        else:
            # Create golden preset if it doesn't exist
            TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(golden_file, 'w') as f:
                json.dump(result, f, indent=2)
            pytest.skip(f"Created golden preset: {golden_file}")
    
    def test_golden_preset_structure_validation(self, generator):
        """Test that golden presets have correct structure"""
        query = "Test tone for structure validation"
        result = generator.generate_tone_from_query(query)
        
        # Validate required structure
        assert "query" in result, "Tone must have query"
        assert "description" in result, "Tone must have description"
        assert "tone_patch" in result, "Tone must have tone_patch"
        assert "gear_used" in result, "Tone must have gear_used"
        assert isinstance(result["tone_patch"], dict), "Tone patch must be a dict"
        
        # Validate tone_patch has required blocks
        tone_patch = result["tone_patch"]
        assert "amp" in tone_patch, "Tone patch must have amp"
        assert "cab" in tone_patch, "Tone patch must have cab"
        
        # Validate each block has required fields
        for block_name, block in tone_patch.items():
            assert "type" in block, f"Block {block_name} must have type"
            assert "parameters" in block, f"Block {block_name} must have parameters"
            assert isinstance(block["parameters"], dict), f"Block {block_name} parameters must be a dict"
    
    def test_golden_preset_parameter_ranges(self, generator):
        """Test that golden preset parameters are within valid ranges"""
        query = "Test tone for parameter range validation"
        result = generator.generate_tone_from_query(query)
        
        # Load FM9 reference for validation
        ref_file = Path(__file__).parent.parent / "data" / "fm9_comprehensive_reference.json"
        if ref_file.exists():
            with open(ref_file, 'r') as f:
                fm9_ref = json.load(f)
            
            # Validate parameter ranges for each block
            tone_patch = result["tone_patch"]
            for block_name, block in tone_patch.items():
                block_type = block_name.lower()
                if f"{block_type}_block" in fm9_ref:
                    block_ref = fm9_ref[f"{block_type}_block"]
                    if "key_parameters" in block_ref:
                        for param_name, param_value in block["parameters"].items():
                            if param_name in block_ref["key_parameters"]:
                                param_spec = block_ref["key_parameters"][param_name]
                                if "min" in param_spec and "max" in param_spec:
                                    assert param_spec["min"] <= param_value <= param_spec["max"], \
                                        f"Parameter {param_name} value {param_value} out of range [{param_spec['min']}, {param_spec['max']}]"
