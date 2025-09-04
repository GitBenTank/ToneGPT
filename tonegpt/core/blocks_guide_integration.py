import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import random


class BlocksGuideIntegration:
    """
    Integrates Blocks Guide and User Manual knowledge into AI tone generation
    Provides intelligent parameter selection based on real-world examples and technical specs
    """
    
    def __init__(self):
        self.blocks_data = self._load_blocks_data()
        self.blocks_guide_knowledge = self._load_blocks_guide_knowledge()
        self.user_manual_knowledge = self._load_user_manual_knowledge()
        self.real_world_examples = self._load_real_world_examples()
        
    def _load_blocks_data(self) -> Dict:
        """Load comprehensive FM9 blocks data"""
        try:
            with open("tonegpt/core/blocks_with_footswitch.json", "r") as f:
                data = json.load(f)
            print(f"🔧 Loaded {len(data)} FM9 blocks for AI integration")
            return data
        except Exception as e:
            print(f"⚠️ Error loading blocks data: {e}")
            return {}
    
    def _load_blocks_guide_knowledge(self) -> Dict:
        """Load blocks guide knowledge and parameter guidance"""
        return {
            "amp_guidance": {
                "marshall_jcm800": {
                    "gain_range": (7.0, 9.5),
                    "bass_range": (3.0, 6.0),
                    "mid_range": (4.0, 7.0),
                    "treble_range": (5.0, 8.0),
                    "presence_range": (4.0, 7.0),
                    "master_volume": (6.0, 9.0),
                    "notes": "Classic Marshall JCM800 - high gain, aggressive mids, tight low end"
                },
                "marshall_plexi": {
                    "gain_range": (6.0, 8.5),
                    "bass_range": (4.0, 7.0),
                    "mid_range": (5.0, 8.0),
                    "treble_range": (6.0, 9.0),
                    "presence_range": (5.0, 8.0),
                    "master_volume": (7.0, 10.0),
                    "notes": "Classic Marshall Plexi - warm, musical overdrive, great for classic rock"
                },
                "mesa_mark_iic": {
                    "gain_range": (6.5, 9.0),
                    "bass_range": (2.0, 5.0),
                    "mid_range": (3.0, 6.0),
                    "treble_range": (4.0, 7.0),
                    "presence_range": (3.0, 6.0),
                    "master_volume": (5.0, 8.0),
                    "notes": "Mesa Mark IIC+ - tight, focused, great for metal and high-gain applications"
                },
                "fender_twin": {
                    "gain_range": (2.0, 5.0),
                    "bass_range": (4.0, 7.0),
                    "mid_range": (3.0, 6.0),
                    "treble_range": (5.0, 8.0),
                    "presence_range": (4.0, 7.0),
                    "master_volume": (6.0, 9.0),
                    "notes": "Fender Twin Reverb - clean, bright, great for country and clean tones"
                }
            },
            "drive_guidance": {
                "boss_sd1": {
                    "drive_range": (3.0, 7.0),
                    "tone_range": (4.0, 7.0),
                    "level_range": (6.0, 9.0),
                    "notes": "Boss SD-1 Super Overdrive - classic mid-hump boost, great for Marshall amps"
                },
                "tube_screamer_808": {
                    "drive_range": (2.0, 6.0),
                    "tone_range": (4.0, 7.0),
                    "level_range": (6.0, 9.0),
                    "notes": "Ibanez TS808 - smooth overdrive, perfect for blues and rock"
                },
                "klon_centaur": {
                    "drive_range": (1.0, 4.0),
                    "tone_range": (4.0, 7.0),
                    "level_range": (6.0, 9.0),
                    "notes": "Klon Centaur - transparent overdrive, great for clean boosts"
                }
            },
            "cab_guidance": {
                "marshall_4x12": {
                    "speaker_type": "Celestion V30",
                    "mic_position": "Cap Edge",
                    "mic_distance": "0.5-2.0 inches",
                    "notes": "Classic Marshall 4x12 with V30s - aggressive, tight, great for metal"
                },
                "mesa_4x12": {
                    "speaker_type": "Celestion V30",
                    "mic_position": "Cap Edge",
                    "mic_distance": "1.0-3.0 inches",
                    "notes": "Mesa 4x12 with V30s - tight, focused, great for high-gain"
                },
                "fender_4x10": {
                    "speaker_type": "Jensen C10N",
                    "mic_position": "Center",
                    "mic_distance": "2.0-4.0 inches",
                    "notes": "Fender 4x10 with Jensens - bright, clean, great for country"
                }
            }
        }
    
    def _load_user_manual_knowledge(self) -> Dict:
        """Load user manual knowledge for tone crafting"""
        return {
            "signal_chain_guidance": {
                "metal": {
                    "drive_order": ["high_gain_drive", "boost"],
                    "amp_type": "high_gain_marshall_or_mesa",
                    "cab_type": "4x12_v30",
                    "eq_emphasis": "mid_scoop",
                    "effects_order": ["compressor", "eq", "delay", "reverb"]
                },
                "blues": {
                    "drive_order": ["tube_screamer", "fuzz"],
                    "amp_type": "fender_or_marshall_plexi",
                    "cab_type": "2x12_or_4x12",
                    "eq_emphasis": "mid_boost",
                    "effects_order": ["compressor", "eq", "delay", "reverb"]
                },
                "country": {
                    "drive_order": ["clean_boost"],
                    "amp_type": "fender_twin_or_deluxe",
                    "cab_type": "1x12_or_2x12",
                    "eq_emphasis": "bright_highs",
                    "effects_order": ["compressor", "eq", "delay", "reverb"]
                }
            },
            "parameter_relationships": {
                "gain_staging": "Drive level should complement amp gain - don't overdrive both",
                "eq_balance": "Use EQ to shape tone after amp selection, not to fix bad amp choice",
                "cab_mic_placement": "Closer mics = more presence, distant mics = more room sound",
                "reverb_timing": "Shorter reverb for tight tones, longer for ambient tones"
            }
        }
    
    def _load_real_world_examples(self) -> Dict:
        """Load real-world examples from blocks guide"""
        return {
            "artist_rigs": {
                "zakk_wylde": {
                    "amp": "Marshall JCM800",
                    "drive": "Boss SD-1",
                    "cab": "Marshall 4x12 V30",
                    "settings": {
                        "amp_gain": 8.5,
                        "amp_bass": 4.0,
                        "amp_mid": 6.0,
                        "amp_treble": 7.0,
                        "drive_drive": 5.0,
                        "drive_tone": 6.0,
                        "drive_level": 8.0
                    }
                },
                "stevie_ray_vaughan": {
                    "amp": "Fender Twin Reverb",
                    "drive": "Ibanez TS808",
                    "cab": "Fender 4x10",
                    "settings": {
                        "amp_gain": 3.0,
                        "amp_bass": 5.0,
                        "amp_mid": 4.0,
                        "amp_treble": 6.0,
                        "drive_drive": 3.0,
                        "drive_tone": 5.0,
                        "drive_level": 7.0
                    }
                },
                "james_hetfield": {
                    "amp": "Mesa Mark IIC+",
                    "drive": "Mesa High Gain",
                    "cab": "Mesa 4x12 V30",
                    "settings": {
                        "amp_gain": 8.0,
                        "amp_bass": 3.0,
                        "amp_mid": 4.0,
                        "amp_treble": 5.0,
                        "drive_drive": 6.0,
                        "drive_tone": 5.0,
                        "drive_level": 7.0
                    }
                }
            }
        }
    
    def get_amp_parameters(self, amp_type: str, genre: str = "rock") -> Dict:
        """Get intelligent amp parameters based on blocks guide knowledge"""
        if amp_type in self.blocks_guide_knowledge["amp_guidance"]:
            guidance = self.blocks_guide_knowledge["amp_guidance"][amp_type]
            
            # Generate parameters within recommended ranges
            params = {}
            for param, value in guidance.items():
                if param.endswith("_range") and isinstance(value, tuple) and len(value) == 2:
                    param_name = param.replace("_range", "")
                    min_val, max_val = value
                    params[param_name] = round(random.uniform(min_val, max_val), 1)
            
            # Add genre-specific adjustments
            if genre == "metal":
                params["gain"] = min(params.get("gain", 7.0) + 1.0, 10.0)
                params["bass"] = max(params.get("bass", 5.0) - 1.0, 0.0)
            elif genre == "blues":
                params["gain"] = max(params.get("gain", 7.0) - 1.0, 0.0)
                params["mid"] = min(params.get("mid", 5.0) + 1.0, 10.0)
            
            return params
        
        # Fallback to generic parameters
        return {
            "gain": 6.0,
            "bass": 5.0,
            "mid": 5.0,
            "treble": 5.0,
            "presence": 5.0,
            "master_volume": 7.0
        }
    
    def get_drive_parameters(self, drive_type: str, amp_type: str = None) -> Dict:
        """Get intelligent drive parameters based on blocks guide knowledge"""
        if drive_type in self.blocks_guide_knowledge["drive_guidance"]:
            guidance = self.blocks_guide_knowledge["drive_guidance"][drive_type]
            
            params = {}
            for param, value in guidance.items():
                if param.endswith("_range") and isinstance(value, tuple) and len(value) == 2:
                    param_name = param.replace("_range", "")
                    min_val, max_val = value
                    params[param_name] = round(random.uniform(min_val, max_val), 1)
            
            # Adjust based on amp type
            if amp_type and "marshall" in amp_type.lower():
                # Boost mids for Marshall
                params["tone"] = min(params.get("tone", 5.0) + 1.0, 10.0)
            elif amp_type and "fender" in amp_type.lower():
                # Boost highs for Fender
                params["tone"] = min(params.get("tone", 5.0) + 1.5, 10.0)
            
            return params
        
        # Fallback to generic parameters
        return {
            "drive": 5.0,
            "tone": 5.0,
            "level": 7.0
        }
    
    def get_cab_parameters(self, cab_type: str, genre: str = "rock") -> Dict:
        """Get intelligent cab parameters based on blocks guide knowledge"""
        if cab_type in self.blocks_guide_knowledge["cab_guidance"]:
            guidance = self.blocks_guide_knowledge["cab_guidance"][cab_type]
            
            # Generate mic placement based on guidance
            mic_distance = guidance.get("mic_distance", "1.0-3.0 inches")
            if "-" in mic_distance:
                min_dist, max_dist = map(float, mic_distance.replace(" inches", "").split("-"))
                distance = round(random.uniform(min_dist, max_dist), 1)
            else:
                distance = float(mic_distance.replace(" inches", ""))
            
            return {
                "mic_type": "Dynamic 57",
                "mic_position": guidance.get("mic_position", "Cap Edge"),
                "mic_distance": distance,
                "room_reverb": 0.2 if genre == "ambient" else 0.0
            }
        
        # Fallback to generic parameters
        return {
            "mic_type": "Dynamic 57",
            "mic_position": "Cap Edge",
            "mic_distance": 2.0,
            "room_reverb": 0.0
        }
    
    def get_signal_chain_guidance(self, genre: str) -> Dict:
        """Get signal chain guidance based on user manual knowledge"""
        return self.user_manual_knowledge["signal_chain_guidance"].get(genre, {
            "drive_order": ["drive"],
            "amp_type": "generic",
            "cab_type": "generic",
            "eq_emphasis": "balanced",
            "effects_order": ["eq", "delay", "reverb"]
        })
    
    def get_real_world_example(self, artist: str) -> Optional[Dict]:
        """Get real-world example settings for an artist"""
        return self.real_world_examples["artist_rigs"].get(artist.lower())
    
    def enhance_tone_with_guidance(self, tone_patch: Dict, query: str) -> Dict:
        """Enhance tone patch with blocks guide knowledge"""
        query_lower = query.lower()
        
        # Detect genre from query
        genre = "rock"
        if any(word in query_lower for word in ["metal", "heavy", "aggressive"]):
            genre = "metal"
        elif any(word in query_lower for word in ["blues", "bluesy"]):
            genre = "blues"
        elif any(word in query_lower for word in ["country", "twang"]):
            genre = "country"
        elif any(word in query_lower for word in ["ambient", "atmospheric"]):
            genre = "ambient"
        
        # Enhance amp parameters
        if "amp" in tone_patch and "parameters" in tone_patch["amp"]:
            amp_name = tone_patch["amp"]["type"]
            # Detect amp type from name
            amp_type = "generic"
            if "brit" in amp_name.lower() and "800" in amp_name.lower():
                amp_type = "marshall_jcm800"
            elif "marshall" in amp_name.lower() and "plexi" in amp_name.lower():
                amp_type = "marshall_plexi"
            elif "mesa" in amp_name.lower() and "mark" in amp_name.lower():
                amp_type = "mesa_mark_iic"
            elif "fender" in amp_name.lower() and "twin" in amp_name.lower():
                amp_type = "fender_twin"
            
            enhanced_params = self.get_amp_parameters(amp_type, genre)
            tone_patch["amp"]["parameters"].update(enhanced_params)
        
        # Enhance drive parameters
        for drive_key in ["drive_1", "drive_2"]:
            if drive_key in tone_patch and "parameters" in tone_patch[drive_key]:
                drive_name = tone_patch[drive_key]["type"]
                # Detect drive type from name
                drive_type = "generic"
                if "sd1" in drive_name.lower() or "super overdrive" in drive_name.lower():
                    drive_type = "boss_sd1"
                elif "tube screamer" in drive_name.lower() or "ts808" in drive_name.lower() or "ts9" in drive_name.lower():
                    drive_type = "tube_screamer_808"
                elif "klon" in drive_name.lower() or "centaur" in drive_name.lower():
                    drive_type = "klon_centaur"
                
                amp_name = tone_patch.get("amp", {}).get("type", "")
                enhanced_params = self.get_drive_parameters(drive_type, amp_name)
                tone_patch[drive_key]["parameters"].update(enhanced_params)
        
        # Enhance cab parameters
        if "cab" in tone_patch and "parameters" in tone_patch["cab"]:
            cab_type = tone_patch["cab"]["type"]
            enhanced_params = self.get_cab_parameters(cab_type, genre)
            tone_patch["cab"]["parameters"].update(enhanced_params)
        
        return tone_patch
    
    def get_genre_appropriate_effects(self, genre: str, effect_type: str, available_models: List[str]) -> List[str]:
        """Get genre-appropriate effects from available models"""
        genre_guidance = {
            "metal": {
                "drive": {
                    "recommended": ["Tube Screamer Pro", "TS808", "TS9", "Super Overdrive", "SD-1"],
                    "avoid": ["Distortion+ Pro", "Rat Distortion", "Fuzz", "Big Muff", "Octave Fuzz"]
                },
                "amp": {
                    "recommended": ["Brit 800 Mod", "Recto 2", "5150", "HBE", "Mesa Mark IIC+", "Modern High Gain"],
                    "avoid": ["Class-A", "Twin Reverb", "Deluxe Reverb", "AC30"]
                },
                "cab": {
                    "recommended": ["4x12 V30", "4x12 EV", "Mesa Oversized", "Marshall 4x12", "V30"],
                    "avoid": ["1x12", "2x10", "Jensen"]
                },
                "eq": {
                    "recommended": ["Graphic EQ", "Parametric EQ", "5 Band EQ", "10 Band EQ"],
                    "avoid": ["Shelving EQ", "Tone Control"]
                },
                "delay": {
                    "recommended": ["Analog Delay", "Dual Delay", "Digital Delay", "Tape Delay"],
                    "avoid": ["Filter Delay", "Reverse Delay", "Ping Pong Delay"]
                },
                "reverb": {
                    "recommended": ["Studio Reverb", "Room Reverb", "Plate Reverb"],
                    "avoid": ["Spring Reverb", "Hall Reverb", "Cathedral Reverb"]
                },
                "pitch": {
                    "recommended": [],  # No pitch effects for standard metal
                    "avoid": ["Ring Modulator", "Pitch Shifter", "Harmonizer", "Whammy"]
                },
                "dynamics": {
                    "recommended": ["Vintage Compressor", "Maximizer", "Compressor", "Opto Compressor"],
                    "avoid": ["De-Esser", "Gate", "Noise Gate"]
                },
                "modulation": {
                    "recommended": [],  # No modulation for standard metal
                    "avoid": ["Chorus", "Flanger", "Phaser", "Tremolo", "Vibrato"]
                }
            },
            "blues": {
                "drive": {
                    "recommended": ["Tube Screamer", "TS808", "TS9", "Fuzz Face", "Big Muff"],
                    "avoid": ["High Gain Distortion", "Metal Distortion"]
                },
                "amp": {
                    "recommended": ["Fender Twin", "Marshall Plexi", "Deluxe Reverb", "AC30"],
                    "avoid": ["High Gain", "Modern", "5150"]
                },
                "cab": {
                    "recommended": ["2x12", "4x12", "1x12", "Jensen"],
                    "avoid": ["V30", "High Gain"]
                },
                "eq": {
                    "recommended": ["Graphic EQ", "Parametric EQ"],
                    "avoid": []
                },
                "delay": {
                    "recommended": ["Analog Delay", "Tape Delay", "Digital Delay"],
                    "avoid": ["Reverse Delay", "Ping Pong Delay"]
                },
                "reverb": {
                    "recommended": ["Spring Reverb", "Plate Reverb", "Room Reverb"],
                    "avoid": ["Cathedral Reverb", "Hall Reverb"]
                },
                "pitch": {
                    "recommended": [],
                    "avoid": ["Ring Modulator", "Harmonizer"]
                },
                "dynamics": {
                    "recommended": ["Vintage Compressor", "Opto Compressor"],
                    "avoid": ["Maximizer", "Gate"]
                },
                "modulation": {
                    "recommended": ["Chorus", "Vibrato"],
                    "avoid": ["Flanger", "Phaser"]
                }
            },
            "country": {
                "drive": {
                    "recommended": ["Clean Boost", "Micro Boost", "Tube Screamer"],
                    "avoid": ["High Gain", "Fuzz", "Distortion"]
                },
                "amp": {
                    "recommended": ["Fender Twin", "Deluxe Reverb", "AC30"],
                    "avoid": ["High Gain", "Marshall", "Mesa"]
                },
                "cab": {
                    "recommended": ["1x12", "2x12", "Jensen"],
                    "avoid": ["4x12", "V30"]
                },
                "eq": {
                    "recommended": ["Graphic EQ", "Parametric EQ"],
                    "avoid": []
                },
                "delay": {
                    "recommended": ["Analog Delay", "Digital Delay"],
                    "avoid": ["Reverse Delay", "Ping Pong Delay"]
                },
                "reverb": {
                    "recommended": ["Spring Reverb", "Room Reverb"],
                    "avoid": ["Cathedral Reverb", "Hall Reverb"]
                },
                "pitch": {
                    "recommended": [],
                    "avoid": ["Ring Modulator", "Harmonizer"]
                },
                "dynamics": {
                    "recommended": ["Vintage Compressor", "Opto Compressor"],
                    "avoid": ["Maximizer", "Gate"]
                },
                "modulation": {
                    "recommended": ["Chorus", "Tremolo"],
                    "avoid": ["Flanger", "Phaser"]
                }
            }
        }
        
        if genre not in genre_guidance or effect_type not in genre_guidance[genre]:
            return available_models
        
        guidance = genre_guidance[genre][effect_type]
        recommended = guidance.get("recommended", [])
        avoid = guidance.get("avoid", [])
        
        # Filter available models based on recommendations
        appropriate_models = []
        
        # First, try to find recommended models
        for model in available_models:
            model_lower = model.lower()
            for rec in recommended:
                if rec.lower() in model_lower or model_lower in rec.lower():
                    appropriate_models.append(model)
                    break
        
        # If no recommended models found, use all available except avoided ones
        if not appropriate_models:
            for model in available_models:
                model_lower = model.lower()
                should_avoid = False
                for avoid_model in avoid:
                    if avoid_model.lower() in model_lower or model_lower in avoid_model.lower():
                        should_avoid = True
                        break
                if not should_avoid:
                    appropriate_models.append(model)
        
        return appropriate_models if appropriate_models else available_models
    
    def should_include_effect(self, genre: str, effect_type: str) -> bool:
        """Determine if an effect should be included for a given genre"""
        genre_rules = {
            "metal": {
                "drive": True,  # Usually 1-2 drives
                "amp": True,
                "cab": True,
                "eq": True,  # Important for mid-scoop
                "delay": True,  # For leads only
                "reverb": True,  # Subtle
                "pitch": False,  # Rarely used
                "dynamics": True,  # Compressor important
                "modulation": False  # Rarely used
            },
            "blues": {
                "drive": True,
                "amp": True,
                "cab": True,
                "eq": True,
                "delay": True,
                "reverb": True,
                "pitch": False,
                "dynamics": True,
                "modulation": True  # Chorus common
            },
            "country": {
                "drive": True,  # Usually just clean boost
                "amp": True,
                "cab": True,
                "eq": True,
                "delay": True,
                "reverb": True,
                "pitch": False,
                "dynamics": True,
                "modulation": True  # Tremolo common
            }
        }
        
        return genre_rules.get(genre, {}).get(effect_type, True)
