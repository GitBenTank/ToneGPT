import json
import re
from pathlib import Path
from typing import Dict, List, Optional

class AmpsListParser:
    """
    Parse the comprehensive Fractal Audio AmpsList.txt file
    Extract detailed amplifier information for ToneGPT integration
    """
    
    def __init__(self, amps_file_path: str):
        self.amps_file_path = Path(amps_file_path)
        self.parsed_amps = []
    
    def parse_amps_list(self) -> List[Dict]:
        """Parse the amps list file and extract structured data"""
        if not self.amps_file_path.exists():
            print(f"❌ Amps list file not found: {self.amps_file_path}")
            return []
        
        print(f"🔍 Parsing amps list from: {self.amps_file_path}")
        
        with open(self.amps_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split content by amp sections (== AMP NAME ==)
        amp_sections = re.split(r'^==(.+?)==$', content, flags=re.MULTILINE)
        
        # Process each amp section
        for i in range(1, len(amp_sections), 2):
            if i + 1 < len(amp_sections):
                amp_name = amp_sections[i].strip()
                amp_content = amp_sections[i + 1].strip()
                
                if amp_name and amp_content:
                    amp_data = self._parse_amp_section(amp_name, amp_content)
                    if amp_data:
                        self.parsed_amps.append(amp_data)
        
        print(f"✅ Parsed {len(self.parsed_amps)} amplifier models")
        return self.parsed_amps
    
    def _parse_amp_section(self, amp_name: str, content: str) -> Optional[Dict]:
        """Parse individual amp section"""
        try:
            # Extract basic information
            amp_data = {
                "name": amp_name,
                "original_name": amp_name,
                "category": self._determine_category(amp_name),
                "brand": self._extract_brand(amp_name),
                "model": self._extract_model(amp_name),
                "description": self._extract_description(content),
                "channels": self._extract_channels(content),
                "power_tubes": self._extract_power_tubes(content),
                "cabinet": self._extract_cabinet(content),
                "controls": self._extract_controls(content),
                "characteristics": self._extract_characteristics(content),
                "source": "Fractal Audio AmpsList.txt",
                "verified": True
            }
            
            return amp_data
            
        except Exception as e:
            print(f"❌ Error parsing amp '{amp_name}': {e}")
            return None
    
    def _determine_category(self, amp_name: str) -> str:
        """Determine amp category based on name"""
        amp_lower = amp_name.lower()
        
        if any(word in amp_lower for word in ["fender", "tweed", "bassman", "twin", "deluxe", "champ"]):
            return "fender"
        elif any(word in amp_lower for word in ["marshall", "jcm", "plexi", "jtm", "jvm", "brit"]):
            return "marshall"
        elif any(word in amp_lower for word in ["mesa", "boogie", "mark", "rectifier", "dual", "triple"]):
            return "mesa_boogie"
        elif any(word in amp_lower for word in ["vox", "ac", "top boost"]):
            return "vox"
        elif any(word in amp_lower for word in ["orange", "or"]):
            return "orange"
        elif any(word in amp_lower for word in ["peavey", "5150", "6505"]):
            return "peavey"
        elif any(word in amp_lower for word in ["engl", "powerball", "savage"]):
            return "engl"
        elif any(word in amp_lower for word in ["diezel", "herbert", "vht"]):
            return "diezel"
        elif any(word in amp_lower for word in ["bogner", "ecstasy", "uberschall"]):
            return "bogner"
        elif any(word in amp_lower for word in ["soldano", "slo"]):
            return "soldano"
        else:
            return "other"
    
    def _extract_brand(self, amp_name: str) -> str:
        """Extract brand from amp name"""
        amp_lower = amp_name.lower()
        
        if "fender" in amp_lower:
            return "Fender"
        elif "marshall" in amp_lower or "brit" in amp_lower:
            return "Marshall"
        elif "mesa" in amp_lower or "boogie" in amp_lower:
            return "Mesa Boogie"
        elif "vox" in amp_lower:
            return "Vox"
        elif "orange" in amp_lower:
            return "Orange"
        elif "peavey" in amp_lower:
            return "Peavey"
        elif "engl" in amp_lower:
            return "Engl"
        elif "diezel" in amp_lower:
            return "Diezel"
        elif "bogner" in amp_lower:
            return "Bogner"
        elif "soldano" in amp_lower:
            return "Soldano"
        else:
            return "Other"
    
    def _extract_model(self, amp_name: str) -> str:
        """Extract model name from amp name"""
        # Remove category prefixes and clean up
        model = amp_name
        if "(" in model and ")" in model:
            # Extract the part in parentheses
            model = re.search(r'\(([^)]+)\)', model)
            if model:
                model = model.group(1)
        
        # Clean up common prefixes
        model = re.sub(r'^(Fender|Marshall|Mesa|Boogie|Vox|Orange|Peavey|Engl|Diezel|Bogner|Soldano)\s*', '', model, flags=re.IGNORECASE)
        
        return model.strip()
    
    def _extract_description(self, content: str) -> str:
        """Extract description from content"""
        # Look for quoted descriptions
        quotes = re.findall(r'"([^"]+)"', content)
        if quotes:
            return quotes[0]
        
        # Look for first meaningful sentence
        sentences = content.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and not sentence.startswith('Model:') and not sentence.startswith('Cab:'):
                return sentence
        
        return "Fractal Audio amplifier model"
    
    def _extract_channels(self, content: str) -> List[str]:
        """Extract channel information"""
        channels = []
        
        if "single channel" in content.lower():
            channels.append("Single")
        elif "dual channel" in content.lower():
            channels.append("Channel 1")
            channels.append("Channel 2")
        elif "three channel" in content.lower():
            channels.append("Channel 1")
            channels.append("Channel 2")
            channels.append("Channel 3")
        elif "four channel" in content.lower():
            channels.append("Channel 1")
            channels.append("Channel 2")
            channels.append("Channel 3")
            channels.append("Channel 4")
        else:
            # Default to single channel
            channels.append("Single")
        
        return channels
    
    def _extract_power_tubes(self, content: str) -> List[str]:
        """Extract power tube information"""
        tubes = []
        
        # Look for power tube patterns
        tube_patterns = [
            r'6V6', r'6L6', r'EL34', r'EL84', r'KT88', r'KT66', r'6550', r'5881'
        ]
        
        for pattern in tube_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                tubes.append(pattern)
        
        return tubes
    
    def _extract_cabinet(self, content: str) -> Dict:
        """Extract cabinet information"""
        cabinet = {
            "original": "",
            "dynacab": "",
            "speaker_size": "",
            "speaker_count": ""
        }
        
        # Look for cabinet information
        cab_match = re.search(r'Cab:\s*(.+)', content, re.IGNORECASE)
        if cab_match:
            cab_info = cab_match.group(1)
            
            # Extract speaker information
            speaker_match = re.search(r'(\d+x\d+)', cab_info)
            if speaker_match:
                cabinet["speaker_count"] = speaker_match.group(1)
            
            # Extract speaker size
            size_match = re.search(r'(\d+")', cab_info)
            if size_match:
                cabinet["speaker_size"] = size_match.group(1)
        
        return cabinet
    
    def _extract_controls(self, content: str) -> List[str]:
        """Extract control information"""
        controls = []
        
        # Look for control patterns
        control_patterns = [
            r'Volume', r'Gain', r'Bass', r'Mid', r'Treble', r'Presence', r'Master',
            r'Reverb', r'Tremolo', r'Vibrato', r'Bright', r'Normal', r'Jumped'
        ]
        
        for pattern in control_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                controls.append(pattern)
        
        return controls
    
    def _extract_characteristics(self, content: str) -> List[str]:
        """Extract tone characteristics"""
        characteristics = []
        
        # Look for characteristic keywords
        char_patterns = [
            r'clean', r'dirty', r'overdrive', r'distortion', r'high gain',
            r'vintage', r'modern', r'warm', r'bright', r'dark', r'punchy',
            r'smooth', r'aggressive', r'crunch', r'lead', r'rhythm'
        ]
        
        for pattern in char_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                characteristics.append(pattern)
        
        return characteristics
    
    def save_parsed_amps(self, output_file: str = "parsed_amps_list.json"):
        """Save parsed amps data to JSON file"""
        if not self.parsed_amps:
            self.parse_amps_list()
        
        output_path = Path(__file__).parent.parent.parent / output_file
        with open(output_path, 'w') as f:
            json.dump(self.parsed_amps, f, indent=2)
        
        print(f"✅ Parsed amps data saved to: {output_path}")
        return output_path
    
    def get_amps_by_category(self) -> Dict[str, List[Dict]]:
        """Organize amps by category"""
        if not self.parsed_amps:
            self.parse_amps_list()
        
        categorized = {}
        for amp in self.parsed_amps:
            category = amp.get('category', 'other')
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(amp)
        
        return categorized

def main():
    """Test the amps list parser"""
    amps_file = "/Users/bentankersley/Downloads/AmpsList.txt"
    parser = AmpsListParser(amps_file)
    
    print("🚀 Starting Amps List Parsing...")
    amps = parser.parse_amps_list()
    
    if amps:
        print(f"\n📊 Parsing Results:")
        print(f"Total amps parsed: {len(amps)}")
        
        # Show first few amps
        print(f"\n🎸 First 5 amps:")
        for i, amp in enumerate(amps[:5]):
            print(f"  {i+1}. {amp['name']} ({amp['brand']})")
        
        # Show categories
        categorized = parser.get_amps_by_category()
        print(f"\n📋 Categories:")
        for category, amp_list in categorized.items():
            print(f"  {category}: {len(amp_list)} amps")
        
        # Save the data
        output_file = parser.save_parsed_amps()
        print(f"\n✅ Amps parsing complete! Data saved to: {output_file}")
    else:
        print("❌ No amps were parsed")

if __name__ == "__main__":
    main()
