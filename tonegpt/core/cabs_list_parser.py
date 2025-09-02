import json
import re
from pathlib import Path
from typing import Dict, List, Optional

class CabsListParser:
    """
    Parser for the comprehensive FM9 cabinet list from Fractal Audio wiki
    """
    
    def __init__(self, cabs_file_path: str):
        self.cabs_file_path = Path(cabs_file_path)
        self.cabs_data = []
        self.categories = {}
    
    def parse_cabs_list(self) -> List[Dict]:
        """Parse the comprehensive cabinet list"""
        print("🎸 Parsing comprehensive FM9 cabinet list...")
        
        try:
            with open(self.cabs_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"❌ Cabinet list file not found: {self.cabs_file_path}")
            return []
        
        # Split content into sections
        sections = content.split('==')
        
        for section in sections:
            if 'Factory Bank' in section or 'Legacy' in section:
                self._parse_section(section)
        
        print(f"✅ Parsed {len(self.cabs_data)} cabinet models")
        return self.cabs_data
    
    def _parse_section(self, section: str):
        """Parse a section of the cabinet list"""
        lines = section.split('\n')
        current_category = None
        current_description = None
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and headers
            if not line or line.startswith('=') or line.startswith('TOC'):
                continue
            
            # Look for category descriptions (in bold)
            if line.startswith("'''") and line.endswith("'''"):
                current_category = line.replace("'''", "").strip()
                continue
            
            # Look for cabinet entries (format: number — name — creator)
            if '—' in line and not line.startswith("'''"):
                self._parse_cabinet_entry(line, current_category, current_description)
            
            # Look for descriptions
            if line.startswith("'''") and not line.endswith("'''"):
                current_description = line.replace("'''", "").strip()
    
    def _parse_cabinet_entry(self, line: str, category: str, description: str):
        """Parse a single cabinet entry"""
        # Clean up the line
        line = re.sub(r'<BR>', '', line)
        line = re.sub(r'<.*?>', '', line)  # Remove HTML tags
        
        # Split by — and clean up
        parts = [part.strip() for part in line.split('—')]
        
        if len(parts) >= 2:
            number = parts[0].strip()
            name = parts[1].strip()
            creator = parts[2].strip() if len(parts) > 2 else "FAS"
            
            # Skip if it's not a valid cabinet entry
            if not number.isdigit() or not name:
                return
            
            # Extract cabinet information
            cab_info = self._extract_cabinet_info(name, creator, category, description)
            
            if cab_info:
                self.cabs_data.append(cab_info)
                
                # Categorize
                brand = cab_info.get('brand', 'other')
                if brand not in self.categories:
                    self.categories[brand] = []
                self.categories[brand].append(cab_info)
    
    def _extract_cabinet_info(self, name: str, creator: str, category: str, description: str) -> Optional[Dict]:
        """Extract detailed information from cabinet name"""
        # Clean up the name
        name = re.sub(r'<.*?>', '', name).strip()
        
        # Extract speaker configuration
        speaker_config = self._extract_speaker_config(name)
        
        # Extract brand
        brand = self._extract_brand(name)
        
        # Extract speaker type
        speaker_type = self._extract_speaker_type(name)
        
        # Extract microphone
        microphone = self._extract_microphone(name)
        
        return {
            "name": name,
            "number": len(self.cabs_data) + 1,
            "creator": creator,
            "category": category or "Factory",
            "description": description or "",
            "speaker_config": speaker_config,
            "brand": brand,
            "speaker_type": speaker_type,
            "microphone": microphone,
            "real_world": self._get_real_world_name(name, brand, speaker_config),
            "parameters": {
                "low_cut": {"min": 20.0, "max": 500.0, "default": 80.0},
                "high_cut": {"min": 2000.0, "max": 20000.0, "default": 8000.0},
                "level": {"min": 0.0, "max": 10.0, "default": 5.0},
                "air": {"min": 0.0, "max": 10.0, "default": 5.0},
                "proximity": {"min": 0.0, "max": 10.0, "default": 5.0}
            },
            "fm9_verified": True,
            "source": "FM9 Factory Cabs"
        }
    
    def _extract_speaker_config(self, name: str) -> str:
        """Extract speaker configuration from name"""
        # Look for patterns like 1x12, 2x12, 4x12, etc.
        config_match = re.search(r'(\d+x\d+)', name)
        if config_match:
            return config_match.group(1)
        
        # Look for single speaker indicators
        if '1x' in name.lower():
            return "1x12"
        elif '2x' in name.lower():
            return "2x12"
        elif '4x' in name.lower():
            return "4x12"
        
        return "Unknown"
    
    def _extract_brand(self, name: str) -> str:
        """Extract brand from cabinet name"""
        name_lower = name.lower()
        
        # Common cabinet brands
        brands = {
            'marshall': ['marshall', 'brit', 'jcm', 'jmp', '1960', '1960a', '1960b'],
            'fender': ['fender', 'twin', 'deluxe', 'bassman', 'super', 'concert', 'bandmaster', 'showman'],
            'mesa': ['mesa', 'boogie', 'recto', 'mark', 'lone', 'stiletto', 'roadster'],
            'orange': ['orange', 'or', 'ppc', 'crush'],
            'vox': ['vox', 'ac', 'ac30', 'ac15', 'ac10'],
            'peavey': ['peavey', '5150', '6505'],
            'engl': ['engl', 'powerball', 'savage'],
            'bogner': ['bogner', 'uberschall', 'ecstasy'],
            'diezel': ['diezel', 'herbert', 'vht'],
            'soldano': ['soldano', 'slo'],
            'hughes': ['hughes', 'kettner', 'tubemeister'],
            'evh': ['evh', '5150'],
            'laney': ['laney', 'ironheart'],
            'hiwatt': ['hiwatt', 'dr103'],
            'ampeg': ['ampeg', 'svt'],
            'gibson': ['gibson', 'ga'],
            'supro': ['supro', 'tremolux'],
            'silvertone': ['silvertone', '1484'],
            'danelectro': ['danelectro', 'dan-o'],
            'pignose': ['pignose', 'pig']
        }
        
        for brand, keywords in brands.items():
            if any(keyword in name_lower for keyword in keywords):
                return brand
        
        return 'other'
    
    def _extract_speaker_type(self, name: str) -> str:
        """Extract speaker type from name"""
        name_lower = name.lower()
        
        speaker_types = {
            'v30': ['v30', 'celestion v30'],
            'greenback': ['greenback', 'g12m'],
            'creamback': ['creamback', 'g12h'],
            'alnico': ['alnico', 'alnico blue'],
            'jensen': ['jensen', 'c12n'],
            'eminence': ['eminence'],
            'weber': ['weber'],
            'wgs': ['wgs'],
            'scumback': ['scumback'],
            'heritage': ['heritage'],
            'g12t': ['g12t'],
            'g12h': ['g12h'],
            'g12m': ['g12m'],
            'c12n': ['c12n'],
            'c12k': ['c12k']
        }
        
        for speaker_type, keywords in speaker_types.items():
            if any(keyword in name_lower for keyword in keywords):
                return speaker_type
        
        return 'unknown'
    
    def _extract_microphone(self, name: str) -> str:
        """Extract microphone type from name"""
        name_lower = name.lower()
        
        mics = {
            'sm57': ['57', 'sm57'],
            'sm58': ['58', 'sm58'],
            'md421': ['421', 'md421'],
            'md441': ['441', 'md421'],
            'u87': ['87', 'u87'],
            'u47': ['47', 'u47'],
            'c414': ['414', 'c414'],
            'ribbon': ['121', '160', '170', 'ribbon'],
            'condenser': ['906', 'a51', 'condenser']
        }
        
        for mic, keywords in mics.items():
            if any(keyword in name_lower for keyword in keywords):
                return mic
        
        return 'unknown'
    
    def _get_real_world_name(self, name: str, brand: str, config: str) -> str:
        """Generate a real-world cabinet name"""
        if brand == 'marshall':
            if '4x12' in config:
                return f"Marshall 4x12 {config} Cabinet"
            elif '2x12' in config:
                return f"Marshall 2x12 {config} Cabinet"
            else:
                return f"Marshall {config} Cabinet"
        elif brand == 'fender':
            if '4x12' in config:
                return f"Fender 4x12 {config} Cabinet"
            elif '2x12' in config:
                return f"Fender 2x12 {config} Cabinet"
            else:
                return f"Fender {config} Cabinet"
        elif brand == 'mesa':
            return f"Mesa Boogie {config} Cabinet"
        elif brand == 'orange':
            return f"Orange {config} Cabinet"
        elif brand == 'vox':
            return f"Vox {config} Cabinet"
        else:
            return f"{brand.title()} {config} Cabinet"
    
    def save_parsed_data(self, output_file: str = None):
        """Save parsed cabinet data to JSON file"""
        if output_file is None:
            output_file = Path(__file__).parent.parent.parent / "parsed_cabs_list.json"
        
        with open(output_file, 'w') as f:
            json.dump(self.cabs_data, f, indent=2)
        
        print(f"✅ Parsed cabinet data saved to: {output_file}")
        
        # Print summary
        print(f"\n📊 Parsing Results:")
        print(f"Total cabs parsed: {len(self.cabs_data)}")
        
        # Show categories
        print(f"\n📋 Categories:")
        for brand, cabs in self.categories.items():
            print(f"  {brand}: {len(cabs)} cabs")
        
        # Show first 5 cabs
        print(f"\n🎸 First 5 cabs:")
        for i, cab in enumerate(self.cabs_data[:5], 1):
            print(f"  {i}. {cab['name']} ({cab['brand']})")

def main():
    """Main function to parse cabinet list"""
    cabs_file = "/Users/bentankersley/Downloads/Cabs_List.txt"
    
    parser = CabsListParser(cabs_file)
    cabs_data = parser.parse_cabs_list()
    
    if cabs_data:
        parser.save_parsed_data()
    else:
        print("❌ No cabinet data parsed")

if __name__ == "__main__":
    main()
