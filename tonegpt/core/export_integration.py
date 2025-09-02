"""
Export & Integration System for ToneGPT
Implements FM9 preset files (.syx), Studio session files, Parameter documentation, 
Audio samples, MIDI control maps, and Studio recall sheets
"""

import json
import struct
import base64
import csv
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional, BinaryIO
from dataclasses import dataclass, asdict
from pathlib import Path
import datetime


@dataclass
class FM9Preset:
    """FM9 preset data structure"""

    preset_number: int
    preset_name: str
    blocks: Dict[str, Dict[str, Any]]
    scenes: List[Dict[str, Any]]
    global_blocks: Dict[str, Any]
    tempo: int
    tuner: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass
class StudioSession:
    """Studio session data structure"""

    session_name: str
    project_path: str
    tracks: List[Dict[str, Any]]
    effects: List[Dict[str, Any]]
    routing: Dict[str, Any]
    tempo: int
    time_signature: str
    sample_rate: int
    bit_depth: int
    metadata: Dict[str, Any]


@dataclass
class ParameterDocumentation:
    """Parameter documentation structure"""

    block_type: str
    block_name: str
    parameters: List[Dict[str, Any]]
    descriptions: Dict[str, str]
    ranges: Dict[str, Dict[str, float]]
    units: Dict[str, str]
    examples: List[Dict[str, Any]]


@dataclass
class MIDIControlMap:
    """MIDI control mapping structure"""

    preset_name: str
    cc_mappings: Dict[int, Dict[str, Any]]
    pc_mappings: Dict[int, str]
    sysex_messages: List[Dict[str, Any]]
    learn_mode: bool
    metadata: Dict[str, Any]


@dataclass
class StudioRecallSheet:
    """Studio recall sheet structure"""

    session_name: str
    date: str
    engineer: str
    preset_settings: Dict[str, Any]
    notes: str
    audio_samples: List[str]
    parameter_snapshots: List[Dict[str, Any]]


