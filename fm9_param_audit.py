#!/usr/bin/env python3
"""
FM9 Parameter Audit Script

TL;DR: Audits FM9 parameters to ensure all are sourced from reference files.
- Validates parameter sourcing from data/fm9_config.json -> data/fm9_comprehensive_reference.json
- Checks for invented parameters or missing references
- Generates audit report for CI integration
- Blocks merges if unknown parameters remain

Constraints:
- FM9 single-mode only (docs/ground-truth.md#Invariants)
- Params from data/fm9_config.json -> fm9_comprehensive_reference.json
- No network calls (pure function)
- Raises ValueError if required param missing (cite file+key)
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Set, Any
from collections import defaultdict


class FM9ParameterAuditor:
    """Audits FM9 parameters for compliance with reference files"""
    
    def __init__(self, blocks_file: Path, config_file: Path, reference_file: Path):
        self.blocks_file = blocks_file
        self.config_file = config_file
        self.reference_file = reference_file
        self.audit_results = {
            "total_blocks": 0,
            "total_parameters": 0,
            "missing_parameters": [],
            "invented_parameters": [],
            "out_of_range_parameters": [],
            "missing_block_types": [],
            "errors": []
        }
    
    def load_data(self) -> Dict[str, Any]:
        """Load all required data files"""
        try:
            with open(self.blocks_file, 'r') as f:
                blocks_data = json.load(f)
            
            with open(self.config_file, 'r') as f:
                config_data = json.load(f)
            
            with open(self.reference_file, 'r') as f:
                reference_data = json.load(f)
            
            return {
                "blocks": blocks_data,
                "config": config_data,
                "reference": reference_data
            }
        except FileNotFoundError as e:
            self.audit_results["errors"].append(f"File not found: {e}")
            return {}
        except json.JSONDecodeError as e:
            self.audit_results["errors"].append(f"JSON decode error: {e}")
            return {}
    
    def audit_parameters(self, data: Dict[str, Any]) -> None:
        """Audit all parameters for compliance"""
        if not data:
            return
        
        blocks_data = data["blocks"]
        config_data = data["config"]
        reference_data = data["reference"]
        
        # Track all parameters found
        all_parameters = defaultdict(set)
        all_block_types = set()
        
        # Process each block
        for block in blocks_data:
            if not isinstance(block, dict):
                continue
            
            block_type = block.get("type", "").lower()
            all_block_types.add(block_type)
            
            # Get parameters for this block
            parameters = block.get("parameters", {})
            if isinstance(parameters, dict):
                for param_name in parameters.keys():
                    all_parameters[block_type].add(param_name)
        
        self.audit_results["total_blocks"] = len(blocks_data)
        self.audit_results["total_parameters"] = sum(len(params) for params in all_parameters.values())
        
        # Audit block types
        self._audit_block_types(all_block_types, config_data, reference_data)
        
        # Audit parameters
        self._audit_parameter_sourcing(all_parameters, reference_data)
        
        # Audit parameter ranges
        self._audit_parameter_ranges(blocks_data, reference_data)
    
    def _audit_block_types(self, block_types: Set[str], config_data: Dict, reference_data: Dict) -> None:
        """Audit that all block types exist in reference files"""
        for block_type in block_types:
            block_ref_key = f"{block_type}_block"
            config_key = block_type.upper()
            
            if block_ref_key not in reference_data and config_key not in config_data:
                self.audit_results["missing_block_types"].append({
                    "block_type": block_type,
                    "missing_from": "both reference and config files"
                })
    
    def _audit_parameter_sourcing(self, all_parameters: Dict[str, Set[str]], reference_data: Dict) -> None:
        """Audit that all parameters are sourced from reference files"""
        for block_type, parameters in all_parameters.items():
            block_ref_key = f"{block_type}_block"
            
            if block_ref_key not in reference_data:
                # Block type not in reference - all parameters are missing
                for param_name in parameters:
                    self.audit_results["missing_parameters"].append({
                        "block_type": block_type,
                        "parameter": param_name,
                        "missing_from": f"data/fm9_comprehensive_reference.json#{block_ref_key}"
                    })
                continue
            
            block_ref = reference_data[block_ref_key]
            if "key_parameters" not in block_ref:
                # No key_parameters section - all parameters are missing
                for param_name in parameters:
                    self.audit_results["missing_parameters"].append({
                        "block_type": block_type,
                        "parameter": param_name,
                        "missing_from": f"data/fm9_comprehensive_reference.json#{block_ref_key}.key_parameters"
                    })
                continue
            
            key_parameters = block_ref["key_parameters"]
            for param_name in parameters:
                if param_name not in key_parameters:
                    self.audit_results["missing_parameters"].append({
                        "block_type": block_type,
                        "parameter": param_name,
                        "missing_from": f"data/fm9_comprehensive_reference.json#{block_ref_key}.key_parameters"
                    })
    
    def _audit_parameter_ranges(self, blocks_data: List[Dict], reference_data: Dict) -> None:
        """Audit that all parameter values are within valid ranges"""
        for block in blocks_data:
            if not isinstance(block, dict):
                continue
            
            block_type = block.get("type", "").lower()
            parameters = block.get("parameters", {})
            
            if not isinstance(parameters, dict):
                continue
            
            block_ref_key = f"{block_type}_block"
            if block_ref_key not in reference_data:
                continue
            
            block_ref = reference_data[block_ref_key]
            if "key_parameters" not in block_ref:
                continue
            
            key_parameters = block_ref["key_parameters"]
            for param_name, param_value in parameters.items():
                if param_name not in key_parameters:
                    continue
                
                param_spec = key_parameters[param_name]
                if "min" in param_spec and "max" in param_spec:
                    # Only validate numeric parameters
                    if isinstance(param_value, (int, float)):
                        if not (param_spec["min"] <= param_value <= param_spec["max"]):
                            self.audit_results["out_of_range_parameters"].append({
                                "block_type": block_type,
                                "parameter": param_name,
                                "value": param_value,
                                "min": param_spec["min"],
                                "max": param_spec["max"],
                                "block_name": block.get("name", "unknown")
                            })
    
    def generate_report(self, output_file: Path = None) -> str:
        """Generate audit report"""
        report_lines = []
        report_lines.append("# FM9 Parameter Audit Report")
        report_lines.append("")
        
        # Summary
        report_lines.append("## Summary")
        report_lines.append(f"- Total blocks audited: {self.audit_results['total_blocks']}")
        report_lines.append(f"- Total parameters audited: {self.audit_results['total_parameters']}")
        report_lines.append(f"- Missing parameters: {len(self.audit_results['missing_parameters'])}")
        report_lines.append(f"- Out of range parameters: {len(self.audit_results['out_of_range_parameters'])}")
        report_lines.append(f"- Missing block types: {len(self.audit_results['missing_block_types'])}")
        report_lines.append(f"- Errors: {len(self.audit_results['errors'])}")
        report_lines.append("")
        
        # Errors
        if self.audit_results["errors"]:
            report_lines.append("## Errors")
            for error in self.audit_results["errors"]:
                report_lines.append(f"- {error}")
            report_lines.append("")
        
        # Missing block types
        if self.audit_results["missing_block_types"]:
            report_lines.append("## Missing Block Types")
            for missing in self.audit_results["missing_block_types"]:
                report_lines.append(f"- {missing['block_type']}: {missing['missing_from']}")
            report_lines.append("")
        
        # Missing parameters
        if self.audit_results["missing_parameters"]:
            report_lines.append("## Missing Parameters")
            for missing in self.audit_results["missing_parameters"]:
                report_lines.append(f"- {missing['block_type']}.{missing['parameter']}: {missing['missing_from']}")
            report_lines.append("")
        
        # Out of range parameters
        if self.audit_results["out_of_range_parameters"]:
            report_lines.append("## Out of Range Parameters")
            for out_of_range in self.audit_results["out_of_range_parameters"]:
                report_lines.append(f"- {out_of_range['block_type']}.{out_of_range['parameter']}: "
                                  f"value {out_of_range['value']} not in range "
                                  f"[{out_of_range['min']}, {out_of_range['max']}] "
                                  f"(block: {out_of_range['block_name']})")
            report_lines.append("")
        
        # Compliance status
        total_issues = (len(self.audit_results["missing_parameters"]) + 
                       len(self.audit_results["out_of_range_parameters"]) + 
                       len(self.audit_results["missing_block_types"]) + 
                       len(self.audit_results["errors"]))
        
        if total_issues == 0:
            report_lines.append("## ✅ Compliance Status: PASSED")
            report_lines.append("All parameters are properly sourced from FM9 reference files.")
        else:
            report_lines.append("## ❌ Compliance Status: FAILED")
            report_lines.append(f"Found {total_issues} compliance issues that must be resolved.")
        
        report = "\n".join(report_lines)
        
        if output_file:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w') as f:
                f.write(report)
        
        return report
    
    def run_audit(self) -> int:
        """Run complete audit and return exit code"""
        data = self.load_data()
        if not data:
            return 1
        
        self.audit_parameters(data)
        
        # Generate report
        report = self.generate_report()
        print(report)
        
        # Return exit code based on compliance
        total_issues = (len(self.audit_results["missing_parameters"]) + 
                       len(self.audit_results["out_of_range_parameters"]) + 
                       len(self.audit_results["missing_block_types"]) + 
                       len(self.audit_results["errors"]))
        
        return 0 if total_issues == 0 else 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="FM9 Parameter Audit Script")
    parser.add_argument("--blocks", required=True, help="Path to blocks JSON file")
    parser.add_argument("--cfg", required=True, help="Path to FM9 config JSON file")
    parser.add_argument("--ref", required=True, help="Path to FM9 comprehensive reference JSON file")
    parser.add_argument("--out", help="Path to output report file")
    
    args = parser.parse_args()
    
    blocks_file = Path(args.blocks)
    config_file = Path(args.cfg)
    reference_file = Path(args.ref)
    output_file = Path(args.out) if args.out else None
    
    auditor = FM9ParameterAuditor(blocks_file, config_file, reference_file)
    exit_code = auditor.run_audit()
    
    if output_file:
        auditor.generate_report(output_file)
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
