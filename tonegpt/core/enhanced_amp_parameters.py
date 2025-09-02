"""
Enhanced Amplifier Parameters for ToneGPT AI
Extracted from Fractal Audio Blocks Guide PDF
"""


class EnhancedAmpParameters:
    """
    Advanced amplifier parameters extracted from FM9 Blocks Guide
    These match the professional parameters seen in FM9-Edit screenshots
    """

    @staticmethod
    def get_advanced_amp_parameters():
        """Get comprehensive advanced amp parameters"""
        return {
            "power_tube_modeling": {
                "power_tube_type": {
                    "description": "Changes the characteristics of the virtual amp power tubes",
                    "options": [
                        "6L6GC GE",
                        "6L6GC RCA",
                        "EL34",
                        "EL84",
                        "KT88",
                        "6550",
                    ],
                    "default": "6L6GC GE",
                    "category": "Power Amp",
                    "source": "FM9 Blocks Guide",
                },
                "grid_bias": {
                    "description": "Sets the bias point of the virtual power amp. Lower values approach pure Class-B",
                    "min": 0.0,
                    "max": 100.0,
                    "default": 58.9,
                    "unit": "%",
                    "category": "Power Amp",
                    "source": "FM9 Blocks Guide",
                },
                "hardness": {
                    "description": "Selecting a Power Tube Type loads the appropriate knee voltage for the virtual power tubes",
                    "min": 0.0,
                    "max": 10.0,
                    "default": 5.0,
                    "unit": "",
                    "category": "Power Amp",
                    "source": "FM9 Blocks Guide",
                },
                "mismatch": {
                    "description": "Simulates power tube mismatch in the virtual power amp",
                    "min": 0.0,
                    "max": 1.0,
                    "default": 0.0,
                    "unit": "",
                    "category": "Power Amp",
                    "source": "FM9 Blocks Guide",
                },
                "bias_excursion": {
                    "description": "Scales all of the other bias excursion parameters in the virtual power amp",
                    "min": 0.0,
                    "max": 100.0,
                    "default": 100.0,
                    "unit": "%",
                    "category": "Power Amp",
                    "source": "FM9 Blocks Guide",
                },
                "plate_suppressor_diodes": {
                    "description": "These diodes (also called snubber or flyback diodes) are found in some amps",
                    "options": ["Off", "On"],
                    "default": "Off",
                    "category": "Power Amp",
                    "source": "FM9 Blocks Guide",
                },
            },
            "power_supply_modeling": {
                "supply_sag": {
                    "description": "Controls dynamics in the virtual power amp. Higher settings simulate higher power supply impedance",
                    "min": 0.0,
                    "max": 10.0,
                    "default": 1.51,
                    "unit": "",
                    "category": "Power Supply",
                    "source": "FM9 Blocks Guide",
                },
                "b_time_constant": {
                    "description": "Interacts with the Supply Sag control by making the virtual power supply response more or less dynamic",
                    "min": 0.0,
                    "max": 100.0,
                    "default": 10.0,
                    "unit": "ms",
                    "category": "Power Supply",
                    "source": "FM9 Blocks Guide",
                },
                "power_type": {
                    "description": "Sets the power supply type for the virtual amp",
                    "options": ["AC", "DC"],
                    "default": "AC",
                    "category": "Power Supply",
                    "source": "FM9 Blocks Guide",
                },
                "ac_line_frequency": {
                    "description": "Sets the AC line frequency for the virtual amp",
                    "min": 50.0,
                    "max": 60.0,
                    "default": 60.0,
                    "unit": "Hz",
                    "category": "Power Supply",
                    "source": "FM9 Blocks Guide",
                },
                "variac": {
                    "description": "Sets the relative AC line voltage into the amp simulation. A Variac changes the volume of an amp",
                    "min": 0.0,
                    "max": 100.0,
                    "default": 100.0,
                    "unit": "%",
                    "category": "Power Supply",
                    "source": "FM9 Blocks Guide",
                },
            },
            "advanced_controls": {
                "bias_tremolo": {
                    "frequency": {
                        "description": "Frequency of the bias tremolo effect",
                        "min": 0.0,
                        "max": 10.0,
                        "default": 5.0,
                        "unit": "Hz",
                        "category": "Advanced Controls",
                        "source": "FM9 Blocks Guide",
                    },
                    "depth": {
                        "description": "Depth of the bias tremolo effect",
                        "min": 0.0,
                        "max": 100.0,
                        "default": 0.0,
                        "unit": "%",
                        "category": "Advanced Controls",
                        "source": "FM9 Blocks Guide",
                    },
                },
                "cathode_follower": {
                    "compression": {
                        "description": "Compression level of the cathode follower",
                        "min": 0.0,
                        "max": 100.0,
                        "default": 0.0,
                        "unit": "%",
                        "category": "Advanced Controls",
                        "source": "FM9 Blocks Guide",
                    },
                    "harmonics": {
                        "description": "Harmonic content of the cathode follower",
                        "min": 0.0,
                        "max": 10.0,
                        "default": 0.0,
                        "unit": "",
                        "category": "Advanced Controls",
                        "source": "FM9 Blocks Guide",
                    },
                },
                "screen_frequency": {
                    "description": "Resonant frequency of the virtual power tube screen filter",
                    "min": 0.0,
                    "max": 20.0,
                    "default": 8.0,
                    "unit": "",
                    "category": "Advanced Controls",
                    "source": "FM9 Blocks Guide",
                },
                "screen_q": {
                    "description": "Q factor of the virtual power tube screen filter",
                    "min": 0.0,
                    "max": 10.0,
                    "default": 0.5,
                    "unit": "",
                    "category": "Advanced Controls",
                    "source": "FM9 Blocks Guide",
                },
            },
            "dynamics_processing": {
                "input_dynamics": {
                    "gain": {
                        "description": "Input dynamics processing gain",
                        "min": 0.0,
                        "max": 20.0,
                        "default": 12.0,
                        "unit": "dB",
                        "category": "Dynamics",
                        "source": "FM9 Blocks Guide",
                    },
                    "threshold": {
                        "description": "Input dynamics processing threshold",
                        "min": -60.0,
                        "max": 0.0,
                        "default": -40.0,
                        "unit": "dB",
                        "category": "Dynamics",
                        "source": "FM9 Blocks Guide",
                    },
                },
                "output_compressor": {
                    "threshold": {
                        "description": "Output compressor threshold",
                        "min": -60.0,
                        "max": 0.0,
                        "default": -40.0,
                        "unit": "dB",
                        "category": "Dynamics",
                        "source": "FM9 Blocks Guide",
                    },
                    "clarity": {
                        "description": "Output compressor clarity",
                        "min": 0.0,
                        "max": 10.0,
                        "default": 6.51,
                        "unit": "",
                        "category": "Dynamics",
                        "source": "FM9 Blocks Guide",
                    },
                },
            },
            "advanced_eq": {
                "input_eq": {
                    "peaking_filter": {
                        "frequency": {
                            "description": "Peaking filter frequency",
                            "min": 20.0,
                            "max": 20000.0,
                            "default": 1000.0,
                            "unit": "Hz",
                            "category": "Input EQ",
                            "source": "FM9 Blocks Guide",
                        },
                        "q": {
                            "description": "Peaking filter Q factor",
                            "min": 0.1,
                            "max": 10.0,
                            "default": 0.707,
                            "unit": "",
                            "category": "Input EQ",
                            "source": "FM9 Blocks Guide",
                        },
                        "gain": {
                            "description": "Peaking filter gain",
                            "min": -12.0,
                            "max": 12.0,
                            "default": 0.0,
                            "unit": "dB",
                            "category": "Input EQ",
                            "source": "FM9 Blocks Guide",
                        },
                    },
                    "low_cut": {
                        "description": "Low cut frequency",
                        "min": 20.0,
                        "max": 20000.0,
                        "default": 645.0,
                        "unit": "Hz",
                        "category": "Input EQ",
                        "source": "FM9 Blocks Guide",
                    },
                    "high_cut": {
                        "description": "High cut frequency",
                        "min": 20.0,
                        "max": 20000.0,
                        "default": 20000.0,
                        "unit": "Hz",
                        "category": "Input EQ",
                        "source": "FM9 Blocks Guide",
                    },
                },
                "output_eq": {
                    "8_band_var_q": {
                        "description": "8 Band Variable Q Equalizer",
                        "bands": [
                            {
                                "freq": 62,
                                "gain": {
                                    "min": -12.0,
                                    "max": 12.0,
                                    "default": 0.0,
                                    "unit": "dB",
                                },
                            },
                            {
                                "freq": 125,
                                "gain": {
                                    "min": -12.0,
                                    "max": 12.0,
                                    "default": 0.0,
                                    "unit": "dB",
                                },
                            },
                            {
                                "freq": 250,
                                "gain": {
                                    "min": -12.0,
                                    "max": 12.0,
                                    "default": 0.0,
                                    "unit": "dB",
                                },
                            },
                            {
                                "freq": 500,
                                "gain": {
                                    "min": -12.0,
                                    "max": 12.0,
                                    "default": 0.0,
                                    "unit": "dB",
                                },
                            },
                            {
                                "freq": 1000,
                                "gain": {
                                    "min": -12.0,
                                    "max": 12.0,
                                    "default": 0.0,
                                    "unit": "dB",
                                },
                            },
                            {
                                "freq": 2000,
                                "gain": {
                                    "min": -12.0,
                                    "max": 12.0,
                                    "default": 0.0,
                                    "unit": "dB",
                                },
                            },
                            {
                                "freq": 4000,
                                "gain": {
                                    "min": -12.0,
                                    "max": 12.0,
                                    "default": 0.0,
                                    "unit": "dB",
                                },
                            },
                            {
                                "freq": 8000,
                                "gain": {
                                    "min": -12.0,
                                    "max": 12.0,
                                    "default": 0.0,
                                    "unit": "dB",
                                },
                            },
                        ],
                        "category": "Output EQ",
                        "source": "FM9 Blocks Guide",
                    }
                },
            },
        }

    @staticmethod
    def get_parameter_categories():
        """Get parameter categories for organization"""
        return [
            "Power Tube Modeling",
            "Power Supply Modeling",
            "Advanced Controls",
            "Dynamics Processing",
            "Advanced EQ",
        ]

    @staticmethod
    def get_parameter_count():
        """Get total count of advanced parameters"""
        params = EnhancedAmpParameters.get_advanced_amp_parameters()
        count = 0
        for category in params.values():
            for param_group in category.values():
                if isinstance(param_group, dict):
                    if "min" in param_group:  # Single parameter
                        count += 1
                    else:  # Parameter group
                        for sub_param in param_group.values():
                            if isinstance(sub_param, dict) and "min" in sub_param:
                                count += 1
        return count