class ExportIntegration:
    """Export and Integration system for FM9"""

    def __init__(self):
        self.fm9_presets: Dict[int, FM9Preset] = {}
        self.studio_sessions: Dict[str, StudioSession] = {}
        self.parameter_docs: Dict[str, ParameterDocumentation] = {}
        self.midi_maps: Dict[str, MIDIControlMap] = {}
        self.recall_sheets: Dict[str, StudioRecallSheet] = {}

        # Export settings
        self.export_settings = {
            "syx_format": "fm9_v1.0",
            "studio_format": "pro_tools",
            "documentation_format": "markdown",
            "midi_format": "standard",
            "audio_format": "wav_24_48",
        }

    def create_fm9_preset(
        self, preset_number: int, preset_name: str, tone_patch: Dict[str, Any]
    ) -> FM9Preset:
        """Create FM9 preset from tone patch"""
        # Convert tone patch to FM9 preset format
        blocks = self._convert_tone_patch_to_blocks(tone_patch)
        scenes = self._create_default_scenes(blocks)
        global_blocks = self._extract_global_blocks(tone_patch)

        preset = FM9Preset(
            preset_number=preset_number,
            preset_name=preset_name,
            blocks=blocks,
            scenes=scenes,
            global_blocks=global_blocks,
            tempo=120,
            tuner={"enabled": True, "frequency": 440},
            metadata={
                "created_by": "ToneGPT",
                "created_date": datetime.datetime.now().isoformat(),
                "version": "1.0",
            },
        )

        self.fm9_presets[preset_number] = preset
        return preset

    def _convert_tone_patch_to_blocks(
        self, tone_patch: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """Convert tone patch to FM9 block format"""
        blocks = {}

        for block_type, block_data in tone_patch.items():
            if isinstance(block_data, dict) and block_data.get("enabled", False):
                fm9_block = {
                    "type": block_type.upper(),
                    "enabled": True,
                    "bypass": False,
                    "channels": block_data.get("channels", {}),
                    "parameters": block_data.get("parameters", {}),
                    "position": self._get_block_position(block_type),
                    "connections": self._get_block_connections(block_type),
                }
                blocks[block_type] = fm9_block

        return blocks

    def _get_block_position(self, block_type: str) -> Dict[str, int]:
        """Get block position in signal chain"""
        positions = {
            "input": {"x": 0, "y": 0},
            "drive": {"x": 1, "y": 0},
            "amp": {"x": 2, "y": 0},
            "cab": {"x": 3, "y": 0},
            "dynamics": {"x": 4, "y": 0},
            "eq": {"x": 5, "y": 0},
            "modulation": {"x": 6, "y": 0},
            "delay": {"x": 7, "y": 0},
            "reverb": {"x": 8, "y": 0},
            "output": {"x": 9, "y": 0},
        }
        return positions.get(block_type, {"x": 0, "y": 0})

    def _get_block_connections(self, block_type: str) -> List[Dict[str, str]]:
        """Get block connections in signal chain"""
        connections = {
            "input": [{"to": "drive", "from": "input"}],
            "drive": [{"to": "amp", "from": "drive"}],
            "amp": [{"to": "cab", "from": "amp"}],
            "cab": [{"to": "dynamics", "from": "cab"}],
            "dynamics": [{"to": "eq", "from": "dynamics"}],
            "eq": [{"to": "modulation", "from": "eq"}],
            "modulation": [{"to": "delay", "from": "modulation"}],
            "delay": [{"to": "reverb", "from": "delay"}],
            "reverb": [{"to": "output", "from": "reverb"}],
        }
        return connections.get(block_type, [])

    def _create_default_scenes(
        self, blocks: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create default scenes for preset"""
        scenes = []
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

        for i, scene_name in enumerate(scene_names):
            scene = {
                "scene_id": i + 1,
                "scene_name": scene_name,
                "block_states": self._generate_scene_states(blocks, scene_name),
                "tempo": 120,
                "description": f"{scene_name} tone scene",
            }
            scenes.append(scene)

        return scenes

    def _generate_scene_states(
        self, blocks: Dict[str, Dict[str, Any]], scene_name: str
    ) -> Dict[str, Any]:
        """Generate block states for a scene"""
        scene_states = {}

        for block_type, block_data in blocks.items():
            scene_states[block_type] = {
                "enabled": block_data["enabled"],
                "bypass": False,
                "channel": "A",
                "parameters": block_data["parameters"].copy(),
            }

            # Scene-specific adjustments
            if scene_name == "Clean":
                if block_type == "amp":
                    scene_states[block_type]["parameters"]["gain"] = 3.0
                elif block_type == "drive":
                    scene_states[block_type]["enabled"] = False
            elif scene_name == "Heavy":
                if block_type == "amp":
                    scene_states[block_type]["parameters"]["gain"] = 8.0
                elif block_type == "drive":
                    scene_states[block_type]["enabled"] = True

        return scene_states

    def _extract_global_blocks(self, tone_patch: Dict[str, Any]) -> Dict[str, Any]:
        """Extract global blocks from tone patch"""
        global_blocks = {}

        # Check for global reverb
        if "reverb" in tone_patch and tone_patch["reverb"].get("enabled"):
            global_blocks["global_reverb"] = {
                "type": "REVERB",
                "enabled": True,
                "parameters": tone_patch["reverb"]["parameters"],
            }

        # Check for global delay
        if "delay" in tone_patch and tone_patch["delay"].get("enabled"):
            global_blocks["global_delay"] = {
                "type": "DELAY",
                "enabled": True,
                "parameters": tone_patch["delay"]["parameters"],
            }

        return global_blocks

    def export_syx_file(self, preset_number: int, filepath: str) -> bool:
        """Export FM9 preset as .syx file"""
        if preset_number not in self.fm9_presets:
            return False

        preset = self.fm9_presets[preset_number]

        # Create SYX file structure
        syx_data = self._create_syx_data(preset)

        try:
            with open(filepath, "wb") as f:
                f.write(syx_data)
            return True
        except Exception as e:
            print(f"Error writing SYX file: {e}")
            return False

    def _create_syx_data(self, preset: FM9Preset) -> bytes:
        """Create SYX file data"""
        # FM9 SYX file format (simplified)
        syx_header = b"\xF0\x00\x01\x74"  # Fractal Audio Systems manufacturer ID
        syx_preset_data = self._encode_preset_data(preset)
        syx_checksum = self._calculate_checksum(syx_preset_data)
        syx_footer = b"\xF7"  # End of SYX

        return syx_header + syx_preset_data + syx_checksum + syx_footer

    def _encode_preset_data(self, preset: FM9Preset) -> bytes:
        """Encode preset data for SYX format"""
        # This is a simplified encoding - real FM9 SYX format is more complex
        data = {
            "preset_number": preset.preset_number,
            "preset_name": preset.preset_name,
            "blocks": preset.blocks,
            "scenes": preset.scenes,
            "tempo": preset.tempo,
        }

        # Convert to binary format
        json_data = json.dumps(data).encode("utf-8")
        return json_data

    def _calculate_checksum(self, data: bytes) -> bytes:
        """Calculate SYX checksum"""
        checksum = sum(data) & 0x7F
        return bytes([checksum])

    def create_studio_session(
        self, session_name: str, project_path: str, tone_patches: List[Dict[str, Any]]
    ) -> StudioSession:
        """Create studio session file"""
        tracks = []
        effects = []

        for i, tone_patch in enumerate(tone_patches):
            track = {
                "track_id": i + 1,
                "track_name": f"Guitar Track {i + 1}",
                "tone_patch": tone_patch,
                "volume": 0.0,
                "pan": 0.0,
                "mute": False,
                "solo": False,
            }
            tracks.append(track)

            # Extract effects for session
            for block_type, block_data in tone_patch.items():
                if isinstance(block_data, dict) and block_data.get("enabled"):
                    effect = {
                        "effect_id": f"{i}_{block_type}",
                        "effect_type": block_type,
                        "parameters": block_data.get("parameters", {}),
                        "enabled": True,
                    }
                    effects.append(effect)

        session = StudioSession(
            session_name=session_name,
            project_path=project_path,
            tracks=tracks,
            effects=effects,
            routing={"master_out": "stereo", "monitor": "stereo"},
            tempo=120,
            time_signature="4/4",
            sample_rate=48000,
            bit_depth=24,
            metadata={
                "created_by": "ToneGPT",
                "created_date": datetime.datetime.now().isoformat(),
                "version": "1.0",
            },
        )

        self.studio_sessions[session_name] = session
        return session

    def export_studio_session(
        self, session_name: str, filepath: str, format: str = "json"
    ) -> bool:
        """Export studio session file"""
        if session_name not in self.studio_sessions:
            return False

        session = self.studio_sessions[session_name]

        try:
            if format == "json":
                with open(filepath, "w") as f:
                    json.dump(asdict(session), f, indent=2)
            elif format == "xml":
                self._export_session_xml(session, filepath)
            elif format == "csv":
                self._export_session_csv(session, filepath)
            else:
                return False

            return True
        except Exception as e:
            print(f"Error exporting studio session: {e}")
            return False

    def _export_session_xml(self, session: StudioSession, filepath: str):
        """Export studio session as XML"""
        root = ET.Element("StudioSession")
        root.set("name", session.session_name)
        root.set("date", session.metadata["created_date"])

        # Add tracks
        tracks_elem = ET.SubElement(root, "Tracks")
        for track in session.tracks:
            track_elem = ET.SubElement(tracks_elem, "Track")
            track_elem.set("id", str(track["track_id"]))
            track_elem.set("name", track["track_name"])
            track_elem.set("volume", str(track["volume"]))
            track_elem.set("pan", str(track["pan"]))

        # Add effects
        effects_elem = ET.SubElement(root, "Effects")
        for effect in session.effects:
            effect_elem = ET.SubElement(effects_elem, "Effect")
            effect_elem.set("id", effect["effect_id"])
            effect_elem.set("type", effect["effect_type"])
            effect_elem.set("enabled", str(effect["enabled"]))

        # Write XML file
        tree = ET.ElementTree(root)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)

    def _export_session_csv(self, session: StudioSession, filepath: str):
        """Export studio session as CSV"""
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow(
                [
                    "Session Name",
                    "Track ID",
                    "Track Name",
                    "Volume",
                    "Pan",
                    "Mute",
                    "Solo",
                ]
            )

            # Write track data
            for track in session.tracks:
                writer.writerow(
                    [
                        session.session_name,
                        track["track_id"],
                        track["track_name"],
                        track["volume"],
                        track["pan"],
                        track["mute"],
                        track["solo"],
                    ]
                )

    def create_parameter_documentation(
        self, block_type: str, tone_patch: Dict[str, Any]
    ) -> ParameterDocumentation:
        """Create parameter documentation for a block"""
        if block_type not in tone_patch:
            return None

        block_data = tone_patch[block_type]
        parameters = []
        descriptions = {}
        ranges = {}
        units = {}
        examples = []

        # Extract parameters
        if "parameters" in block_data:
            for param_name, param_value in block_data["parameters"].items():
                parameters.append(
                    {
                        "name": param_name,
                        "value": param_value,
                        "type": type(param_value).__name__,
                    }
                )

                # Add descriptions
                descriptions[param_name] = self._get_parameter_description(
                    block_type, param_name
                )

                # Add ranges
                ranges[param_name] = self._get_parameter_range(block_type, param_name)

                # Add units
                units[param_name] = self._get_parameter_unit(block_type, param_name)

        # Add examples
        examples = self._get_parameter_examples(block_type)

        doc = ParameterDocumentation(
            block_type=block_type,
            block_name=block_data.get("model", "Unknown"),
            parameters=parameters,
            descriptions=descriptions,
            ranges=ranges,
            units=units,
            examples=examples,
        )

        self.parameter_docs[block_type] = doc
        return doc

    def _get_parameter_description(self, block_type: str, param_name: str) -> str:
        """Get parameter description"""
        descriptions = {
            "amp": {
                "gain": "Controls the preamp gain/distortion level",
                "bass": "Controls the low frequency response",
                "mid": "Controls the mid frequency response",
                "treble": "Controls the high frequency response",
                "presence": "Controls the high frequency presence",
                "master": "Controls the overall output level",
            },
            "cab": {
                "low_cut": "High-pass filter frequency",
                "high_cut": "Low-pass filter frequency",
                "level": "Output level of the cabinet",
            },
            "delay": {
                "time": "Delay time in milliseconds",
                "feedback": "Feedback amount (0-100%)",
                "mix": "Dry/wet mix (0-100%)",
            },
            "reverb": {
                "mix": "Dry/wet mix (0-100%)",
                "decay": "Reverb decay time in seconds",
                "room_size": "Size of the reverb room",
            },
        }

        return descriptions.get(block_type, {}).get(
            param_name, "Parameter description not available"
        )

    def _get_parameter_range(
        self, block_type: str, param_name: str
    ) -> Dict[str, float]:
        """Get parameter range"""
        ranges = {
            "amp": {
                "gain": {"min": 0.0, "max": 10.0},
                "bass": {"min": 0.0, "max": 10.0},
                "mid": {"min": 0.0, "max": 10.0},
                "treble": {"min": 0.0, "max": 10.0},
                "presence": {"min": 0.0, "max": 10.0},
                "master": {"min": 0.0, "max": 10.0},
            },
            "cab": {
                "low_cut": {"min": 20.0, "max": 1000.0},
                "high_cut": {"min": 1000.0, "max": 20000.0},
                "level": {"min": 0.0, "max": 10.0},
            },
            "delay": {
                "time": {"min": 1.0, "max": 2000.0},
                "feedback": {"min": 0.0, "max": 100.0},
                "mix": {"min": 0.0, "max": 100.0},
            },
            "reverb": {
                "mix": {"min": 0.0, "max": 100.0},
                "decay": {"min": 0.1, "max": 20.0},
                "room_size": {"min": 0.1, "max": 10.0},
            },
        }

        return ranges.get(block_type, {}).get(param_name, {"min": 0.0, "max": 100.0})

    def _get_parameter_unit(self, block_type: str, param_name: str) -> str:
        """Get parameter unit"""
        units = {
            "amp": {
                "gain": "",
                "bass": "",
                "mid": "",
                "treble": "",
                "presence": "",
                "master": "",
            },
            "cab": {"low_cut": "Hz", "high_cut": "Hz", "level": ""},
            "delay": {"time": "ms", "feedback": "%", "mix": "%"},
            "reverb": {"mix": "%", "decay": "s", "room_size": ""},
        }

        return units.get(block_type, {}).get(param_name, "")

    def _get_parameter_examples(self, block_type: str) -> List[Dict[str, Any]]:
        """Get parameter examples"""
        examples = {
            "amp": [
                {"name": "Clean", "gain": 3.0, "bass": 5.0, "mid": 6.0, "treble": 5.0},
                {"name": "Crunch", "gain": 6.0, "bass": 6.0, "mid": 7.0, "treble": 6.0},
                {"name": "Heavy", "gain": 8.0, "bass": 7.0, "mid": 4.0, "treble": 6.0},
            ],
            "cab": [
                {"name": "Bright", "low_cut": 100, "high_cut": 8000, "level": 7.0},
                {"name": "Warm", "low_cut": 80, "high_cut": 6000, "level": 7.0},
            ],
            "delay": [
                {"name": "Short", "time": 250, "feedback": 25, "mix": 20},
                {"name": "Long", "time": 500, "feedback": 40, "mix": 30},
            ],
            "reverb": [
                {"name": "Room", "mix": 25, "decay": 2.0, "room_size": 5.0},
                {"name": "Hall", "mix": 40, "decay": 4.0, "room_size": 8.0},
            ],
        }

        return examples.get(block_type, [])

    def export_parameter_documentation(
        self, block_type: str, filepath: str, format: str = "markdown"
    ) -> bool:
        """Export parameter documentation"""
        if block_type not in self.parameter_docs:
            return False

        doc = self.parameter_docs[block_type]

        try:
            if format == "markdown":
                self._export_doc_markdown(doc, filepath)
            elif format == "html":
                self._export_doc_html(doc, filepath)
            elif format == "json":
                with open(filepath, "w") as f:
                    json.dump(asdict(doc), f, indent=2)
            else:
                return False

            return True
        except Exception as e:
            print(f"Error exporting documentation: {e}")
            return False

    def _export_doc_markdown(self, doc: ParameterDocumentation, filepath: str):
        """Export documentation as Markdown"""
        with open(filepath, "w") as f:
            f.write(f"# {doc.block_type.upper()} Block Documentation\n\n")
            f.write(f"**Block Name:** {doc.block_name}\n\n")

            f.write("## Parameters\n\n")
            for param in doc.parameters:
                f.write(f"### {param['name']}\n")
                f.write(f"**Value:** {param['value']}\n")
                f.write(f"**Type:** {param['type']}\n")
                f.write(
                    f"**Description:** {doc.descriptions.get(param['name'], 'N/A')}\n"
                )

                if param["name"] in doc.ranges:
                    range_info = doc.ranges[param["name"]]
                    f.write(f"**Range:** {range_info['min']} - {range_info['max']}\n")

                if param["name"] in doc.units:
                    f.write(f"**Unit:** {doc.units[param['name']]}\n")

                f.write("\n")

            if doc.examples:
                f.write("## Examples\n\n")
                for example in doc.examples:
                    f.write(f"### {example['name']}\n")
                    for key, value in example.items():
                        if key != "name":
                            f.write(f"- **{key}:** {value}\n")
                    f.write("\n")

    def _export_doc_html(self, doc: ParameterDocumentation, filepath: str):
        """Export documentation as HTML"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{doc.block_type.upper()} Block Documentation</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #666; }}
                h3 {{ color: #888; }}
                .parameter {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; }}
                .example {{ margin: 15px 0; padding: 10px; background: #f5f5f5; }}
            </style>
        </head>
        <body>
            <h1>{doc.block_type.upper()} Block Documentation</h1>
            <p><strong>Block Name:</strong> {doc.block_name}</p>
            
            <h2>Parameters</h2>
        """

        for param in doc.parameters:
            html += f"""
            <div class="parameter">
                <h3>{param['name']}</h3>
                <p><strong>Value:</strong> {param['value']}</p>
                <p><strong>Type:</strong> {param['type']}</p>
                <p><strong>Description:</strong> {doc.descriptions.get(param['name'], 'N/A')}</p>
            """

            if param["name"] in doc.ranges:
                range_info = doc.ranges[param["name"]]
                html += f"<p><strong>Range:</strong> {range_info['min']} - {range_info['max']}</p>"

            if param["name"] in doc.units:
                html += f"<p><strong>Unit:</strong> {doc.units[param['name']]}</p>"

            html += "</div>"

        if doc.examples:
            html += "<h2>Examples</h2>"
            for example in doc.examples:
                html += f"""
                <div class="example">
                    <h3>{example['name']}</h3>
                """
                for key, value in example.items():
                    if key != "name":
                        html += f"<p><strong>{key}:</strong> {value}</p>"
                html += "</div>"

        html += """
        </body>
        </html>
        """

        with open(filepath, "w") as f:
            f.write(html)

    def create_midi_control_map(
        self, preset_name: str, cc_mappings: Dict[int, Dict[str, Any]]
    ) -> MIDIControlMap:
        """Create MIDI control mapping"""
        midi_map = MIDIControlMap(
            preset_name=preset_name,
            cc_mappings=cc_mappings,
            pc_mappings={1: "Clean", 2: "Crunch", 3: "Lead", 4: "Heavy"},
            sysex_messages=[],
            learn_mode=False,
            metadata={
                "created_by": "ToneGPT",
                "created_date": datetime.datetime.now().isoformat(),
                "version": "1.0",
            },
        )

        self.midi_maps[preset_name] = midi_map
        return midi_map

    def export_midi_control_map(self, preset_name: str, filepath: str) -> bool:
        """Export MIDI control mapping"""
        if preset_name not in self.midi_maps:
            return False

        midi_map = self.midi_maps[preset_name]

        try:
            with open(filepath, "w") as f:
                json.dump(asdict(midi_map), f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting MIDI map: {e}")
            return False

    def create_studio_recall_sheet(
        self, session_name: str, engineer: str, preset_settings: Dict[str, Any]
    ) -> StudioRecallSheet:
        """Create studio recall sheet"""
        recall_sheet = StudioRecallSheet(
            session_name=session_name,
            date=datetime.datetime.now().strftime("%Y-%m-%d"),
            engineer=engineer,
            preset_settings=preset_settings,
            notes="",
            audio_samples=[],
            parameter_snapshots=[],
        )

        self.recall_sheets[session_name] = recall_sheet
        return recall_sheet

    def export_studio_recall_sheet(self, session_name: str, filepath: str) -> bool:
        """Export studio recall sheet"""
        if session_name not in self.recall_sheets:
            return False

        recall_sheet = self.recall_sheets[session_name]

        try:
            with open(filepath, "w") as f:
                json.dump(asdict(recall_sheet), f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting recall sheet: {e}")
            return False

    def get_export_summary(self) -> Dict[str, Any]:
        """Get summary of all export data"""
        return {
            "fm9_presets": len(self.fm9_presets),
            "studio_sessions": len(self.studio_sessions),
            "parameter_docs": len(self.parameter_docs),
            "midi_maps": len(self.midi_maps),
            "recall_sheets": len(self.recall_sheets),
            "export_settings": self.export_settings,
        }

    def export_all_data(self, output_dir: str) -> bool:
        """Export all data to directory"""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)

            # Export FM9 presets
            for preset_number, preset in self.fm9_presets.items():
                syx_file = output_path / f"preset_{preset_number:03d}.syx"
                self.export_syx_file(preset_number, str(syx_file))

            # Export studio sessions
            for session_name, session in self.studio_sessions.items():
                session_file = output_path / f"{session_name}_session.json"
                self.export_studio_session(session_name, str(session_file))

            # Export parameter documentation
            for block_type, doc in self.parameter_docs.items():
                doc_file = output_path / f"{block_type}_documentation.md"
                self.export_parameter_documentation(block_type, str(doc_file))

            # Export MIDI maps
            for preset_name, midi_map in self.midi_maps.items():
                midi_file = output_path / f"{preset_name}_midi_map.json"
                self.export_midi_control_map(preset_name, str(midi_file))

            # Export recall sheets
            for session_name, recall_sheet in self.recall_sheets.items():
                recall_file = output_path / f"{session_name}_recall_sheet.json"
                self.export_studio_recall_sheet(session_name, str(recall_file))

            return True
        except Exception as e:
            print(f"Error exporting all data: {e}")
            return False
