"""
Advanced Tone Features System for ToneGPT
Implements A/B tone comparison, Parameter locking, Tone variations, Genre blending, 
Playing style adaptation, and Guitar type optimization
"""

import json
import random
import copy
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np


class ComparisonMode(Enum):
    SIDE_BY_SIDE = "side_by_side"
    A_B_SWITCH = "a_b_switch"
    BLEND = "blend"
    DIFFERENCE = "difference"


class ParameterLockType(Enum):
    ABSOLUTE = "absolute"
    RELATIVE = "relative"
    RANGE = "range"
    EXPRESSION = "expression"


class VariationType(Enum):
    SUBTLE = "subtle"
    MODERATE = "moderate"
    DRAMATIC = "dramatic"
    CUSTOM = "custom"


class GenreBlendType(Enum):
    LINEAR = "linear"
    WEIGHTED = "weighted"
    SELECTIVE = "selective"
    HYBRID = "hybrid"


class PlayingStyle(Enum):
    FINGERPICKING = "fingerpicking"
    STRUMMING = "strumming"
    PICKING = "picking"
    SLIDE = "slide"
    HAMMER_ON = "hammer_on"
    PULL_OFF = "pull_off"
    BEND = "bend"
    VIBRATO = "vibrato"


class GuitarType(Enum):
    STRATOCASTER = "stratocaster"
    LES_PAUL = "les_paul"
    TELECASTER = "telecaster"
    SG = "sg"
    JAZZMASTER = "jazzmaster"
    HUMBUCKER = "humbucker"
    SINGLE_COIL = "single_coil"
    P90 = "p90"


@dataclass
class ToneComparison:
    """A/B tone comparison data"""

    tone_a: Dict[str, Any]
    tone_b: Dict[str, Any]
    comparison_mode: ComparisonMode
    differences: Dict[str, Any]
    blend_ratio: float  # 0.0 = 100% A, 1.0 = 100% B
    metadata: Dict[str, Any]


@dataclass
class ParameterLock:
    """Parameter locking configuration"""

    parameter_name: str
    block_type: str
    lock_type: ParameterLockType
    locked_value: Any
    min_range: Optional[float] = None
    max_range: Optional[float] = None
    expression_source: Optional[str] = None


@dataclass
class ToneVariation:
    """Tone variation configuration"""

    base_tone: Dict[str, Any]
    variation_type: VariationType
    variation_amount: float  # 0.0 = no change, 1.0 = maximum change
    modified_parameters: Dict[str, Any]
    description: str


@dataclass
class GenreBlend:
    """Genre blending configuration"""

    primary_genre: str
    secondary_genre: str
    blend_type: GenreBlendType
    blend_ratio: float  # 0.0 = 100% primary, 1.0 = 100% secondary
    blended_tone: Dict[str, Any]
    blend_parameters: Dict[str, Any]


@dataclass
class PlayingStyleAdaptation:
    """Playing style adaptation configuration"""

    base_tone: Dict[str, Any]
    playing_style: PlayingStyle
    adapted_tone: Dict[str, Any]
    style_parameters: Dict[str, Any]
    sensitivity: float  # 0.0 = no adaptation, 1.0 = full adaptation


@dataclass
class GuitarOptimization:
    """Guitar type optimization configuration"""

    base_tone: Dict[str, Any]
    guitar_type: GuitarType
    optimized_tone: Dict[str, Any]
    optimization_parameters: Dict[str, Any]
    pickup_type: str
    scale_length: float


