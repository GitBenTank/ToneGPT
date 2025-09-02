import json
import re
from pathlib import Path
from typing import Dict, List, Optional
import PyPDF2
import fitz  # PyMuPDF


class FM9GuideParser:
    """
    Parse FM9 Owner's Manual, Blocks Guide, and Footswitch Guide PDFs
    Extract actual parameter ranges, block definitions, and hardware specs
    """

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.manual_path = self.base_dir / "FM9-Owners-Manual (1).pdf"
        self.blocks_guide_path = self.base_dir / "Fractal-Audio-Blocks-Guide (3).pdf"
        self.footswitch_guide_path = (
            self.base_dir / "Fractal-Audio-Footswitch-Functions-Guide (1).pdf"
        )

        self.manual_data = {}
        self.blocks_data = {}
        self.footswitch_data = {}

    def parse_all_guides(self) -> Dict:
        """Parse all three guides and return combined data"""
        print("🔍 Parsing FM9 Owner's Manual...")
        self.manual_data = self._parse_manual()

        print("🔍 Parsing Blocks Guide...")
        self.blocks_data = self._parse_blocks_guide()

        print("🔍 Parsing Footswitch Guide...")
        self.footswitch_data = self._parse_footswitch_guide()

        return {
            "manual": self.manual_data,
            "blocks": self.blocks_data,
            "footswitch": self.footswitch_data,
            "parsed_at": str(Path.cwd()),
            "guide_files": {
                "manual": str(self.manual_path),
                "blocks": str(self.blocks_guide_path),
                "footswitch": str(self.footswitch_guide_path),
            },
        }

    def _parse_manual(self) -> Dict:
        """Parse FM9 Owner's Manual for hardware specs and basic parameters"""
        if not self.manual_path.exists():
            print(f"❌ Manual not found: {self.manual_path}")
            return {}

        try:
            # Try PyMuPDF first (better text extraction)
            doc = fitz.open(self.manual_path)
            text = ""
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
            doc.close()

            # Extract hardware specifications
            hardware_specs = self._extract_hardware_specs(text)

            # Extract parameter ranges
            parameter_ranges = self._extract_parameter_ranges(text)

            # Extract block information
            block_info = self._extract_block_info(text)

            return {
                "hardware_specs": hardware_specs,
                "parameter_ranges": parameter_ranges,
                "block_info": block_info,
                "total_pages": doc.page_count,
                "extracted_text_length": len(text),
            }

        except Exception as e:
            print(f"❌ Error parsing manual: {e}")
            return {}

    def _parse_blocks_guide(self) -> Dict:
        """Parse Blocks Guide for detailed block definitions and parameters"""
        if not self.blocks_guide_path.exists():
            print(f"❌ Blocks guide not found: {self.blocks_guide_path}")
            return {}

        try:
            doc = fitz.open(self.blocks_guide_path)
            text = ""
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
            doc.close()

            # Extract block definitions
            block_definitions = self._extract_block_definitions(text)

            # Extract parameter details
            parameter_details = self._extract_parameter_details(text)

            return {
                "block_definitions": block_definitions,
                "parameter_details": parameter_details,
                "total_pages": doc.page_count,
                "extracted_text_length": len(text),
            }

        except Exception as e:
            print(f"❌ Error parsing blocks guide: {e}")
            return {}

    def _parse_footswitch_guide(self) -> Dict:
        """Parse Footswitch Guide for control functions and assignments"""
        if not self.footswitch_guide_path.exists():
            print(f"❌ Footswitch guide not found: {self.footswitch_guide_path}")
            return {}

        try:
            doc = fitz.open(self.footswitch_guide_path)
            text = ""
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
            doc.close()

            # Extract footswitch functions
            footswitch_functions = self._extract_footswitch_functions(text)

            # Extract control assignments
            control_assignments = self._extract_control_assignments(text)

            return {
                "footswitch_functions": footswitch_functions,
                "control_assignments": control_assignments,
                "total_pages": doc.page_count,
                "extracted_text_length": len(text),
            }

        except Exception as e:
            print(f"❌ Error parsing footswitch guide: {e}")
            return {}

    def _extract_hardware_specs(self, text: str) -> Dict:
        """Extract hardware specifications from manual text"""
        specs = {}

        # Look for common hardware spec patterns
        patterns = {
            "max_blocks": r"(\d+)\s*blocks?",
            "scenes": r"(\d+)\s*scenes?",
            "channels": r"(\d+)\s*channels?",
            "grid_size": r"(\d+x\d+)\s*grid",
            "audio_quality": r"(\d+)-bit/(\d+)kHz",
            "footswitches": r"(\d+)\s*footswitches?",
            "expression_pedals": r"(\d+)\s*expression\s+pedals?",
            "midi_ports": r"(\d+)\s*MIDI\s+ports?",
            "usb_ports": r"(\d+)\s*USB\s+ports?",
        }

        for key, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                if key == "audio_quality":
                    specs[key] = f"{matches[0][0]}-bit/{matches[0][1]}kHz"
                else:
                    specs[key] = (
                        matches[0] if isinstance(matches[0], str) else matches[0][0]
                    )

        return specs

    def _extract_parameter_ranges(self, text: str) -> Dict:
        """Extract parameter ranges from manual text"""
        ranges = {}

        # Look for parameter range patterns
        patterns = {
            "gain": r"gain.*?(\d+\.?\d*)\s*to\s*(\d+\.?\d*)",
            "bass": r"bass.*?(\d+\.?\d*)\s*to\s*(\d+\.?\d*)",
            "mid": r"mid.*?(\d+\.?\d*)\s*to\s*(\d+\.?\d*)",
            "treble": r"treble.*?(\d+\.?\d*)\s*to\s*(\d+\.?\d*)",
            "presence": r"presence.*?(\d+\.?\d*)\s*to\s*(\d+\.?\d*)",
            "master": r"master.*?(\d+\.?\d*)\s*to\s*(\d+\.?\d*)",
            "level": r"level.*?(\d+\.?\d*)\s*to\s*(\d+\.?\d*)",
            "time": r"time.*?(\d+\.?\d*)\s*to\s*(\d+\.?\d*)",
            "mix": r"mix.*?(\d+\.?\d*)\s*to\s*(\d+\.?\d*)",
            "feedback": r"feedback.*?(\d+\.?\d*)\s*to\s*(\d+\.?\d*)",
        }

        for param, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                ranges[param] = {
                    "min": float(matches[0][0]),
                    "max": float(matches[0][1]),
                }

        return ranges

    def _extract_block_info(self, text: str) -> Dict:
        """Extract block information from manual text"""
        blocks = {}

        # Look for block type patterns
        block_patterns = [
            r"amplifier\s+blocks?",
            r"cabinet\s+blocks?",
            r"drive\s+blocks?",
            r"delay\s+blocks?",
            r"reverb\s+blocks?",
            r"eq\s+blocks?",
            r"filter\s+blocks?",
            r"modulation\s+blocks?",
            r"pitch\s+blocks?",
            r"synth\s+blocks?",
            r"utility\s+blocks?",
        ]

        for pattern in block_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                block_type = matches[0].lower().replace(" ", "_")
                blocks[block_type] = {"name": matches[0], "mentioned": True}

        return blocks

    def _extract_block_definitions(self, text: str) -> Dict:
        """Extract detailed block definitions from blocks guide"""
        definitions = {}

        # Look for specific block definitions
        # This would need to be more sophisticated for real extraction
        # For now, return basic structure
        return {
            "extraction_method": "text_pattern_matching",
            "note": "This is a basic implementation - would need more sophisticated parsing for full extraction",
        }

    def _extract_parameter_details(self, text: str) -> Dict:
        """Extract detailed parameter information from blocks guide"""
        details = {}

        # Look for parameter detail patterns
        return {
            "extraction_method": "text_pattern_matching",
            "note": "This is a basic implementation - would need more sophisticated parsing for full extraction",
        }

    def _extract_footswitch_functions(self, text: str) -> List[str]:
        """Extract footswitch functions from footswitch guide"""
        functions = []

        # Look for footswitch function patterns
        patterns = [
            r"scene\s+switching",
            r"block\s+bypass",
            r"channel\s+switching",
            r"parameter\s+control",
            r"looper\s+control",
            r"tap\s+tempo",
            r"tuner\s+access",
            r"preset\s+change",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                functions.extend(matches)

        return list(set(functions))  # Remove duplicates

    def _extract_control_assignments(self, text: str) -> Dict:
        """Extract control assignments from footswitch guide"""
        assignments = {}

        # Look for control assignment patterns
        return {
            "extraction_method": "text_pattern_matching",
            "note": "This is a basic implementation - would need more sophisticated parsing for full extraction",
        }

    def save_parsed_data(self, output_file: str = "parsed_guide_data.json"):
        """Save parsed guide data to JSON file"""
        data = self.parse_all_guides()

        output_path = self.base_dir / output_file
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Parsed guide data saved to: {output_path}")
        return output_path


def main():
    """Test the guide parser"""
    parser = FM9GuideParser()

    print("🚀 Starting FM9 Guide Parsing...")
    data = parser.parse_all_guides()

    print(f"\n📊 Parsing Results:")
    print(f"Manual data: {len(data.get('manual', {}))} items")
    print(f"Blocks data: {len(data.get('blocks', {}))} items")
    print(f"Footswitch data: {len(data.get('footswitch', {}))} items")

    # Save the data
    output_file = parser.save_parsed_data()

    print(f"\n✅ Guide parsing complete! Data saved to: {output_file}")


if __name__ == "__main__":
    main()
