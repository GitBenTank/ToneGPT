"""
Comprehensive ToneGPT System Integration
Integrates all advanced features: Parameter Control, Controllers & Modifiers, Analysis Tools, 
Export & Integration, Advanced Tone Features, and Workflow Features
"""

import json
import uuid
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import copy

# Import all the new systems
from .advanced_parameter_control import (
    AdvancedParameterControl,
    Scene,
    Channel,
    GlobalBlock,
)
from .controllers_modifiers import ControllersModifiers, LFO, ADSR, Modifier
from .analysis_tools import (
    AnalysisTools,
    FrequencyResponse,
    HarmonicContent,
    DynamicRange,
)
from .export_integration import (
    ExportIntegration,
    FM9Preset,
    StudioSession,
    ParameterDocumentation,
)
from .advanced_tone_features import (
    AdvancedToneFeatures,
    ToneComparison,
    GenreBlend,
    PlayingStyleAdaptation,
)
from .workflow_features import WorkflowFeatures, HistoryEntry, ToneMetadata, BatchJob


@dataclass
class ComprehensiveTone:
    """Comprehensive tone with all advanced features"""

    tone_id: str
    name: str
    base_tone: Dict[str, Any]
    scenes: List[Scene]
    channels: Dict[str, Dict[str, Channel]]
    global_blocks: Dict[str, GlobalBlock]
    controllers: Dict[str, Any]
    modifiers: Dict[str, Modifier]
    analysis_data: Dict[str, Any]
    metadata: ToneMetadata
    advanced_features: Dict[str, Any]
    created_date: datetime
    modified_date: datetime


