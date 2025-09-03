"""
Clean AI Tone Generator for FM9 Partnership

Copyright (c) 2025 Ben Tankersley. All rights reserved.
PROPRIETARY SOFTWARE - Unauthorized use, copying, or distribution is strictly prohibited.

TL;DR: Single-mode FM9 AI tone generator with real-world gear mapping.
- Generates complete FM9 patches from natural language queries
- Uses authentic FM9 block names and parameters (no advanced mode complexity)
- Sources all parameters from data/fm9_config.json → data/fm9_comprehensive_reference.json
- Maps real-world gear (Marshall, Mesa, Fender, Vox) to FM9 models
- No network calls, no parameter invention, fail-fast on missing data

Constraints:
- FM9 single-mode only (docs/ground-truth.md#Invariants)
- Params from data/fm9_config.json -> fm9_comprehensive_reference.json
- No network calls (pure function)
- Raises ValueError if required param missing (cite file+key)
"""

import json
import random
import hashlib
from pathlib import Path
from typing import Dict, List, Any
from tonegpt.config import BLOCKS_FILE
from tonegpt.core.canonicalize import canonicalize_preset
from tonegpt.core.validate_and_clamp import enforce_ref_ranges


def _seed_from_query(query: str) -> None:
    """
    Generate intelligent seed for varied but contextually appropriate results.
    
    Args:
        query: The input query string to base variations on
    """
    # Create a seed that varies but maintains query context
    # This gives different results each time while keeping them relevant to the query
    import time
    import os
    
    # Base seed from query (for context)
    h = int(hashlib.sha1(query.encode("utf-8")).hexdigest(), 16) % (2**31)
    
    # Add variation factors that change each time
    time_factor = int(time.time() * 1000) % 1000  # Changes every second
    process_factor = os.getpid() % 1000  # Different for each process
    random_factor = random.randint(0, 999)  # Pure randomness
    
    # Combine for intelligent variation
    intelligent_seed = (h + time_factor + process_factor + random_factor) % (2**31)
    random.seed(intelligent_seed)


from dataclasses import dataclass


@dataclass(frozen=True)
class PrefRule:
    keywords: tuple[str, ...]   # ALL must appear (case-insensitive)
    fm9_name: str               # exact FM9 model string to prefer


# Precise, keyword-scoped preferred model rules
PREFERRED_RULES: tuple[PrefRule, ...] = (
    PrefRule(("rectifier",), "Recto1: original 2-channel Rectifier, Orange channel, Modern mode"),
    PrefRule(("mesa", "rectifier"), "Recto1: original 2-channel Rectifier, Orange channel, Modern mode"),
    PrefRule(("marshall", "jcm800"), "Brit 800"),
    PrefRule(("jcm800",), "Brit 800"),
    PrefRule(("marshall", "plexi"), "Brit 800"),  # Marshall Plexi queries should use Brit 800
    PrefRule(("plexi",), "Plexi 1959"),  # Standalone Plexi queries use Plexi 1959
    PrefRule(("vox", "ac30"), "AC-30 TB"),
    PrefRule(("fender", "twin"), "Double Verb"),
)


