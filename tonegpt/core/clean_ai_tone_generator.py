"""
Clean AI Tone Generator for FM9 Partnership
Focuses on accurate real-world gear modeling without dual mode complexity
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Any
from tonegpt.config import BLOCKS_FILE


class CleanAIToneGenerator:
    """Clean AI tone generator focused on accurate FM9 modeling"""
    
    def __init__(self):
        self.blocks_data = self._load_blocks_data()
        self.amp_models = self._load_amp_models()
        self.cab_models = self._load_cab_models()
        self.drive_models = self._load_drive_models()
        self.effect_models = self._load_effect_models()
        
        # Real-world gear mapping for accurate modeling
        self.gear_mapping = self._load_gear_mapping()
    
    def _load_blocks_data(self) -> Dict:
        """Load comprehensive FM9 blocks data"""
        try:
            with open(BLOCKS_FILE, 'r') as f:
                data = json.load(f)
            print(f"🔧 Loaded {len(data)} FM9 blocks")
            return data
        except Exception as e:
            print(f"⚠️ Error loading blocks data: {e}")
            return {}
    
    def _load_amp_models(self) -> List[str]:
        """Load available amp models from real FM9 data"""
        amp_blocks = [block for block in self.blocks_data if block.get('category') == 'amp']
        if amp_blocks:
            amp_names = [block.get('name', '') for block in amp_blocks if block.get('name')]
            print(f"🔧 Loaded {len(amp_names)} real amp models from FM9 blocks data")
            return amp_names
        return []
    
    def _load_cab_models(self) -> List[str]:
        """Load available cab models from real FM9 data"""
        cab_blocks = [block for block in self.blocks_data if block.get('category') == 'cab']
        if cab_blocks:
            cab_names = [block.get('name', '') for block in cab_blocks if block.get('name')]
            print(f"🔧 Loaded {len(cab_names)} real cab models from FM9 blocks data")
            return cab_names
        return []
    
    def _load_drive_models(self) -> List[str]:
        """Load available drive models from real FM9 data"""
        drive_blocks = [block for block in self.blocks_data if block.get('category') == 'drive']
        if drive_blocks:
            drive_names = [block.get('name', '') for block in drive_blocks if block.get('name')]
            print(f"🔧 Loaded {len(drive_names)} real drive models from FM9 blocks data")
            return drive_names
        return []
    
    def _load_effect_models(self) -> Dict[str, List[str]]:
        """Load available effect models by category"""
        effects = {}
        effect_categories = ['delay', 'reverb', 'modulation', 'pitch', 'dynamics', 'eq', 'utility']
        
        for category in effect_categories:
            category_blocks = [block for block in self.blocks_data if block.get('category') == category]
            if category_blocks:
                effect_names = [block.get('name', '') for block in category_blocks if block.get('name')]
                effects[category] = effect_names
                print(f"🔧 Loaded {len(effect_names)} {category} effects from FM9 blocks data")
        
        return effects
    
    def _load_gear_mapping(self) -> Dict:
        """Load real-world gear mapping for accurate modeling"""
        return {
            "amps": {
                "marshall": {
                    "jcm800": ["Brit 800", "Brit 800 Pro", "BRIT 800 2204 HIGH", "BRIT 800 2203 HIGH"],
                    "jcm900": ["Brit 900", "Brit 900 Pro"],
                    "plexi": ["Brit Plexi", "Brit Plexi Pro", "Brit 800 #34"],
                    "jvm": ["Brit JVM", "Brit JVM Pro"]
                },
                "mesa": {
                    "dual_rectifier": ["Recto Pro", "RECTO1 ORANGE MODERN", "Recto1: original 2-channel Rectifier, Orange channel, Modern mode"],
                    "rectifier": ["Recto Pro", "RECTO1 ORANGE MODERN", "Recto1: original 2-channel Rectifier, Orange channel, Modern mode"],
                    "boogie": ["Recto Pro", "RECTO1 ORANGE MODERN", "Recto1: original 2-channel Rectifier, Orange channel, Modern mode"],
                    "mark_iic": ["Mesa Mark IIC+"],
                    "mark_iv": ["USA MK IV", "USA MK IV LEAD"],
                    "mark_v": ["USA MK V", "USA MK V LEAD"]
                },
                "fender": {
                    "tweed": ["5F1 TWEED", "5F1 TWEED EC", "5E3 TWEED", "5F8 TWEED"],
                    "deluxe": ["DELUXE VERB", "DELUXE VERB NORMAL", "DELUXE VERB VIBRATO"],
                    "twin": ["TWIN REVERB", "TWIN REVERB NORMAL", "TWIN REVERB VIBRATO"],
                    "bassman": ["BASSMAN", "BASSMAN 59", "BASSMAN 59 EC"]
                },
                "vox": {
                    "ac30": ["AC30", "AC30 TOP BOOST", "AC30 TOP BOOST EC"],
                    "ac15": ["AC15", "AC15 TOP BOOST", "AC15 TOP BOOST EC"]
                }
            },
            "drives": {
                "tube_screamer": ["TS808", "TS808 Mod", "TS9", "TS9 Mod"],
                "klon": ["Klon", "Klon Pro"],
                "rat": ["Rat Distortion", "Rat Distortion Pro"],
                "fuzz_face": ["Fuzz Face", "Fuzz Face Pro"],
                "big_muff": ["Big Muff", "Big Muff Pro"],
                "blues_driver": ["Blues Driver", "Blues Driver Pro"]
            },
            "cabs": {
                "marshall_4x12": ["Marshall 4x12", "Legacy 4x12 V30", "DynaCab 4x12 V30"],
                "mesa_4x12": ["Mesa Boogie", "Legacy 4x12 V30", "DynaCab 4x12 V30"],
                "fender_2x12": ["Fender 2x12", "Legacy 2x12 Greenback", "DynaCab 2x12 Greenback"],
                "vox_2x12": ["Vox 2x12", "Legacy 2x12 Greenback", "DynaCab 2x12 Greenback"]
            }
        }
    
    def generate_tone_from_query(self, query: str) -> Dict:
        """Generate a tone patch from a natural language query"""
        try:
            # Parse the query to understand intent
            intent = self._parse_query_intent(query)
            
            # Generate the tone structure
            tone_structure = self._generate_tone_structure(intent)
            tone_structure['query'] = query
            
            # Generate specific parameters
            tone_patch = self._generate_tone_patch(tone_structure)
            
            # Generate description
            description = self._generate_tone_description(tone_patch, intent)
            
            return {
                "query": query,
                "intent": intent,
                "tone_patch": tone_patch,
                "description": description,
                "gear_used": self._extract_gear_used(tone_patch)
            }
            
        except Exception as e:
            print(f"❌ Error generating tone: {e}")
            return self._get_fallback_tone(query)
    
    def _parse_query_intent(self, query: str) -> Dict:
        """Parse query to understand user intent"""
        query_lower = query.lower()
        
        # Genre detection
        genre = "rock"
        if any(word in query_lower for word in ["metal", "heavy", "distorted", "aggressive"]):
            genre = "metal"
        elif any(word in query_lower for word in ["blues", "bluesy", "soulful"]):
            genre = "blues"
        elif any(word in query_lower for word in ["jazz", "clean", "smooth"]):
            genre = "jazz"
        elif any(word in query_lower for word in ["funk", "rhythm", "groove"]):
            genre = "funk"
        elif any(word in query_lower for word in ["ambient", "atmospheric", "ethereal"]):
            genre = "ambient"
        
        # Characteristics
        characteristics = []
        if "lead" in query_lower:
            characteristics.append("lead")
        if "rhythm" in query_lower:
            characteristics.append("rhythm")
        if "clean" in query_lower:
            characteristics.append("clean")
        if "distorted" in query_lower or "dirty" in query_lower:
            characteristics.append("distorted")
        if "bright" in query_lower:
            characteristics.append("bright")
        if "warm" in query_lower:
            characteristics.append("warm")
        
        return {
            "genre": genre,
            "characteristics": characteristics,
            "query": query
        }
    
    def _generate_tone_structure(self, intent: Dict) -> Dict:
        """Generate the basic structure of the tone"""
        genre = intent.get("genre", "rock")
        
        # Determine which blocks to enable based on genre
        structure = {
            "genre": genre,
            "drive_1_enabled": genre in ["metal", "rock", "blues"],
            "drive_2_enabled": genre in ["metal", "rock"],
            "amp_enabled": True,
            "cab_enabled": True,
            "eq_enabled": True,
            "delay_enabled": genre in ["ambient", "rock", "metal"],
            "reverb_enabled": True,
            "modulation_enabled": genre in ["ambient", "funk", "jazz"],
            "pitch_enabled": genre in ["metal", "rock"],
            "dynamics_enabled": True,
            "utility_enabled": False
        }
        
        return structure
    
    def _generate_tone_patch(self, structure: Dict) -> Dict:
        """Generate the complete tone patch"""
        tone_patch = {}
        
        # Generate each block
        if structure.get("drive_1_enabled", False):
            tone_patch["drive_1"] = self._generate_drive_block(structure, 1)
        
        if structure.get("drive_2_enabled", False):
            tone_patch["drive_2"] = self._generate_drive_block(structure, 2)
        
        if structure.get("amp_enabled", True):
            tone_patch["amp"] = self._generate_amp_block(structure)
        
        if structure.get("cab_enabled", True):
            tone_patch["cab"] = self._generate_cab_block(structure)
        
        if structure.get("eq_enabled", True):
            tone_patch["eq"] = self._generate_eq_block(structure)
        
        if structure.get("delay_enabled", False):
            tone_patch["delay"] = self._generate_delay_block(structure)
        
        if structure.get("reverb_enabled", True):
            tone_patch["reverb"] = self._generate_reverb_block(structure)
        
        if structure.get("modulation_enabled", False):
            tone_patch["modulation"] = self._generate_modulation_block(structure)
        
        if structure.get("pitch_enabled", False):
            tone_patch["pitch"] = self._generate_pitch_block(structure)
        
        if structure.get("dynamics_enabled", True):
            tone_patch["dynamics"] = self._generate_dynamics_block(structure)
        
        if structure.get("utility_enabled", False):
            tone_patch["utility"] = self._generate_utility_block(structure)
        
        return tone_patch
    
    def _generate_amp_block(self, structure: Dict) -> Dict:
        """Generate an amp block with accurate FM9 modeling"""
        genre = structure.get('genre', 'rock')
        query = structure.get('query', '').lower()
        
        # Try to match specific amp requests using gear mapping
        selected_amp = None
        
        # Check for specific amp requests
        if 'marshall' in query or 'jcm' in query or '800' in query:
            marshall_amps = self.gear_mapping["amps"]["marshall"]["jcm800"]
            available_marshall = [amp for amp in marshall_amps if amp in self.amp_models]
            if available_marshall:
                selected_amp = random.choice(available_marshall)
        
        elif 'mesa' in query or 'boogie' in query or 'recto' in query or 'rectifier' in query:
            # Try different Mesa Boogie variations
            mesa_amps = []
            if 'rectifier' in query or 'recto' in query:
                mesa_amps.extend(self.gear_mapping["amps"]["mesa"]["rectifier"])
            if 'boogie' in query:
                mesa_amps.extend(self.gear_mapping["amps"]["mesa"]["boogie"])
            if 'dual' in query:
                mesa_amps.extend(self.gear_mapping["amps"]["mesa"]["dual_rectifier"])
            
            # Remove duplicates and check availability
            mesa_amps = list(set(mesa_amps))
            available_mesa = [amp for amp in mesa_amps if amp in self.amp_models]
            if available_mesa:
                selected_amp = random.choice(available_mesa)
        
        elif 'fender' in query or 'tweed' in query or 'deluxe' in query:
            fender_amps = self.gear_mapping["amps"]["fender"]["tweed"]
            available_fender = [amp for amp in fender_amps if amp in self.amp_models]
            if available_fender:
                selected_amp = random.choice(available_fender)
        
        # If no specific match, select based on genre
        if not selected_amp:
            if genre == 'metal':
                metal_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ['mesa', 'recto', '5150', 'mark', 'brit', '800'])]
                selected_amp = random.choice(metal_amps) if metal_amps else random.choice(self.amp_models)
            elif genre == 'blues':
                blues_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ['fender', 'tweed', 'deluxe', 'vox', 'ac30'])]
                selected_amp = random.choice(blues_amps) if blues_amps else random.choice(self.amp_models)
            elif genre == 'jazz':
                jazz_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ['fender', 'tweed', 'deluxe', 'clean'])]
                selected_amp = random.choice(jazz_amps) if jazz_amps else random.choice(self.amp_models)
            else:
                selected_amp = random.choice(self.amp_models)
        
        # Generate realistic parameters based on genre
        if genre == "metal":
            gain = random.uniform(7.5, 9.5)
            bass = random.uniform(6.0, 8.0)
            mid = random.uniform(3.0, 5.0)  # Scooped mids
            treble = random.uniform(6.0, 8.0)
            presence = random.uniform(6.0, 8.0)
            master = random.uniform(2.0, 6.0)
        elif genre == "blues":
            gain = random.uniform(4.0, 7.0)
            bass = random.uniform(5.0, 7.0)
            mid = random.uniform(6.0, 8.0)  # Boosted mids
            treble = random.uniform(5.0, 7.0)
            presence = random.uniform(3.0, 7.0)
            master = random.uniform(4.0, 8.0)
        elif genre == "jazz":
            gain = random.uniform(1.0, 3.5)
            bass = random.uniform(4.0, 7.0)
            mid = random.uniform(5.0, 8.0)
            treble = random.uniform(3.0, 6.0)
            presence = random.uniform(2.0, 6.0)
            master = random.uniform(7.0, 10.0)
        else:  # rock
            gain = random.uniform(5.0, 8.0)
            bass = random.uniform(5.0, 8.0)
            mid = random.uniform(5.0, 8.0)
            treble = random.uniform(5.0, 8.0)
            presence = random.uniform(4.0, 7.0)
            master = random.uniform(3.0, 7.0)
        
        return {
            "enabled": True,
            "type": selected_amp,
            "parameters": {
                "gain": round(gain, 1),
                "bass": round(bass, 1),
                "mid": round(mid, 1),
                "treble": round(treble, 1),
                "presence": round(presence, 1),
                "master": round(master, 1)
            }
        }
    
    def _generate_drive_block(self, structure: Dict, drive_num: int) -> Dict:
        """Generate a drive block with accurate FM9 modeling"""
        genre = structure.get('genre', 'rock')
        query = structure.get('query', '').lower()
        
        # Try to match specific drive requests
        selected_drive = None
        
        if 'tube screamer' in query or 'ts808' in query or 'ts9' in query:
            ts_drives = self.gear_mapping["drives"]["tube_screamer"]
            available_ts = [drive for drive in ts_drives if drive in self.drive_models]
            if available_ts:
                selected_drive = random.choice(available_ts)
        
        elif 'klon' in query:
            klon_drives = self.gear_mapping["drives"]["klon"]
            available_klon = [drive for drive in klon_drives if drive in self.drive_models]
            if available_klon:
                selected_drive = random.choice(available_klon)
        
        elif 'rat' in query:
            rat_drives = self.gear_mapping["drives"]["rat"]
            available_rat = [drive for drive in rat_drives if drive in self.drive_models]
            if available_rat:
                selected_drive = random.choice(available_rat)
        
        # If no specific match, select based on genre
        if not selected_drive:
            if genre == 'blues':
                blues_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ['ts', 'tube', 'screamer', 'klon'])]
                selected_drive = random.choice(blues_drives) if blues_drives else random.choice(self.drive_models)
            elif genre == 'metal':
                metal_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ['rat', 'distortion', 'fuzz', 'boost'])]
                selected_drive = random.choice(metal_drives) if metal_drives else random.choice(self.drive_models)
            else:
                selected_drive = random.choice(self.drive_models)
        
        # Generate realistic parameters
        if genre == "metal":
            drive = random.uniform(7.0, 10.0)
            tone = random.uniform(5.0, 8.0)
            level = random.uniform(3.0, 8.0)
        elif genre == "blues":
            drive = random.uniform(3.0, 7.0)
            tone = random.uniform(4.0, 7.0)
            level = random.uniform(4.0, 8.0)
        else:  # rock
            drive = random.uniform(4.0, 8.0)
            tone = random.uniform(4.0, 7.0)
            level = random.uniform(3.0, 7.0)
        
        return {
            "enabled": True,
            "type": selected_drive,
            "parameters": {
                "drive": round(drive, 1),
                "tone": round(tone, 1),
                "level": round(level, 1)
            }
        }
    
    def _generate_cab_block(self, structure: Dict) -> Dict:
        """Generate a cab block with accurate FM9 modeling"""
        genre = structure.get('genre', 'rock')
        query = structure.get('query', '').lower()
        
        # Try to match specific cab requests
        selected_cab = None
        
        if 'marshall' in query or '4x12' in query:
            marshall_cabs = self.gear_mapping["cabs"]["marshall_4x12"]
            available_marshall = [cab for cab in marshall_cabs if cab in self.cab_models]
            if available_marshall:
                selected_cab = random.choice(available_marshall)
        
        elif 'mesa' in query or 'boogie' in query:
            mesa_cabs = self.gear_mapping["cabs"]["mesa_4x12"]
            available_mesa = [cab for cab in mesa_cabs if cab in self.cab_models]
            if available_mesa:
                selected_cab = random.choice(available_mesa)
        
        # If no specific match, select based on genre
        if not selected_cab:
            if genre == 'metal':
                metal_cabs = [cab for cab in self.cab_models if any(word in cab.lower() for word in ['4x12', 'marshall', 'mesa', 'v30'])]
                selected_cab = random.choice(metal_cabs) if metal_cabs else random.choice(self.cab_models)
            elif genre == 'blues':
                blues_cabs = [cab for cab in self.cab_models if any(word in cab.lower() for word in ['2x12', 'fender', 'tweed', 'greenback'])]
                selected_cab = random.choice(blues_cabs) if blues_cabs else random.choice(self.cab_models)
            elif genre == 'jazz':
                jazz_cabs = [cab for cab in self.cab_models if any(word in cab.lower() for word in ['1x12', '2x12', 'fender', 'tweed'])]
                selected_cab = random.choice(jazz_cabs) if jazz_cabs else random.choice(self.cab_models)
            else:
                selected_cab = random.choice(self.cab_models)
        
        # Generate realistic parameters
        low_cut = random.uniform(60.0, 200.0)
        high_cut = random.uniform(8000.0, 15000.0)
        level = random.uniform(-3.0, 6.0)
        
        return {
            "enabled": True,
            "type": selected_cab,
            "parameters": {
                "low_cut": round(low_cut, 1),
                "high_cut": round(high_cut, 1),
                "level": round(level, 1)
            }
        }
    
    def _generate_eq_block(self, structure: Dict) -> Dict:
        """Generate an EQ block"""
        eq_models = self.effect_models.get('eq', [])
        selected_eq = random.choice(eq_models) if eq_models else "Parametric EQ"
        
        return {
            "enabled": True,
            "type": selected_eq,
            "parameters": {
                "low_freq": 80.0,
                "low_gain": 0.0,
                "low_mid_freq": 500.0,
                "low_mid_gain": 0.0,
                "high_mid_freq": 2000.0,
                "high_mid_gain": 0.0,
                "high_freq": 8000.0,
                "high_gain": 0.0
            }
        }
    
    def _generate_delay_block(self, structure: Dict) -> Dict:
        """Generate a delay block"""
        delay_models = self.effect_models.get('delay', [])
        selected_delay = random.choice(delay_models) if delay_models else "Digital Delay"
        
        return {
            "enabled": True,
            "type": selected_delay,
            "parameters": {
                "time": random.uniform(200.0, 800.0),
                "feedback": random.uniform(20.0, 40.0),
                "mix": random.uniform(15.0, 35.0)
            }
        }
    
    def _generate_reverb_block(self, structure: Dict) -> Dict:
        """Generate a reverb block"""
        reverb_models = self.effect_models.get('reverb', [])
        selected_reverb = random.choice(reverb_models) if reverb_models else "Room Reverb"
        
        return {
            "enabled": True,
            "type": selected_reverb,
            "parameters": {
                "room_size": random.uniform(50.0, 80.0),
                "decay": random.uniform(1.5, 3.0),
                "mix": random.uniform(20.0, 40.0)
            }
        }
    
    def _generate_modulation_block(self, structure: Dict) -> Dict:
        """Generate a modulation block"""
        modulation_models = self.effect_models.get('modulation', [])
        selected_mod = random.choice(modulation_models) if modulation_models else "Chorus"
        
        return {
            "enabled": True,
            "type": selected_mod,
            "parameters": {
                "rate": random.uniform(0.5, 2.0),
                "depth": random.uniform(30.0, 70.0),
                "mix": random.uniform(25.0, 50.0)
            }
        }
    
    def _generate_pitch_block(self, structure: Dict) -> Dict:
        """Generate a pitch block"""
        pitch_models = self.effect_models.get('pitch', [])
        selected_pitch = random.choice(pitch_models) if pitch_models else "Pitch Shifter"
        
        return {
            "enabled": True,
            "type": selected_pitch,
            "parameters": {
                "pitch": random.uniform(-12.0, 12.0),
                "mix": random.uniform(30.0, 70.0)
            }
        }
    
    def _generate_dynamics_block(self, structure: Dict) -> Dict:
        """Generate a dynamics block"""
        dynamics_models = self.effect_models.get('dynamics', [])
        selected_dynamics = random.choice(dynamics_models) if dynamics_models else "Compressor"
        
        return {
            "enabled": True,
            "type": selected_dynamics,
            "parameters": {
                "threshold": random.uniform(-20.0, -5.0),
                "ratio": random.uniform(2.0, 8.0),
                "attack": random.uniform(1.0, 10.0),
                "release": random.uniform(50.0, 200.0)
            }
        }
    
    def _generate_utility_block(self, structure: Dict) -> Dict:
        """Generate a utility block"""
        utility_models = self.effect_models.get('utility', [])
        selected_utility = random.choice(utility_models) if utility_models else "Volume"
        
        return {
            "enabled": True,
            "type": selected_utility,
            "parameters": {
                "volume": random.uniform(-6.0, 6.0)
            }
        }
    
    def _generate_tone_description(self, tone_patch: Dict, intent: Dict) -> str:
        """Generate a detailed description of the tone"""
        description_parts = []
        
        # Genre and style
        genre = intent.get('genre', 'rock')
        description_parts.append(f"A {genre} tone")
        
        # Add specific gear details
        gear_details = []
        
        # Amp details
        amp_data = tone_patch.get('amp', {})
        if amp_data.get('enabled', False):
            amp_type = amp_data.get('type', 'Unknown')
            if amp_type != 'None':
                gear_details.append(f"using {amp_type}")
        
        # Drive details
        drive_1 = tone_patch.get('drive_1', {})
        drive_2 = tone_patch.get('drive_2', {})
        drives_used = []
        if drive_1.get('enabled', False) and drive_1.get('type', 'None') != 'None':
            drives_used.append(drive_1.get('type', 'Unknown'))
        if drive_2.get('enabled', False) and drive_2.get('type', 'None') != 'None':
            drives_used.append(drive_2.get('type', 'Unknown'))
        
        if drives_used:
            if len(drives_used) == 1:
                gear_details.append(f"with {drives_used[0]}")
            else:
                gear_details.append(f"with {drives_used[0]} and {drives_used[1]}")
        
        # Effects details
        effects_used = []
        for effect_name in ['delay', 'reverb', 'modulation', 'pitch', 'dynamics']:
            effect_data = tone_patch.get(effect_name, {})
            if effect_data.get('enabled', False) and effect_data.get('type', 'None') != 'None':
                effects_used.append(effect_data.get('type', 'Unknown'))
        
        if effects_used:
            if len(effects_used) == 1:
                gear_details.append(f"and {effects_used[0]}")
            elif len(effects_used) == 2:
                gear_details.append(f"with {effects_used[0]} and {effects_used[1]}")
            else:
                gear_details.append(f"with {', '.join(effects_used[:-1])} and {effects_used[-1]}")
        
        # Combine all parts
        if gear_details:
            description_parts.append(" ".join(gear_details))
        
        # Characteristics
        if intent.get('characteristics'):
            characteristics = ", ".join(intent['characteristics'])
            description_parts.append(f"featuring {characteristics}")
        
        return ", ".join(description_parts) + "."
    
    def _extract_gear_used(self, tone_patch: Dict) -> Dict:
        """Extract the gear used in the tone patch"""
        gear_used = {}
        
        for block_name, block_data in tone_patch.items():
            if block_data.get('enabled', False) and block_data.get('type', 'None') != 'None':
                gear_used[block_name] = {
                    "type": block_data.get('type'),
                    "parameters": block_data.get('parameters', {})
                }
        
        return gear_used
    
    def _get_fallback_tone(self, query: str) -> Dict:
        """Get a fallback tone if generation fails"""
        return {
            "query": query,
            "intent": {"genre": "rock", "characteristics": []},
            "tone_patch": {
                "amp": {
                    "enabled": True,
                    "type": "Brit 800",
                    "parameters": {"gain": 6.0, "bass": 6.0, "mid": 6.0, "treble": 6.0, "presence": 6.0, "master": 5.0}
                },
                "cab": {
                    "enabled": True,
                    "type": "Legacy 4x12 V30",
                    "parameters": {"low_cut": 100.0, "high_cut": 10000.0, "level": 0.0}
                }
            },
            "description": "A rock tone using Brit 800 with Legacy 4x12 V30",
            "gear_used": {}
        }
    
    def _get_default_blocks(self) -> Dict:
        """Get default blocks data for fallback purposes"""
        return {
            "amp": {
                "parameters": {
                    "gain": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "bass": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "mid": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "treble": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "presence": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "master": {"min": 0.0, "max": 10.0, "default": 5.0}
                }
            },
            "cab": {
                "parameters": {
                    "low_cut": {"min": 20.0, "max": 500.0, "default": 100.0},
                    "high_cut": {"min": 2000.0, "max": 20000.0, "default": 10000.0},
                    "level": {"min": -20.0, "max": 20.0, "default": 0.0}
                }
            },
            "gain": {
                "types": ["FAS Boost", "TS808 Mod", "Klon", "Fuzz Face", "Rat Distortion", "Blues Driver"]
            },
            "pitch": {
                "types": ["Pitch Shifter", "Harmonizer", "Whammy", "Pitch Shifter Pro", "Harmonizer Pro"]
            }
        }