class ComprehensiveSystem:
    """Comprehensive ToneGPT system integrating all advanced features"""

    def __init__(self):
        # Initialize all subsystems
        self.parameter_control = AdvancedParameterControl()
        self.controllers_modifiers = ControllersModifiers()
        self.analysis_tools = AnalysisTools()
        self.export_integration = ExportIntegration()
        self.advanced_tone_features = AdvancedToneFeatures()
        self.workflow_features = WorkflowFeatures()

        # Comprehensive tones storage
        self.comprehensive_tones: Dict[str, ComprehensiveTone] = {}

        # System settings
        self.system_settings = {
            "auto_analysis": True,
            "auto_export": False,
            "real_time_monitoring": True,
            "advanced_features_enabled": True,
            "workflow_automation": True,
            "integration_level": "full",  # basic, intermediate, full
        }

    def create_comprehensive_tone(
        self, name: str, base_tone: Dict[str, Any], created_by: str = "ToneGPT"
    ) -> str:
        """Create a comprehensive tone with all advanced features"""
        tone_id = str(uuid.uuid4())

        # Create tone metadata
        metadata = self.workflow_features.create_tone_metadata(
            tone_id, name, base_tone, created_by
        )

        # Get scenes and channels from parameter control
        scenes = self.parameter_control.scenes
        channels = self.parameter_control.channels
        global_blocks = self.parameter_control.global_blocks

        # Get controllers and modifiers
        controllers = self.controllers_modifiers.get_controller_summary()
        modifiers = {
            mod_id: asdict(mod)
            for mod_id, mod in self.controllers_modifiers.modifiers.items()
        }

        # Perform analysis if enabled
        analysis_data = {}
        if self.system_settings["auto_analysis"]:
            analysis_data = self._perform_comprehensive_analysis(base_tone)

        # Get advanced features
        advanced_features = {
            "comparisons": len(self.advanced_tone_features.tone_comparisons),
            "variations": len(self.advanced_tone_features.tone_variations),
            "genre_blends": len(self.advanced_tone_features.genre_blends),
            "playing_style_adaptations": len(
                self.advanced_tone_features.playing_style_adaptations
            ),
            "guitar_optimizations": len(
                self.advanced_tone_features.guitar_optimizations
            ),
        }

        # Create comprehensive tone
        comprehensive_tone = ComprehensiveTone(
            tone_id=tone_id,
            name=name,
            base_tone=base_tone,
            scenes=scenes,
            channels=channels,
            global_blocks=global_blocks,
            controllers=controllers,
            modifiers=modifiers,
            analysis_data=analysis_data,
            metadata=metadata,
            advanced_features=advanced_features,
            created_date=datetime.now(),
            modified_date=datetime.now(),
        )

        self.comprehensive_tones[tone_id] = comprehensive_tone

        # Add to workflow history
        self.workflow_features.add_to_history(
            "create", base_tone, f"Created comprehensive tone: {name}"
        )

        return tone_id

    def _perform_comprehensive_analysis(
        self, tone_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform comprehensive analysis on tone data"""
        analysis_data = {}

        try:
            # Frequency response analysis
            freq_response = self.analysis_tools.analyze_frequency_response()
            analysis_data["frequency_response"] = asdict(freq_response)

            # Harmonic content analysis
            harmonic_content = self.analysis_tools.analyze_harmonic_content()
            analysis_data["harmonic_content"] = asdict(harmonic_content)

            # Dynamic range analysis
            dynamic_range = self.analysis_tools.analyze_dynamic_range()
            analysis_data["dynamic_range"] = asdict(dynamic_range)

            # Gain staging analysis
            gain_staging = self.analysis_tools.analyze_gain_staging(
                input_level=-12.0,  # Example values
                output_level=-6.0,
                compression_settings={},
            )
            analysis_data["gain_staging"] = asdict(gain_staging)

            # CPU usage monitoring
            block_usage = self._estimate_cpu_usage(tone_data)
            cpu_usage = self.analysis_tools.monitor_cpu_usage(block_usage)
            analysis_data["cpu_usage"] = asdict(cpu_usage)

        except Exception as e:
            analysis_data["error"] = str(e)

        return analysis_data

    def _estimate_cpu_usage(self, tone_data: Dict[str, Any]) -> Dict[str, float]:
        """Estimate CPU usage for tone blocks"""
        # Simplified CPU usage estimation
        cpu_usage = {}

        for block_type, block_data in tone_data.items():
            if isinstance(block_data, dict) and block_data.get("enabled", False):
                # Base CPU usage by block type
                base_usage = {
                    "amp": 15.0,
                    "cab": 8.0,
                    "drive": 5.0,
                    "delay": 12.0,
                    "reverb": 20.0,
                    "dynamics": 6.0,
                    "modulation": 8.0,
                    "eq": 4.0,
                }

                cpu_usage[block_type] = base_usage.get(block_type, 5.0)

        return cpu_usage

    def switch_scene(self, tone_id: str, scene_id: int) -> Dict[str, Any]:
        """Switch scene for a comprehensive tone"""
        if tone_id not in self.comprehensive_tones:
            return {}

        tone = self.comprehensive_tones[tone_id]
        scene_data = self.parameter_control.switch_scene(scene_id)

        if scene_data:
            # Update tone with scene data
            tone.modified_date = datetime.now()

            # Add to history
            self.workflow_features.add_to_history(
                "modify",
                tone.base_tone,
                f"Switched to scene {scene_id}: {scene_data.get('scene_name', 'Unknown')}",
            )

        return scene_data

    def switch_channel(
        self, tone_id: str, block_type: str, channel_id: str
    ) -> Dict[str, Any]:
        """Switch channel for a block in comprehensive tone"""
        if tone_id not in self.comprehensive_tones:
            return {}

        tone = self.comprehensive_tones[tone_id]
        channel_data = self.parameter_control.switch_channel(block_type, channel_id)

        if channel_data:
            # Update tone
            tone.modified_date = datetime.now()

            # Add to history
            self.workflow_features.add_to_history(
                "modify",
                tone.base_tone,
                f"Switched {block_type} to channel {channel_id}",
            )

        return channel_data

    def apply_modifier(
        self, tone_id: str, modifier_id: str, time: float = 0.0, gate: bool = True
    ) -> Dict[str, Any]:
        """Apply modifier to comprehensive tone"""
        if tone_id not in self.comprehensive_tones:
            return {}

        tone = self.comprehensive_tones[tone_id]

        # Apply modifier using controllers & modifiers system
        modified_tone = copy.deepcopy(tone.base_tone)

        for block_type, block_data in modified_tone.items():
            if isinstance(block_data, dict) and "parameters" in block_data:
                for param_name, param_value in block_data["parameters"].items():
                    if isinstance(param_value, (int, float)):
                        modified_value = self.controllers_modifiers.apply_modifier(
                            modifier_id, param_value, time, gate
                        )
                        block_data["parameters"][param_name] = modified_value

        # Update tone
        tone.base_tone = modified_tone
        tone.modified_date = datetime.now()

        # Add to history
        self.workflow_features.add_to_history(
            "modify", modified_tone, f"Applied modifier: {modifier_id}"
        )

        return modified_tone

    def create_tone_comparison(
        self, tone_id: str, comparison_tone: Dict[str, Any], comparison_name: str
    ) -> str:
        """Create tone comparison for comprehensive tone"""
        if tone_id not in self.comprehensive_tones:
            return ""

        tone = self.comprehensive_tones[tone_id]

        # Create comparison using advanced tone features
        comparison = self.advanced_tone_features.create_tone_comparison(
            tone.base_tone, comparison_tone, "side_by_side", comparison_name
        )

        return comparison_name

    def create_tone_variation(
        self,
        tone_id: str,
        variation_type: str,
        variation_amount: float,
        variation_name: str,
    ) -> str:
        """Create tone variation for comprehensive tone"""
        if tone_id not in self.comprehensive_tones:
            return ""

        tone = self.comprehensive_tones[tone_id]

        # Create variation using advanced tone features
        variation = self.advanced_tone_features.create_tone_variation(
            tone.base_tone, variation_type, variation_amount, variation_name
        )

        return variation_name

    def optimize_for_guitar(
        self, tone_id: str, guitar_type: str, optimization_name: str
    ) -> str:
        """Optimize comprehensive tone for guitar type"""
        if tone_id not in self.comprehensive_tones:
            return ""

        tone = self.comprehensive_tones[tone_id]

        # Create guitar optimization using advanced tone features
        optimization = self.advanced_tone_features.create_guitar_optimization(
            tone.base_tone, guitar_type, optimization_name
        )

        return optimization_name

    def adapt_for_playing_style(
        self, tone_id: str, playing_style: str, sensitivity: float, adaptation_name: str
    ) -> str:
        """Adapt comprehensive tone for playing style"""
        if tone_id not in self.comprehensive_tones:
            return ""

        tone = self.comprehensive_tones[tone_id]

        # Create playing style adaptation using advanced tone features
        adaptation = self.advanced_tone_features.create_playing_style_adaptation(
            tone.base_tone, playing_style, sensitivity, adaptation_name
        )

        return adaptation_name

    def export_comprehensive_tone(
        self, tone_id: str, export_format: str = "syx"
    ) -> bool:
        """Export comprehensive tone in various formats"""
        if tone_id not in self.comprehensive_tones:
            return False

        tone = self.comprehensive_tones[tone_id]

        try:
            if export_format == "syx":
                # Export as FM9 preset
                preset = self.export_integration.create_fm9_preset(
                    1, tone.name, tone.base_tone
                )
                return self.export_integration.export_syx_file(1, f"{tone.name}.syx")

            elif export_format == "studio":
                # Export as studio session
                session = self.export_integration.create_studio_session(
                    tone.name, f"./sessions/{tone.name}", [tone.base_tone]
                )
                return self.export_integration.export_studio_session(
                    tone.name, f"{tone.name}_session.json"
                )

            elif export_format == "documentation":
                # Export parameter documentation
                for block_type in tone.base_tone.keys():
                    doc = self.export_integration.create_parameter_documentation(
                        block_type, tone.base_tone
                    )
                    if doc:
                        self.export_integration.export_parameter_documentation(
                            block_type, f"{tone.name}_{block_type}_docs.md"
                        )
                return True

            else:
                return False

        except Exception as e:
            print(f"Error exporting tone: {e}")
            return False

    def batch_process_tones(
        self, operation: str, tone_ids: List[str], parameters: Dict[str, Any]
    ) -> str:
        """Batch process multiple comprehensive tones"""
        # Create batch job using workflow features
        batch_operation = getattr(
            self.workflow_features.BatchOperation, operation.upper(), None
        )
        if not batch_operation:
            return ""

        job_id = self.workflow_features.create_batch_job(
            batch_operation, tone_ids, parameters
        )

        # Execute batch job
        self.workflow_features.execute_batch_job(job_id)

        return job_id

    def search_tones(
        self,
        filters: Dict[str, Any],
        sort_by: str = "name",
        sort_order: str = "ascending",
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Search comprehensive tones"""
        # Create search query using workflow features
        search_filters = {}
        for filter_name, filter_value in filters.items():
            filter_enum = getattr(
                self.workflow_features.SearchFilter, filter_name.upper(), None
            )
            if filter_enum:
                search_filters[filter_enum] = filter_value

        sort_enum = getattr(self.workflow_features.SearchFilter, sort_by.upper(), None)
        order_enum = getattr(self.workflow_features.SortOrder, sort_order.upper(), None)

        if not sort_enum or not order_enum:
            return []

        query_id = self.workflow_features.create_search_query(
            search_filters, sort_enum, order_enum, limit
        )

        # Execute search
        results = self.workflow_features.execute_search(query_id)

        # Enhance results with comprehensive tone data
        enhanced_results = []
        for result in results:
            tone_id = result["tone_id"]
            if tone_id in self.comprehensive_tones:
                tone = self.comprehensive_tones[tone_id]
                enhanced_result = {
                    **result,
                    "comprehensive_tone": asdict(tone),
                    "scenes": [asdict(scene) for scene in tone.scenes],
                    "channels": tone.channels,
                    "global_blocks": {
                        bid: asdict(block) for bid, block in tone.global_blocks.items()
                    },
                    "analysis_data": tone.analysis_data,
                    "advanced_features": tone.advanced_features,
                }
                enhanced_results.append(enhanced_result)

        return enhanced_results

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "comprehensive_tones": len(self.comprehensive_tones),
            "parameter_control": self.parameter_control.get_scene_summary(),
            "controllers_modifiers": self.controllers_modifiers.get_controller_summary(),
            "analysis_tools": self.analysis_tools.get_analysis_summary(),
            "export_integration": self.export_integration.get_export_summary(),
            "advanced_tone_features": self.advanced_tone_features.get_advanced_features_summary(),
            "workflow_features": self.workflow_features.get_workflow_summary(),
            "system_settings": self.system_settings,
        }

    def get_comprehensive_tone_summary(self, tone_id: str) -> Dict[str, Any]:
        """Get comprehensive summary of a specific tone"""
        if tone_id not in self.comprehensive_tones:
            return {}

        tone = self.comprehensive_tones[tone_id]

        return {
            "tone_id": tone_id,
            "name": tone.name,
            "metadata": asdict(tone.metadata),
            "scenes": [asdict(scene) for scene in tone.scenes],
            "channels": tone.channels,
            "global_blocks": {
                bid: asdict(block) for bid, block in tone.global_blocks.items()
            },
            "controllers": tone.controllers,
            "modifiers": tone.modifiers,
            "analysis_data": tone.analysis_data,
            "advanced_features": tone.advanced_features,
            "created_date": tone.created_date.isoformat(),
            "modified_date": tone.modified_date.isoformat(),
        }

    def export_system_data(self, output_dir: str) -> bool:
        """Export all system data"""
        try:
            import os

            os.makedirs(output_dir, exist_ok=True)

            # Export comprehensive tones
            tones_data = {
                tone_id: asdict(tone)
                for tone_id, tone in self.comprehensive_tones.items()
            }
            with open(f"{output_dir}/comprehensive_tones.json", "w") as f:
                json.dump(tones_data, f, indent=2, default=str)

            # Export subsystem data
            self.parameter_control.save_to_file(f"{output_dir}/parameter_control.json")
            self.controllers_modifiers.save_to_file(
                f"{output_dir}/controllers_modifiers.json"
            )
            self.analysis_tools.save_analysis_to_file(
                f"{output_dir}/analysis_tools.json"
            )
            self.workflow_features.save_workflow_to_file(
                f"{output_dir}/workflow_features.json"
            )
            self.advanced_tone_features.save_advanced_features_to_file(
                f"{output_dir}/advanced_tone_features.json"
            )

            # Export system settings
            with open(f"{output_dir}/system_settings.json", "w") as f:
                json.dump(self.system_settings, f, indent=2)

            return True

        except Exception as e:
            print(f"Error exporting system data: {e}")
            return False

    def load_system_data(self, input_dir: str) -> bool:
        """Load all system data"""
        try:
            # Load comprehensive tones
            with open(f"{input_dir}/comprehensive_tones.json", "r") as f:
                tones_data = json.load(f)

            for tone_id, tone_data in tones_data.items():
                # Reconstruct comprehensive tone
                tone = ComprehensiveTone(**tone_data)
                self.comprehensive_tones[tone_id] = tone

            # Load subsystem data
            self.parameter_control.load_from_file(f"{input_dir}/parameter_control.json")
            self.controllers_modifiers.load_from_file(
                f"{input_dir}/controllers_modifiers.json"
            )
            self.analysis_tools.load_analysis_from_file(
                f"{input_dir}/analysis_tools.json"
            )
            self.workflow_features.load_workflow_from_file(
                f"{input_dir}/workflow_features.json"
            )
            self.advanced_tone_features.load_advanced_features_from_file(
                f"{input_dir}/advanced_tone_features.json"
            )

            # Load system settings
            with open(f"{input_dir}/system_settings.json", "r") as f:
                self.system_settings = json.load(f)

            return True

        except Exception as e:
            print(f"Error loading system data: {e}")
            return False
