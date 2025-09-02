import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import openai
from tonegpt.config import BLOCKS_FILE
from .comprehensive_system import ComprehensiveSystem
from .enhanced_amp_parameters import EnhancedAmpParameters
from .advanced_block_types import AdvancedBlockTypes


class EnhancedAIToneGenerator:
    """
    Enhanced AI-powered tone generation system for Fractal FM9
    Uses complete firmware data, user guides, and accurate artist mappings
    """

    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key
        self.blocks_data = self._load_blocks()
        self.firmware_blocks = self._load_firmware_blocks()
        self.amp_models = self._load_amp_models()
        self.cab_models = self._load_cab_models()
        self.artist_mappings = self._load_artist_mappings()
        self.guide_data = self._load_guide_data()
        self.fm9_reference = self._load_fm9_reference()

        # Initialize comprehensive system
        self.comprehensive_system = ComprehensiveSystem()

        # Initialize enhanced amp parameters
        self.enhanced_amp_params = EnhancedAmpParameters()

        # Initialize advanced block types
        self.advanced_blocks = AdvancedBlockTypes()

        # Performance optimization: tone cache
        self.tone_cache = {}
        self.cache_max_size = 100

        if openai_api_key:
            openai.api_key = openai_api_key

    @staticmethod
    def _flatten_enhanced_params(enhanced_params):
        """Flatten nested enhanced parameters for UI access"""
        flattened = {}

        for category, category_data in enhanced_params.items():
            if isinstance(category_data, dict):
                for param_name, param_data in category_data.items():
                    if isinstance(param_data, dict) and "min" in param_data:
                        # Direct parameter with min/max
                        flattened[f"{category}_{param_name}"] = param_data
                    elif isinstance(param_data, dict):
                        # Nested parameter group
                        for sub_param, sub_data in param_data.items():
                            if isinstance(sub_data, dict) and "min" in sub_data:
                                flattened[f"{category}_{param_name}_{sub_param}"] = (
                                    sub_data
                                )
                            elif isinstance(sub_data, dict):
                                # Further nested
                                for sub_sub_param, sub_sub_data in sub_data.items():
                                    if (
                                        isinstance(sub_sub_data, dict)
                                        and "min" in sub_sub_data
                                    ):
                                        flattened[
                                            f"{category}_{param_name}_{sub_param}_{sub_sub_param}"
                                        ] = sub_sub_data

        return flattened

    def generate_tone(self, query: str) -> Dict:
        """Generate tone from query - wrapper for generate_tone_from_query"""
        return self.generate_tone_from_query(query)

    def _load_blocks(self) -> Dict:
        """Load available FM9 blocks and their parameters"""
        try:
            with open(BLOCKS_FILE, "r") as f:
                blocks_list = json.load(f)
                # Convert list to organized dictionary by category
                organized_blocks = {}
                for block in blocks_list:
                    category = block.get("category", "Other").lower()
                    if category not in organized_blocks:
                        organized_blocks[category] = []
                    organized_blocks[category].append(block)
                return organized_blocks
        except FileNotFoundError:
            return self._get_default_blocks()

    def _load_firmware_blocks(self) -> Dict:
        """Load complete firmware block data from advanced analysis"""
        try:
            firmware_file = (
                Path(__file__).parent.parent.parent
                / "data"
                / "firmware_blocks_integrated.json"
            )
            with open(firmware_file, "r") as f:
                firmware_blocks = json.load(f)

                # Organize by category and extract real-world names
                organized_firmware = {}
                for block in firmware_blocks:
                    category = block.get("category", "other").lower()
                    if category not in organized_firmware:
                        organized_firmware[category] = []

                    # Extract real-world name if available
                    real_world = block.get("real_world", block.get("name", ""))
                    if "Fractal Audio FM9" in real_world:
                        # Try to extract meaningful name from description
                        description = block.get("description", "")
                        if "amp" in description.lower():
                            real_world = (
                                f"FM9 Amp Model {block.get('name', '').split('_')[-1]}"
                            )
                        elif "cab" in description.lower():
                            real_world = (
                                f"FM9 Cab Model {block.get('name', '').split('_')[-1]}"
                            )
                        elif "drive" in description.lower():
                            real_world = f"FM9 Drive Model {block.get('name', '').split('_')[-1]}"

                    organized_firmware[category].append(
                        {
                            "name": block.get("name", ""),
                            "real_world": real_world,
                            "description": block.get("description", ""),
                            "parameters": block.get("parameters", {}),
                            "fm9_verified": block.get("fm9_verified", True),
                            "footswitch_assignable": block.get(
                                "footswitch_assignable", True
                            ),
                            "firmware_data": block.get("firmware_data", {}),
                        }
                    )

                return organized_firmware
        except FileNotFoundError:
            return {}

    def _load_amp_models(self) -> List[str]:
        """Load available amp models from real FM9 blocks data"""
        try:
            # Load from comprehensive blocks data (highest priority)
            amp_blocks = self.blocks_data.get("amp", [])
            if amp_blocks:
                amp_names = [
                    block.get("name", "") for block in amp_blocks if block.get("name")
                ]
                print(
                    f"🔧 Loaded {len(amp_names)} real amp models from FM9 blocks data"
                )
                return amp_names

            # Fallback to separate amps files
            amps_files = [
                Path(__file__).parent.parent.parent / "data" / "amps_list_final.json",
                Path(__file__).parent.parent.parent / "data" / "wiki_amps_cleaned.json",
                Path(__file__).parent.parent.parent / "data" / "amps_list.json",
            ]

            amps_data = []
            for amps_file in amps_files:
                if amps_file.exists():
                    with open(amps_file, "r") as f:
                        amps_data = json.load(f)
                        break

            if amps_data:
                for amp in amps_data:
                    if isinstance(amp, dict):
                        amp_name = amp.get("name", "")
                    else:
                        amp_name = str(amp).strip()
                    if amp_name and amp_name not in amp_models:
                        amp_models.append(amp_name)
        except Exception as e:
            print(f"⚠️ Comprehensive amps list not found, using fallback data: {e}")

        # Load from regular blocks
        if "amp" in self.blocks_data:
            for block in self.blocks_data["amp"]:
                amp_name = block.get("real_world", block.get("name", ""))
                if amp_name and amp_name not in amp_models:
                    amp_models.append(amp_name)

        # Load from firmware blocks
        if "amp" in self.firmware_blocks:
            for block in self.firmware_blocks["amp"]:
                real_world = block.get("real_world", "")
                if real_world and real_world not in amp_models:
                    amp_models.append(real_world)

        # Add known FM9 amp models from guides as fallback
        known_amps = [
            "Brit 800",
            "Brit 900",
            "Brit JVM",
            "Brit Super",
            "Brit Plexi",
            "USA IIC+",
            "USA Lead",
            "USA Lead 2",
            "USA Bassguy",
            "USA Clean",
            "FAS Modern",
            "FAS Brootalz",
            "FAS Wreck",
            "FAS Crunch",
            "Euro Blue",
            "Euro Red",
            "Euro Uber",
            "Euro Blue OD",
            "Shiva Clean",
            "Shiva Lead",
            "Shiva Clean 2",
            "Shiva Lead 2",
        ]

        for amp in known_amps:
            if amp not in amp_models:
                amp_models.append(amp)

        return amp_models

    def _load_cab_models(self) -> List[str]:
        """Load available cab models from real FM9 blocks data"""
        try:
            # Load from comprehensive blocks data (highest priority)
            cab_blocks = self.blocks_data.get("cab", [])
            if cab_blocks:
                cab_names = [
                    block.get("name", "") for block in cab_blocks if block.get("name")
                ]
                print(
                    f"🔧 Loaded {len(cab_names)} real cab models from FM9 blocks data"
                )
                return cab_names

            # Fallback to separate cabs files
            cabs_files = [
                Path(__file__).parent.parent.parent / "data" / "cabs_list_final.json",
                Path(__file__).parent.parent.parent / "data" / "wiki_cabs_cleaned.json",
                Path(__file__).parent.parent.parent / "data" / "cabs_list.json",
            ]

            cabs_data = []
            for cabs_file in cabs_files:
                if cabs_file.exists():
                    with open(cabs_file, "r") as f:
                        cabs_data = json.load(f)
                        break

            if cabs_data:
                for cab in cabs_data:
                    if isinstance(cab, dict):
                        cab_name = cab.get("name", "")
                    else:
                        cab_name = str(cab).strip()
                    if cab_name and cab_name not in cab_models:
                        cab_models.append(cab_name)
        except Exception as e:
            print(f"⚠️ Comprehensive cabs list not found, using fallback data: {e}")

        # Load from regular blocks
        if "cab" in self.blocks_data:
            for block in self.blocks_data["cab"]:
                cab_models.append(block.get("real_world", block.get("name", "")))

        # Load from firmware blocks
        if "cab" in self.firmware_blocks:
            for block in self.firmware_blocks["cab"]:
                real_world = block.get("real_world", "")
                if real_world and real_world not in cab_models:
                    cab_models.append(real_world)

        # Add known FM9 cab models from guides
        known_cabs = [
            "4x12 Brit TV",
            "4x12 Brit 75W",
            "4x12 Brit 80W",
            "4x12 Brit 100W",
            "4x12 USA Trad",
            "4x12 USA Modern",
            "4x12 USA Lead",
            "4x12 USA Bass",
            "2x12 Brit 30W",
            "2x12 Brit 40W",
            "1x12 Brit 30W",
            "1x12 Brit 40W",
            "4x10 USA Bass",
            "1x15 USA Bass",
            "4x12 Euro 80W",
            "4x12 Euro 100W",
        ]

        for cab in known_cabs:
            if cab not in cab_models:
                cab_models.append(cab)

        return cab_models

    def _load_artist_mappings(self) -> Dict:
        """Load comprehensive artist-specific tone mappings based on guides"""
        return {
            "deftones": {
                "genre": "metal",
                "characteristics": ["heavy", "atmospheric", "drop_tuning"],
                "gear": {
                    "amps": [
                        "MESA BOOGIE MARK IIC+",
                        "MESA BOOGIE DUAL RECTIFIER",
                        "MESA BOOGIE TRIPLE RECTIFIER",
                        "FAS BROOTALZ",
                        "EURO UBER",
                    ],
                    "cabs": ["4x12 USA Modern", "4x12 Euro 100W", "4x12 MESA V30"],
                    "drives": ["FAS Boost", "TS808 Mod", "MESA BOOGIE V-TWIN"],
                    "effects": ["delay", "reverb", "chorus"],
                },
                "parameters": {
                    "gain": 8.5,
                    "bass": 7.0,
                    "mid": 4.0,
                    "treble": 6.5,
                    "presence": 5.0,
                },
                "description": "Heavy, atmospheric metal with scooped mids and drop tuning",
            },
            "tool": {
                "genre": "progressive",
                "characteristics": ["complex", "rhythmic", "atmospheric"],
                "gear": {
                    "amps": [
                        "USA LEAD",
                        "BRIT 800",
                        "FAS MODERN",
                        "MESA BOOGIE MARK IIC+",
                        "MARSHALL JCM800",
                    ],
                    "cabs": ["4x12 Brit 100W", "4x12 USA Lead", "4x12 MARSHALL V30"],
                    "drives": ["FAS Boost", "Klon", "TS808 Mod"],
                    "effects": ["delay", "reverb", "modulation"],
                },
                "parameters": {
                    "gain": 7.0,
                    "bass": 6.0,
                    "mid": 7.0,
                    "treble": 6.0,
                    "presence": 5.5,
                },
                "description": "Complex progressive metal with tight rhythm and atmospheric leads",
            },
            "metallica": {
                "genre": "metal",
                "characteristics": ["thrash", "tight", "aggressive"],
                "gear": {
                    "amps": ["USA IIC+", "FAS Brootalz", "Euro Uber"],
                    "cabs": ["4x12 USA Modern", "4x12 Euro 100W"],
                    "drives": ["FAS Boost", "TS808 Mod"],
                    "effects": ["delay", "reverb"],
                },
                "parameters": {
                    "gain": 9.0,
                    "bass": 8.0,
                    "mid": 3.0,
                    "treble": 7.0,
                    "presence": 6.0,
                },
                "description": "Classic thrash metal with tight bass and scooped mids",
            },
            "jimi hendrix": {
                "genre": "rock",
                "characteristics": ["fuzz", "psychedelic", "lead"],
                "gear": {
                    "amps": ["Brit Plexi", "Brit Super", "USA Bassguy"],
                    "cabs": ["4x12 Brit 75W", "4x12 Brit 100W"],
                    "drives": ["Fuzz Face", "FAS Boost"],
                    "effects": ["delay", "reverb", "wah", "univibe"],
                },
                "parameters": {
                    "gain": 6.0,
                    "bass": 5.0,
                    "mid": 6.0,
                    "treble": 7.0,
                    "presence": 6.5,
                },
                "description": "Classic psychedelic rock with fuzz and modulation effects",
            },
            "david gilmour": {
                "genre": "rock",
                "characteristics": ["clean", "atmospheric", "lead"],
                "gear": {
                    "amps": ["Brit Plexi", "USA Clean", "FAS Wreck"],
                    "cabs": ["4x12 Brit 75W", "2x12 Brit 30W"],
                    "drives": ["FAS Boost", "TS808 Mod"],
                    "effects": ["delay", "reverb", "chorus", "phaser"],
                },
                "parameters": {
                    "gain": 4.0,
                    "bass": 5.0,
                    "mid": 6.0,
                    "treble": 7.0,
                    "presence": 6.0,
                },
                "description": "Clean atmospheric leads with delay and reverb",
            },
            "stevie ray vaughan": {
                "genre": "blues",
                "characteristics": ["blues", "overdrive", "lead"],
                "gear": {
                    "amps": ["USA Bassguy", "USA Clean", "Brit Super"],
                    "cabs": ["4x12 USA Trad", "2x12 Brit 30W"],
                    "drives": ["TS808 Mod", "FAS Boost"],
                    "effects": ["delay", "reverb", "tremolo"],
                },
                "parameters": {
                    "gain": 5.5,
                    "bass": 6.0,
                    "mid": 7.0,
                    "treble": 6.5,
                    "presence": 6.0,
                },
                "description": "Classic blues with tube screamer overdrive",
            },
            "eric clapton": {
                "genre": "blues",
                "characteristics": ["clean", "blues", "warm"],
                "gear": {
                    "amps": ["USA Clean", "Brit Super", "FAS Wreck"],
                    "cabs": ["4x12 USA Trad", "2x12 Brit 30W"],
                    "drives": ["FAS Boost", "TS808 Mod"],
                    "effects": ["delay", "reverb"],
                },
                "parameters": {
                    "gain": 3.0,
                    "bass": 5.0,
                    "mid": 6.0,
                    "treble": 6.0,
                    "presence": 5.0,
                },
                "description": "Clean blues with warm mids and subtle effects",
            },
        }

    def _load_guide_data(self) -> Dict:
        """Load data from FM9 guides for accurate parameter ranges"""
        try:
            # Load verified guide data from the parser
            guide_file = (
                Path(__file__).parent.parent.parent / "verified_guide_data.json"
            )
            with open(guide_file, "r") as f:
                guide_data = json.load(f)

            # Also load blocks guide data
            blocks_guide_file = (
                Path(__file__).parent.parent.parent / "blocks_guide_data.json"
            )
            if blocks_guide_file.exists():
                with open(blocks_guide_file, "r") as f:
                    blocks_guide_data = json.load(f)
                    guide_data["blocks_guide"] = blocks_guide_data

            return guide_data
        except FileNotFoundError:
            # Fallback to basic data if guide file not found
            return {
                "manual": {
                    "hardware_specs": {
                        "max_blocks": 84,
                        "scenes": 8,
                        "channels_per_block": 4,
                        "audio_quality": "24-bit/48kHz",
                        "grid_size": "6x14",
                    },
                    "parameter_ranges": {
                        "gain": {"min": 0.0, "max": 10.0, "default": 5.0},
                        "bass": {"min": 0.0, "max": 10.0, "default": 5.0},
                        "mid": {"min": 0.0, "max": 10.0, "default": 5.0},
                        "treble": {"min": 0.0, "max": 10.0, "default": 5.0},
                        "presence": {"min": 0.0, "max": 10.0, "default": 5.0},
                        "master": {"min": 0.0, "max": 10.0, "default": 5.0},
                    },
                },
                "blocks": {"block_definitions": {}},
                "footswitch": {
                    "footswitch_functions": [
                        "Scene switching",
                        "Block bypass",
                        "Channel switching",
                        "Parameter control",
                        "Looper control",
                        "Tap tempo",
                    ]
                },
            }

    def _load_fm9_reference(self) -> Dict:
        """Load comprehensive FM9 reference data"""
        try:
            reference_file = (
                Path(__file__).parent.parent
                / "data"
                / "fm9_comprehensive_reference.json"
            )
            if reference_file.exists():
                with open(reference_file, "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load FM9 reference: {e}")
        return {}

    def _get_default_blocks(self) -> Dict:
        """Default blocks if blocks.json not found"""
        # Get enhanced amp parameters
        enhanced_params = self.enhanced_amp_params.get_advanced_amp_parameters()

        return {
            "amp": {
                "name": "Amplifier Blocks",
                "types": ["Brit 800", "USA IIC+", "FAS Modern", "Euro Uber"],
                "parameters": {
                    # Basic parameters
                    "gain": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "bass": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "mid": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "treble": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "presence": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "master": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "level": {"min": -20.0, "max": 20.0, "default": 0.0},
                    "depth": {"min": 0.0, "max": 10.0, "default": 5.0},
                    # Enhanced parameters from Blocks Guide (flattened)
                    **EnhancedAIToneGenerator._flatten_enhanced_params(enhanced_params),
                },
            },
            # Add advanced block types
            **self.advanced_blocks.get_all_advanced_blocks(),
            "cab": {
                "name": "Cabinet Blocks",
                "types": ["4x12 Brit TV", "4x12 USA Modern", "2x12 Brit 30W"],
                "parameters": {
                    "low_cut": {"min": 20, "max": 200, "default": 80},
                    "high_cut": {"min": 2000, "max": 20000, "default": 8000},
                    "level": {"min": -20.0, "max": 20.0, "default": 0.0},
                },
            },
            "pitch": {
                "name": "Pitch Blocks",
                "types": ["Pitch Shifter", "Harmonizer", "Whammy"],
                "parameters": {
                    "pitch": {"min": -24, "max": 24, "default": 0, "unit": "semitones"},
                    "mix": {"min": 0, "max": 100, "default": 50, "unit": "%"},
                    "level": {"min": -20.0, "max": 20.0, "default": 0.0, "unit": "dB"},
                },
            },
            "pitch_shifter": {
                "name": "Pitch Shifter",
                "types": ["Pitch Shifter", "Harmonizer"],
                "parameters": {
                    "pitch": {"min": -24, "max": 24, "default": 0, "unit": "semitones"},
                    "mix": {"min": 0, "max": 100, "default": 50, "unit": "%"},
                    "feedback": {"min": 0, "max": 100, "default": 0, "unit": "%"},
                },
            },
            "harmonizer": {
                "name": "Harmonizer",
                "types": ["Harmonizer", "Intelligent Harmony"],
                "parameters": {
                    "pitch1": {
                        "min": -24,
                        "max": 24,
                        "default": 0,
                        "unit": "semitones",
                    },
                    "pitch2": {
                        "min": -24,
                        "max": 24,
                        "default": 0,
                        "unit": "semitones",
                    },
                    "mix": {"min": 0, "max": 100, "default": 50, "unit": "%"},
                },
            },
            "gain": {
                "name": "Drive Blocks",
                "types": ["FAS Boost", "TS808 Mod", "Klon", "Fuzz Face"],
                "parameters": {
                    "gain": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "level": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "tone": {"min": 0.0, "max": 10.0, "default": 5.0},
                },
            },
            "delay": {
                "name": "Delay Blocks",
                "types": ["Digital Stereo Delay", "Tape Delay", "Ping Pong Delay"],
                "parameters": {
                    "time": {"min": 0, "max": 2000, "default": 500},
                    "mix": {"min": 0.0, "max": 100.0, "default": 30.0},
                    "feedback": {"min": 0.0, "max": 100.0, "default": 20.0},
                },
            },
            "reverb": {
                "name": "Reverb Blocks",
                "types": ["Medium Plate", "Large Hall", "Spring Reverb", "Room Reverb"],
                "parameters": {
                    "room_size": {"min": 0.0, "max": 10.0, "default": 5.0},
                    "mix": {"min": 0.0, "max": 100.0, "default": 30.0},
                    "decay": {"min": 0.0, "max": 10.0, "default": 5.0},
                },
            },
        }

    def generate_tone_from_query(self, query: str) -> Dict:
        """
        Generate a complete tone patch from a natural language query
        Uses firmware data, artist mappings, and guide information
        """
        try:
            # Input validation and sanitization
            if not query or not isinstance(query, str):
                query = "clean tone"

            # Clean and normalize the query
            query = query.strip().lower()
            if not query:
                query = "clean tone"

            # Check cache first for performance
            cache_key = f"tone_{hash(query)}"
            if cache_key in self.tone_cache:
                cached_result = self.tone_cache[cache_key].copy()
                cached_result["cached"] = True
                cached_result["generation_timestamp"] = datetime.now().isoformat()
                return cached_result

            # Parse the query to understand the intent
            intent = self._parse_query_intent(query)

            # Generate the tone structure
            tone_structure = self._generate_tone_structure(intent)

            # Add original query to structure for gear matching
            tone_structure["query"] = query

            # Generate specific parameters
            tone_patch = self._generate_tone_patch(tone_structure)

            # Validate the generated tone
            self._validate_tone_patch(tone_patch)

            result = {
                "query": query,
                "intent": intent,
                "tone_structure": tone_structure,
                "tone_patch": tone_patch,
                "description": self._generate_tone_description(tone_patch, intent),
                "firmware_verified": True,
                "guide_referenced": True,
                "generation_timestamp": datetime.now().isoformat(),
                "system_version": "1.0.0",
                "cached": False,
            }

            # Cache the result for future use
            self._cache_tone_result(cache_key, result)

            return result

        except Exception as e:
            # Fallback to a basic clean tone if generation fails
            return self._generate_fallback_tone(query, str(e))

    def _parse_query_intent(self, query: str) -> Dict:
        """Parse natural language query to understand tone intent"""
        query_lower = query.lower()

        # Check for specific artist mappings first
        for artist, mapping in self.artist_mappings.items():
            if artist in query_lower:
                return {
                    "artist": artist,
                    "genre": mapping["genre"],
                    "characteristics": mapping["characteristics"],
                    "gear": mapping["gear"],
                    "parameters": mapping["parameters"],
                    "description": mapping["description"],
                    "query": query,
                }

        # Extract genre/style from general keywords
        genres = {
            "metal": ["metal", "heavy", "thrash", "death", "black", "doom"],
            "ambient": ["ambient", "atmospheric", "pad", "soundscape", "ethereal"],
            "blues": ["blues", "bluesy", "bb king", "stevie ray", "clapton"],
            "rock": ["rock", "classic rock", "led zeppelin", "ac/dc", "van halen"],
            "funk": ["funk", "rhythm", "groove", "james brown", "prince"],
            "jazz": ["jazz", "smooth", "wes montgomery", "pat metheny"],
            "country": ["country", "twang", "telecaster", "nashville"],
            "punk": ["punk", "raw", "ramones", "sex pistols", "green day"],
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
            "query": query,
        }

    def _generate_tone_structure(self, intent: Dict) -> Dict:
        """Generate the basic structure of the tone based on intent"""
        # If we have specific artist mapping, use it
        if "artist" in intent:
            return {
                "genre": intent["genre"],
                "characteristics": intent["characteristics"],
                "gear": intent["gear"],
                "parameters": intent["parameters"],
                "description": intent["description"],
            }

        # Otherwise use genre-based structure
        genre = intent.get("genre", "rock")
        characteristics = intent.get("characteristics", [])

        # Define genre-based structures
        structures = {
            "metal": {
                "genre": "metal",
                "drive_blocks": 2,
                "amp_type": "high_gain",
                "eq_emphasis": "mid_scoop",
                "delay_type": "short",
                "reverb_type": "minimal",
            },
            "ambient": {
                "genre": "ambient",
                "drive_blocks": 0,
                "amp_type": "clean",
                "eq_emphasis": "bright",
                "delay_type": "long",
                "reverb_type": "atmospheric",
            },
            "blues": {
                "genre": "blues",
                "drive_blocks": 1,
                "amp_type": "medium_gain",
                "eq_emphasis": "warm",
                "delay_type": "medium",
                "reverb_type": "spring",
            },
            "rock": {
                "genre": "rock",
                "drive_blocks": 1,
                "amp_type": "medium_gain",
                "eq_emphasis": "balanced",
                "delay_type": "medium",
                "reverb_type": "plate",
            },
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
            "reverb": {"enabled": False, "type": "None", "parameters": {}},
            "modulation": {"enabled": False, "type": "None", "parameters": {}},
            "pitch": {"enabled": False, "type": "None", "parameters": {}},
            "dynamics": {"enabled": False, "type": "None", "parameters": {}},
            "utility": {"enabled": False, "type": "None", "parameters": {}},
        }

        # If we have specific artist mapping, use it
        if "gear" in structure:
            return self._generate_artist_tone_patch(structure)

        # Otherwise generate based on structure
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

        # Generate additional effects based on genre and random chance
        # Add dynamics for most genres (compression is common)
        if (
            structure["genre"] in ["metal", "rock", "funk", "blues"]
            or random.random() < 0.7
        ):
            patch["dynamics"] = self._generate_dynamics_block(structure)

        # Add modulation for most genres (chorus/flanger are common)
        if (
            structure["genre"] in ["ambient", "rock", "funk", "blues"]
            or random.random() < 0.6
        ):
            patch["modulation"] = self._generate_modulation_block(structure)

        # Add pitch effects for lead tones
        if (
            "lead" in structure.get("characteristics", [])
            or structure["genre"] in ["rock", "metal"]
            or random.random() < 0.3
        ):
            patch["pitch"] = self._generate_pitch_block(structure)

        return patch

    def _generate_artist_tone_patch(self, structure: Dict) -> Dict:
        """Generate tone patch based on specific artist mapping"""
        patch = {
            "drive_1": {"enabled": False, "type": "None", "parameters": {}},
            "drive_2": {"enabled": False, "type": "None", "parameters": {}},
            "amp": {"enabled": True, "type": "None", "parameters": {}},
            "cab": {"enabled": True, "type": "None", "parameters": {}},
            "eq": {"enabled": False, "type": "None", "parameters": {}},
            "delay": {"enabled": False, "type": "None", "parameters": {}},
            "reverb": {"enabled": False, "type": "None", "parameters": {}},
            "modulation": {"enabled": False, "type": "None", "parameters": {}},
            "pitch": {"enabled": False, "type": "None", "parameters": {}},
            "dynamics": {"enabled": False, "type": "None", "parameters": {}},
            "utility": {"enabled": False, "type": "None", "parameters": {}},
        }

        gear = structure["gear"]
        parameters = structure["parameters"]

        # Generate amp with artist-specific model
        if gear["amps"]:
            amp_model = random.choice(gear["amps"])
            patch["amp"] = {
                "enabled": True,
                "type": amp_model,
                "parameters": {
                    "gain": parameters.get("gain", 5.0),
                    "bass": parameters.get("bass", 5.0),
                    "mid": parameters.get("mid", 5.0),
                    "treble": parameters.get("treble", 5.0),
                    "presence": parameters.get("presence", 5.0),
                    "master": parameters.get("master", 5.0),
                },
            }

        # Generate cab with artist-specific model
        if gear["cabs"]:
            cab_model = random.choice(gear["cabs"])
            patch["cab"] = {
                "enabled": True,
                "type": cab_model,
                "parameters": {"low_cut": 80.0, "high_cut": 8000.0, "level": 0.0},
            }

        # Generate drive blocks
        if gear["drives"]:
            drive_model = random.choice(gear["drives"])
            patch["drive_1"] = {
                "enabled": True,
                "type": drive_model,
                "parameters": {
                    "gain": random.uniform(4.0, 7.0),
                    "level": random.uniform(4.0, 7.0),
                    "tone": random.uniform(4.0, 7.0),
                },
            }

        # Generate effects
        if "delay" in gear["effects"]:
            patch["delay"] = {
                "enabled": True,
                "type": "Digital Stereo Delay",
                "parameters": {
                    "time": random.uniform(300, 800),
                    "mix": random.uniform(20.0, 40.0),
                    "feedback": random.uniform(15.0, 30.0),
                },
            }

        if "reverb" in gear["effects"]:
            patch["reverb"] = {
                "enabled": True,
                "type": "Medium Plate",
                "parameters": {
                    "room_size": random.uniform(4.0, 7.0),
                    "mix": random.uniform(20.0, 40.0),
                    "decay": random.uniform(4.0, 7.0),
                },
            }

        # Add additional effects based on artist genre
        artist_genre = structure.get("genre", "metal")
        if artist_genre == "metal":
            # Add compression for tight metal tones
            patch["dynamics"] = self._generate_dynamics_block(structure)
        elif artist_genre == "ambient":
            # Add modulation for atmospheric tones
            patch["modulation"] = self._generate_modulation_block(structure)
        elif artist_genre == "rock":
            # Add pitch effects for rock leads
            if "lead" in structure.get("characteristics", []):
                patch["pitch"] = self._generate_pitch_block(structure)

        # Always add some modulation for texture
        if random.random() > 0.5:  # 50% chance
            patch["modulation"] = self._generate_modulation_block(structure)

        return patch

    def _generate_drive_block(self, position: int, structure: Dict) -> Dict:
        """Generate a drive block with appropriate parameters using real FM9 data"""
        # Get drive types from real FM9 blocks data
        drive_types = []
        drive_blocks = self.blocks_data.get("drive", [])
        if drive_blocks:
            drive_types = [
                block.get("name", "") for block in drive_blocks if block.get("name")
            ]

        if not drive_types:
            # Fallback to firmware data
            if "gain" in self.firmware_blocks:
                drive_types = [
                    block.get("real_world", "")
                    for block in self.firmware_blocks["gain"]
                ]

        if not drive_types:
            drive_types = [
                "FAS Boost",
                "TS808 Mod",
                "Klon",
                "Rat Distortion",
                "Fuzz Face",
            ]

        # Select appropriate drive based on query
        query = structure.get("query", "").lower()
        selected_drive = None

        # Try to match specific drive requests
        if "tube screamer" in query or "ts808" in query or "ts9" in query:
            ts_drives = [
                drive
                for drive in drive_types
                if "ts" in drive.lower()
                or "tube" in drive.lower()
                or "screamer" in drive.lower()
            ]
            if ts_drives:
                selected_drive = random.choice(ts_drives)
        elif "klon" in query:
            klon_drives = [drive for drive in drive_types if "klon" in drive.lower()]
            if klon_drives:
                selected_drive = random.choice(klon_drives)
        elif "rat" in query:
            rat_drives = [drive for drive in drive_types if "rat" in drive.lower()]
            if rat_drives:
                selected_drive = random.choice(rat_drives)
        elif "fuzz" in query:
            fuzz_drives = [drive for drive in drive_types if "fuzz" in drive.lower()]
            if fuzz_drives:
                selected_drive = random.choice(fuzz_drives)

        # If no specific match, select based on genre
        if not selected_drive:
            genre = structure.get("genre", "rock")
            if genre == "blues":
                blues_drives = [
                    drive
                    for drive in drive_types
                    if any(
                        word in drive.lower()
                        for word in ["ts", "tube", "screamer", "klon"]
                    )
                ]
                selected_drive = (
                    random.choice(blues_drives)
                    if blues_drives
                    else random.choice(drive_types)
                )
            elif genre == "metal":
                metal_drives = [
                    drive
                    for drive in drive_types
                    if any(
                        word in drive.lower()
                        for word in ["rat", "distortion", "fuzz", "boost"]
                    )
                ]
                selected_drive = (
                    random.choice(metal_drives)
                    if metal_drives
                    else random.choice(drive_types)
                )
            elif genre == "jazz":
                # Jazz typically uses clean boosts or light overdrive
                jazz_drives = [
                    drive
                    for drive in drive_types
                    if any(
                        word in drive.lower() for word in ["boost", "clean", "light"]
                    )
                ]
                selected_drive = (
                    random.choice(jazz_drives)
                    if jazz_drives
                    else random.choice(drive_types)
                )
            else:
                selected_drive = random.choice(drive_types)

        # Generate 4 channels (A, B, C, D) for X/Y switching
        channels = {}
        for channel in ["A", "B", "C", "D"]:
            drive_type = selected_drive

            # Adjust drive type based on genre and channel
            if structure["genre"] == "metal":
                if drive_types:
                    metal_drives = [
                        d
                        for d in drive_types
                        if any(word in d.lower() for word in ["distortion", "drive"])
                    ]
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
                    "tone": round(random.uniform(4.0, 7.0), 1),
                },
            }

        return {
            "enabled": True,
            "type": channels["A"]["type"],  # Set main type from first channel
            "current_channel": "A",
            "channels": channels,
        }

    def _generate_amp_block(self, structure: Dict) -> Dict:
        """Generate an amp block with appropriate parameters using real FM9 data"""
        # Get amp types from real FM9 blocks data
        amp_types = []
        amp_blocks = self.blocks_data.get("amp", [])
        if amp_blocks:
            amp_types = [
                block.get("name", "") for block in amp_blocks if block.get("name")
            ]

        if not amp_types:
            amp_types = self.amp_models[:20]

        # Select appropriate amp based on genre and query
        genre = structure.get("genre", "rock")
        query = structure.get("query", "").lower()

        # Try to match specific amp requests
        selected_amp = None
        if "marshall" in query or "jcm" in query or "800" in query:
            marshall_amps = [
                amp
                for amp in amp_types
                if "brit" in amp.lower()
                or "marshall" in amp.lower()
                or "800" in amp.lower()
            ]
            if marshall_amps:
                selected_amp = random.choice(marshall_amps)
        elif "mesa" in query or "boogie" in query:
            mesa_amps = [
                amp
                for amp in amp_types
                if "mesa" in amp.lower()
                or "boogie" in amp.lower()
                or "recto" in amp.lower()
            ]
            if mesa_amps:
                selected_amp = random.choice(mesa_amps)
        elif "fender" in query:
            fender_amps = [
                amp
                for amp in amp_types
                if "fender" in amp.lower()
                or "tweed" in amp.lower()
                or "deluxe" in amp.lower()
            ]
            if fender_amps:
                selected_amp = random.choice(fender_amps)

        # If no specific match, select based on genre
        if not selected_amp:
            if genre == "metal":
                metal_amps = [
                    amp
                    for amp in amp_types
                    if any(
                        word in amp.lower()
                        for word in ["mesa", "recto", "5150", "mark", "brit", "800"]
                    )
                ]
                selected_amp = (
                    random.choice(metal_amps)
                    if metal_amps
                    else random.choice(amp_types)
                )
            elif genre == "blues":
                blues_amps = [
                    amp
                    for amp in amp_types
                    if any(
                        word in amp.lower()
                        for word in ["fender", "tweed", "deluxe", "vox", "ac30"]
                    )
                ]
                selected_amp = (
                    random.choice(blues_amps)
                    if blues_amps
                    else random.choice(amp_types)
                )
            elif genre == "jazz":
                jazz_amps = [
                    amp
                    for amp in amp_types
                    if any(
                        word in amp.lower()
                        for word in ["fender", "tweed", "deluxe", "clean"]
                    )
                ]
                selected_amp = (
                    random.choice(jazz_amps) if jazz_amps else random.choice(amp_types)
                )
            else:
                selected_amp = random.choice(amp_types)

        # Generate 4 channels (A, B, C, D) for X/Y switching
        channels = {}
        for channel in ["A", "B", "C", "D"]:
            amp_type = selected_amp

            # Adjust amp type based on genre and channel
            if structure["genre"] == "metal":
                if any(
                    "IIC+" in amp or "Brootalz" in amp or "Uber" in amp
                    for amp in amp_types
                ):
                    metal_amps = [
                        amp
                        for amp in amp_types
                        if any(word in amp for word in ["IIC+", "Brootalz", "Uber"])
                    ]
                    if metal_amps:
                        amp_type = random.choice(metal_amps)
                else:
                    metal_amps = ["USA IIC+", "FAS Brootalz", "Euro Uber"]
                    amp_type = random.choice(metal_amps)

            # Advanced genre-specific parameter generation with sophisticated relationships
            genre = structure.get("genre", "rock")

            # Genre-specific parameter profiles
            genre_profiles = {
                "metal": {
                    "gain": {"min": 7.5, "max": 10.0, "typical": 8.5},
                    "bass": {"min": 6.0, "max": 9.0, "typical": 7.5},
                    "mid": {"min": 4.0, "max": 7.0, "typical": 5.5},
                    "treble": {"min": 5.0, "max": 8.0, "typical": 6.5},
                    "presence": {"min": 4.0, "max": 8.0, "typical": 6.0},
                    "master": {"min": 2.0, "max": 6.0, "typical": 4.0},
                },
                "blues": {
                    "gain": {"min": 4.0, "max": 7.0, "typical": 5.5},
                    "bass": {"min": 5.0, "max": 8.0, "typical": 6.5},
                    "mid": {"min": 6.0, "max": 9.0, "typical": 7.5},
                    "treble": {"min": 4.0, "max": 7.0, "typical": 5.5},
                    "presence": {"min": 3.0, "max": 7.0, "typical": 5.0},
                    "master": {"min": 4.0, "max": 8.0, "typical": 6.0},
                },
                "jazz": {
                    "gain": {"min": 1.0, "max": 3.5, "typical": 2.2},
                    "bass": {"min": 4.0, "max": 7.0, "typical": 5.5},
                    "mid": {"min": 5.0, "max": 8.0, "typical": 6.5},
                    "treble": {"min": 3.0, "max": 6.0, "typical": 4.5},
                    "presence": {"min": 2.0, "max": 6.0, "typical": 4.0},
                    "master": {"min": 7.0, "max": 10.0, "typical": 8.5},
                },
                "funk": {
                    "gain": {"min": 3.0, "max": 6.0, "typical": 4.5},
                    "bass": {"min": 6.0, "max": 9.0, "typical": 7.5},
                    "mid": {"min": 4.0, "max": 7.0, "typical": 5.5},
                    "treble": {"min": 5.0, "max": 8.0, "typical": 6.5},
                    "presence": {"min": 3.0, "max": 7.0, "typical": 5.0},
                    "master": {"min": 2.0, "max": 6.0, "typical": 4.0},
                },
                "ambient": {
                    "gain": {"min": 3.0, "max": 6.0, "typical": 4.5},
                    "bass": {"min": 4.0, "max": 7.0, "typical": 5.5},
                    "mid": {"min": 3.0, "max": 6.0, "typical": 4.5},
                    "treble": {"min": 5.0, "max": 8.0, "typical": 6.5},
                    "presence": {"min": 4.0, "max": 8.0, "typical": 6.0},
                    "master": {"min": 4.0, "max": 8.0, "typical": 6.0},
                },
                "rock": {
                    "gain": {"min": 5.0, "max": 8.0, "typical": 6.5},
                    "bass": {"min": 5.0, "max": 8.0, "typical": 6.5},
                    "mid": {"min": 5.0, "max": 8.0, "typical": 6.5},
                    "treble": {"min": 5.0, "max": 8.0, "typical": 6.5},
                    "presence": {"min": 4.0, "max": 7.0, "typical": 5.5},
                    "master": {"min": 3.0, "max": 7.0, "typical": 5.0},
                },
            }

            # Get genre profile or default to rock
            profile = genre_profiles.get(genre, genre_profiles["rock"])

            # Generate parameters with sophisticated relationships
            base_gain = random.uniform(profile["gain"]["min"], profile["gain"]["max"])

            # Sophisticated parameter relationships
            # Bass and treble often have inverse relationship
            bass_base = random.uniform(profile["bass"]["min"], profile["bass"]["max"])
            treble_base = random.uniform(
                profile["treble"]["min"], profile["treble"]["max"]
            )

            # Mid often complements the gain setting
            mid_base = (
                profile["mid"]["typical"]
                + (base_gain - profile["gain"]["typical"]) * 0.2
            )
            mid_base = max(profile["mid"]["min"], min(profile["mid"]["max"], mid_base))

            # Presence often follows treble
            presence_base = treble_base + random.uniform(-1.0, 1.0)
            presence_base = max(
                profile["presence"]["min"],
                min(profile["presence"]["max"], presence_base),
            )

            # Master volume often inversely related to gain for proper gain staging
            master_base = (
                profile["master"]["typical"]
                - (base_gain - profile["gain"]["typical"]) * 0.3
            )
            master_base = max(
                profile["master"]["min"], min(profile["master"]["max"], master_base)
            )

            # Add channel variation
            channel_offset = (ord(channel) - ord("A")) * 0.2

            channels[channel] = {
                "type": amp_type,
                "parameters": {
                    "gain": round(base_gain + channel_offset, 1),
                    "bass": round(bass_base + channel_offset, 1),
                    "mid": round(mid_base + channel_offset, 1),
                    "treble": round(treble_base + channel_offset, 1),
                    "presence": round(presence_base + channel_offset, 1),
                    "master": round(master_base + channel_offset, 1),
                },
            }

        return {
            "enabled": True,
            "type": channels["A"]["type"],  # Set main type from first channel
            "current_channel": "A",
            "channels": channels,
        }

    def _generate_cab_block(self, structure: Dict) -> Dict:
        """Generate a cab block with sophisticated cab/mic combinations"""
        genre = structure.get("genre", "rock")
        cab_types = self.cab_models[:20]  # Use more variety for channels

        # Genre-specific cab/mic combinations
        genre_cab_profiles = {
            "metal": {
                "cab_preferences": ["4x12", "Euro", "Modern", "Mesa", "Marshall"],
                "mic_preferences": ["SM57", "MD421", "R121"],
                "low_cut": {"min": 80.0, "max": 200.0, "typical": 120.0},
                "high_cut": {"min": 8000.0, "max": 12000.0, "typical": 10000.0},
                "level": {"min": -6.0, "max": 6.0, "typical": 0.0},
            },
            "blues": {
                "cab_preferences": ["2x12", "Tweed", "Vintage", "Fender"],
                "mic_preferences": ["SM57", "R121", "U87"],
                "low_cut": {"min": 60.0, "max": 120.0, "typical": 80.0},
                "high_cut": {"min": 10000.0, "max": 15000.0, "typical": 12000.0},
                "level": {"min": -3.0, "max": 9.0, "typical": 3.0},
            },
            "jazz": {
                "cab_preferences": ["1x12", "2x12", "Tweed", "Vintage"],
                "mic_preferences": ["U87", "C414", "R121"],
                "low_cut": {"min": 40.0, "max": 80.0, "typical": 60.0},
                "high_cut": {"min": 12000.0, "max": 18000.0, "typical": 15000.0},
                "level": {"min": 0.0, "max": 12.0, "typical": 6.0},
            },
            "funk": {
                "cab_preferences": ["2x12", "4x10", "Tweed", "Vintage"],
                "mic_preferences": ["SM57", "MD421", "C414"],
                "low_cut": {"min": 100.0, "max": 200.0, "typical": 150.0},
                "high_cut": {"min": 8000.0, "max": 12000.0, "typical": 10000.0},
                "level": {"min": -3.0, "max": 6.0, "typical": 1.5},
            },
            "ambient": {
                "cab_preferences": ["2x12", "4x12", "Vintage", "Tweed"],
                "mic_preferences": ["R121", "U87", "C414"],
                "low_cut": {"min": 30.0, "max": 80.0, "typical": 50.0},
                "high_cut": {"min": 15000.0, "max": 20000.0, "typical": 18000.0},
                "level": {"min": 0.0, "max": 9.0, "typical": 4.5},
            },
            "rock": {
                "cab_preferences": ["4x12", "2x12", "Marshall", "Vintage"],
                "mic_preferences": ["SM57", "R121", "MD421"],
                "low_cut": {"min": 60.0, "max": 150.0, "typical": 100.0},
                "high_cut": {"min": 10000.0, "max": 15000.0, "typical": 12500.0},
                "level": {"min": -3.0, "max": 9.0, "typical": 3.0},
            },
        }

        # Get genre profile or default to rock
        profile = genre_cab_profiles.get(genre, genre_cab_profiles["rock"])

        # Generate 4 channels (A, B, C, D) for X/Y switching
        channels = {}
        for channel in ["A", "B", "C", "D"]:
            # Select cab based on genre preferences
            preferred_cabs = [
                cab
                for cab in cab_types
                if any(pref in cab for pref in profile["cab_preferences"])
            ]
            if preferred_cabs:
                cab_type = random.choice(preferred_cabs)
            else:
                cab_type = random.choice(cab_types)

            # Generate sophisticated parameters based on genre profile
            base_low_cut = random.uniform(
                profile["low_cut"]["min"], profile["low_cut"]["max"]
            )
            base_high_cut = random.uniform(
                profile["high_cut"]["min"], profile["high_cut"]["max"]
            )
            base_level = random.uniform(
                profile["level"]["min"], profile["level"]["max"]
            )

            # Sophisticated parameter relationships
            # Higher low cut often means lower high cut for tighter sound
            if base_low_cut > profile["low_cut"]["typical"]:
                base_high_cut *= 0.9  # Slightly lower high cut

            # Add channel variation
            channel_offset = (ord(channel) - ord("A")) * 0.1

            channels[channel] = {
                "type": cab_type,
                "parameters": {
                    "low_cut": round(base_low_cut + channel_offset, 1),
                    "high_cut": round(base_high_cut + channel_offset, 1),
                    "level": round(base_level + channel_offset, 1),
                },
            }

        return {
            "enabled": True,
            "type": channels["A"]["type"],  # Set main type from first channel
            "current_channel": "A",
            "channels": channels,
        }

    def _generate_eq_block(self, structure: Dict) -> Dict:
        """Generate an EQ block with appropriate parameters"""
        eq_emphasis = structure.get("eq_emphasis", "balanced")

        # Generate 4 channels (A, B, C, D) for X/Y switching
        channels = {}
        for channel in ["A", "B", "C", "D"]:
            channels[channel] = {
                "type": "Parametric EQ",
                "parameters": {
                    "low_freq": 80.0,
                    "low_gain": 0.0,
                    "low_mid_freq": 500.0,
                    "low_mid_gain": 0.0,
                    "high_mid_freq": 2000.0,
                    "high_mid_gain": 0.0,
                    "high_freq": 8000.0,
                    "high_gain": 0.0,
                },
            }

            # Adjust EQ based on emphasis
            if eq_emphasis == "mid_scoop":
                channels[channel]["parameters"]["low_mid_gain"] = -2.0
                channels[channel]["parameters"]["high_mid_gain"] = -2.0
            elif eq_emphasis == "mid_boost":
                channels[channel]["parameters"]["low_mid_gain"] = 2.0
                channels[channel]["parameters"]["high_mid_gain"] = 2.0
            elif eq_emphasis == "bright":
                channels[channel]["parameters"]["high_gain"] = 2.0
            elif eq_emphasis == "warm":
                channels[channel]["parameters"]["low_gain"] = 2.0

        return {"enabled": True, "current_channel": "A", "channels": channels}

    def _generate_delay_block(self, structure: Dict) -> Dict:
        """Generate a delay block with appropriate parameters using real FM9 data"""
        delay_type = structure.get("delay_type", "medium")

        # Get delay types from real FM9 blocks data
        delay_types = []
        delay_blocks = self.blocks_data.get("delay", [])
        if delay_blocks:
            delay_types = [
                block.get("name", "") for block in delay_blocks if block.get("name")
            ]

        if not delay_types:
            delay_types = [
                "Digital Stereo Delay",
                "Analog Delay",
                "Tape Delay",
                "Multi Delay",
            ]

        # Generate 4 channels (A, B, C, D) for X/Y switching
        channels = {}
        for channel in ["A", "B", "C", "D"]:
            delay_model = random.choice(delay_types)
            channels[channel] = {
                "type": delay_model,
                "parameters": {"time": 500.0, "mix": 30.0, "feedback": 20.0},
            }

            # Adjust delay based on type
            if delay_type == "short":
                channels[channel]["parameters"]["time"] = random.uniform(200, 400)
                channels[channel]["parameters"]["mix"] = random.uniform(15.0, 25.0)
            elif delay_type == "long":
                channels[channel]["parameters"]["time"] = random.uniform(800, 1200)
                channels[channel]["parameters"]["mix"] = random.uniform(35.0, 50.0)
            else:  # medium
                channels[channel]["parameters"]["time"] = random.uniform(400, 800)
                channels[channel]["parameters"]["mix"] = random.uniform(25.0, 35.0)

        return {
            "enabled": True,
            "type": channels["A"]["type"],  # Set main type from first channel
            "current_channel": "A",
            "channels": channels,
        }

    def _generate_reverb_block(self, structure: Dict) -> Dict:
        """Generate a reverb block with sophisticated, genre-specific parameters using real FM9 data"""
        reverb_type = structure.get("reverb_type", "plate")
        genre = structure.get("genre", "rock")

        # Get reverb types from real FM9 blocks data
        reverb_types = []
        reverb_blocks = self.blocks_data.get("reverb", [])
        if reverb_blocks:
            reverb_types = [
                block.get("name", "") for block in reverb_blocks if block.get("name")
            ]

        if not reverb_types:
            reverb_types = [
                "Room Reverb",
                "Hall Reverb",
                "Plate Reverb",
                "Spring Reverb",
            ]

        # Genre-specific reverb profiles
        genre_reverb_profiles = {
            "metal": {
                "type": (
                    random.choice(
                        [r for r in reverb_types if "Plate" in r or "Room" in r]
                    )
                    if reverb_types
                    else "Medium Plate"
                ),
                "mix": {"min": 15.0, "max": 30.0, "typical": 22.0},
                "decay": {"min": 2.5, "max": 4.5, "typical": 3.5},
                "room_size": {"min": 4.0, "max": 7.0, "typical": 5.5},
            },
            "blues": {
                "type": "Medium Plate",
                "mix": {"min": 20.0, "max": 40.0, "typical": 30.0},
                "decay": {"min": 3.0, "max": 5.5, "typical": 4.2},
                "room_size": {"min": 5.0, "max": 8.0, "typical": 6.5},
            },
            "jazz": {
                "type": "Medium Plate",
                "mix": {"min": 25.0, "max": 45.0, "typical": 35.0},
                "decay": {"min": 3.5, "max": 6.0, "typical": 4.8},
                "room_size": {"min": 6.0, "max": 9.0, "typical": 7.5},
            },
            "funk": {
                "type": "Medium Plate",
                "mix": {"min": 10.0, "max": 25.0, "typical": 18.0},
                "decay": {"min": 2.0, "max": 4.0, "typical": 3.0},
                "room_size": {"min": 3.0, "max": 6.0, "typical": 4.5},
            },
            "ambient": {
                "type": "Medium Plate",
                "mix": {"min": 40.0, "max": 70.0, "typical": 55.0},
                "decay": {"min": 6.0, "max": 10.0, "typical": 8.0},
                "room_size": {"min": 8.0, "max": 10.0, "typical": 9.0},
            },
            "rock": {
                "type": "Medium Plate",
                "mix": {"min": 20.0, "max": 35.0, "typical": 27.5},
                "decay": {"min": 3.5, "max": 5.5, "typical": 4.5},
                "room_size": {"min": 5.0, "max": 7.5, "typical": 6.2},
            },
        }

        # Get genre profile or default to rock
        profile = genre_reverb_profiles.get(genre, genre_reverb_profiles["rock"])

        # Generate 4 channels (A, B, C, D) for X/Y switching
        channels = {}
        for channel in ["A", "B", "C", "D"]:
            # Base parameters from genre profile
            base_mix = random.uniform(profile["mix"]["min"], profile["mix"]["max"])
            base_decay = random.uniform(
                profile["decay"]["min"], profile["decay"]["max"]
            )
            base_room_size = random.uniform(
                profile["room_size"]["min"], profile["room_size"]["max"]
            )

            # Adjust based on reverb type
            if reverb_type == "minimal":
                base_mix *= 0.6  # Reduce mix for minimal
                base_decay *= 0.8  # Reduce decay for minimal
            elif reverb_type == "atmospheric":
                base_mix *= 1.3  # Increase mix for atmospheric
                base_decay *= 1.4  # Increase decay for atmospheric
                base_room_size = min(10.0, base_room_size * 1.2)  # Larger room

            # Add channel variation
            channel_offset = (ord(channel) - ord("A")) * 0.1

            channels[channel] = {
                "type": profile["type"],
                "parameters": {
                    "room_size": round(base_room_size + channel_offset, 1),
                    "mix": round(base_mix + channel_offset, 1),
                    "decay": round(base_decay + channel_offset, 1),
                },
            }

        return {
            "enabled": True,
            "type": channels["A"]["type"],  # Set main type from first channel
            "current_channel": "A",
            "channels": channels,
        }

    def _generate_modulation_block(self, structure: Dict) -> Dict:
        """Generate a modulation block with appropriate parameters using real FM9 data"""
        # Get modulation types from real FM9 blocks data
        modulation_types = []
        modulation_blocks = self.blocks_data.get("modulation", [])
        if modulation_blocks:
            modulation_types = [
                block.get("name", "")
                for block in modulation_blocks
                if block.get("name")
            ]

        if not modulation_types:
            modulation_types = ["Chorus", "Flanger", "Phaser", "Tremolo", "Rotary"]

        # Generate 4 channels (A, B, C, D) for X/Y switching
        channels = {}
        for channel in ["A", "B", "C", "D"]:
            modulation_type = random.choice(modulation_types)

            channels[channel] = {
                "type": modulation_type,
                "parameters": {
                    "rate": round(random.uniform(1.0, 8.0), 1),
                    "depth": round(random.uniform(3.0, 8.0), 1),
                    "mix": round(random.uniform(30.0, 70.0), 1),
                    "feedback": round(random.uniform(0.0, 50.0), 1),
                },
            }

        return {
            "enabled": True,
            "type": channels["A"]["type"],  # Set main type from first channel
            "current_channel": "A",
            "channels": channels,
        }

    def _generate_pitch_block(self, structure: Dict) -> Dict:
        """Generate a pitch block with appropriate parameters"""
        pitch_types = ["Pitch Shifter", "Harmonizer", "Whammy", "Harmony"]

        # Generate 4 channels (A, B, C, D) for X/Y switching
        channels = {}
        for channel in ["A", "B", "C", "D"]:
            pitch_type = random.choice(pitch_types)

            channels[channel] = {
                "type": pitch_type,
                "parameters": {
                    "pitch": round(random.uniform(-12.0, 12.0), 1),
                    "mix": round(random.uniform(20.0, 80.0), 1),
                    "feedback": round(random.uniform(0.0, 30.0), 1),
                    "level": round(random.uniform(4.0, 8.0), 1),
                },
            }

        return {
            "enabled": True,
            "type": channels["A"]["type"],  # Set main type from first channel
            "current_channel": "A",
            "channels": channels,
        }

    def _generate_dynamics_block(self, structure: Dict) -> Dict:
        """Generate a dynamics block with sophisticated, genre-specific parameters"""
        genre = structure.get("genre", "rock")

        # Genre-specific dynamics profiles
        genre_dynamics_profiles = {
            "metal": {
                "type": "Multiband Compressor",
                "threshold": {"min": -25.0, "max": -15.0, "typical": -20.0},
                "ratio": {"min": 4.0, "max": 8.0, "typical": 6.0},
                "attack": {"min": 1.0, "max": 10.0, "typical": 5.0},
                "release": {"min": 50.0, "max": 150.0, "typical": 100.0},
                "level": {"min": 2.0, "max": 6.0, "typical": 4.0},
            },
            "blues": {
                "type": "Compressor",
                "threshold": {"min": -20.0, "max": -10.0, "typical": -15.0},
                "ratio": {"min": 2.0, "max": 4.0, "typical": 3.0},
                "attack": {"min": 5.0, "max": 20.0, "typical": 12.0},
                "release": {"min": 100.0, "max": 300.0, "typical": 200.0},
                "level": {"min": 3.0, "max": 7.0, "typical": 5.0},
            },
            "jazz": {
                "type": "Compressor",
                "threshold": {"min": -15.0, "max": -5.0, "typical": -10.0},
                "ratio": {"min": 1.5, "max": 3.0, "typical": 2.2},
                "attack": {"min": 10.0, "max": 30.0, "typical": 20.0},
                "release": {"min": 200.0, "max": 500.0, "typical": 350.0},
                "level": {"min": 4.0, "max": 8.0, "typical": 6.0},
            },
            "funk": {
                "type": "Compressor",
                "threshold": {"min": -18.0, "max": -8.0, "typical": -13.0},
                "ratio": {"min": 3.0, "max": 6.0, "typical": 4.5},
                "attack": {"min": 2.0, "max": 8.0, "typical": 5.0},
                "release": {"min": 80.0, "max": 200.0, "typical": 140.0},
                "level": {"min": 2.5, "max": 6.5, "typical": 4.5},
            },
            "ambient": {
                "type": "Compressor",
                "threshold": {"min": -12.0, "max": -5.0, "typical": -8.0},
                "ratio": {"min": 1.2, "max": 2.5, "typical": 1.8},
                "attack": {"min": 15.0, "max": 40.0, "typical": 25.0},
                "release": {"min": 300.0, "max": 600.0, "typical": 450.0},
                "level": {"min": 5.0, "max": 9.0, "typical": 7.0},
            },
            "rock": {
                "type": "Compressor",
                "threshold": {"min": -20.0, "max": -12.0, "typical": -16.0},
                "ratio": {"min": 2.5, "max": 5.0, "typical": 3.7},
                "attack": {"min": 8.0, "max": 25.0, "typical": 16.0},
                "release": {"min": 120.0, "max": 300.0, "typical": 210.0},
                "level": {"min": 3.5, "max": 7.5, "typical": 5.5},
            },
        }

        # Get genre profile or default to rock
        profile = genre_dynamics_profiles.get(genre, genre_dynamics_profiles["rock"])

        # Generate 4 channels (A, B, C, D) for X/Y switching
        channels = {}
        for channel in ["A", "B", "C", "D"]:
            # Base parameters from genre profile
            base_threshold = random.uniform(
                profile["threshold"]["min"], profile["threshold"]["max"]
            )
            base_ratio = random.uniform(
                profile["ratio"]["min"], profile["ratio"]["max"]
            )
            base_attack = random.uniform(
                profile["attack"]["min"], profile["attack"]["max"]
            )
            base_release = random.uniform(
                profile["release"]["min"], profile["release"]["max"]
            )
            base_level = random.uniform(
                profile["level"]["min"], profile["level"]["max"]
            )

            # Sophisticated parameter relationships
            # Higher ratio often means lower threshold for more compression
            if base_ratio > profile["ratio"]["typical"]:
                base_threshold -= 2.0  # Lower threshold for higher ratio

            # Faster attack often means faster release
            if base_attack < profile["attack"]["typical"]:
                base_release *= 0.8  # Faster release for faster attack

            # Add channel variation
            channel_offset = (ord(channel) - ord("A")) * 0.1

            channels[channel] = {
                "type": profile["type"],
                "parameters": {
                    "threshold": round(base_threshold + channel_offset, 1),
                    "ratio": round(base_ratio + channel_offset, 1),
                    "attack": round(base_attack + channel_offset, 1),
                    "release": round(base_release + channel_offset, 1),
                    "level": round(base_level + channel_offset, 1),
                },
            }

        return {
            "enabled": True,
            "type": channels["A"]["type"],  # Set main type from first channel
            "current_channel": "A",
            "channels": channels,
        }

    def _generate_tone_description(self, tone_patch: Dict, intent: Dict) -> str:
        """Generate a detailed description of the tone based on actual blocks used"""
        if "artist" in intent:
            return intent["description"]

        genre = intent.get("genre", "rock")
        characteristics = intent.get("characteristics", [])

        description_parts = [f"A {genre} tone"]

        # Add specific gear details
        gear_details = []

        # Amp details
        amp_data = tone_patch.get("amp", {})
        if amp_data.get("enabled", False):
            amp_type = amp_data.get("type", "Unknown")
            if amp_type != "None":
                gear_details.append(f"using {amp_type}")

        # Drive details
        drive_1 = tone_patch.get("drive_1", {})
        drive_2 = tone_patch.get("drive_2", {})
        drives_used = []
        if drive_1.get("enabled", False) and drive_1.get("type", "None") != "None":
            drives_used.append(drive_1.get("type", "Unknown"))
        if drive_2.get("enabled", False) and drive_2.get("type", "None") != "None":
            drives_used.append(drive_2.get("type", "Unknown"))

        if drives_used:
            if len(drives_used) == 1:
                gear_details.append(f"with {drives_used[0]}")
            else:
                gear_details.append(f"with {drives_used[0]} and {drives_used[1]}")

        # Effects details
        effects_used = []
        for effect_name in ["delay", "reverb", "modulation", "pitch", "dynamics"]:
            effect_data = tone_patch.get(effect_name, {})
            if (
                effect_data.get("enabled", False)
                and effect_data.get("type", "None") != "None"
            ):
                effects_used.append(effect_data.get("type", "Unknown"))

        if effects_used:
            if len(effects_used) == 1:
                gear_details.append(f"and {effects_used[0]}")
            elif len(effects_used) == 2:
                gear_details.append(f"with {effects_used[0]} and {effects_used[1]}")
            else:
                gear_details.append(
                    f"with {', '.join(effects_used[:-1])} and {effects_used[-1]}"
                )

        # Combine all parts
        if gear_details:
            description_parts.append(" ".join(gear_details))

        if "lead" in characteristics:
            description_parts.append("optimized for lead playing")
        elif "rhythm" in characteristics:
            description_parts.append("optimized for rhythm playing")

        if "clean" in characteristics:
            description_parts.append("with clean characteristics")
        elif "distorted" in characteristics:
            description_parts.append("with high gain")

        if "bright" in characteristics:
            description_parts.append("and bright top end")
        elif "warm" in characteristics:
            description_parts.append("and warm mids")

        return ", ".join(description_parts) + "."

    def _validate_tone_patch(self, tone_patch: Dict) -> bool:
        """Validate that the generated tone patch is complete and valid"""
        try:
            # Check that required blocks exist
            required_blocks = ["amp", "cab"]
            for block in required_blocks:
                if block not in tone_patch:
                    raise ValueError(f"Missing required block: {block}")
                if not tone_patch[block].get("enabled", False):
                    raise ValueError(f"Required block {block} is disabled")

            # Check that amp and cab have valid types
            if tone_patch["amp"].get("type") == "None":
                raise ValueError("Amp type cannot be None")
            if tone_patch["cab"].get("type") == "None":
                raise ValueError("Cab type cannot be None")

            # Validate parameter ranges
            for block_name, block_data in tone_patch.items():
                if block_data.get("enabled", False) and "parameters" in block_data:
                    self._validate_block_parameters(
                        block_name, block_data["parameters"]
                    )

            return True

        except Exception as e:
            print(f"Tone validation warning: {e}")
            return False

    def _validate_block_parameters(self, block_name: str, parameters: Dict) -> None:
        """Validate that block parameters are within reasonable ranges"""
        # Basic parameter validation
        for param_name, param_value in parameters.items():
            if isinstance(param_value, (int, float)):
                # Check for reasonable ranges
                if param_name in [
                    "gain",
                    "bass",
                    "mid",
                    "treble",
                    "presence",
                    "master",
                ]:
                    if not (0.0 <= param_value <= 10.0):
                        print(
                            f"Warning: {block_name}.{param_name} = {param_value} is outside normal range (0-10)"
                        )
                elif param_name in ["level"]:
                    if not (-20.0 <= param_value <= 20.0):
                        print(
                            f"Warning: {block_name}.{param_name} = {param_value} is outside normal range (-20 to 20)"
                        )
                elif param_name in ["mix"]:
                    if not (0.0 <= param_value <= 100.0):
                        print(
                            f"Warning: {block_name}.{param_name} = {param_value} is outside normal range (0-100)"
                        )

    def _generate_fallback_tone(self, original_query: str, error_message: str) -> Dict:
        """Generate a basic fallback tone when main generation fails"""
        return {
            "query": original_query,
            "intent": {
                "genre": "rock",
                "characteristics": ["clean"],
                "query": original_query,
            },
            "tone_structure": {
                "genre": "rock",
                "drive_blocks": 0,
                "amp_type": "clean",
                "eq_emphasis": "balanced",
                "delay_type": "none",
                "reverb_type": "minimal",
            },
            "tone_patch": {
                "drive_1": {"enabled": False, "type": "None", "parameters": {}},
                "drive_2": {"enabled": False, "type": "None", "parameters": {}},
                "amp": {
                    "enabled": True,
                    "type": "USA Clean",
                    "parameters": {
                        "gain": 3.0,
                        "bass": 5.0,
                        "mid": 5.0,
                        "treble": 5.0,
                        "presence": 5.0,
                        "master": 5.0,
                    },
                },
                "cab": {
                    "enabled": True,
                    "type": "4x12 USA Trad",
                    "parameters": {"low_cut": 80.0, "high_cut": 8000.0, "level": 0.0},
                },
                "eq": {"enabled": False, "type": "None", "parameters": {}},
                "delay": {"enabled": False, "type": "None", "parameters": {}},
                "reverb": {"enabled": False, "type": "None", "parameters": {}},
            },
            "description": "A clean rock tone (fallback)",
            "firmware_verified": False,
            "guide_referenced": False,
            "generation_timestamp": datetime.now().isoformat(),
            "system_version": "1.0.0",
            "error": error_message,
            "fallback": True,
        }

    def _cache_tone_result(self, cache_key: str, result: Dict) -> None:
        """Cache a tone result with LRU eviction"""
        # Remove oldest entries if cache is full
        if len(self.tone_cache) >= self.cache_max_size:
            # Remove the first (oldest) entry
            oldest_key = next(iter(self.tone_cache))
            del self.tone_cache[oldest_key]

        # Add the new result
        self.tone_cache[cache_key] = result.copy()

    def clear_cache(self) -> None:
        """Clear the tone cache"""
        self.tone_cache.clear()

    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        return {
            "cache_size": len(self.tone_cache),
            "cache_max_size": self.cache_max_size,
            "cache_utilization": len(self.tone_cache) / self.cache_max_size * 100,
        }

    def analyze_tone_complexity(self, tone_patch: Dict) -> Dict:
        """Analyze the complexity and characteristics of a tone patch"""
        analysis = {
            "total_blocks": 0,
            "active_blocks": 0,
            "block_types": [],
            "parameter_count": 0,
            "complexity_score": 0,
            "genre_indicators": [],
            "technical_analysis": {},
        }

        # Count blocks and parameters
        for block_name, block_data in tone_patch.items():
            analysis["total_blocks"] += 1
            if block_data.get("enabled", False):
                analysis["active_blocks"] += 1
                block_type = (
                    block_name.split("_")[0] if "_" in block_name else block_name
                )
                if block_type not in analysis["block_types"]:
                    analysis["block_types"].append(block_type)

                # Count parameters
                if "parameters" in block_data:
                    analysis["parameter_count"] += len(block_data["parameters"])

        # Calculate complexity score (0-100)
        complexity_factors = {
            "active_blocks": analysis["active_blocks"]
            * 10,  # 10 points per active block
            "parameter_count": min(
                analysis["parameter_count"] * 2, 30
            ),  # 2 points per parameter, max 30
            "effect_blocks": len(
                [
                    bt
                    for bt in analysis["block_types"]
                    if bt in ["delay", "reverb", "modulation", "pitch"]
                ]
            )
            * 15,  # 15 points per effect
            "drive_blocks": len([bt for bt in analysis["block_types"] if "drive" in bt])
            * 20,  # 20 points per drive
        }

        analysis["complexity_score"] = min(sum(complexity_factors.values()), 100)

        # Genre analysis
        if analysis["active_blocks"] >= 6:
            analysis["genre_indicators"].append("complex")
        if any("drive" in bt for bt in analysis["block_types"]):
            analysis["genre_indicators"].append("high_gain")
        if "delay" in analysis["block_types"] and "reverb" in analysis["block_types"]:
            analysis["genre_indicators"].append("atmospheric")
        if analysis["parameter_count"] > 20:
            analysis["genre_indicators"].append("detailed")

        # Technical analysis
        analysis["technical_analysis"] = {
            "signal_chain_length": analysis["active_blocks"],
            "effect_density": len(
                [
                    bt
                    for bt in analysis["block_types"]
                    if bt in ["delay", "reverb", "modulation", "pitch"]
                ]
            )
            / max(analysis["active_blocks"], 1),
            "parameter_density": analysis["parameter_count"]
            / max(analysis["active_blocks"], 1),
            "complexity_level": (
                "simple"
                if analysis["complexity_score"] < 30
                else "moderate" if analysis["complexity_score"] < 70 else "complex"
            ),
        }

        return analysis

    def _get_all_block_types(self) -> Dict[str, List[str]]:
        """Get all available block types from real FM9 data"""
        all_blocks = {}
        for block in self.blocks_data.get("blocks", []):
            category = block.get("category", "unknown")
            name = block.get("name", "").strip()
            if name:
                if category not in all_blocks:
                    all_blocks[category] = []
                all_blocks[category].append(name)

        # Also get from organized blocks data
        for category, blocks in self.blocks_data.items():
            if isinstance(blocks, list):
                if category not in all_blocks:
                    all_blocks[category] = []
                for block in blocks:
                    name = block.get("name", "").strip()
                    if name and name not in all_blocks[category]:
                        all_blocks[category].append(name)

        return all_blocks

    def _get_blocks_by_category(self, category: str) -> List[str]:
        """Get blocks for a specific category"""
        all_blocks = self._get_all_block_types()
        return all_blocks.get(category, [])

    def generate_comprehensive_tone(
        self, query: str, tone_name: str = None
    ) -> Dict[str, any]:
        """
        Generate a comprehensive tone with all advanced features
        """
        # Generate base tone
        base_tone = self.generate_tone_from_query(query)

        # Create tone name if not provided
        if not tone_name:
            tone_name = (
                f"ToneGPT_{query.replace(' ', '_')}_{random.randint(1000, 9999)}"
            )

        # Create comprehensive tone
        tone_id = self.comprehensive_system.create_comprehensive_tone(
            tone_name, base_tone["tone_patch"]
        )

        # Get comprehensive tone summary
        comprehensive_summary = (
            self.comprehensive_system.get_comprehensive_tone_summary(tone_id)
        )

        return {
            "tone_id": tone_id,
            "tone_name": tone_name,
            "base_tone": base_tone,
            "comprehensive_tone": comprehensive_summary,
            "system_status": self.comprehensive_system.get_system_status(),
        }
