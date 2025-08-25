import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import openai
from tonegpt.config import BLOCKS_FILE

class AIToneGenerator:
    """
    AI-powered tone generation system for Fractal FM9
    Generates unique, accurate tone patches based on natural language queries
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key
        self.blocks_data = self._load_blocks()
        self.amp_models = self._load_amp_models()
        self.cab_models = self._load_cab_models()
        
        if openai_api_key:
            openai.api_key = openai_api_key
    
    def _load_blocks(self) -> Dict:
        """Load available FM9 blocks and their parameters"""
        try:
            with open(BLOCKS_FILE, 'r') as f:
                blocks_list = json.load(f)
                # Convert list to organized dictionary by category
                organized_blocks = {}
                for block in blocks_list:
                    category = block.get('category', 'Other').lower()
                    if category not in organized_blocks:
                        organized_blocks[category] = []
                    organized_blocks[category].append(block)
                return organized_blocks
        except FileNotFoundError:
            return self._get_default_blocks()
    
    def _load_amp_models(self) -> List[str]:
        """Load available amp models"""
        amps_file = Path(__file__).parent.parent.parent / "data" / "amps_list.json"
        
        try:
            with open(amps_file, 'r') as f:
                data = json.load(f)
                
                if isinstance(data, list):
                    # Handle both string lists and dictionary lists
                    if data and isinstance(data[0], str):
                        # Simple string list
                        return [amp.strip() for amp in data if amp.strip()]
                    elif data and isinstance(data[0], dict):
                        # Dictionary list with 'Model' key
                        return [item.get('Model', '') for item in data if isinstance(item, dict) and item.get('Model')]
                
                return []
        except Exception as e:
            return ["FAS Modern", "FAS Brown", "FAS Lead", "Mesa Boogie Mark IIC+", "Marshall JCM800"]
    
    def _load_cab_models(self) -> List[str]:
        """Load available cab models"""
        cabs_file = Path(__file__).parent.parent.parent / "data" / "cabs_list.json"
        
        try:
            with open(cabs_file, 'r') as f:
                data = json.load(f)
                
                if isinstance(data, list):
                    # Handle both string lists and dictionary lists
                    if data and isinstance(data[0], str):
                        # Simple string list
                        return [cab.strip() for cab in data if cab.strip()]
                    elif data and isinstance(data[0], dict):
                        # Dictionary list with 'Cab' key
                        return [item.get('Cab', '') for item in data if isinstance(item, dict) and item.get('Cab')]
                
                return []
        except Exception as e:
            return ["4x12 V30", "4x12 Greenback", "2x12 V30", "1x12 Open Back"]
    
    def _get_default_blocks(self) -> Dict:
        """Default blocks if blocks.json not found"""
        return {
            "gain": {
                "name": "Gain Blocks",
                "types": ["FAS Boost", "TS808 Mod", "Klon", "Rat Distortion", "Fuzz Face"],
                "parameters": {
                    "gain": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "level": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "tone": {"min": 0.0, "max": 10.0, "default": 5.0}
                }
            },
            "amp": {
                "name": "Amp Blocks",
                "types": self._load_amp_models(),
                "parameters": {
                    "gain": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "master": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "bass": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "mid": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "treble": {"min": 0.0, "max": 10.0, "default": 5.0}
                }
            },
            "cab": {
                "name": "Cab Blocks",
                "types": self._load_cab_models(),
                "parameters": {
                    "lowcut": {"min": 20, "max": 1000, "default": 80},
                    "highcut": {"min": 2000, "max": 20000, "default": 8000}
                }
            },
            "eq": {
                "name": "EQ Blocks",
                "types": ["5 Band EQ", "10 Band EQ", "Parametric EQ"],
                "parameters": {
                    "low": {"min": -12.0, "max": 12.0, "default": 0.0},
                    "mid": {"min": -12.0, "max": 12.0, "default": 0.0},
                    "high": {"min": -12.0, "max": 12.0, "default": 0.0}
                }
            },
            "delay": {
                "name": "Delay Blocks",
                "types": ["Digital Stereo Delay", "Tape Delay", "Ping Pong Delay"],
                "parameters": {
                    "time": {"min": 0, "max": 2000, "default": 500},
                    "mix": {"min": 0.0, "max": 100.0, "default": 30.0},
                    "feedback": {"min": 0.0, "max": 100.0, "default": 20.0}
                }
            },
            "reverb": {
                "name": "Reverb Blocks",
                "types": ["Medium Plate", "Large Hall", "Spring Reverb", "Room Reverb"],
                "parameters": {
                    "room_size": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "mix": {"min": 0.0, "max": 100.0, "default": 30.0},
                    "decay": {"min": 0.0, "max": 10.0, "default": 5.0}
                }
            }
        }
    
    def generate_tone_from_query(self, query: str) -> Dict:
        """
        Generate a complete tone patch from a natural language query
        Example: "give me a tone that sounds like deftones"
        """
        # Parse the query to understand the intent
        intent = self._parse_query_intent(query)
        
        # Generate the tone structure
        tone_structure = self._generate_tone_structure(intent)
        
        # Generate specific parameters
        tone_patch = self._generate_tone_patch(tone_structure)
        
        return {
            "query": query,
            "intent": intent,
            "tone_structure": tone_structure,
            "tone_patch": tone_patch,
            "description": self._generate_tone_description(tone_patch, intent)
        }
    
    def _parse_query_intent(self, query: str) -> Dict:
        """Parse natural language query to understand tone intent"""
        query_lower = query.lower()
        
        # Extract genre/style
        genres = {
            "metal": ["metal", "heavy", "deftones", "tool", "meshuggah", "djent"],
            "ambient": ["ambient", "atmospheric", "pad", "soundscape", "ethereal"],
            "blues": ["blues", "bluesy", "bb king", "stevie ray", "clapton"],
            "rock": ["rock", "classic rock", "led zeppelin", "ac/dc", "van halen"],
            "funk": ["funk", "rhythm", "groove", "james brown", "prince"],
            "jazz": ["jazz", "smooth", "wes montgomery", "pat metheny"],
            "country": ["country", "twang", "telecaster", "nashville"],
            "punk": ["punk", "raw", "ramones", "sex pistols", "green day"]
        }
        
        detected_genre = "rock"  # default
        for genre, keywords in genres.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_genre = genre
                break
        
        # Extract specific characteristics
        characteristics = []
        if "lead" in query_lower or "solo" in query_lower:
            characteristics.append("lead")
        if "rhythm" in query_lower or "chord" in query_lower:
            characteristics.append("rhythm")
        if "clean" in query_lower:
            characteristics.append("clean")
        if "dirty" in query_lower or "distorted" in query_lower:
            characteristics.append("distorted")
        if "bright" in query_lower or "sparkly" in query_lower:
            characteristics.append("bright")
        if "warm" in query_lower or "dark" in query_lower:
            characteristics.append("warm")
        
        return {
            "genre": detected_genre,
            "characteristics": characteristics,
            "query": query
        }
    
    def _generate_tone_structure(self, intent: Dict) -> Dict:
        """Generate the basic structure of the tone based on intent"""
        genre = intent.get("genre", "rock")  # Ensure genre exists
        characteristics = intent.get("characteristics", [])
        
        # Define genre-based structures
        structures = {
            "metal": {
                "genre": "metal",
                "drive_blocks": 2,
                "amp_type": "high_gain",
                "eq_emphasis": "mid_scoop",
                "delay_type": "short",
                "reverb_type": "minimal"
            },
            "ambient": {
                "genre": "ambient",
                "drive_blocks": 0,
                "amp_type": "clean",
                "eq_emphasis": "bright",
                "delay_type": "long",
                "reverb_type": "atmospheric"
            },
            "blues": {
                "genre": "blues",
                "drive_blocks": 1,
                "amp_type": "medium_gain",
                "eq_emphasis": "warm",
                "delay_type": "medium",
                "reverb_type": "spring"
            },
            "rock": {
                "genre": "rock",
                "drive_blocks": 1,
                "amp_type": "medium_gain",
                "eq_emphasis": "balanced",
                "delay_type": "medium",
                "reverb_type": "plate"
            }
        }
        
        base_structure = structures.get(genre, structures["rock"]).copy()
        
        # Adjust based on characteristics
        if "lead" in characteristics:
            base_structure["drive_blocks"] = min(base_structure["drive_blocks"] + 1, 2)
            base_structure["eq_emphasis"] = "bright"
        
        if "rhythm" in characteristics:
            base_structure["eq_emphasis"] = "mid_boost"
        
        return base_structure
    
    def _generate_tone_patch(self, structure: Dict) -> Dict:
        """Generate the actual tone patch with specific parameters"""
        patch = {
            "drive_1": {"enabled": False, "type": "None", "parameters": {}},
            "drive_2": {"enabled": False, "type": "None", "parameters": {}},
            "amp": {"enabled": True, "type": "None", "parameters": {}},
            "cab": {"enabled": True, "type": "None", "parameters": {}},
            "eq": {"enabled": False, "type": "None", "parameters": {}},
            "delay": {"enabled": False, "type": "None", "parameters": {}},
            "reverb": {"enabled": False, "type": "None", "parameters": {}}
        }
        
        # Generate drive blocks
        if structure["drive_blocks"] >= 1:
            patch["drive_1"] = self._generate_drive_block(1, structure)
        if structure["drive_blocks"] >= 2:
            patch["drive_2"] = self._generate_drive_block(2, structure)
        
        # Generate amp
        patch["amp"] = self._generate_amp_block(structure)
        
        # Generate cab
        patch["cab"] = self._generate_cab_block(structure)
        
        # Generate EQ
        if structure["eq_emphasis"] != "balanced":
            patch["eq"] = self._generate_eq_block(structure)
        
        # Generate delay
        if structure["delay_type"] != "none":
            patch["delay"] = self._generate_delay_block(structure)
        
        # Generate reverb
        if structure["reverb_type"] != "none":
            patch["reverb"] = self._generate_reverb_block(structure)
        
        return patch
    
    def _generate_drive_block(self, position: int, structure: Dict) -> Dict:
        """Generate a drive block with appropriate parameters and X/Y channels"""
        # Get drive types from blocks data or use defaults
        drive_types = []
        if "gain" in self.blocks_data:
            drive_types = [block.get("name", "") for block in self.blocks_data["gain"]]
        
        if not drive_types:
            drive_types = ["FAS Boost", "TS808 Mod", "Klon", "Rat Distortion", "Fuzz Face"]
        
        # Generate 4 channels (A, B, C, D) for X/Y switching
        channels = {}
        for channel in ["A", "B", "C", "D"]:
            drive_type = random.choice(drive_types)
            
            # Adjust drive type based on genre and channel
            if structure["genre"] == "metal":
                if drive_types:
                    metal_drives = [d for d in drive_types if any(word in d.lower() for word in ["distortion", "drive"])]
                    if metal_drives:
                        drive_type = random.choice(metal_drives)
                else:
                    metal_drives = ["Rat Distortion", "Fuzz Face", "FAS Boost"]
                    drive_type = random.choice(metal_drives)
            
            # Vary parameters per channel
            base_gain = random.uniform(3.0, 8.0)
            channels[channel] = {
                "type": drive_type,
                "parameters": {
                    "gain": round(base_gain + (ord(channel) - ord("A")) * 0.5, 1),
                    "level": round(random.uniform(4.0, 7.0), 1),
                    "tone": round(random.uniform(4.0, 7.0), 1)
                }
            }
        
        return {
            "enabled": True,
            "current_channel": "A",
            "channels": channels
        }
    
    def _generate_amp_block(self, structure: Dict) -> Dict:
        """Generate an amp block with appropriate parameters and X/Y channels"""
        amp_types = self.amp_models[:20]  # Use more variety for channels
        
        # Generate 4 channels (A, B, C, D) for X/Y switching
        channels = {}
        for channel in ["A", "B", "C", "D"]:
            amp_type = random.choice(amp_types)
            
            # Adjust amp type based on genre and channel
            if structure["genre"] == "metal":
                metal_amps = [amp for amp in amp_types if any(word in amp.lower() for word in ["modern", "lead", "brown", "mesa"])]
                if metal_amps:
                    amp_type = random.choice(metal_amps)
            
            # Vary gain per channel (A=clean, B=crunch, C=lead, D=high gain)
            channel_gains = {"A": (2.0, 4.0), "B": (4.0, 6.0), "C": (6.0, 8.0), "D": (7.0, 9.0)}
            gain_range = channel_gains.get(channel, (4.0, 7.0))
            
            channels[channel] = {
                "type": amp_type,
                "parameters": {
                    "gain": round(random.uniform(*gain_range), 1),
                    "master": round(random.uniform(3.0, 7.0), 1),
                    "bass": round(random.uniform(4.0, 8.0), 1),
                    "mid": round(random.uniform(3.0, 8.0), 1),
                    "treble": round(random.uniform(4.0, 8.0), 1)
                }
            }
        
        return {
            "enabled": True,
            "current_channel": "A",
            "channels": channels
        }
    
    def _generate_cab_block(self, structure: Dict) -> Dict:
        """Generate a cab block with appropriate parameters"""
        cab_types = self.cab_models[:8]  # Limit for variety
        cab_type = random.choice(cab_types)
        
        return {
            "enabled": True,
            "type": cab_type,
            "parameters": {
                "lowcut": random.randint(60, 120),
                "highcut": random.randint(6000, 12000)
            }
        }
    
    def _generate_eq_block(self, structure: Dict) -> Dict:
        """Generate an EQ block based on the intended emphasis"""
        # Get EQ types from blocks data or use defaults
        eq_types = []
        if "eq" in self.blocks_data:
            eq_types = [block.get("name", "") for block in self.blocks_data["eq"]]
        
        if not eq_types:
            eq_types = ["5 Band EQ", "10 Band EQ", "Parametric EQ"]
        
        eq_type = random.choice(eq_types)
        
        if structure["eq_emphasis"] == "mid_scoop":
            params = {"low": 2.0, "mid": -3.0, "high": 2.0}
        elif structure["eq_emphasis"] == "mid_boost":
            params = {"low": -1.0, "mid": 3.0, "high": -1.0}
        elif structure["eq_emphasis"] == "bright":
            params = {"low": -1.0, "mid": 0.0, "high": 3.0}
        elif structure["eq_emphasis"] == "warm":
            params = {"low": 2.0, "mid": 1.0, "high": -2.0}
        else:
            params = {"low": 0.0, "mid": 0.0, "high": 0.0}
        
        return {
            "enabled": True,
            "type": eq_type,
            "parameters": params
        }
    
    def _generate_delay_block(self, structure: Dict) -> Dict:
        """Generate a delay block based on the intended type"""
        # Get delay types from blocks data or use defaults
        delay_types = []
        if "delay" in self.blocks_data:
            delay_types = [block.get("name", "") for block in self.blocks_data["delay"]]
        
        if not delay_types:
            delay_types = ["Digital Stereo Delay", "Tape Delay", "Ping Pong Delay"]
        
        delay_type = random.choice(delay_types)
        
        if structure["delay_type"] == "short":
            time_range = (100, 400)
        elif structure["delay_type"] == "long":
            time_range = (800, 1500)
        else:  # medium
            time_range = (400, 800)
        
        return {
            "enabled": True,
            "type": delay_type,
            "parameters": {
                "time": random.randint(*time_range),
                "mix": round(random.uniform(15.0, 45.0), 1),
                "feedback": round(random.uniform(10.0, 35.0), 1)
            }
        }
    
    def _generate_reverb_block(self, structure: Dict) -> Dict:
        """Generate a reverb block based on the intended type"""
        # Get reverb types from blocks data or use defaults
        reverb_types = []
        if "reverb" in self.blocks_data:
            reverb_types = [block.get("name", "") for block in self.blocks_data["reverb"]]
        
        if not reverb_types:
            reverb_types = ["Medium Plate", "Large Hall", "Spring Reverb", "Room Reverb"]
        
        reverb_type = random.choice(reverb_types)
        
        if structure["reverb_type"] == "atmospheric":
            room_size = random.uniform(7.0, 10.0)
            mix = random.uniform(40.0, 60.0)
        elif structure["reverb_type"] == "spring":
            room_size = random.uniform(3.0, 6.0)
            mix = random.uniform(20.0, 40.0)
        else:  # minimal/plate
            room_size = random.uniform(4.0, 7.0)
            mix = random.uniform(15.0, 35.0)
        
        return {
            "enabled": True,
            "type": reverb_type,
            "parameters": {
                "room_size": round(room_size, 1),
                "mix": round(mix, 1),
                "decay": round(random.uniform(3.0, 7.0), 1)
            }
        }
    
    def _generate_tone_description(self, tone_patch: Dict, intent: Dict) -> str:
        """Generate a human-readable description of the tone"""
        genre = intent["genre"]
        characteristics = intent["characteristics"]
        
        desc_parts = [f"A {genre} tone"]
        
        if "lead" in characteristics:
            desc_parts.append("optimized for lead playing")
        elif "rhythm" in characteristics:
            desc_parts.append("designed for rhythm work")
        
        # Handle X/Y channel descriptions
        if tone_patch["drive_1"]["enabled"]:
            drive_info = tone_patch['drive_1']
            if "channels" in drive_info:
                current_channel = drive_info.get("current_channel", "A")
                drive_type = drive_info["channels"][current_channel]["type"]
                desc_parts.append(f"with {drive_type} drive (Ch.{current_channel})")
            else:
                desc_parts.append(f"with {drive_info['type']} drive")
        
        # Handle amp channels
        amp_info = tone_patch['amp']
        if "channels" in amp_info:
            current_channel = amp_info.get("current_channel", "A")
            amp_type = amp_info["channels"][current_channel]["type"]
            desc_parts.append(f"using {amp_type} amp (Ch.{current_channel})")
        else:
            desc_parts.append(f"using {amp_info['type']} amp")
        
        desc_parts.append(f"and {tone_patch['cab']['type']} cabinet")
        
        if tone_patch["eq"]["enabled"]:
            desc_parts.append("with custom EQ shaping")
        
        if tone_patch["delay"]["enabled"]:
            desc_parts.append("featuring delay effects")
        
        if tone_patch["reverb"]["enabled"]:
            desc_parts.append("with reverb ambience")
        
        # Add X/Y switching info
        desc_parts.append("with X/Y switching")
        
        return " ".join(desc_parts) + "."
    
    def generate_multiple_tones(self, query: str, count: int = 3) -> List[Dict]:
        """Generate multiple unique tone variations for the same query"""
        tones = []
        for i in range(count):
            # Add some randomization to make each tone unique
            tone = self.generate_tone_from_query(query)
            tone["variation"] = i + 1
            tones.append(tone)
        return tones
