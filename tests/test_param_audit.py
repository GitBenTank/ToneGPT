"""
Test FM9 Parameter Audit Script

TL;DR: Tests the parameter audit script functionality.
- Validates audit script can detect missing parameters
- Tests audit report generation
- Ensures CI integration works correctly
- Validates exit codes for pass/fail scenarios

Constraints:
- FM9 single-mode only (docs/ground-truth.md#Invariants)
- Params from data/fm9_config.json -> fm9_comprehensive_reference.json
- No network calls (pure function)
- Raises ValueError if required param missing (cite file+key)
"""

import json
import pytest
import tempfile
import subprocess
import sys
from pathlib import Path
from fm9_param_audit import FM9ParameterAuditor


class TestParameterAudit:
    """Test the FM9 parameter audit script"""
    
    def test_audit_script_imports(self):
        """Test that audit script can be imported"""
        from fm9_param_audit import FM9ParameterAuditor
        assert FM9ParameterAuditor is not None
    
    def test_audit_script_initialization(self):
        """Test audit script initialization"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create dummy files
            blocks_file = temp_path / "blocks.json"
            config_file = temp_path / "config.json"
            reference_file = temp_path / "reference.json"
            
            # Create minimal valid JSON files
            blocks_file.write_text('[]')
            config_file.write_text('{}')
            reference_file.write_text('{}')
            
            auditor = FM9ParameterAuditor(blocks_file, config_file, reference_file)
            assert auditor.blocks_file == blocks_file
            assert auditor.config_file == config_file
            assert auditor.reference_file == reference_file
    
    def test_audit_script_with_valid_data(self):
        """Test audit script with valid FM9 data"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test data files
            blocks_file = temp_path / "blocks.json"
            config_file = temp_path / "config.json"
            reference_file = temp_path / "reference.json"
            
            # Create valid blocks data
            blocks_data = [
                {
                    "type": "amp",
                    "name": "Test Amp",
                    "parameters": {
                        "gain": 5.0,
                        "bass": 3.0,
                        "mid": 4.0,
                        "treble": 6.0
                    }
                }
            ]
            
            # Create valid config data
            config_data = {
                "AMP": {
                    "gain": {"min": 0.0, "max": 10.0},
                    "bass": {"min": 0.0, "max": 10.0},
                    "mid": {"min": 0.0, "max": 10.0},
                    "treble": {"min": 0.0, "max": 10.0}
                }
            }
            
            # Create valid reference data
            reference_data = {
                "amp_block": {
                    "key_parameters": {
                        "gain": {"min": 0.0, "max": 10.0, "description": "Gain control"},
                        "bass": {"min": 0.0, "max": 10.0, "description": "Bass control"},
                        "mid": {"min": 0.0, "max": 10.0, "description": "Mid control"},
                        "treble": {"min": 0.0, "max": 10.0, "description": "Treble control"}
                    }
                }
            }
            
            # Write test data
            blocks_file.write_text(json.dumps(blocks_data))
            config_file.write_text(json.dumps(config_data))
            reference_file.write_text(json.dumps(reference_data))
            
            # Run audit
            auditor = FM9ParameterAuditor(blocks_file, config_file, reference_file)
            exit_code = auditor.run_audit()
            
            # Should pass (exit code 0)
            assert exit_code == 0
            assert len(auditor.audit_results["missing_parameters"]) == 0
            assert len(auditor.audit_results["out_of_range_parameters"]) == 0
            assert len(auditor.audit_results["missing_block_types"]) == 0
    
    def test_audit_script_with_missing_parameters(self):
        """Test audit script detects missing parameters"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test data files
            blocks_file = temp_path / "blocks.json"
            config_file = temp_path / "config.json"
            reference_file = temp_path / "reference.json"
            
            # Create blocks data with parameter not in reference
            blocks_data = [
                {
                    "type": "amp",
                    "name": "Test Amp",
                    "parameters": {
                        "gain": 5.0,
                        "unknown_param": 3.0  # This parameter is not in reference
                    }
                }
            ]
            
            # Create reference data without the unknown parameter
            reference_data = {
                "amp_block": {
                    "key_parameters": {
                        "gain": {"min": 0.0, "max": 10.0, "description": "Gain control"}
                        # unknown_param is missing
                    }
                }
            }
            
            # Write test data
            blocks_file.write_text(json.dumps(blocks_data))
            config_file.write_text(json.dumps({}))
            reference_file.write_text(json.dumps(reference_data))
            
            # Run audit
            auditor = FM9ParameterAuditor(blocks_file, config_file, reference_file)
            exit_code = auditor.run_audit()
            
            # Should fail (exit code 1)
            assert exit_code == 1
            assert len(auditor.audit_results["missing_parameters"]) > 0
            assert "unknown_param" in str(auditor.audit_results["missing_parameters"])
    
    def test_audit_script_with_out_of_range_parameters(self):
        """Test audit script detects out of range parameters"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test data files
            blocks_file = temp_path / "blocks.json"
            config_file = temp_path / "config.json"
            reference_file = temp_path / "reference.json"
            
            # Create blocks data with out of range parameter
            blocks_data = [
                {
                    "type": "amp",
                    "name": "Test Amp",
                    "parameters": {
                        "gain": 15.0  # This is out of range (max should be 10.0)
                    }
                }
            ]
            
            # Create reference data with valid range
            reference_data = {
                "amp_block": {
                    "key_parameters": {
                        "gain": {"min": 0.0, "max": 10.0, "description": "Gain control"}
                    }
                }
            }
            
            # Write test data
            blocks_file.write_text(json.dumps(blocks_data))
            config_file.write_text(json.dumps({}))
            reference_file.write_text(json.dumps(reference_data))
            
            # Run audit
            auditor = FM9ParameterAuditor(blocks_file, config_file, reference_file)
            exit_code = auditor.run_audit()
            
            # Should fail (exit code 1)
            assert exit_code == 1
            assert len(auditor.audit_results["out_of_range_parameters"]) > 0
            assert "gain" in str(auditor.audit_results["out_of_range_parameters"])
    
    def test_audit_script_report_generation(self):
        """Test audit script report generation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test data files
            blocks_file = temp_path / "blocks.json"
            config_file = temp_path / "config.json"
            reference_file = temp_path / "reference.json"
            output_file = temp_path / "report.md"
            
            # Create valid test data
            blocks_data = [{"type": "amp", "name": "Test", "parameters": {"gain": 5.0}}]
            config_data = {}
            reference_data = {
                "amp_block": {
                    "key_parameters": {
                        "gain": {"min": 0.0, "max": 10.0, "description": "Gain control"}
                    }
                }
            }
            
            # Write test data
            blocks_file.write_text(json.dumps(blocks_data))
            config_file.write_text(json.dumps(config_data))
            reference_file.write_text(json.dumps(reference_data))
            
            # Run audit
            auditor = FM9ParameterAuditor(blocks_file, config_file, reference_file)
            auditor.run_audit()
            
            # Generate report
            report = auditor.generate_report(output_file)
            
            # Check report content
            assert "FM9 Parameter Audit Report" in report
            assert "Summary" in report
            assert "Compliance Status" in report
            assert "PASSED" in report or "FAILED" in report
            
            # Check output file was created
            assert output_file.exists()
            assert "FM9 Parameter Audit Report" in output_file.read_text()
    
    def test_audit_script_command_line_interface(self):
        """Test audit script command line interface"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test data files
            blocks_file = temp_path / "blocks.json"
            config_file = temp_path / "config.json"
            reference_file = temp_path / "reference.json"
            output_file = temp_path / "report.md"
            
            # Create valid test data
            blocks_data = [{"type": "amp", "name": "Test", "parameters": {"gain": 5.0}}]
            config_data = {}
            reference_data = {
                "amp_block": {
                    "key_parameters": {
                        "gain": {"min": 0.0, "max": 10.0, "description": "Gain control"}
                    }
                }
            }
            
            # Write test data
            blocks_file.write_text(json.dumps(blocks_data))
            config_file.write_text(json.dumps(config_data))
            reference_file.write_text(json.dumps(reference_data))
            
            # Run audit script via command line
            cmd = [
                sys.executable, "fm9_param_audit.py",
                "--blocks", str(blocks_file),
                "--cfg", str(config_file),
                "--ref", str(reference_file),
                "--out", str(output_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Should succeed
            assert result.returncode == 0
            assert "FM9 Parameter Audit Report" in result.stdout
            assert output_file.exists()
    
    def test_audit_script_with_missing_files(self):
        """Test audit script handles missing files gracefully"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create non-existent files
            blocks_file = temp_path / "nonexistent_blocks.json"
            config_file = temp_path / "nonexistent_config.json"
            reference_file = temp_path / "nonexistent_reference.json"
            
            # Run audit
            auditor = FM9ParameterAuditor(blocks_file, config_file, reference_file)
            exit_code = auditor.run_audit()
            
            # Should fail (exit code 1)
            assert exit_code == 1
            assert len(auditor.audit_results["errors"]) > 0
            assert "File not found" in str(auditor.audit_results["errors"])