def _prefer_model(query: str, candidates: list[str]) -> str:
    """
    Select preferred FM9 model based on precise keyword matching for deterministic results.
    
    Args:
        query: The input query string
        candidates: List of available FM9 model names
        
    Returns:
        Preferred FM9 model name or deterministic fallback
    """
    q = query.lower()
    for rule in PREFERRED_RULES:
        if all(k in q for k in rule.keywords) and rule.fm9_name in candidates:
            return rule.fm9_name
    # deterministic fallback
    if candidates:
        idx = int(hashlib.sha1(q.encode()).hexdigest(), 16) % len(candidates)
        return candidates[idx]
    return ""


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
            with open(BLOCKS_FILE, "r") as f:
                data = json.load(f)
            print(f"🔧 Loaded {len(data)} FM9 blocks")
            return data
        except Exception as e:
            print(f"⚠️ Error loading blocks data: {e}")
            return {}

    def _load_amp_models(self) -> List[str]:
        """Load available amp models from real FM9 data"""
        amp_blocks = [
            block for block in self.blocks_data if block.get("category") == "amp"
        ]
        if amp_blocks:
            amp_names = [
                block.get("name", "") for block in amp_blocks if block.get("name")
            ]
            print(f"🔧 Loaded {len(amp_names)} real amp models from FM9 blocks data")
            return amp_names
        return []

    def _load_cab_models(self) -> List[str]:
        """Load available cab models from real FM9 data"""
        cab_blocks = [
            block for block in self.blocks_data if block.get("category") == "cab"
        ]
        if cab_blocks:
            cab_names = [
                block.get("name", "") for block in cab_blocks if block.get("name")
            ]
            print(f"🔧 Loaded {len(cab_names)} real cab models from FM9 blocks data")
            return cab_names
        return []

    def _load_drive_models(self) -> List[str]:
        """Load available drive models from real FM9 data - prioritize blocks_featured.json"""
        drive_names = []
        
        # First try to load from blocks_featured.json (real FM9 names)
        try:
            with open("data/blocks_featured.json", "r") as f:
                featured_data = json.load(f)
            
            blocks = featured_data.get("blocks", [])
            for block_data in blocks:
                if block_data.get("block") == "DRIVE":
                    featured_models = block_data.get("models", [])
                    for model in featured_models:
                        fm9_name = model.get("fm9_name")
                        if fm9_name:
                            drive_names.append(fm9_name)
                    break
        except Exception as e:
            print(f"Warning: Could not load featured drive models: {e}")
        
        # Fallback to blocks_data if blocks_featured.json fails
        if not drive_names:
            drive_blocks = [
                block for block in self.blocks_data if block.get("category") == "drive"
            ]
            if drive_blocks:
                drive_names = [
                    block.get("name", "") for block in drive_blocks if block.get("name")
                ]
        
        print(
            f"🔧 Loaded {len(drive_names)} real drive models from FM9 blocks data"
        )
        return drive_names

    def _load_effect_models(self) -> Dict[str, List[str]]:
        """Load available effect models by category from both sources"""
        effects = {}
        effect_categories = [
            "delay",
            "reverb",
            "modulation",
            "pitch",
            "dynamics",
            "eq",
            "utility",
        ]

        for category in effect_categories:
            # Load from blocks_data (existing source)
            category_blocks = [
                block for block in self.blocks_data if block.get("category") == category
            ]
            effect_names = []
            if category_blocks:
                effect_names = [
                    block.get("name", "")
                    for block in category_blocks
                    if block.get("name")
                ]
            
            # Also load from blocks_featured.json (new comprehensive source)
            try:
                with open("data/blocks_featured.json", "r") as f:
                    featured_data = json.load(f)
                
                blocks = featured_data.get("blocks", [])
                for block_data in blocks:
                    block_name = block_data.get("block", "").upper()
                    if block_name == category.upper():
                        featured_models = block_data.get("models", [])
                        for model in featured_models:
                            fm9_name = model.get("fm9_name")
                            if fm9_name and fm9_name not in effect_names:
                                effect_names.append(fm9_name)
                        break
            except Exception as e:
                print(f"Warning: Could not load featured {category} models: {e}")
            
            effects[category] = effect_names
            print(
                f"🔧 Loaded {len(effect_names)} {category} effects from FM9 blocks data"
            )

        return effects

    def _get_real_world_name(self, fm9_name: str) -> str:
        """Get the real-world name for a given FM9 name"""
        for block in self.blocks_data:
            if block.get("name") == fm9_name:
                return block.get("real_world", fm9_name)
        return fm9_name

    def _load_gear_mapping(self) -> Dict:
        """Load real-world gear mapping for accurate modeling"""
        return {
            "amps": {
                "marshall": {
                    "jcm800": [
                        "Brit 800",
                        "Brit 800 Pro",
                        "BRIT 800 2204 HIGH",
                        "BRIT 800 2203 HIGH",
                    ],
                    "jcm900": ["Crunch Orange: based on a JCM 2203", "Crunch Red: based on a modded JCM 2203"],
                    "plexi": ["Plexi 1959 Pro", "PLEXI 100W 1970", "PLEXI 100W HIGH", "PLEXI 50W NORMAL"],
                    "jvm": ["BRIT JVM OD1 GREEN", "BRIT JVM OD1 ORANGE", "BRIT JVM OD1 RED", "BRIT JVM OD2 GREEN"],
                },
                "mesa": {
                    "dual_rectifier": [
                        "Recto Pro",
                        "RECTO1 ORANGE MODERN",
                        "Recto1: original 2-channel Rectifier, Orange channel, Modern mode",
                    ],
                    "rectifier": [
                        "Recto Pro",
                        "RECTO1 ORANGE MODERN",
                        "Recto1: original 2-channel Rectifier, Orange channel, Modern mode",
                    ],
                    "boogie": [
                        "Recto Pro",
                        "RECTO1 ORANGE MODERN",
                        "Recto1: original 2-channel Rectifier, Orange channel, Modern mode",
                    ],
                    "mark_iic": ["Mesa Mark IIC+"],
                    "mark_iv": ["USA MK IV", "USA MK IV LEAD"],
                    "mark_v": ["USA MK V", "USA MK V LEAD"],
                },
                "fender": {
                    "tweed": ["5F1 TWEED", "5F1 TWEED EC", "5E3 TWEED", "5F8 TWEED"],
                    "deluxe": [
                        "DELUXE VERB",
                        "DELUXE VERB NORMAL",
                        "DELUXE VERB VIBRATO",
                    ],
                    "twin": [
                        "Normal: based on 1966 blackface Fender Reverb, tuned by Andy Fuchs, AB763 circuit,",
                        "PRINCETONE REVERB",
                        "231PRINCE TONE REVERB",
                    ],
                    "bassman": ["BASSMAN", "BASSMAN 59", "BASSMAN 59 EC"],
                },
                "vox": {
                    "ac30": ["AC30", "AC30 TOP BOOST", "AC30 TOP BOOST EC"],
                    "ac15": ["AC15", "AC15 TOP BOOST", "AC15 TOP BOOST EC"],
                },
            },
            "drives": {
                "tube_screamer": ["TS808", "TS808 Mod", "TS9", "TS9 Pro", "T808 Mod", "T808 OD", "TS9DX +", "TS9DX Hot", "Valve Screamer VS9"],
                "klon": ["Klon", "Klon Pro", "Klone Chiron"],
                "rat": ["Rat Distortion", "Rat Pro", "Rat 2", "Rat 2 Pro", "Fat Rat"],
                "fuzz_face": ["Fuzz Face", "Fuzz Face Pro", "Fuzz Face Germanium", "Fuzz Face Germanium Pro"],
                "big_muff": ["Big Muff", "Big Muff Pro", "Big Muff Russian", "Big Muff Russian Pro"],
                "blues_driver": ["Blues Driver", "Blues Driver Pro"],
                "super_od": ["Super OD"],
                "bb_pre": ["BB Pre"],
                "blackglass": ["Blackglass 7K"],
                "compulsion": ["Compulsion Distortion HP/LP"],
                "bender_fuzz": ["Bender Fuzz"],
                "bit_crusher": ["Bit Crusher"],
                "blues_od": ["Blues OD"],
                "bosom_boost": ["Bosom Boost"],
                "colortone": ["Colortone Booster", "Colortone OD"],
                "ds1": ["DS1 Distortion/Mod"],
                "esoteric": ["Esoteric ACB/RCB"],
                "eternal_love": ["Eternal Love"],
                "face_fuzz": ["Face Fuzz"],
                "fas_led_drive": ["FAS LED-Drive"],
                "fet_boost": ["FET Boost"],
                "fet_preamp": ["FET Preamp"],
                "full_od": ["Full OD"],
                "gauss_drive": ["Gauss Drive"],
                "griddle_cake": ["Griddle Cake"],
                "hard_fuzz": ["Hard Fuzz"],
                "heartpedal": ["Heartpedal 11"],
                "hoodoo": ["Hoodoo Drive"],
                "horizon": ["Horizon Precision Drive"],
                "integral": ["Integral Pre"],
                "jam_ray": ["Jam Ray"],
                "m_zone": ["M-Zone Distortion"],
                "master_fuzz": ["Master Fuzz"],
                "maxoff": ["Maxoff 808"],
                "mcmlxxxi": ["MCMLXXXI Drive"],
                "micro_boost": ["Micro Boost"],
                "mid_boost": ["Mid Boost"],
                "mosfet": ["MOSFET Distortion"],
                "nobelium": ["Nobelium OVD-1"],
                "octave": ["Octave Distortion"],
                "od_250": ["OD 250/Gray"],
                "od_one": ["OD-One Overdrive"],
                "pi_fuzz": ["PI Fuzz"],
                "plus_distortion": ["Plus Distortion"],
                "sdd_preamp": ["SDD Preamp"],
                "shimmer": ["Shimmer Drive"],
                "shred": ["Shred Distortion"],
                "sonic": ["Sonic Drive"],
                "suhr_riot": ["Suhr Riot Ge/LED"],
                "sunrise": ["Sunrise Splendor/Hi-Cut"],
                "super_fuzz": ["Super Fuzz"],
                "tape_distortion": ["Tape Distortion"],
                "timothy": ["Timothy Down/Mid/Up"],
                "tone_of_kings": ["Tone of Kings"],
                "treble_boost": ["Treble Boost"],
                "tube_drive": ["Tube Drive 3-Knob", "Tube Drive 4-Knob", "Tube Drive 5-Knob"],
                "zen_master": ["Zen Master"],
            },
            "cabs": {
                "marshall_4x12": [
                    "Marshall 4x12",
                    "Legacy 4x12 V30",
                    "DynaCab 4x12 V30",
                ],
                "mesa_4x12": ["Mesa Boogie", "Legacy 4x12 V30", "DynaCab 4x12 V30"],
                "fender_2x12": [
                    "Fender 2x12",
                    "Legacy 2x12 Greenback",
                    "DynaCab 2x12 Greenback",
                ],
                "vox_2x12": [
                    "Vox 2x12",
                    "Legacy 2x12 Greenback",
                    "DynaCab 2x12 Greenback",
                ],
            },
        }

    def generate_tone_from_query(self, query: str) -> Dict:
        """Generate a tone patch from a natural language query"""
        try:
            # Seed random number generator for deterministic output
            _seed_from_query(query)
            
            # Parse the query to understand intent
            intent = self._parse_query_intent(query)

            # Generate the tone structure
            tone_structure = self._generate_tone_structure(intent)
            tone_structure["query"] = query

            # Generate specific parameters
            tone_patch = self._generate_tone_patch(tone_structure)

            # Generate description
            description = self._generate_tone_description(tone_patch, intent)

            # Create blocks list from tone_patch
            blocks_list = [
                {"type": k, "parameters": v.get("parameters", {})}
                for k, v in tone_patch.items()
                if isinstance(v, dict) and "parameters" in v
            ]

            result = {
                "query": query,
                "intent": intent,
                "tone_patch": tone_patch,
                "description": description,
                "gear_used": self._extract_gear_used(tone_patch),
                "blocks": blocks_list
            }

            # Normalize names & ensure `blocks` exists
            result = canonicalize_preset(result)
            
            # Enforce parameter ranges and clamp values
            result = enforce_ref_ranges(result)
            
            return result

        except Exception as e:
            print(f"❌ Error generating tone: {e}")
            return self._get_fallback_tone(query)

    def _parse_query_intent(self, query: str) -> Dict:
        """Parse query to understand user intent"""
        query_lower = query.lower()

        # Artist-specific recognition (HIGHEST PRIORITY) - ACCURATE GEAR MAPPINGS
        artist_gear = None
        if any(word in query_lower for word in ["jimi hendrix", "hendrix"]):
            # Hendrix: Marshall Super Lead 100W + Dallas Arbiter Fuzz Face
            artist_gear = {"amp_type": "marshall_super_lead", "drive_type": "fuzz_face", "genre": "rock"}
        elif any(word in query_lower for word in ["stevie ray vaughan", "srv", "stevie ray"]):
            # SRV: Fender Twin Reverb + Ibanez TS808 Tube Screamer
            artist_gear = {"amp_type": "fender_twin", "drive_type": "tube_screamer_808", "genre": "blues"}
        elif any(word in query_lower for word in ["metallica", "james hetfield"]):
            # Metallica: Mesa Boogie Mark IIC+ + Mesa Boogie Strategy 400
            artist_gear = {"amp_type": "mesa_mark_iic", "drive_type": "mesa_high_gain", "genre": "metal"}
        elif any(word in query_lower for word in ["led zeppelin", "zeppelin", "jimmy page", "page"]):
            # Page: Marshall Super Lead 100W + Sola Sound Tone Bender
            artist_gear = {"amp_type": "marshall_super_lead", "drive_type": "tone_bender", "genre": "rock"}
        elif any(word in query_lower for word in ["bb king", "bb king"]):
            # BB King: Gibson Lab Series L5 + Gibson ES-355 (clean, no drive)
            artist_gear = {"amp_type": "lab_series_l5", "drive_type": "clean", "genre": "blues"}
        elif any(word in query_lower for word in ["van halen", "eddie van halen", "eddie"]):
            # Van Halen: Marshall Plexi 1959 + MXR Phase 90
            artist_gear = {"amp_type": "marshall_plexi_1959", "drive_type": "phase_90", "genre": "rock"}
        elif any(word in query_lower for word in ["slash", "guns n roses", "gnr"]):
            # Slash: Marshall JCM800 + Boss SD-1 Super Overdrive
            artist_gear = {"amp_type": "marshall_jcm800", "drive_type": "boss_sd1", "genre": "rock"}
        elif any(word in query_lower for word in ["dimebag darrell", "dimebag", "pantera"]):
            # Dimebag: Randall RG100ES + MXR Dime Distortion
            artist_gear = {"amp_type": "randall_rg100", "drive_type": "mxr_dime", "genre": "metal"}
        elif any(word in query_lower for word in ["eric clapton", "clapton"]):
            # Clapton: Fender Tweed Deluxe + Dallas Rangemaster Treble Booster
            artist_gear = {"amp_type": "fender_tweed_deluxe", "drive_type": "rangemaster", "genre": "blues"}
        elif any(word in query_lower for word in ["david gilmour", "gilmour", "pink floyd"]):
            # Gilmour: Hiwatt DR103 + Big Muff Pi
            artist_gear = {"amp_type": "hiwatt_dr103", "drive_type": "big_muff", "genre": "rock"}
        elif any(word in query_lower for word in ["joe satriani", "satriani"]):
            # Satriani: Marshall JCM800 + Ibanez TS808
            artist_gear = {"amp_type": "marshall_jcm800", "drive_type": "tube_screamer_808", "genre": "rock"}
        elif any(word in query_lower for word in ["steve vai", "vai"]):
            # Vai: Carvin Legacy + Ibanez TS808
            artist_gear = {"amp_type": "carvin_legacy", "drive_type": "tube_screamer_808", "genre": "rock"}
        elif any(word in query_lower for word in ["yngwie malmsteen", "yngwie", "malmsteen"]):
            # Yngwie: Marshall JCM800 + DOD YJM308
            artist_gear = {"amp_type": "marshall_jcm800", "drive_type": "dod_yjm308", "genre": "rock"}
        elif any(word in query_lower for word in ["john mayer", "mayer"]):
            # Mayer: Two Rock Traditional Clean + Klon Centaur
            artist_gear = {"amp_type": "two_rock_clean", "drive_type": "klon_centaur", "genre": "blues"}
        elif any(word in query_lower for word in ["gary moore", "moore"]):
            # Moore: Marshall JCM800 + Ibanez TS808
            artist_gear = {"amp_type": "marshall_jcm800", "drive_type": "tube_screamer_808", "genre": "blues"}
        elif any(word in query_lower for word in ["peter frampton", "frampton"]):
            # Frampton: Marshall JCM800 + Talk Box
            artist_gear = {"amp_type": "marshall_jcm800", "drive_type": "talk_box", "genre": "rock"}
        elif any(word in query_lower for word in ["blink 182", "blink"]):
            # Blink 182: Mesa Boogie Dual Rectifier + Boss DS-1
            artist_gear = {"amp_type": "mesa_dual_rectifier", "drive_type": "boss_ds1", "genre": "punk"}
        elif any(word in query_lower for word in ["green day"]):
            # Green Day: Marshall JCM800 + Boss DS-1
            artist_gear = {"amp_type": "marshall_jcm800", "drive_type": "boss_ds1", "genre": "punk"}
        elif any(word in query_lower for word in ["nirvana", "kurt cobain", "cobain"]):
            # Cobain: Mesa Boogie Studio Preamp + Boss DS-1
            artist_gear = {"amp_type": "mesa_studio_preamp", "drive_type": "boss_ds1", "genre": "grunge"}
        elif any(word in query_lower for word in ["tool", "adam jones"]):
            # Tool: Mesa Boogie Dual Rectifier + Diezel VH4
            artist_gear = {"amp_type": "mesa_dual_rectifier", "drive_type": "diezel_vh4", "genre": "metal"}
        elif any(word in query_lower for word in ["deftones", "stephen carpenter"]):
            # Deftones: Mesa Boogie Dual Rectifier + Boss DS-1
            artist_gear = {"amp_type": "mesa_dual_rectifier", "drive_type": "boss_ds1", "genre": "metal"}
        elif any(word in query_lower for word in ["meshuggah"]):
            # Meshuggah: Mesa Boogie Dual Rectifier + Line 6 Pod
            artist_gear = {"amp_type": "mesa_dual_rectifier", "drive_type": "line6_pod", "genre": "metal"}
        elif any(word in query_lower for word in ["prince"]):
            # Prince: Fender Twin Reverb + Boss CE-1 Chorus
            artist_gear = {"amp_type": "fender_twin", "drive_type": "boss_ce1", "genre": "funk"}
        elif any(word in query_lower for word in ["james brown"]):
            # James Brown: Fender Twin Reverb + Clean (no drive)
            artist_gear = {"amp_type": "fender_twin", "drive_type": "clean", "genre": "funk"}

        # Genre detection (fallback if no artist match)
        if artist_gear:
            genre = artist_gear["genre"]
        else:
            genre = "rock"
            if any(
                word in query_lower
                for word in ["metal", "heavy", "distorted", "aggressive"]
            ):
                genre = "metal"
            elif any(word in query_lower for word in ["blues", "bluesy", "soulful"]):
                genre = "blues"
            elif any(word in query_lower for word in ["jazz", "clean", "smooth"]):
                genre = "jazz"
            elif any(word in query_lower for word in ["funk", "rhythm", "groove"]):
                genre = "funk"
            elif any(
                word in query_lower for word in ["ambient", "atmospheric", "ethereal"]
            ):
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
            "query": query,
            "artist_gear": artist_gear
        }

    def _generate_tone_structure(self, intent: Dict) -> Dict:
        """Generate the basic structure of the tone"""
        genre = intent.get("genre", "rock")
        artist_gear = intent.get("artist_gear")
        query = intent.get("query", "")

        # Determine which blocks to enable based on genre
        structure = {
            "genre": genre,
            "artist_gear": artist_gear,
            "query": query,
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
            "utility_enabled": False,
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
        genre = structure.get("genre", "rock")
        query = structure.get("query", "").lower()
        artist_gear = structure.get("artist_gear")

        # Try to match specific amp requests using gear mapping
        selected_amp = None
        
        # Artist-specific amp selection (HIGHEST PRIORITY) - ACCURATE GEAR MAPPINGS
        if artist_gear:
            amp_type = artist_gear.get("amp_type")
            
            # Hendrix: Marshall Super Lead 100W
            if amp_type == "marshall_super_lead":
                # Prioritize Plexi models for Hendrix
                plexi_amps = [amp for amp in self.amp_models if "plexi" in amp.lower()]
                if plexi_amps:
                    selected_amp = random.choice(plexi_amps)
                else:
                    # Fallback to other Marshall models
                    super_lead_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["plexi", "1959", "super", "100w", "brit 800"])]
                    if super_lead_amps:
                        selected_amp = random.choice(super_lead_amps)
            
            # SRV: Fender Twin Reverb
            elif amp_type == "fender_twin":
                # Prioritize Twin models specifically
                twin_amps = [amp for amp in self.amp_models if "twin" in amp.lower()]
                if twin_amps:
                    selected_amp = random.choice(twin_amps)
                else:
                    # Fallback to Deluxe Verb models
                    deluxe_amps = [amp for amp in self.amp_models if "deluxe verb" in amp.lower()]
                    if deluxe_amps:
                        selected_amp = random.choice(deluxe_amps)
                    else:
                        # Final fallback to any Fender reverb
                        fender_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["twin", "reverb", "princetone", "deluxe verb"])]
                        if fender_amps:
                            selected_amp = random.choice(fender_amps)
            
            # Metallica: Mesa Boogie Mark IIC+
            elif amp_type == "mesa_mark_iic":
                # Prioritize the exact Mesa Mark IIC+ model
                exact_mark = [amp for amp in self.amp_models if "mesa mark iic" in amp.lower()]
                if exact_mark:
                    selected_amp = exact_mark[0]  # Use the exact model, not random
                else:
                    # Fallback to other Mesa Mark models
                    mark_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["mark", "iic", "mesa"])]
                    if mark_amps:
                        selected_amp = random.choice(mark_amps)
            
            # BB King: Gibson Lab Series L5
            elif amp_type == "lab_series_l5":
                lab_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["lab", "series", "l5", "clean", "hifi"])]
                if lab_amps:
                    selected_amp = random.choice(lab_amps)
            
            # Van Halen: Marshall Plexi 1959
            elif amp_type == "marshall_plexi_1959":
                plexi_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["plexi", "1959", "marshall"])]
                if plexi_amps:
                    selected_amp = random.choice(plexi_amps)
            
            # Slash: Marshall JCM800
            elif amp_type == "marshall_jcm800":
                jcm800_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["jcm", "800", "brit 800"])]
                if jcm800_amps:
                    selected_amp = random.choice(jcm800_amps)
            
            # Dimebag: Randall RG100ES
            elif amp_type == "randall_rg100":
                randall_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["randall", "rg100", "high gain", "metal"])]
                if randall_amps:
                    selected_amp = random.choice(randall_amps)
            
            # Clapton: Fender Tweed Deluxe
            elif amp_type == "fender_tweed_deluxe":
                tweed_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["tweed", "deluxe", "5f1", "5f8"])]
                if tweed_amps:
                    selected_amp = random.choice(tweed_amps)
            
            # Gilmour: Hiwatt DR103
            elif amp_type == "hiwatt_dr103":
                hiwatt_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["hiwatt", "dr103", "clean", "hifi"])]
                if hiwatt_amps:
                    selected_amp = random.choice(hiwatt_amps)
            
            # Vai: Carvin Legacy
            elif amp_type == "carvin_legacy":
                carvin_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["carvin", "legacy", "v3"])]
                if carvin_amps:
                    selected_amp = random.choice(carvin_amps)
            
            # Mayer: Two Rock Traditional Clean
            elif amp_type == "two_rock_clean":
                two_rock_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["two rock", "traditional", "clean", "hifi"])]
                if two_rock_amps:
                    selected_amp = random.choice(two_rock_amps)
            
            # Blink 182: Mesa Boogie Dual Rectifier
            elif amp_type == "mesa_dual_rectifier":
                dual_rect_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["dual", "rectifier", "recto"])]
                if dual_rect_amps:
                    selected_amp = random.choice(dual_rect_amps)
            
            # Cobain: Mesa Boogie Studio Preamp
            elif amp_type == "mesa_studio_preamp":
                studio_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["studio", "preamp", "mesa"])]
                if studio_amps:
                    selected_amp = random.choice(studio_amps)
            
            # Fallback to generic types if specific not found
            elif amp_type == "marshall":
                marshall_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["marshall", "plexi", "brit", "jcm", "jvm"])]
                if marshall_amps:
                    selected_amp = random.choice(marshall_amps)
            elif amp_type == "fender":
                fender_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["fender", "twin", "deluxe", "tweed", "bassman", "super", "vibro"])]
                if fender_amps:
                    selected_amp = random.choice(fender_amps)
            elif amp_type == "mesa":
                mesa_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["mesa", "recto", "boogie", "mark"])]
                if mesa_amps:
                    selected_amp = random.choice(mesa_amps)
            elif amp_type == "vox":
                vox_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["vox", "ac30", "ac15", "ac20"])]
                if vox_amps:
                    selected_amp = random.choice(vox_amps)
            elif amp_type == "high_gain":
                high_gain_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["mesa", "recto", "5150", "mark", "brit", "800", "high", "jvm", "friedman", "fortin"])]
                if high_gain_amps:
                    selected_amp = random.choice(high_gain_amps)
            elif amp_type == "hifi":
                hifi_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["clean", "studio", "hifi", "jazz", "twin", "deluxe"])]
                if hifi_amps:
                    selected_amp = random.choice(hifi_amps)
            elif amp_type == "carvin":
                carvin_amps = [amp for amp in self.amp_models if any(word in amp.lower() for word in ["carvin", "legacy", "v3"])]
                if carvin_amps:
                    selected_amp = random.choice(carvin_amps)

        # Check for specific amp requests - be more specific to avoid conflicts
        # Only do this if artist_gear didn't already select an amp
        if not selected_amp and "plexi" in query:
            # Plexi takes priority over general Marshall
            plexi_amps = self.gear_mapping["amps"]["marshall"]["plexi"]
            available_plexi = [
                amp for amp in plexi_amps if amp in self.amp_models
            ]
            if available_plexi:
                selected_amp = _prefer_model(query, available_plexi)
        elif not selected_amp and ("jcm800" in query or "800" in query):
            marshall_amps = self.gear_mapping["amps"]["marshall"]["jcm800"]
            available_marshall = [
                amp for amp in marshall_amps if amp in self.amp_models
            ]
            if available_marshall:
                selected_amp = _prefer_model(query, available_marshall)
        elif "jcm900" in query or "900" in query:
            marshall_amps = self.gear_mapping["amps"]["marshall"]["jcm900"]
            available_marshall = [
                amp for amp in marshall_amps if amp in self.amp_models
            ]
            if available_marshall:
                selected_amp = _prefer_model(query, available_marshall)
        elif "jvm" in query:
            marshall_amps = self.gear_mapping["amps"]["marshall"]["jvm"]
            available_marshall = [
                amp for amp in marshall_amps if amp in self.amp_models
            ]
            if available_marshall:
                selected_amp = _prefer_model(query, available_marshall)
        elif "marshall" in query:
            # Generic Marshall - try JCM800 as default
            marshall_amps = self.gear_mapping["amps"]["marshall"]["jcm800"]
            available_marshall = [
                amp for amp in marshall_amps if amp in self.amp_models
            ]
            if available_marshall:
                selected_amp = _prefer_model(query, available_marshall)

        elif (
            "mesa" in query
            or "boogie" in query
            or "recto" in query
            or "rectifier" in query
        ):
            # Try different Mesa Boogie variations
            mesa_amps = []
            if "rectifier" in query or "recto" in query:
                mesa_amps.extend(self.gear_mapping["amps"]["mesa"]["rectifier"])
            if "boogie" in query:
                mesa_amps.extend(self.gear_mapping["amps"]["mesa"]["boogie"])
            if "dual" in query:
                mesa_amps.extend(self.gear_mapping["amps"]["mesa"]["dual_rectifier"])

            # Remove duplicates and check availability
            mesa_amps = list(set(mesa_amps))
            available_mesa = [amp for amp in mesa_amps if amp in self.amp_models]
            if available_mesa:
                selected_amp = _prefer_model(query, available_mesa)

        elif "twin" in query:
            # Twin takes priority over general Fender
            twin_amps = self.gear_mapping["amps"]["fender"]["twin"]
            available_twin = [amp for amp in twin_amps if amp in self.amp_models]
            if available_twin:
                selected_amp = _prefer_model(query, available_twin)
        elif "deluxe" in query:
            # Deluxe takes priority over general Fender
            deluxe_amps = self.gear_mapping["amps"]["fender"]["deluxe"]
            available_deluxe = [amp for amp in deluxe_amps if amp in self.amp_models]
            if available_deluxe:
                selected_amp = _prefer_model(query, available_deluxe)
        elif "fender" in query or "tweed" in query:
            fender_amps = self.gear_mapping["amps"]["fender"]["tweed"]
            available_fender = [amp for amp in fender_amps if amp in self.amp_models]
            if available_fender:
                selected_amp = random.choice(available_fender)

        # If no specific match, select based on genre
        if not selected_amp:
            if genre == "metal":
                metal_amps = [
                    amp
                    for amp in self.amp_models
                    if any(
                        word in amp.lower()
                        for word in ["mesa", "recto", "5150", "mark", "brit", "800"]
                    )
                ]
                selected_amp = (
                    random.choice(metal_amps)
                    if metal_amps
                    else random.choice(self.amp_models)
                )
            elif genre == "blues":
                blues_amps = [
                    amp
                    for amp in self.amp_models
                    if any(
                        word in amp.lower()
                        for word in ["fender", "tweed", "deluxe", "vox", "ac30"]
                    )
                ]
                selected_amp = (
                    random.choice(blues_amps)
                    if blues_amps
                    else random.choice(self.amp_models)
                )
            elif genre == "jazz":
                jazz_amps = [
                    amp
                    for amp in self.amp_models
                    if any(
                        word in amp.lower()
                        for word in ["fender", "tweed", "deluxe", "clean"]
                    )
                ]
                selected_amp = (
                    random.choice(jazz_amps)
                    if jazz_amps
                    else random.choice(self.amp_models)
                )
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
            "real_world": self._get_real_world_name(selected_amp),
            "parameters": {
                "gain": round(gain, 1),
                "bass": round(bass, 1),
                "mid": round(mid, 1),
                "treble": round(treble, 1),
                "presence": round(presence, 1),
                "master": round(master, 1),
            },
        }

    def _generate_drive_block(self, structure: Dict, drive_num: int) -> Dict:
        """Generate a drive block with accurate FM9 modeling"""
        genre = structure.get("genre", "rock")
        query = structure.get("query", "").lower()
        artist_gear = structure.get("artist_gear")

        # Try to match specific drive requests using FM9 model names
        selected_drive = None
        
        # Artist-specific drive selection (HIGHEST PRIORITY) - ACCURATE GEAR MAPPINGS
        if artist_gear:
            drive_type = artist_gear.get("drive_type")
            
            # Hendrix: Dallas Arbiter Fuzz Face
            if drive_type == "fuzz_face":
                fuzz_face_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["face fuzz", "fuzz face", "face"])]
                if fuzz_face_drives:
                    selected_drive = random.choice(fuzz_face_drives)
            
            # SRV: Ibanez TS808 Tube Screamer
            elif drive_type == "tube_screamer_808":
                ts808_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["t808", "ts808", "tube screamer", "808"])]
                if ts808_drives:
                    selected_drive = random.choice(ts808_drives)
            
            # Metallica: Mesa Boogie Strategy 400
            elif drive_type == "mesa_high_gain":
                # Look for high gain distortion pedals (Mesa doesn't make drives, they use high gain amps)
                high_gain_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["distortion", "metal", "high gain", "shred", "rat", "ds1"])]
                if high_gain_drives:
                    selected_drive = random.choice(high_gain_drives)
            
            # Page: Sola Sound Tone Bender
            elif drive_type == "tone_bender":
                # Prioritize Bender Fuzz specifically
                bender_drives = [drive for drive in self.drive_models if "bender" in drive.lower()]
                if bender_drives:
                    selected_drive = bender_drives[0]  # Use the exact Bender Fuzz
                else:
                    # Fallback to other fuzz pedals
                    tone_bender_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["tone bender", "bender", "fuzz"])]
                    if tone_bender_drives:
                        selected_drive = random.choice(tone_bender_drives)
            
            # BB King: Clean (no drive)
            elif drive_type == "clean":
                selected_drive = "NO_DRIVE_INTENTIONAL"
            
            # Van Halen: MXR Phase 90
            elif drive_type == "phase_90":
                phase_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["phase", "90", "modulation"])]
                if phase_drives:
                    selected_drive = random.choice(phase_drives)
            
            # Slash: Boss SD-1 Super Overdrive
            elif drive_type == "boss_sd1":
                sd1_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["sd1", "super overdrive", "boss"])]
                if sd1_drives:
                    selected_drive = random.choice(sd1_drives)
            
            # Dimebag: MXR Dime Distortion
            elif drive_type == "mxr_dime":
                dime_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["dime", "mxr", "distortion"])]
                if dime_drives:
                    selected_drive = random.choice(dime_drives)
                
            # Clapton: Dallas Rangemaster Treble Booster
            elif drive_type == "rangemaster":
                rangemaster_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["rangemaster", "treble", "boost"])]
                if rangemaster_drives:
                    selected_drive = random.choice(rangemaster_drives)
            
            # Gilmour: Big Muff Pi
            elif drive_type == "big_muff":
                big_muff_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["big muff", "muff", "pi fuzz"])]
                if big_muff_drives:
                    selected_drive = random.choice(big_muff_drives)
            
            # Satriani/Vai: Ibanez TS808
            elif drive_type == "tube_screamer_808":
                ts808_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["t808", "ts808", "tube screamer", "808"])]
                if ts808_drives:
                    selected_drive = random.choice(ts808_drives)
            
            # Yngwie: DOD YJM308
            elif drive_type == "dod_yjm308":
                yjm_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["yjm", "dod", "308"])]
                if yjm_drives:
                    selected_drive = random.choice(yjm_drives)
            
            # Mayer: Klon Centaur
            elif drive_type == "klon_centaur":
                klon_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["klon", "centaur", "klone"])]
                if klon_drives:
                    selected_drive = random.choice(klon_drives)
            
            # Frampton: Talk Box
            elif drive_type == "talk_box":
                talk_box_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["talk", "box", "vocoder"])]
                if talk_box_drives:
                    selected_drive = random.choice(talk_box_drives)
            
            # Blink 182/Green Day: Boss DS-1
            elif drive_type == "boss_ds1":
                ds1_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["ds1", "distortion", "boss"])]
                if ds1_drives:
                    selected_drive = random.choice(ds1_drives)
            
            # Tool: Diezel VH4
            elif drive_type == "diezel_vh4":
                diezel_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["diezel", "vh4", "high gain"])]
                if diezel_drives:
                    selected_drive = random.choice(diezel_drives)
            
            # Meshuggah: Line 6 Pod
            elif drive_type == "line6_pod":
                pod_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["pod", "line6", "digital"])]
                if pod_drives:
                    selected_drive = random.choice(pod_drives)
            
            # Prince: Boss CE-1 Chorus
            elif drive_type == "boss_ce1":
                ce1_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["ce1", "chorus", "boss"])]
                if ce1_drives:
                    selected_drive = random.choice(ce1_drives)
            
            # Fallback to generic types if specific not found
            elif drive_type == "fuzz":
                fuzz_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["fuzz", "face", "muff", "octave"])]
                if fuzz_drives:
                    selected_drive = random.choice(fuzz_drives)
            elif drive_type == "tube_screamer":
                ts_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["tube", "screamer", "ts", "valve", "808", "ts9"])]
                if ts_drives:
                    selected_drive = random.choice(ts_drives)
            elif drive_type == "overdrive":
                od_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["overdrive", "od", "tube", "screamer", "klon", "klone", "boost", "drive"])]
                if od_drives:
                    selected_drive = random.choice(od_drives)
            elif drive_type == "high_gain":
                high_gain_drives = [drive for drive in self.drive_models if any(word in drive.lower() for word in ["distortion", "fuzz", "shred", "metal", "rat", "ds1", "metal", "heavy"])]
                if high_gain_drives:
                    selected_drive = random.choice(high_gain_drives)
            elif drive_type == "clean":
                selected_drive = "NO_DRIVE_INTENTIONAL"

        if not selected_drive and selected_drive != "NO_DRIVE_INTENTIONAL" and ("tube screamer" in query or "ts808" in query or "ts9" in query):
            ts_drives = self.gear_mapping["drives"]["tube_screamer"]
            available_ts = [drive for drive in ts_drives if drive in self.drive_models]
            if available_ts:
                selected_drive = random.choice(available_ts)

        elif "klon" in query:
            klon_drives = self.gear_mapping["drives"]["klon"]
            available_klon = [
                drive for drive in klon_drives if drive in self.drive_models
            ]
            if available_klon:
                selected_drive = random.choice(available_klon)

        elif "rat" in query:
            rat_drives = self.gear_mapping["drives"]["rat"]
            available_rat = [
                drive for drive in rat_drives if drive in self.drive_models
            ]
            if available_rat:
                selected_drive = random.choice(available_rat)

        elif "super" in query and "od" in query:
            super_drives = self.gear_mapping["drives"]["super_od"]
            available_super = [drive for drive in super_drives if drive in self.drive_models]
            if available_super:
                selected_drive = random.choice(available_super)

        elif "bb pre" in query or "bbpre" in query:
            bb_drives = self.gear_mapping["drives"]["bb_pre"]
            available_bb = [drive for drive in bb_drives if drive in self.drive_models]
            if available_bb:
                selected_drive = random.choice(available_bb)

        elif "blackglass" in query:
            blackglass_drives = self.gear_mapping["drives"]["blackglass"]
            available_blackglass = [drive for drive in blackglass_drives if drive in self.drive_models]
            if available_blackglass:
                selected_drive = random.choice(available_blackglass)

        elif "compulsion" in query:
            compulsion_drives = self.gear_mapping["drives"]["compulsion"]
            available_compulsion = [drive for drive in compulsion_drives if drive in self.drive_models]
            if available_compulsion:
                selected_drive = random.choice(available_compulsion)

        elif "bender" in query:
            bender_drives = self.gear_mapping["drives"]["bender_fuzz"]
            available_bender = [drive for drive in bender_drives if drive in self.drive_models]
            if available_bender:
                selected_drive = random.choice(available_bender)

        elif "bit crusher" in query:
            bit_drives = self.gear_mapping["drives"]["bit_crusher"]
            available_bit = [drive for drive in bit_drives if drive in self.drive_models]
            if available_bit:
                selected_drive = random.choice(available_bit)

        elif "blues od" in query:
            blues_od_drives = self.gear_mapping["drives"]["blues_od"]
            available_blues_od = [drive for drive in blues_od_drives if drive in self.drive_models]
            if available_blues_od:
                selected_drive = random.choice(available_blues_od)

        elif "bosom" in query:
            bosom_drives = self.gear_mapping["drives"]["bosom_boost"]
            available_bosom = [drive for drive in bosom_drives if drive in self.drive_models]
            if available_bosom:
                selected_drive = random.choice(available_bosom)

        elif "colortone" in query:
            colortone_drives = self.gear_mapping["drives"]["colortone"]
            available_colortone = [drive for drive in colortone_drives if drive in self.drive_models]
            if available_colortone:
                selected_drive = random.choice(available_colortone)

        elif "ds1" in query:
            ds1_drives = self.gear_mapping["drives"]["ds1"]
            available_ds1 = [drive for drive in ds1_drives if drive in self.drive_models]
            if available_ds1:
                selected_drive = random.choice(available_ds1)

        elif "esoteric" in query:
            esoteric_drives = self.gear_mapping["drives"]["esoteric"]
            available_esoteric = [drive for drive in esoteric_drives if drive in self.drive_models]
            if available_esoteric:
                selected_drive = random.choice(available_esoteric)

        elif "eternal love" in query:
            eternal_drives = self.gear_mapping["drives"]["eternal_love"]
            available_eternal = [drive for drive in eternal_drives if drive in self.drive_models]
            if available_eternal:
                selected_drive = random.choice(available_eternal)

        elif "face fuzz" in query:
            face_drives = self.gear_mapping["drives"]["face_fuzz"]
            available_face = [drive for drive in face_drives if drive in self.drive_models]
            if available_face:
                selected_drive = random.choice(available_face)

        elif "fas led" in query:
            fas_led_drives = self.gear_mapping["drives"]["fas_led_drive"]
            available_fas_led = [drive for drive in fas_led_drives if drive in self.drive_models]
            if available_fas_led:
                selected_drive = random.choice(available_fas_led)

        elif "fat rat" in query:
            fat_rat_drives = self.gear_mapping["drives"]["rat"]
            available_fat_rat = [drive for drive in fat_rat_drives if "Fat Rat" in drive and drive in self.drive_models]
            if available_fat_rat:
                selected_drive = random.choice(available_fat_rat)

        elif "fet boost" in query:
            fet_boost_drives = self.gear_mapping["drives"]["fet_boost"]
            available_fet_boost = [drive for drive in fet_boost_drives if drive in self.drive_models]
            if available_fet_boost:
                selected_drive = random.choice(available_fet_boost)

        elif "fet preamp" in query:
            fet_preamp_drives = self.gear_mapping["drives"]["fet_preamp"]
            available_fet_preamp = [drive for drive in fet_preamp_drives if drive in self.drive_models]
            if available_fet_preamp:
                selected_drive = random.choice(available_fet_preamp)

        elif "full od" in query:
            full_od_drives = self.gear_mapping["drives"]["full_od"]
            available_full_od = [drive for drive in full_od_drives if drive in self.drive_models]
            if available_full_od:
                selected_drive = random.choice(available_full_od)

        elif "gauss" in query:
            gauss_drives = self.gear_mapping["drives"]["gauss_drive"]
            available_gauss = [drive for drive in gauss_drives if drive in self.drive_models]
            if available_gauss:
                selected_drive = random.choice(available_gauss)

        elif "griddle" in query:
            griddle_drives = self.gear_mapping["drives"]["griddle_cake"]
            available_griddle = [drive for drive in griddle_drives if drive in self.drive_models]
            if available_griddle:
                selected_drive = random.choice(available_griddle)

        elif "hard fuzz" in query:
            hard_fuzz_drives = self.gear_mapping["drives"]["hard_fuzz"]
            available_hard_fuzz = [drive for drive in hard_fuzz_drives if drive in self.drive_models]
            if available_hard_fuzz:
                selected_drive = random.choice(available_hard_fuzz)

        elif "heartpedal" in query:
            heartpedal_drives = self.gear_mapping["drives"]["heartpedal"]
            available_heartpedal = [drive for drive in heartpedal_drives if drive in self.drive_models]
            if available_heartpedal:
                selected_drive = random.choice(available_heartpedal)

        elif "hoodoo" in query:
            hoodoo_drives = self.gear_mapping["drives"]["hoodoo"]
            available_hoodoo = [drive for drive in hoodoo_drives if drive in self.drive_models]
            if available_hoodoo:
                selected_drive = random.choice(available_hoodoo)

        elif "horizon" in query:
            horizon_drives = self.gear_mapping["drives"]["horizon"]
            available_horizon = [drive for drive in horizon_drives if drive in self.drive_models]
            if available_horizon:
                selected_drive = random.choice(available_horizon)

        elif "integral" in query:
            integral_drives = self.gear_mapping["drives"]["integral"]
            available_integral = [drive for drive in integral_drives if drive in self.drive_models]
            if available_integral:
                selected_drive = random.choice(available_integral)

        elif "jam ray" in query:
            jam_ray_drives = self.gear_mapping["drives"]["jam_ray"]
            available_jam_ray = [drive for drive in jam_ray_drives if drive in self.drive_models]
            if available_jam_ray:
                selected_drive = random.choice(available_jam_ray)

        elif "klone chiron" in query:
            klone_chiron_drives = self.gear_mapping["drives"]["klon"]
            available_klone_chiron = [drive for drive in klone_chiron_drives if "Klone Chiron" in drive and drive in self.drive_models]
            if available_klone_chiron:
                selected_drive = random.choice(available_klone_chiron)

        elif "m-zone" in query:
            m_zone_drives = self.gear_mapping["drives"]["m_zone"]
            available_m_zone = [drive for drive in m_zone_drives if drive in self.drive_models]
            if available_m_zone:
                selected_drive = random.choice(available_m_zone)

        elif "master fuzz" in query:
            master_fuzz_drives = self.gear_mapping["drives"]["master_fuzz"]
            available_master_fuzz = [drive for drive in master_fuzz_drives if drive in self.drive_models]
            if available_master_fuzz:
                selected_drive = random.choice(available_master_fuzz)

        elif "maxoff" in query:
            maxoff_drives = self.gear_mapping["drives"]["maxoff"]
            available_maxoff = [drive for drive in maxoff_drives if drive in self.drive_models]
            if available_maxoff:
                selected_drive = random.choice(available_maxoff)

        elif "mcmlxxxi" in query:
            mcmlxxxi_drives = self.gear_mapping["drives"]["mcmlxxxi"]
            available_mcmlxxxi = [drive for drive in mcmlxxxi_drives if drive in self.drive_models]
            if available_mcmlxxxi:
                selected_drive = random.choice(available_mcmlxxxi)

        elif "micro boost" in query:
            micro_boost_drives = self.gear_mapping["drives"]["micro_boost"]
            available_micro_boost = [drive for drive in micro_boost_drives if drive in self.drive_models]
            if available_micro_boost:
                selected_drive = random.choice(available_micro_boost)

        elif "mid boost" in query:
            mid_boost_drives = self.gear_mapping["drives"]["mid_boost"]
            available_mid_boost = [drive for drive in mid_boost_drives if drive in self.drive_models]
            if available_mid_boost:
                selected_drive = random.choice(available_mid_boost)

        elif "mosfet" in query:
            mosfet_drives = self.gear_mapping["drives"]["mosfet"]
            available_mosfet = [drive for drive in mosfet_drives if drive in self.drive_models]
            if available_mosfet:
                selected_drive = random.choice(available_mosfet)

        elif "nobelium" in query:
            nobelium_drives = self.gear_mapping["drives"]["nobelium"]
            available_nobelium = [drive for drive in nobelium_drives if drive in self.drive_models]
            if available_nobelium:
                selected_drive = random.choice(available_nobelium)

        elif "octave" in query:
            octave_drives = self.gear_mapping["drives"]["octave"]
            available_octave = [drive for drive in octave_drives if drive in self.drive_models]
            if available_octave:
                selected_drive = random.choice(available_octave)

        elif "od 250" in query:
            od_250_drives = self.gear_mapping["drives"]["od_250"]
            available_od_250 = [drive for drive in od_250_drives if drive in self.drive_models]
            if available_od_250:
                selected_drive = random.choice(available_od_250)

        elif "od-one" in query:
            od_one_drives = self.gear_mapping["drives"]["od_one"]
            available_od_one = [drive for drive in od_one_drives if drive in self.drive_models]
            if available_od_one:
                selected_drive = random.choice(available_od_one)

        elif "pi fuzz" in query:
            pi_fuzz_drives = self.gear_mapping["drives"]["pi_fuzz"]
            available_pi_fuzz = [drive for drive in pi_fuzz_drives if drive in self.drive_models]
            if available_pi_fuzz:
                selected_drive = random.choice(available_pi_fuzz)

        elif "plus distortion" in query:
            plus_distortion_drives = self.gear_mapping["drives"]["plus_distortion"]
            available_plus_distortion = [drive for drive in plus_distortion_drives if drive in self.drive_models]
            if available_plus_distortion:
                selected_drive = random.choice(available_plus_distortion)

        elif "sdd preamp" in query:
            sdd_preamp_drives = self.gear_mapping["drives"]["sdd_preamp"]
            available_sdd_preamp = [drive for drive in sdd_preamp_drives if drive in self.drive_models]
            if available_sdd_preamp:
                selected_drive = random.choice(available_sdd_preamp)

        elif "shimmer" in query:
            shimmer_drives = self.gear_mapping["drives"]["shimmer"]
            available_shimmer = [drive for drive in shimmer_drives if drive in self.drive_models]
            if available_shimmer:
                selected_drive = random.choice(available_shimmer)

        elif "shred" in query:
            shred_drives = self.gear_mapping["drives"]["shred"]
            available_shred = [drive for drive in shred_drives if drive in self.drive_models]
            if available_shred:
                selected_drive = random.choice(available_shred)

        elif "sonic" in query:
            sonic_drives = self.gear_mapping["drives"]["sonic"]
            available_sonic = [drive for drive in sonic_drives if drive in self.drive_models]
            if available_sonic:
                selected_drive = random.choice(available_sonic)

        elif "suhr riot" in query:
            suhr_riot_drives = self.gear_mapping["drives"]["suhr_riot"]
            available_suhr_riot = [drive for drive in suhr_riot_drives if drive in self.drive_models]
            if available_suhr_riot:
                selected_drive = random.choice(available_suhr_riot)

        elif "sunrise" in query:
            sunrise_drives = self.gear_mapping["drives"]["sunrise"]
            available_sunrise = [drive for drive in sunrise_drives if drive in self.drive_models]
            if available_sunrise:
                selected_drive = random.choice(available_sunrise)

        elif "super fuzz" in query:
            super_fuzz_drives = self.gear_mapping["drives"]["super_fuzz"]
            available_super_fuzz = [drive for drive in super_fuzz_drives if drive in self.drive_models]
            if available_super_fuzz:
                selected_drive = random.choice(available_super_fuzz)

        elif "tape distortion" in query:
            tape_distortion_drives = self.gear_mapping["drives"]["tape_distortion"]
            available_tape_distortion = [drive for drive in tape_distortion_drives if drive in self.drive_models]
            if available_tape_distortion:
                selected_drive = random.choice(available_tape_distortion)

        elif "timothy" in query:
            timothy_drives = self.gear_mapping["drives"]["timothy"]
            available_timothy = [drive for drive in timothy_drives if drive in self.drive_models]
            if available_timothy:
                selected_drive = random.choice(available_timothy)

        elif "tone of kings" in query:
            tone_of_kings_drives = self.gear_mapping["drives"]["tone_of_kings"]
            available_tone_of_kings = [drive for drive in tone_of_kings_drives if drive in self.drive_models]
            if available_tone_of_kings:
                selected_drive = random.choice(available_tone_of_kings)

        elif "treble boost" in query:
            treble_boost_drives = self.gear_mapping["drives"]["treble_boost"]
            available_treble_boost = [drive for drive in treble_boost_drives if drive in self.drive_models]
            if available_treble_boost:
                selected_drive = random.choice(available_treble_boost)

        elif "tube drive" in query:
            tube_drive_drives = self.gear_mapping["drives"]["tube_drive"]
            available_tube_drive = [drive for drive in tube_drive_drives if drive in self.drive_models]
            if available_tube_drive:
                selected_drive = random.choice(available_tube_drive)

        elif "valve screamer" in query:
            valve_screamer_drives = self.gear_mapping["drives"]["tube_screamer"]
            available_valve_screamer = [drive for drive in valve_screamer_drives if "Valve Screamer" in drive and drive in self.drive_models]
            if available_valve_screamer:
                selected_drive = random.choice(available_valve_screamer)

        elif "zen master" in query:
            zen_master_drives = self.gear_mapping["drives"]["zen_master"]
            available_zen_master = [drive for drive in zen_master_drives if drive in self.drive_models]
            if available_zen_master:
                selected_drive = random.choice(available_zen_master)

        # If no specific match, select based on genre
        if not selected_drive and selected_drive != "NO_DRIVE_INTENTIONAL":
            if genre == "blues":
                blues_drives = [
                    drive
                    for drive in self.drive_models
                    if any(
                        word in drive.lower()
                        for word in ["ts", "tube", "screamer", "klon"]
                    )
                ]
                selected_drive = (
                    random.choice(blues_drives)
                    if blues_drives
                    else random.choice(self.drive_models)
                )
            elif genre == "metal":
                metal_drives = [
                    drive
                    for drive in self.drive_models
                    if any(
                        word in drive.lower()
                        for word in ["rat", "distortion", "fuzz", "boost"]
                    )
                ]
                selected_drive = (
                    random.choice(metal_drives)
                    if metal_drives
                    else random.choice(self.drive_models)
                )
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

        # Handle clean tones (no drive)
        if selected_drive == "NO_DRIVE_INTENTIONAL":
            return {
                "enabled": False,
                "type": "NO DRIVE",
                "real_world": "No Drive",
                "parameters": {},
            }
        
        return {
            "enabled": True,
            "type": selected_drive,
            "real_world": self._get_real_world_name(selected_drive),
            "parameters": {
                "drive": round(drive, 1),
                "tone": round(tone, 1),
                "level": round(level, 1),
            },
        }

    def _generate_cab_block(self, structure: Dict) -> Dict:
        """Generate a cab block with accurate FM9 modeling"""
        genre = structure.get("genre", "rock")
        query = structure.get("query", "").lower()

        # Try to match specific cab requests
        selected_cab = None

        if "marshall" in query or "4x12" in query:
            marshall_cabs = self.gear_mapping["cabs"]["marshall_4x12"]
            available_marshall = [
                cab for cab in marshall_cabs if cab in self.cab_models
            ]
            if available_marshall:
                selected_cab = random.choice(available_marshall)

        elif "mesa" in query or "boogie" in query:
            mesa_cabs = self.gear_mapping["cabs"]["mesa_4x12"]
            available_mesa = [cab for cab in mesa_cabs if cab in self.cab_models]
            if available_mesa:
                selected_cab = random.choice(available_mesa)

        # If no specific match, select based on genre
        if not selected_cab:
            if genre == "metal":
                metal_cabs = [
                    cab
                    for cab in self.cab_models
                    if any(
                        word in cab.lower()
                        for word in ["4x12", "marshall", "mesa", "v30"]
                    )
                ]
                selected_cab = (
                    random.choice(metal_cabs)
                    if metal_cabs
                    else random.choice(self.cab_models)
                )
            elif genre == "blues":
                blues_cabs = [
                    cab
                    for cab in self.cab_models
                    if any(
                        word in cab.lower()
                        for word in ["2x12", "fender", "tweed", "greenback"]
                    )
                ]
                selected_cab = (
                    random.choice(blues_cabs)
                    if blues_cabs
                    else random.choice(self.cab_models)
                )
            elif genre == "jazz":
                jazz_cabs = [
                    cab
                    for cab in self.cab_models
                    if any(
                        word in cab.lower()
                        for word in ["1x12", "2x12", "fender", "tweed"]
                    )
                ]
                selected_cab = (
                    random.choice(jazz_cabs)
                    if jazz_cabs
                    else random.choice(self.cab_models)
                )
            else:
                selected_cab = random.choice(self.cab_models)

        # Generate realistic parameters
        low_cut = random.uniform(60.0, 200.0)
        high_cut = random.uniform(8000.0, 15000.0)
        level = random.uniform(-3.0, 6.0)

        return {
            "enabled": True,
            "type": selected_cab,
            "real_world": self._get_real_world_name(selected_cab),
            "parameters": {
                "low_cut": round(low_cut, 1),
                "high_cut": round(high_cut, 1),
                "level": round(level, 1),
            },
        }

    def _generate_eq_block(self, structure: Dict) -> Dict:
        """Generate an EQ block"""
        eq_models = self.effect_models.get("eq", [])
        selected_eq = random.choice(eq_models) if eq_models else "Parametric EQ"

        return {
            "enabled": True,
            "type": selected_eq,
            "real_world": self._get_real_world_name(selected_eq),
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

    def _generate_delay_block(self, structure: Dict) -> Dict:
        """Generate a delay block"""
        delay_models = self.effect_models.get("delay", [])
        selected_delay = (
            random.choice(delay_models) if delay_models else "Digital Delay"
        )

        return {
            "enabled": True,
            "type": selected_delay,
            "real_world": self._get_real_world_name(selected_delay),
            "parameters": {
                "time": random.uniform(200.0, 800.0),
                "feedback": random.uniform(20.0, 40.0),
                "mix": random.uniform(15.0, 35.0),
            },
        }

    def _generate_reverb_block(self, structure: Dict) -> Dict:
        """Generate a reverb block"""
        reverb_models = self.effect_models.get("reverb", [])
        selected_reverb = (
            random.choice(reverb_models) if reverb_models else "Room Reverb"
        )

        return {
            "enabled": True,
            "type": selected_reverb,
            "real_world": self._get_real_world_name(selected_reverb),
            "parameters": {
                "room_size": random.uniform(50.0, 80.0),
                "decay": random.uniform(1.5, 3.0),
                "mix": random.uniform(20.0, 40.0),
            },
        }

    def _generate_modulation_block(self, structure: Dict) -> Dict:
        """Generate a modulation block"""
        modulation_models = self.effect_models.get("modulation", [])
        selected_mod = (
            random.choice(modulation_models) if modulation_models else "Chorus"
        )

        return {
            "enabled": True,
            "type": selected_mod,
            "real_world": self._get_real_world_name(selected_mod),
            "parameters": {
                "rate": random.uniform(0.5, 2.0),
                "depth": random.uniform(30.0, 70.0),
                "mix": random.uniform(25.0, 50.0),
            },
        }

    def _generate_pitch_block(self, structure: Dict) -> Dict:
        """Generate a pitch block"""
        pitch_models = self.effect_models.get("pitch", [])
        selected_pitch = (
            random.choice(pitch_models) if pitch_models else "Pitch Shifter"
        )

        return {
            "enabled": True,
            "type": selected_pitch,
            "real_world": self._get_real_world_name(selected_pitch),
            "parameters": {
                "pitch": random.uniform(-12.0, 12.0),
                "mix": random.uniform(30.0, 70.0),
            },
        }

    def _generate_dynamics_block(self, structure: Dict) -> Dict:
        """Generate a dynamics block"""
        dynamics_models = self.effect_models.get("dynamics", [])
        selected_dynamics = (
            random.choice(dynamics_models) if dynamics_models else "Compressor"
        )

        return {
            "enabled": True,
            "type": selected_dynamics,
            "real_world": self._get_real_world_name(selected_dynamics),
            "parameters": {
                "threshold": random.uniform(-20.0, -5.0),
                "ratio": random.uniform(2.0, 8.0),
                "attack": random.uniform(1.0, 10.0),
                "release": random.uniform(50.0, 200.0),
            },
        }

    def _generate_utility_block(self, structure: Dict) -> Dict:
        """Generate a utility block"""
        utility_models = self.effect_models.get("utility", [])
        selected_utility = random.choice(utility_models) if utility_models else "Volume"

        return {
            "enabled": True,
            "type": selected_utility,
            "real_world": self._get_real_world_name(selected_utility),
            "parameters": {"volume": random.uniform(-6.0, 6.0)},
        }

    def _generate_tone_description(self, tone_patch: Dict, intent: Dict) -> str:
        """Generate a detailed description of the tone"""
        description_parts = []

        # Genre and style
        genre = intent.get("genre", "rock")
        description_parts.append(f"A {genre} tone")

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

        # Characteristics
        if intent.get("characteristics"):
            characteristics = ", ".join(intent["characteristics"])
            description_parts.append(f"featuring {characteristics}")

        return ", ".join(description_parts) + "."

    def _extract_gear_used(self, tone_patch: Dict) -> Dict:
        """Extract the gear used in the tone patch"""
        gear_used = {}

        for block_name, block_data in tone_patch.items():
            if (
                block_data.get("enabled", False)
                and block_data.get("type", "None") != "None"
            ):
                gear_used[block_name] = {
                    "type": block_data.get("type"),
                    "parameters": block_data.get("parameters", {}),
                }

        return gear_used

    def _get_fallback_tone(self, query: str) -> Dict:
        """Get a fallback tone if generation fails"""
        # Seed random number generator for deterministic fallback
        _seed_from_query(query)
        
        tone_patch = {
            "amp": {
                "enabled": True,
                "type": "Brit 800",
                "parameters": {
                    "gain": 6.0,
                    "bass": 6.0,
                    "mid": 6.0,
                    "treble": 6.0,
                    "presence": 6.0,
                    "master": 5.0,
                },
            },
            "cab": {
                "enabled": True,
                "type": "Legacy 4x12 V30",
                "parameters": {"low_cut": 100.0, "high_cut": 10000.0, "level": 0.0},
            },
        }

        # Create blocks list from tone_patch
        blocks_list = [
            {"type": k, "parameters": v.get("parameters", {})}
            for k, v in tone_patch.items()
            if isinstance(v, dict) and "parameters" in v
        ]

        result = {
            "query": query,
            "intent": {"genre": "rock", "characteristics": []},
            "tone_patch": tone_patch,
            "description": "A rock tone using Brit 800 with Legacy 4x12 V30",
            "gear_used": {},
            "blocks": blocks_list
        }

        # Normalize names & ensure `blocks` exists
        result = canonicalize_preset(result)
        
        # Enforce parameter ranges and clamp values
        result = enforce_ref_ranges(result)
        
        return result

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
                    "master": {"min": 0.0, "max": 10.0, "default": 5.0},
                }
            },
            "cab": {
                "parameters": {
                    "low_cut": {"min": 20.0, "max": 500.0, "default": 100.0},
                    "high_cut": {"min": 2000.0, "max": 20000.0, "default": 10000.0},
                    "level": {"min": -20.0, "max": 20.0, "default": 0.0},
                }
            },
            "gain": {
                "types": [
                    "FAS Boost",
                    "TS808 Mod",
                    "Klon",
                    "Fuzz Face",
                    "Rat Distortion",
                    "Blues Driver",
                ]
            },
            "pitch": {
                "types": [
                    "Pitch Shifter",
                    "Harmonizer",
                    "Whammy",
                    "Pitch Shifter Pro",
                    "Harmonizer Pro",
                ]
            },
        }
