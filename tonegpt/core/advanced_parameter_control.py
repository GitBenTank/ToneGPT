"""
Advanced Parameter Control System for ToneGPT
Implements Scene switching, Channel switching, Global blocks, Spillover, Global EQ, and Tempo integration
"""

import json
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Scene:
    """Represents a scene with specific block states"""

    scene_id: int
    name: str
    block_states: Dict[str, Dict[str, Any]]
    tempo: Optional[int] = None
    description: str = ""


@dataclass
class Channel:
    """Represents a channel with specific model and parameters"""

    channel_id: str  # A, B, C, D
    model: str
    parameters: Dict[str, Any]
    enabled: bool = True


@dataclass
class GlobalBlock:
    """Represents a global block that can be shared across presets"""

    block_id: str
    block_type: str
    name: str
    parameters: Dict[str, Any]
    shared_presets: List[str] = None


class AdvancedParameterControl:
    """Advanced parameter control system for FM9"""

    def __init__(self):
        self.scenes: List[Scene] = []
        self.channels: Dict[str, Dict[str, Channel]] = (
            {}
        )  # block_type -> channel_id -> Channel
        self.global_blocks: Dict[str, GlobalBlock] = {}
        self.spillover_settings: Dict[str, Any] = {}
        self.global_eq: Dict[str, Any] = {}
        self.tempo_settings: Dict[str, Any] = {}

        # Initialize with default scenes
        self._initialize_default_scenes()
        self._initialize_default_channels()
        self._initialize_global_blocks()
        self._initialize_spillover()
        self._initialize_global_eq()
        self._initialize_tempo()

    def _initialize_default_scenes(self):
        """Initialize 8 default scenes"""
        scene_names = [
            "Clean",
            "Crunch",
            "Lead",
            "Rhythm",
            "Ambient",
            "Heavy",
            "Solo",
            "Acoustic",
        ]

        for i, name in enumerate(scene_names):
            scene = Scene(
                scene_id=i + 1,
                name=name,
                block_states=self._generate_scene_block_states(name),
                tempo=self._get_scene_tempo(name),
                description=f"{name} tone scene",
            )
            self.scenes.append(scene)

    def _generate_scene_block_states(
        self, scene_name: str
    ) -> Dict[str, Dict[str, Any]]:
        """Generate block states for a specific scene"""
        block_states = {}

        # Scene-specific block configurations
        scene_configs = {
            "Clean": {
                "amp": {"enabled": True, "channel": "A", "gain": 3.0, "master": 7.0},
                "cab": {
                    "enabled": True,
                    "channel": "A",
                    "low_cut": 80,
                    "high_cut": 8000,
                },
                "reverb": {"enabled": True, "channel": "A", "mix": 25, "decay": 2.5},
                "delay": {"enabled": False},
                "drive": {"enabled": False},
                "dynamics": {
                    "enabled": True,
                    "channel": "A",
                    "threshold": -20,
                    "ratio": 2.0,
                },
            },
            "Crunch": {
                "amp": {"enabled": True, "channel": "B", "gain": 5.5, "master": 6.0},
                "cab": {
                    "enabled": True,
                    "channel": "B",
                    "low_cut": 100,
                    "high_cut": 7000,
                },
                "reverb": {"enabled": True, "channel": "B", "mix": 20, "decay": 2.0},
                "delay": {
                    "enabled": True,
                    "channel": "A",
                    "time": 300,
                    "feedback": 25,
                    "mix": 15,
                },
                "drive": {"enabled": True, "channel": "A", "drive": 4.0, "level": 6.0},
                "dynamics": {
                    "enabled": True,
                    "channel": "B",
                    "threshold": -15,
                    "ratio": 3.0,
                },
            },
            "Lead": {
                "amp": {"enabled": True, "channel": "C", "gain": 7.0, "master": 5.5},
                "cab": {
                    "enabled": True,
                    "channel": "C",
                    "low_cut": 120,
                    "high_cut": 6000,
                },
                "reverb": {"enabled": True, "channel": "C", "mix": 35, "decay": 3.5},
                "delay": {
                    "enabled": True,
                    "channel": "B",
                    "time": 400,
                    "feedback": 30,
                    "mix": 25,
                },
                "drive": {"enabled": True, "channel": "B", "drive": 6.0, "level": 7.0},
                "dynamics": {
                    "enabled": True,
                    "channel": "C",
                    "threshold": -12,
                    "ratio": 4.0,
                },
            },
            "Rhythm": {
                "amp": {"enabled": True, "channel": "D", "gain": 6.5, "master": 6.5},
                "cab": {
                    "enabled": True,
                    "channel": "D",
                    "low_cut": 90,
                    "high_cut": 6500,
                },
                "reverb": {"enabled": True, "channel": "D", "mix": 15, "decay": 1.8},
                "delay": {"enabled": False},
                "drive": {"enabled": True, "channel": "C", "drive": 5.5, "level": 6.5},
                "dynamics": {
                    "enabled": True,
                    "channel": "D",
                    "threshold": -18,
                    "ratio": 3.5,
                },
            },
            "Ambient": {
                "amp": {"enabled": True, "channel": "A", "gain": 4.0, "master": 6.0},
                "cab": {
                    "enabled": True,
                    "channel": "A",
                    "low_cut": 60,
                    "high_cut": 10000,
                },
                "reverb": {"enabled": True, "channel": "A", "mix": 60, "decay": 8.0},
                "delay": {
                    "enabled": True,
                    "channel": "C",
                    "time": 600,
                    "feedback": 40,
                    "mix": 35,
                },
                "drive": {"enabled": False},
                "dynamics": {
                    "enabled": True,
                    "channel": "A",
                    "threshold": -25,
                    "ratio": 2.5,
                },
            },
            "Heavy": {
                "amp": {"enabled": True, "channel": "B", "gain": 8.5, "master": 5.0},
                "cab": {
                    "enabled": True,
                    "channel": "B",
                    "low_cut": 150,
                    "high_cut": 5000,
                },
                "reverb": {"enabled": True, "channel": "B", "mix": 20, "decay": 2.2},
                "delay": {
                    "enabled": True,
                    "channel": "D",
                    "time": 250,
                    "feedback": 20,
                    "mix": 12,
                },
                "drive": {"enabled": True, "channel": "D", "drive": 7.5, "level": 8.0},
                "dynamics": {
                    "enabled": True,
                    "channel": "B",
                    "threshold": -10,
                    "ratio": 6.0,
                },
            },
            "Solo": {
                "amp": {"enabled": True, "channel": "C", "gain": 7.5, "master": 5.8},
                "cab": {
                    "enabled": True,
                    "channel": "C",
                    "low_cut": 110,
                    "high_cut": 5500,
                },
                "reverb": {"enabled": True, "channel": "C", "mix": 40, "decay": 4.0},
                "delay": {
                    "enabled": True,
                    "channel": "A",
                    "time": 350,
                    "feedback": 35,
                    "mix": 30,
                },
                "drive": {"enabled": True, "channel": "B", "drive": 6.5, "level": 7.5},
                "dynamics": {
                    "enabled": True,
                    "channel": "C",
                    "threshold": -14,
                    "ratio": 4.5,
                },
            },
            "Acoustic": {
                "amp": {"enabled": True, "channel": "D", "gain": 2.5, "master": 7.5},
                "cab": {
                    "enabled": True,
                    "channel": "D",
                    "low_cut": 70,
                    "high_cut": 12000,
                },
                "reverb": {"enabled": True, "channel": "D", "mix": 30, "decay": 3.0},
                "delay": {
                    "enabled": True,
                    "channel": "B",
                    "time": 500,
                    "feedback": 25,
                    "mix": 20,
                },
                "drive": {"enabled": False},
                "dynamics": {
                    "enabled": True,
                    "channel": "D",
                    "threshold": -22,
                    "ratio": 2.0,
                },
            },
        }

        return scene_configs.get(scene_name, scene_configs["Clean"])

    def _get_scene_tempo(self, scene_name: str) -> int:
        """Get appropriate tempo for scene"""
        tempo_map = {
            "Clean": 120,
            "Crunch": 130,
            "Lead": 140,
            "Rhythm": 125,
            "Ambient": 90,
            "Heavy": 160,
            "Solo": 150,
            "Acoustic": 110,
        }
        return tempo_map.get(scene_name, 120)

    def _initialize_default_channels(self):
        """Initialize 4 channels for each block type"""
        block_types = [
            "amp",
            "cab",
            "drive",
            "delay",
            "reverb",
            "dynamics",
            "modulation",
            "eq",
        ]

        for block_type in block_types:
            self.channels[block_type] = {}
            for channel_id in ["A", "B", "C", "D"]:
                channel = Channel(
                    channel_id=channel_id,
                    model=self._get_channel_model(block_type, channel_id),
                    parameters=self._get_channel_parameters(block_type, channel_id),
                    enabled=True,
                )
                self.channels[block_type][channel_id] = channel

    def _get_channel_model(self, block_type: str, channel_id: str) -> str:
        """Get appropriate model for channel"""
        models = {
            "amp": {
                "A": "Fender Twin Reverb",
                "B": "Marshall Plexi 100W",
                "C": "Mesa Boogie Dual Rectifier",
                "D": "Vox AC30",
            },
            "cab": {
                "A": "Fender Twin 2x12",
                "B": "Marshall 1960A 4x12",
                "C": "Mesa Rectifier 4x12",
                "D": "Vox AC30 2x12",
            },
            "drive": {
                "A": "Tube Screamer TS808",
                "B": "Boss DS-1",
                "C": "ProCo Rat",
                "D": "Klon Centaur",
            },
            "delay": {
                "A": "Analog Delay",
                "B": "Tape Delay",
                "C": "Digital Stereo",
                "D": "Ping Pong",
            },
            "reverb": {
                "A": "Spring Reverb",
                "B": "Plate Reverb",
                "C": "Hall Reverb",
                "D": "Room Reverb",
            },
            "dynamics": {
                "A": "Studio Compressor",
                "B": "Optical Compressor",
                "C": "Multiband Compressor",
                "D": "Gate/Expander",
            },
            "modulation": {
                "A": "Chorus",
                "B": "Flanger",
                "C": "Phaser",
                "D": "Tremolo",
            },
            "eq": {
                "A": "Graphic EQ 10-band",
                "B": "Parametric EQ",
                "C": "Dynamic EQ",
                "D": "Tilt EQ",
            },
        }

        return models.get(block_type, {}).get(channel_id, "Default")

    def _get_channel_parameters(
        self, block_type: str, channel_id: str
    ) -> Dict[str, Any]:
        """Get default parameters for channel"""
        # This would be expanded with actual parameter ranges
        return {"level": 7.0, "enabled": True, "bypass": False}

    def _initialize_global_blocks(self):
        """Initialize global blocks that can be shared across presets"""
        global_blocks = [
            {
                "block_id": "global_reverb",
                "block_type": "reverb",
                "name": "Global Hall Reverb",
                "parameters": {
                    "type": "Hall",
                    "mix": 25,
                    "decay": 3.0,
                    "size": 7.0,
                    "pre_delay": 20,
                },
            },
            {
                "block_id": "global_delay",
                "block_type": "delay",
                "name": "Global Tape Delay",
                "parameters": {
                    "type": "Tape",
                    "time": 400,
                    "feedback": 30,
                    "mix": 20,
                    "modulation": 15,
                },
            },
            {
                "block_id": "global_comp",
                "block_type": "dynamics",
                "name": "Global Studio Comp",
                "parameters": {
                    "type": "Studio",
                    "threshold": -18,
                    "ratio": 3.0,
                    "attack": 5,
                    "release": 100,
                },
            },
        ]

        for block_data in global_blocks:
            global_block = GlobalBlock(
                block_id=block_data["block_id"],
                block_type=block_data["block_type"],
                name=block_data["name"],
                parameters=block_data["parameters"],
                shared_presets=[],
            )
            self.global_blocks[block_data["block_id"]] = global_block

    def _initialize_spillover(self):
        """Initialize spillover settings"""
        self.spillover_settings = {
            "delay_spillover": True,
            "reverb_spillover": True,
            "modulation_spillover": False,
            "spillover_time": 2.0,  # seconds
            "spillover_fade": True,
        }

    def _initialize_global_eq(self):
        """Initialize global EQ settings"""
        self.global_eq = {
            "output_1": {
                "enabled": True,
                "low_cut": 80,
                "high_cut": 8000,
                "low_shelf": {"freq": 100, "gain": 0},
                "high_shelf": {"freq": 8000, "gain": 0},
                "parametric": [
                    {"freq": 200, "q": 1.0, "gain": 0},
                    {"freq": 1000, "q": 1.0, "gain": 0},
                    {"freq": 4000, "q": 1.0, "gain": 0},
                ],
            },
            "output_2": {
                "enabled": True,
                "low_cut": 80,
                "high_cut": 8000,
                "low_shelf": {"freq": 100, "gain": 0},
                "high_shelf": {"freq": 8000, "gain": 0},
                "parametric": [
                    {"freq": 200, "q": 1.0, "gain": 0},
                    {"freq": 1000, "q": 1.0, "gain": 0},
                    {"freq": 4000, "q": 1.0, "gain": 0},
                ],
            },
        }

    def _initialize_tempo(self):
        """Initialize tempo settings"""
        self.tempo_settings = {
            "global_tempo": 120,
            "tap_tempo": True,
            "tempo_sync": True,
            "tempo_source": "internal",  # internal, external, tap
            "tempo_multiplier": 1.0,
            "tempo_divisions": {
                "delay": "quarter",
                "modulation": "eighth",
                "tremolo": "quarter",
            },
        }

    def switch_scene(self, scene_id: int) -> Dict[str, Any]:
        """Switch to a specific scene"""
        if 1 <= scene_id <= 8:
            scene = self.scenes[scene_id - 1]
            return {
                "scene_id": scene_id,
                "scene_name": scene.name,
                "block_states": scene.block_states,
                "tempo": scene.tempo,
                "description": scene.description,
            }
        return {}

    def switch_channel(self, block_type: str, channel_id: str) -> Dict[str, Any]:
        """Switch to a specific channel for a block"""
        if block_type in self.channels and channel_id in self.channels[block_type]:
            channel = self.channels[block_type][channel_id]
            return {
                "block_type": block_type,
                "channel_id": channel_id,
                "model": channel.model,
                "parameters": channel.parameters,
                "enabled": channel.enabled,
            }
        return {}

    def create_global_block(
        self, block_id: str, block_type: str, name: str, parameters: Dict[str, Any]
    ) -> bool:
        """Create a new global block"""
        if block_id not in self.global_blocks:
            global_block = GlobalBlock(
                block_id=block_id,
                block_type=block_type,
                name=name,
                parameters=parameters,
                shared_presets=[],
            )
            self.global_blocks[block_id] = global_block
            return True
        return False

    def share_global_block(self, block_id: str, preset_name: str) -> bool:
        """Share a global block with a preset"""
        if block_id in self.global_blocks:
            if preset_name not in self.global_blocks[block_id].shared_presets:
                self.global_blocks[block_id].shared_presets.append(preset_name)
            return True
        return False

    def set_spillover(self, effect_type: str, enabled: bool) -> bool:
        """Enable/disable spillover for an effect type"""
        if effect_type in self.spillover_settings:
            self.spillover_settings[f"{effect_type}_spillover"] = enabled
            return True
        return False

    def set_global_eq(self, output: str, eq_settings: Dict[str, Any]) -> bool:
        """Set global EQ for an output"""
        if output in self.global_eq:
            self.global_eq[output].update(eq_settings)
            return True
        return False

    def set_tempo(self, tempo: int, source: str = "internal") -> bool:
        """Set global tempo"""
        if 60 <= tempo <= 200:
            self.tempo_settings["global_tempo"] = tempo
            self.tempo_settings["tempo_source"] = source
            return True
        return False

    def get_scene_summary(self) -> Dict[str, Any]:
        """Get summary of all scenes"""
        return {
            "scenes": [
                {
                    "id": scene.scene_id,
                    "name": scene.name,
                    "tempo": scene.tempo,
                    "description": scene.description,
                }
                for scene in self.scenes
            ],
            "current_scene": 1,
            "total_scenes": len(self.scenes),
        }

    def get_channel_summary(self) -> Dict[str, Any]:
        """Get summary of all channels"""
        summary = {}
        for block_type, channels in self.channels.items():
            summary[block_type] = {
                channel_id: {"model": channel.model, "enabled": channel.enabled}
                for channel_id, channel in channels.items()
            }
        return summary

    def get_global_blocks_summary(self) -> Dict[str, Any]:
        """Get summary of global blocks"""
        return {
            block_id: {
                "block_type": block.block_type,
                "name": block.name,
                "shared_presets": block.shared_presets,
            }
            for block_id, block in self.global_blocks.items()
        }

    def export_preset(self, preset_name: str) -> Dict[str, Any]:
        """Export a complete preset with all advanced features"""
        return {
            "preset_name": preset_name,
            "scenes": [scene.__dict__ for scene in self.scenes],
            "channels": {
                block_type: {
                    channel_id: channel.__dict__
                    for channel_id, channel in channels.items()
                }
                for block_type, channels in self.channels.items()
            },
            "global_blocks": {
                block_id: block.__dict__
                for block_id, block in self.global_blocks.items()
            },
            "spillover_settings": self.spillover_settings,
            "global_eq": self.global_eq,
            "tempo_settings": self.tempo_settings,
        }

    def save_to_file(self, filepath: str):
        """Save advanced parameter control settings to file"""
        data = self.export_preset("advanced_control")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filepath: str):
        """Load advanced parameter control settings from file"""
        with open(filepath, "r") as f:
            data = json.load(f)

        # Reconstruct scenes
        self.scenes = [Scene(**scene_data) for scene_data in data.get("scenes", [])]

        # Reconstruct channels
        self.channels = {}
        for block_type, channels_data in data.get("channels", {}).items():
            self.channels[block_type] = {
                channel_id: Channel(**channel_data)
                for channel_id, channel_data in channels_data.items()
            }

        # Reconstruct global blocks
        self.global_blocks = {
            block_id: GlobalBlock(**block_data)
            for block_id, block_data in data.get("global_blocks", {}).items()
        }

        # Load other settings
        self.spillover_settings = data.get("spillover_settings", {})
        self.global_eq = data.get("global_eq", {})
        self.tempo_settings = data.get("tempo_settings", {})
