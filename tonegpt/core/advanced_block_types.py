"""
Advanced Block Types for ToneGPT AI
Extracted from Fractal Audio Blocks Guide PDF
"""


class AdvancedBlockTypes:
    """
    Advanced block types extracted from FM9 Blocks Guide
    These are the missing block types that enhance ToneGPT AI's capabilities
    """

    @staticmethod
    def get_advanced_delay_types():
        """Get advanced delay block types"""
        return {
            "plex_delay": {
                "name": "Plex Delay",
                "description": "Up to eight delay lines and pitch shifters interacting in a matrix. Gorgeous!",
                "parameters": {
                    "delay_lines": {
                        "min": 1,
                        "max": 8,
                        "default": 4,
                        "unit": "",
                        "description": "Number of delay lines",
                    },
                    "pitch_shift": {
                        "min": -24.0,
                        "max": 24.0,
                        "default": 0.0,
                        "unit": "semitones",
                        "description": "Pitch shift amount",
                    },
                    "feedback": {
                        "min": 0.0,
                        "max": 100.0,
                        "default": 30.0,
                        "unit": "%",
                        "description": "Feedback amount",
                    },
                    "mix": {
                        "min": 0.0,
                        "max": 100.0,
                        "default": 50.0,
                        "unit": "%",
                        "description": "Wet/dry mix",
                    },
                    "time": {
                        "min": 0.0,
                        "max": 2000.0,
                        "default": 500.0,
                        "unit": "ms",
                        "description": "Delay time",
                    },
                },
                "category": "Advanced Delay",
                "source": "FM9 Blocks Guide",
            },
            "multitap_delay": {
                "name": "Multitap Delay",
                "description": "Multiple delay taps with individual control",
                "parameters": {
                    "tap_count": {
                        "min": 1,
                        "max": 16,
                        "default": 4,
                        "unit": "",
                        "description": "Number of delay taps",
                    },
                    "tap_1_time": {
                        "min": 0.0,
                        "max": 2000.0,
                        "default": 250.0,
                        "unit": "ms",
                        "description": "Tap 1 delay time",
                    },
                    "tap_2_time": {
                        "min": 0.0,
                        "max": 2000.0,
                        "default": 500.0,
                        "unit": "ms",
                        "description": "Tap 2 delay time",
                    },
                    "tap_3_time": {
                        "min": 0.0,
                        "max": 2000.0,
                        "default": 750.0,
                        "unit": "ms",
                        "description": "Tap 3 delay time",
                    },
                    "tap_4_time": {
                        "min": 0.0,
                        "max": 2000.0,
                        "default": 1000.0,
                        "unit": "ms",
                        "description": "Tap 4 delay time",
                    },
                    "feedback": {
                        "min": 0.0,
                        "max": 100.0,
                        "default": 25.0,
                        "unit": "%",
                        "description": "Feedback amount",
                    },
                    "mix": {
                        "min": 0.0,
                        "max": 100.0,
                        "default": 40.0,
                        "unit": "%",
                        "description": "Wet/dry mix",
                    },
                },
                "category": "Advanced Delay",
                "source": "FM9 Blocks Guide",
            },
            "ten_tap_delay": {
                "name": "Ten-Tap Delay",
                "description": "Set the time, pan, and spacing of one to ten separate echoes",
                "parameters": {
                    "tap_count": {
                        "min": 1,
                        "max": 10,
                        "default": 5,
                        "unit": "",
                        "description": "Number of delay taps",
                    },
                    "base_time": {
                        "min": 0.0,
                        "max": 2000.0,
                        "default": 300.0,
                        "unit": "ms",
                        "description": "Base delay time",
                    },
                    "spacing": {
                        "min": 0.0,
                        "max": 1000.0,
                        "default": 100.0,
                        "unit": "ms",
                        "description": "Time between taps",
                    },
                    "pan_spread": {
                        "min": 0.0,
                        "max": 100.0,
                        "default": 50.0,
                        "unit": "%",
                        "description": "Pan spread between taps",
                    },
                    "feedback": {
                        "min": 0.0,
                        "max": 100.0,
                        "default": 20.0,
                        "unit": "%",
                        "description": "Feedback amount",
                    },
                    "mix": {
                        "min": 0.0,
                        "max": 100.0,
                        "default": 35.0,
                        "unit": "%",
                        "description": "Wet/dry mix",
                    },
                },
                "category": "Advanced Delay",
                "source": "FM9 Blocks Guide",
            },
            "megatap_delay": {
                "name": "Megatap Delay",
                "description": "Massive delay with up to 1000 taps for complex patterns",
                "parameters": {
                    "tap_count": {
                        "min": 1,
                        "max": 1000,
                        "default": 100,
                        "unit": "",
                        "description": "Number of delay taps",
                    },
                    "pattern_type": {
                        "options": [
                            "Linear",
                            "Exponential",
                            "Fibonacci",
                            "Random",
                            "Custom",
                        ],
                        "default": "Linear",
                        "description": "Tap pattern type",
                    },
                    "base_time": {
                        "min": 0.0,
                        "max": 5000.0,
                        "default": 100.0,
                        "unit": "ms",
                        "description": "Base delay time",
                    },
                    "time_multiplier": {
                        "min": 0.1,
                        "max": 10.0,
                        "default": 1.0,
                        "unit": "",
                        "description": "Time multiplier between taps",
                    },
                    "feedback": {
                        "min": 0.0,
                        "max": 100.0,
                        "default": 15.0,
                        "unit": "%",
                        "description": "Feedback amount",
                    },
                    "mix": {
                        "min": 0.0,
                        "max": 100.0,
                        "default": 30.0,
                        "unit": "%",
                        "description": "Wet/dry mix",
                    },
                },
                "category": "Advanced Delay",
                "source": "FM9 Blocks Guide",
            },
        }

    @staticmethod
    def get_audio_routing_blocks():
        """Get audio routing and mixing blocks"""
        return {
            "mixer": {
                "name": "Mixer",
                "description": "Allows you to mix up to six stereo signals",
                "parameters": {
                    "input_count": {
                        "min": 2,
                        "max": 6,
                        "default": 4,
                        "unit": "",
                        "description": "Number of input channels",
                    },
                    "input_1_level": {
                        "min": -60.0,
                        "max": 20.0,
                        "default": 0.0,
                        "unit": "dB",
                        "description": "Input 1 level",
                    },
                    "input_2_level": {
                        "min": -60.0,
                        "max": 20.0,
                        "default": 0.0,
                        "unit": "dB",
                        "description": "Input 2 level",
                    },
                    "input_3_level": {
                        "min": -60.0,
                        "max": 20.0,
                        "default": 0.0,
                        "unit": "dB",
                        "description": "Input 3 level",
                    },
                    "input_4_level": {
                        "min": -60.0,
                        "max": 20.0,
                        "default": 0.0,
                        "unit": "dB",
                        "description": "Input 4 level",
                    },
                    "master_level": {
                        "min": -60.0,
                        "max": 20.0,
                        "default": 0.0,
                        "unit": "dB",
                        "description": "Master output level",
                    },
                    "pan_1": {
                        "min": -100.0,
                        "max": 100.0,
                        "default": 0.0,
                        "unit": "%",
                        "description": "Input 1 pan",
                    },
                    "pan_2": {
                        "min": -100.0,
                        "max": 100.0,
                        "default": 0.0,
                        "unit": "%",
                        "description": "Input 2 pan",
                    },
                },
                "category": "Audio Routing",
                "source": "FM9 Blocks Guide",
            },
            "crossover": {
                "name": "Crossover",
                "description": "Split a signal into high and low frequency components",
                "parameters": {
                    "crossover_frequency": {
                        "min": 20.0,
                        "max": 20000.0,
                        "default": 1000.0,
                        "unit": "Hz",
                        "description": "Crossover frequency",
                    },
                    "slope": {
                        "options": ["6dB/oct", "12dB/oct", "18dB/oct", "24dB/oct"],
                        "default": "12dB/oct",
                        "description": "Crossover slope",
                    },
                    "high_level": {
                        "min": -60.0,
                        "max": 20.0,
                        "default": 0.0,
                        "unit": "dB",
                        "description": "High frequency level",
                    },
                    "low_level": {
                        "min": -60.0,
                        "max": 20.0,
                        "default": 0.0,
                        "unit": "dB",
                        "description": "Low frequency level",
                    },
                    "high_phase": {
                        "options": ["Normal", "Inverted"],
                        "default": "Normal",
                        "description": "High frequency phase",
                    },
                    "low_phase": {
                        "options": ["Normal", "Inverted"],
                        "default": "Normal",
                        "description": "Low frequency phase",
                    },
                },
                "category": "Audio Routing",
                "source": "FM9 Blocks Guide",
            },
        }

    @staticmethod
    def get_specialized_effects():
        """Get specialized effect blocks"""
        return {
            "resonator": {
                "name": "Resonator",
                "description": "Resonant comb filters in parallel. Create chords and more",
                "parameters": {
                    "resonator_count": {
                        "min": 1,
                        "max": 8,
                        "default": 4,
                        "unit": "",
                        "description": "Number of resonators",
                    },
                    "fundamental_freq": {
                        "min": 20.0,
                        "max": 20000.0,
                        "default": 440.0,
                        "unit": "Hz",
                        "description": "Fundamental frequency",
                    },
                    "resonance": {
                        "min": 0.0,
                        "max": 100.0,
                        "default": 50.0,
                        "unit": "%",
                        "description": "Resonance amount",
                    },
                    "decay": {
                        "min": 0.0,
                        "max": 10.0,
                        "default": 2.0,
                        "unit": "s",
                        "description": "Decay time",
                    },
                    "mix": {
                        "min": 0.0,
                        "max": 100.0,
                        "default": 30.0,
                        "unit": "%",
                        "description": "Wet/dry mix",
                    },
                },
                "category": "Specialized Effects",
                "source": "FM9 Blocks Guide",
            },
            "formant": {
                "name": "Formant",
                "description": "Create dynamic vowel sounds with this multi-mode formant filter",
                "parameters": {
                    "vowel_type": {
                        "options": ["A", "E", "I", "O", "U", "Custom"],
                        "default": "A",
                        "description": "Vowel type",
                    },
                    "formant_1_freq": {
                        "min": 200.0,
                        "max": 1000.0,
                        "default": 730.0,
                        "unit": "Hz",
                        "description": "Formant 1 frequency",
                    },
                    "formant_2_freq": {
                        "min": 800.0,
                        "max": 3000.0,
                        "default": 1090.0,
                        "unit": "Hz",
                        "description": "Formant 2 frequency",
                    },
                    "formant_3_freq": {
                        "min": 2000.0,
                        "max": 4000.0,
                        "default": 2440.0,
                        "unit": "Hz",
                        "description": "Formant 3 frequency",
                    },
                    "sensitivity": {
                        "min": 0.0,
                        "max": 100.0,
                        "default": 50.0,
                        "unit": "%",
                        "description": "Input sensitivity",
                    },
                    "mix": {
                        "min": 0.0,
                        "max": 100.0,
                        "default": 50.0,
                        "unit": "%",
                        "description": "Wet/dry mix",
                    },
                },
                "category": "Specialized Effects",
                "source": "FM9 Blocks Guide",
            },
            "vocoder": {
                "name": "Vocoder",
                "description": "Digital re-creation of the analog classic",
                "parameters": {
                    "band_count": {
                        "min": 8,
                        "max": 32,
                        "default": 16,
                        "unit": "",
                        "description": "Number of vocoder bands",
                    },
                    "carrier_source": {
                        "options": ["Internal", "External", "Guitar"],
                        "default": "Internal",
                        "description": "Carrier signal source",
                    },
                    "modulator_source": {
                        "options": ["Internal", "External", "Guitar"],
                        "default": "External",
                        "description": "Modulator signal source",
                    },
                    "bandwidth": {
                        "min": 0.1,
                        "max": 2.0,
                        "default": 1.0,
                        "unit": "",
                        "description": "Bandwidth control",
                    },
                    "sensitivity": {
                        "min": 0.0,
                        "max": 100.0,
                        "default": 50.0,
                        "unit": "%",
                        "description": "Input sensitivity",
                    },
                    "mix": {
                        "min": 0.0,
                        "max": 100.0,
                        "default": 70.0,
                        "unit": "%",
                        "description": "Wet/dry mix",
                    },
                },
                "category": "Specialized Effects",
                "source": "FM9 Blocks Guide",
            },
        }

    @staticmethod
    def get_dynacab_support():
        """Get DynaCab and UltraRes support"""
        return {
            "dynacab": {
                "name": "DynaCab",
                "description": "DynaCab™ transforms the experience of finding your tone. Instead of cycling through countless IRs",
                "features": {
                    "cab_count": 2150,
                    "mic_positions": ["Close", "Mid", "Far"],
                    "mic_types": ["Dynamic", "Condenser", "Ribbon"],
                    "room_types": ["Studio", "Live", "Ambient"],
                    "resolution": "UltraRes",
                },
                "parameters": {
                    "cab_model": {
                        "options": [
                            "4x12 Brit TV",
                            "4x12 USA Modern",
                            "2x12 Brit 30W",
                            "1x12 Open Back",
                        ],
                        "default": "4x12 Brit TV",
                        "description": "Cabinet model",
                    },
                    "mic_position": {
                        "options": ["Close", "Mid", "Far"],
                        "default": "Close",
                        "description": "Microphone position",
                    },
                    "mic_type": {
                        "options": ["Dynamic", "Condenser", "Ribbon"],
                        "default": "Dynamic",
                        "description": "Microphone type",
                    },
                    "room_type": {
                        "options": ["Studio", "Live", "Ambient"],
                        "default": "Studio",
                        "description": "Room type",
                    },
                    "low_cut": {
                        "min": 20.0,
                        "max": 1000.0,
                        "default": 80.0,
                        "unit": "Hz",
                        "description": "Low frequency cut",
                    },
                    "high_cut": {
                        "min": 2000.0,
                        "max": 20000.0,
                        "default": 8000.0,
                        "unit": "Hz",
                        "description": "High frequency cut",
                    },
                    "level": {
                        "min": -20.0,
                        "max": 20.0,
                        "default": 0.0,
                        "unit": "dB",
                        "description": "Output level",
                    },
                },
                "category": "Cabinet Technology",
                "source": "FM9 Blocks Guide",
            },
            "ultrares": {
                "name": "UltraRes",
                "description": "UltraRes and FullRes IRs provide higher resolution cabinet simulation",
                "features": {
                    "resolution": "UltraRes/FullRes",
                    "frequency_response": "Extended",
                    "phase_accuracy": "High",
                    "compatibility": "FM9/Axe-Fx III",
                },
                "parameters": {
                    "resolution_mode": {
                        "options": ["Standard", "UltraRes", "FullRes"],
                        "default": "UltraRes",
                        "description": "IR resolution mode",
                    },
                    "phase_correction": {
                        "options": ["Off", "On"],
                        "default": "On",
                        "description": "Phase correction",
                    },
                    "minimum_phase": {
                        "options": ["Off", "On"],
                        "default": "On",
                        "description": "Minimum phase transformation",
                    },
                },
                "category": "Cabinet Technology",
                "source": "FM9 Blocks Guide",
            },
        }

    @staticmethod
    def get_all_advanced_blocks():
        """Get all advanced block types"""
        return {
            **AdvancedBlockTypes.get_advanced_delay_types(),
            **AdvancedBlockTypes.get_audio_routing_blocks(),
            **AdvancedBlockTypes.get_specialized_effects(),
            **AdvancedBlockTypes.get_dynacab_support(),
        }

    @staticmethod
    def get_block_count():
        """Get total count of advanced blocks"""
        return len(AdvancedBlockTypes.get_all_advanced_blocks())