class AdvancedToneFeatures:
    """Advanced tone features system for FM9"""

    def __init__(self):
        self.tone_comparisons: Dict[str, ToneComparison] = {}
        self.parameter_locks: Dict[str, ParameterLock] = {}
        self.tone_variations: Dict[str, ToneVariation] = {}
        self.genre_blends: Dict[str, GenreBlend] = {}
        self.playing_style_adaptations: Dict[str, PlayingStyleAdaptation] = {}
        self.guitar_optimizations: Dict[str, GuitarOptimization] = {}

        # Style and guitar type profiles
        self.playing_style_profiles = self._initialize_playing_style_profiles()
        self.guitar_type_profiles = self._initialize_guitar_type_profiles()
        self.genre_blend_profiles = self._initialize_genre_blend_profiles()

    def _initialize_playing_style_profiles(self) -> Dict[PlayingStyle, Dict[str, Any]]:
        """Initialize playing style profiles"""
        return {
            PlayingStyle.FINGERPICKING: {
                "dynamics": {
                    "threshold": -25,
                    "ratio": 2.0,
                    "attack": 10,
                    "release": 100,
                },
                "eq": {"bass": 6.0, "mid": 7.0, "treble": 5.0},
                "reverb": {"mix": 30, "decay": 2.5, "room_size": 6.0},
                "delay": {"time": 400, "feedback": 20, "mix": 15},
            },
            PlayingStyle.STRUMMING: {
                "dynamics": {
                    "threshold": -20,
                    "ratio": 3.0,
                    "attack": 5,
                    "release": 80,
                },
                "eq": {"bass": 5.0, "mid": 6.0, "treble": 6.0},
                "reverb": {"mix": 25, "decay": 2.0, "room_size": 5.0},
                "delay": {"time": 300, "feedback": 25, "mix": 20},
            },
            PlayingStyle.PICKING: {
                "dynamics": {
                    "threshold": -18,
                    "ratio": 4.0,
                    "attack": 3,
                    "release": 60,
                },
                "eq": {"bass": 4.0, "mid": 7.0, "treble": 7.0},
                "reverb": {"mix": 20, "decay": 1.8, "room_size": 4.0},
                "delay": {"time": 250, "feedback": 30, "mix": 25},
            },
            PlayingStyle.SLIDE: {
                "dynamics": {
                    "threshold": -22,
                    "ratio": 2.5,
                    "attack": 8,
                    "release": 120,
                },
                "eq": {"bass": 6.0, "mid": 6.0, "treble": 5.0},
                "reverb": {"mix": 35, "decay": 3.0, "room_size": 7.0},
                "delay": {"time": 500, "feedback": 35, "mix": 30},
            },
            PlayingStyle.HAMMER_ON: {
                "dynamics": {
                    "threshold": -16,
                    "ratio": 3.5,
                    "attack": 2,
                    "release": 50,
                },
                "eq": {"bass": 5.0, "mid": 7.0, "treble": 6.0},
                "reverb": {"mix": 22, "decay": 2.2, "room_size": 5.5},
                "delay": {"time": 280, "feedback": 28, "mix": 22},
            },
            PlayingStyle.PULL_OFF: {
                "dynamics": {
                    "threshold": -17,
                    "ratio": 3.2,
                    "attack": 2,
                    "release": 55,
                },
                "eq": {"bass": 5.0, "mid": 7.0, "treble": 6.0},
                "reverb": {"mix": 22, "decay": 2.2, "room_size": 5.5},
                "delay": {"time": 280, "feedback": 28, "mix": 22},
            },
            PlayingStyle.BEND: {
                "dynamics": {
                    "threshold": -19,
                    "ratio": 3.0,
                    "attack": 4,
                    "release": 70,
                },
                "eq": {"bass": 5.0, "mid": 6.5, "treble": 6.0},
                "reverb": {"mix": 25, "decay": 2.5, "room_size": 6.0},
                "delay": {"time": 320, "feedback": 30, "mix": 25},
            },
            PlayingStyle.VIBRATO: {
                "dynamics": {
                    "threshold": -18,
                    "ratio": 3.0,
                    "attack": 3,
                    "release": 65,
                },
                "eq": {"bass": 5.0, "mid": 6.5, "treble": 6.0},
                "reverb": {"mix": 25, "decay": 2.5, "room_size": 6.0},
                "delay": {"time": 320, "feedback": 30, "mix": 25},
            },
        }

    def _initialize_guitar_type_profiles(self) -> Dict[GuitarType, Dict[str, Any]]:
        """Initialize guitar type profiles"""
        return {
            GuitarType.STRATOCASTER: {
                "pickup_type": "single_coil",
                "scale_length": 25.5,
                "eq_adjustments": {"bass": -1.0, "mid": 0.0, "treble": 1.0},
                "gain_adjustment": -0.5,
                "presence_adjustment": 0.5,
            },
            GuitarType.LES_PAUL: {
                "pickup_type": "humbucker",
                "scale_length": 24.75,
                "eq_adjustments": {"bass": 1.0, "mid": 0.5, "treble": -0.5},
                "gain_adjustment": 0.5,
                "presence_adjustment": -0.5,
            },
            GuitarType.TELECASTER: {
                "pickup_type": "single_coil",
                "scale_length": 25.5,
                "eq_adjustments": {"bass": -0.5, "mid": 0.5, "treble": 0.0},
                "gain_adjustment": -0.3,
                "presence_adjustment": 0.3,
            },
            GuitarType.SG: {
                "pickup_type": "humbucker",
                "scale_length": 24.75,
                "eq_adjustments": {"bass": 0.5, "mid": 0.0, "treble": -0.5},
                "gain_adjustment": 0.3,
                "presence_adjustment": -0.3,
            },
            GuitarType.JAZZMASTER: {
                "pickup_type": "single_coil",
                "scale_length": 25.5,
                "eq_adjustments": {"bass": 0.0, "mid": -0.5, "treble": 0.5},
                "gain_adjustment": -0.2,
                "presence_adjustment": 0.2,
            },
            GuitarType.HUMBUCKER: {
                "pickup_type": "humbucker",
                "scale_length": 24.75,
                "eq_adjustments": {"bass": 0.8, "mid": 0.3, "treble": -0.8},
                "gain_adjustment": 0.6,
                "presence_adjustment": -0.6,
            },
            GuitarType.SINGLE_COIL: {
                "pickup_type": "single_coil",
                "scale_length": 25.5,
                "eq_adjustments": {"bass": -0.8, "mid": 0.0, "treble": 0.8},
                "gain_adjustment": -0.6,
                "presence_adjustment": 0.6,
            },
            GuitarType.P90: {
                "pickup_type": "p90",
                "scale_length": 24.75,
                "eq_adjustments": {"bass": 0.3, "mid": 0.5, "treble": -0.3},
                "gain_adjustment": 0.2,
                "presence_adjustment": -0.2,
            },
        }

    def _initialize_genre_blend_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Initialize genre blend profiles"""
        return {
            "metal_blues": {
                "amp": {"gain": 0.7, "bass": 0.3, "mid": 0.8, "treble": 0.5},
                "drive": {"drive": 0.6, "level": 0.4},
                "dynamics": {"threshold": 0.5, "ratio": 0.3},
                "reverb": {"mix": 0.8, "decay": 0.6},
            },
            "jazz_rock": {
                "amp": {"gain": 0.3, "bass": 0.7, "mid": 0.5, "treble": 0.6},
                "drive": {"drive": 0.2, "level": 0.3},
                "dynamics": {"threshold": 0.8, "ratio": 0.2},
                "reverb": {"mix": 0.9, "decay": 0.8},
            },
            "country_metal": {
                "amp": {"gain": 0.8, "bass": 0.4, "mid": 0.3, "treble": 0.7},
                "drive": {"drive": 0.7, "level": 0.5},
                "dynamics": {"threshold": 0.4, "ratio": 0.6},
                "reverb": {"mix": 0.6, "decay": 0.4},
            },
            "ambient_metal": {
                "amp": {"gain": 0.9, "bass": 0.5, "mid": 0.2, "treble": 0.6},
                "drive": {"drive": 0.8, "level": 0.6},
                "dynamics": {"threshold": 0.3, "ratio": 0.7},
                "reverb": {"mix": 0.95, "decay": 0.9},
            },
        }

    def create_tone_comparison(
        self,
        tone_a: Dict[str, Any],
        tone_b: Dict[str, Any],
        comparison_mode: ComparisonMode,
        name: str,
    ) -> ToneComparison:
        """Create A/B tone comparison"""
        differences = self._calculate_tone_differences(tone_a, tone_b)

        comparison = ToneComparison(
            tone_a=tone_a,
            tone_b=tone_b,
            comparison_mode=comparison_mode,
            differences=differences,
            blend_ratio=0.5,
            metadata={
                "created_by": "ToneGPT",
                "created_date": "2024-01-01",
                "version": "1.0",
            },
        )

        self.tone_comparisons[name] = comparison
        return comparison

    def _calculate_tone_differences(
        self, tone_a: Dict[str, Any], tone_b: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate differences between two tones"""
        differences = {}

        for block_type in set(tone_a.keys()) | set(tone_b.keys()):
            if block_type in tone_a and block_type in tone_b:
                block_a = tone_a[block_type]
                block_b = tone_b[block_type]

                if isinstance(block_a, dict) and isinstance(block_b, dict):
                    block_diffs = {}

                    # Compare parameters
                    if "parameters" in block_a and "parameters" in block_b:
                        params_a = block_a["parameters"]
                        params_b = block_b["parameters"]

                        for param_name in set(params_a.keys()) | set(params_b.keys()):
                            if param_name in params_a and param_name in params_b:
                                if isinstance(
                                    params_a[param_name], (int, float)
                                ) and isinstance(params_b[param_name], (int, float)):
                                    block_diffs[param_name] = (
                                        params_b[param_name] - params_a[param_name]
                                    )
                                else:
                                    block_diffs[param_name] = (
                                        f"{params_a[param_name]} → {params_b[param_name]}"
                                    )
                            elif param_name in params_a:
                                block_diffs[param_name] = (
                                    f"{params_a[param_name]} → None"
                                )
                            else:
                                block_diffs[param_name] = (
                                    f"None → {params_b[param_name]}"
                                )

                    if block_diffs:
                        differences[block_type] = block_diffs

        return differences

    def blend_tones(self, comparison_name: str, blend_ratio: float) -> Dict[str, Any]:
        """Blend two tones based on comparison"""
        if comparison_name not in self.tone_comparisons:
            return {}

        comparison = self.tone_comparisons[comparison_name]
        comparison.blend_ratio = blend_ratio

        return self._create_blended_tone(
            comparison.tone_a, comparison.tone_b, blend_ratio
        )

    def _create_blended_tone(
        self, tone_a: Dict[str, Any], tone_b: Dict[str, Any], blend_ratio: float
    ) -> Dict[str, Any]:
        """Create blended tone from two tones"""
        blended_tone = {}

        for block_type in set(tone_a.keys()) | set(tone_b.keys()):
            if block_type in tone_a and block_type in tone_b:
                block_a = tone_a[block_type]
                block_b = tone_b[block_type]

                if isinstance(block_a, dict) and isinstance(block_b, dict):
                    blended_block = block_a.copy()

                    # Blend parameters
                    if "parameters" in block_a and "parameters" in block_b:
                        params_a = block_a["parameters"]
                        params_b = block_b["parameters"]

                        blended_params = {}
                        for param_name in set(params_a.keys()) | set(params_b.keys()):
                            if param_name in params_a and param_name in params_b:
                                if isinstance(
                                    params_a[param_name], (int, float)
                                ) and isinstance(params_b[param_name], (int, float)):
                                    blended_params[param_name] = (
                                        params_a[param_name]
                                        + (params_b[param_name] - params_a[param_name])
                                        * blend_ratio
                                    )
                                else:
                                    blended_params[param_name] = (
                                        params_b[param_name]
                                        if blend_ratio > 0.5
                                        else params_a[param_name]
                                    )
                            elif param_name in params_a:
                                blended_params[param_name] = params_a[param_name]
                            else:
                                blended_params[param_name] = params_b[param_name]

                        blended_block["parameters"] = blended_params

                    blended_tone[block_type] = blended_block
            elif block_type in tone_a:
                blended_tone[block_type] = tone_a[block_type]
            else:
                blended_tone[block_type] = tone_b[block_type]

        return blended_tone

    def create_parameter_lock(
        self,
        parameter_name: str,
        block_type: str,
        lock_type: ParameterLockType,
        locked_value: Any,
        name: str,
    ) -> ParameterLock:
        """Create parameter lock"""
        lock = ParameterLock(
            parameter_name=parameter_name,
            block_type=block_type,
            lock_type=lock_type,
            locked_value=locked_value,
        )

        self.parameter_locks[name] = lock
        return lock

    def apply_parameter_locks(self, tone_patch: Dict[str, Any]) -> Dict[str, Any]:
        """Apply parameter locks to tone patch"""
        locked_tone = copy.deepcopy(tone_patch)

        for lock_name, lock in self.parameter_locks.items():
            if lock.block_type in locked_tone:
                block = locked_tone[lock.block_type]
                if isinstance(block, dict) and "parameters" in block:
                    if lock.lock_type == ParameterLockType.ABSOLUTE:
                        block["parameters"][lock.parameter_name] = lock.locked_value
                    elif lock.lock_type == ParameterLockType.RELATIVE:
                        if lock.parameter_name in block["parameters"]:
                            block["parameters"][
                                lock.parameter_name
                            ] += lock.locked_value
                    elif lock.lock_type == ParameterLockType.RANGE:
                        if lock.parameter_name in block["parameters"]:
                            current_value = block["parameters"][lock.parameter_name]
                            if (
                                lock.min_range is not None
                                and current_value < lock.min_range
                            ):
                                block["parameters"][
                                    lock.parameter_name
                                ] = lock.min_range
                            if (
                                lock.max_range is not None
                                and current_value > lock.max_range
                            ):
                                block["parameters"][
                                    lock.parameter_name
                                ] = lock.max_range

        return locked_tone

    def create_tone_variation(
        self,
        base_tone: Dict[str, Any],
        variation_type: VariationType,
        variation_amount: float,
        name: str,
    ) -> ToneVariation:
        """Create tone variation"""
        modified_parameters = self._generate_variation_parameters(
            base_tone, variation_type, variation_amount
        )

        variation = ToneVariation(
            base_tone=base_tone,
            variation_type=variation_type,
            variation_amount=variation_amount,
            modified_parameters=modified_parameters,
            description=f"{variation_type.value} variation with {variation_amount:.1%} intensity",
        )

        self.tone_variations[name] = variation
        return variation

    def _generate_variation_parameters(
        self,
        base_tone: Dict[str, Any],
        variation_type: VariationType,
        variation_amount: float,
    ) -> Dict[str, Any]:
        """Generate variation parameters"""
        variation_params = {}

        # Define variation ranges based on type
        variation_ranges = {
            VariationType.SUBTLE: 0.1,
            VariationType.MODERATE: 0.3,
            VariationType.DRAMATIC: 0.6,
            VariationType.CUSTOM: variation_amount,
        }

        range_multiplier = variation_ranges.get(variation_type, 0.3)

        for block_type, block_data in base_tone.items():
            if isinstance(block_data, dict) and "parameters" in block_data:
                block_variations = {}

                for param_name, param_value in block_data["parameters"].items():
                    if isinstance(param_value, (int, float)):
                        # Calculate variation range
                        variation_range = range_multiplier * variation_amount

                        # Generate random variation
                        variation = random.uniform(-variation_range, variation_range)
                        new_value = param_value + variation

                        # Clamp to reasonable ranges
                        if param_name in [
                            "gain",
                            "bass",
                            "mid",
                            "treble",
                            "presence",
                            "master",
                        ]:
                            new_value = max(0, min(10, new_value))
                        elif param_name in ["mix", "feedback"]:
                            new_value = max(0, min(100, new_value))
                        elif param_name == "time":
                            new_value = max(1, min(2000, new_value))
                        elif param_name == "decay":
                            new_value = max(0.1, min(20, new_value))

                        block_variations[param_name] = new_value

                if block_variations:
                    variation_params[block_type] = block_variations

        return variation_params

    def create_genre_blend(
        self,
        primary_genre: str,
        secondary_genre: str,
        blend_type: GenreBlendType,
        blend_ratio: float,
        name: str,
    ) -> GenreBlend:
        """Create genre blend"""
        blend_key = f"{primary_genre}_{secondary_genre}"
        if blend_key not in self.genre_blend_profiles:
            blend_key = f"{secondary_genre}_{primary_genre}"

        if blend_key in self.genre_blend_profiles:
            blend_profile = self.genre_blend_profiles[blend_key]
            blended_tone = self._create_genre_blended_tone(blend_profile, blend_ratio)
        else:
            blended_tone = self._create_generic_genre_blend(
                primary_genre, secondary_genre, blend_ratio
            )

        blend = GenreBlend(
            primary_genre=primary_genre,
            secondary_genre=secondary_genre,
            blend_type=blend_type,
            blend_ratio=blend_ratio,
            blended_tone=blended_tone,
            blend_parameters=(
                blend_profile if blend_key in self.genre_blend_profiles else {}
            ),
        )

        self.genre_blends[name] = blend
        return blend

    def _create_genre_blended_tone(
        self, blend_profile: Dict[str, Any], blend_ratio: float
    ) -> Dict[str, Any]:
        """Create genre blended tone from profile"""
        blended_tone = {}

        for block_type, block_params in blend_profile.items():
            blended_block = {"enabled": True, "parameters": {}}

            for param_name, param_weight in block_params.items():
                # Apply blend ratio to parameter weight
                blended_value = param_weight * blend_ratio
                blended_block["parameters"][param_name] = blended_value

            blended_tone[block_type] = blended_block

        return blended_tone

    def _create_generic_genre_blend(
        self, primary_genre: str, secondary_genre: str, blend_ratio: float
    ) -> Dict[str, Any]:
        """Create generic genre blend"""
        # This would be expanded with actual genre profiles
        return {
            "amp": {
                "enabled": True,
                "parameters": {
                    "gain": 5.0 + (blend_ratio * 2.0),
                    "bass": 5.0 + (blend_ratio * 1.0),
                    "mid": 5.0 + (blend_ratio * 0.5),
                    "treble": 5.0 + (blend_ratio * 1.5),
                },
            },
            "reverb": {
                "enabled": True,
                "parameters": {
                    "mix": 25 + (blend_ratio * 15),
                    "decay": 2.0 + (blend_ratio * 1.0),
                },
            },
        }

    def create_playing_style_adaptation(
        self,
        base_tone: Dict[str, Any],
        playing_style: PlayingStyle,
        sensitivity: float,
        name: str,
    ) -> PlayingStyleAdaptation:
        """Create playing style adaptation"""
        style_profile = self.playing_style_profiles.get(playing_style, {})
        adapted_tone = self._adapt_tone_for_playing_style(
            base_tone, style_profile, sensitivity
        )

        adaptation = PlayingStyleAdaptation(
            base_tone=base_tone,
            playing_style=playing_style,
            adapted_tone=adapted_tone,
            style_parameters=style_profile,
            sensitivity=sensitivity,
        )

        self.playing_style_adaptations[name] = adaptation
        return adaptation

    def _adapt_tone_for_playing_style(
        self,
        base_tone: Dict[str, Any],
        style_profile: Dict[str, Any],
        sensitivity: float,
    ) -> Dict[str, Any]:
        """Adapt tone for playing style"""
        adapted_tone = copy.deepcopy(base_tone)

        for block_type, style_params in style_profile.items():
            if block_type in adapted_tone and isinstance(
                adapted_tone[block_type], dict
            ):
                block = adapted_tone[block_type]
                if "parameters" in block:
                    for param_name, style_value in style_params.items():
                        if param_name in block["parameters"]:
                            current_value = block["parameters"][param_name]
                            # Blend current value with style value based on sensitivity
                            adapted_value = (
                                current_value
                                + (style_value - current_value) * sensitivity
                            )
                            block["parameters"][param_name] = adapted_value

        return adapted_tone

    def create_guitar_optimization(
        self, base_tone: Dict[str, Any], guitar_type: GuitarType, name: str
    ) -> GuitarOptimization:
        """Create guitar type optimization"""
        guitar_profile = self.guitar_type_profiles.get(guitar_type, {})
        optimized_tone = self._optimize_tone_for_guitar(base_tone, guitar_profile)

        optimization = GuitarOptimization(
            base_tone=base_tone,
            guitar_type=guitar_type,
            optimized_tone=optimized_tone,
            optimization_parameters=guitar_profile,
            pickup_type=guitar_profile.get("pickup_type", "unknown"),
            scale_length=guitar_profile.get("scale_length", 25.5),
        )

        self.guitar_optimizations[name] = optimization
        return optimization

    def _optimize_tone_for_guitar(
        self, base_tone: Dict[str, Any], guitar_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Optimize tone for guitar type"""
        optimized_tone = copy.deepcopy(base_tone)

        # Apply EQ adjustments
        if "eq_adjustments" in guitar_profile and "amp" in optimized_tone:
            amp_block = optimized_tone["amp"]
            if isinstance(amp_block, dict) and "parameters" in amp_block:
                eq_adjustments = guitar_profile["eq_adjustments"]

                for eq_param, adjustment in eq_adjustments.items():
                    if eq_param in amp_block["parameters"]:
                        current_value = amp_block["parameters"][eq_param]
                        amp_block["parameters"][eq_param] = max(
                            0, min(10, current_value + adjustment)
                        )

        # Apply gain adjustment
        if "gain_adjustment" in guitar_profile and "amp" in optimized_tone:
            amp_block = optimized_tone["amp"]
            if isinstance(amp_block, dict) and "parameters" in amp_block:
                if "gain" in amp_block["parameters"]:
                    current_gain = amp_block["parameters"]["gain"]
                    gain_adjustment = guitar_profile["gain_adjustment"]
                    amp_block["parameters"]["gain"] = max(
                        0, min(10, current_gain + gain_adjustment)
                    )

        # Apply presence adjustment
        if "presence_adjustment" in guitar_profile and "amp" in optimized_tone:
            amp_block = optimized_tone["amp"]
            if isinstance(amp_block, dict) and "parameters" in amp_block:
                if "presence" in amp_block["parameters"]:
                    current_presence = amp_block["parameters"]["presence"]
                    presence_adjustment = guitar_profile["presence_adjustment"]
                    amp_block["parameters"]["presence"] = max(
                        0, min(10, current_presence + presence_adjustment)
                    )

        return optimized_tone

    def get_advanced_features_summary(self) -> Dict[str, Any]:
        """Get summary of all advanced features"""
        return {
            "tone_comparisons": len(self.tone_comparisons),
            "parameter_locks": len(self.parameter_locks),
            "tone_variations": len(self.tone_variations),
            "genre_blends": len(self.genre_blends),
            "playing_style_adaptations": len(self.playing_style_adaptations),
            "guitar_optimizations": len(self.guitar_optimizations),
            "available_playing_styles": [style.value for style in PlayingStyle],
            "available_guitar_types": [guitar.value for guitar in GuitarType],
            "available_comparison_modes": [mode.value for mode in ComparisonMode],
        }

    def export_advanced_features(self) -> Dict[str, Any]:
        """Export all advanced features data"""
        return {
            "tone_comparisons": {
                name: asdict(comp) for name, comp in self.tone_comparisons.items()
            },
            "parameter_locks": {
                name: asdict(lock) for name, lock in self.parameter_locks.items()
            },
            "tone_variations": {
                name: asdict(var) for name, var in self.tone_variations.items()
            },
            "genre_blends": {
                name: asdict(blend) for name, blend in self.genre_blends.items()
            },
            "playing_style_adaptations": {
                name: asdict(adapt)
                for name, adapt in self.playing_style_adaptations.items()
            },
            "guitar_optimizations": {
                name: asdict(opt) for name, opt in self.guitar_optimizations.items()
            },
            "playing_style_profiles": {
                style.value: profile
                for style, profile in self.playing_style_profiles.items()
            },
            "guitar_type_profiles": {
                guitar.value: profile
                for guitar, profile in self.guitar_type_profiles.items()
            },
            "genre_blend_profiles": self.genre_blend_profiles,
        }

    def save_advanced_features_to_file(self, filepath: str):
        """Save advanced features data to file"""
        data = self.export_advanced_features()
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def load_advanced_features_from_file(self, filepath: str):
        """Load advanced features data from file"""
        with open(filepath, "r") as f:
            data = json.load(f)

        # Reconstruct objects
        self.tone_comparisons = {
            name: ToneComparison(**comp_data)
            for name, comp_data in data.get("tone_comparisons", {}).items()
        }
        self.parameter_locks = {
            name: ParameterLock(**lock_data)
            for name, lock_data in data.get("parameter_locks", {}).items()
        }
        self.tone_variations = {
            name: ToneVariation(**var_data)
            for name, var_data in data.get("tone_variations", {}).items()
        }
        self.genre_blends = {
            name: GenreBlend(**blend_data)
            for name, blend_data in data.get("genre_blends", {}).items()
        }
        self.playing_style_adaptations = {
            name: PlayingStyleAdaptation(**adapt_data)
            for name, adapt_data in data.get("playing_style_adaptations", {}).items()
        }
        self.guitar_optimizations = {
            name: GuitarOptimization(**opt_data)
            for name, opt_data in data.get("guitar_optimizations", {}).items()
        }

        # Load profiles
        self.genre_blend_profiles = data.get("genre_blend_profiles", {})
