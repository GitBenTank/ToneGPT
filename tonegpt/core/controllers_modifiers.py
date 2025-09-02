"""
Controllers & Modifiers System for ToneGPT
Implements LFO modulation, ADSR envelopes, Envelope follower, Sequencer, Pitch detector, and External controller mapping
"""

import json
import math
import random
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class Waveform(Enum):
    SINE = "sine"
    TRIANGLE = "triangle"
    SAWTOOTH = "sawtooth"
    SQUARE = "square"
    RANDOM = "random"


class ControllerType(Enum):
    LFO = "lfo"
    ADSR = "adsr"
    ENVELOPE_FOLLOWER = "envelope_follower"
    SEQUENCER = "sequencer"
    PITCH_DETECTOR = "pitch_detector"
    EXTERNAL = "external"


@dataclass
class LFO:
    """Low Frequency Oscillator"""

    lfo_id: int
    name: str
    rate: float  # Hz
    depth: float  # 0-100%
    waveform: Waveform
    phase: float  # 0-360 degrees
    sync: bool
    tempo_sync: bool
    tempo_division: str  # quarter, eighth, sixteenth, etc.
    enabled: bool = True


@dataclass
class ADSR:
    """Attack, Decay, Sustain, Release envelope"""

    adsr_id: int
    name: str
    attack: float  # ms
    decay: float  # ms
    sustain: float  # 0-100%
    release: float  # ms
    curve: str  # linear, exponential, logarithmic
    enabled: bool = True


@dataclass
class EnvelopeFollower:
    """Envelope follower for dynamic control"""

    name: str
    attack: float  # ms
    release: float  # ms
    sensitivity: float  # 0-100%
    scale: float  # 0-100%
    invert: bool
    enabled: bool = True


@dataclass
class Sequencer:
    """Step sequencer for modulation"""

    name: str
    steps: int  # up to 64
    rate: float  # Hz
    values: List[float]  # step values
    sync: bool
    tempo_sync: bool
    tempo_division: str
    loop: bool
    enabled: bool = True


@dataclass
class PitchDetector:
    """Pitch detection for modulation"""

    name: str
    tracking_mode: str  # poly, mono
    key: str  # musical key
    scale: str  # musical scale
    formant_preservation: bool
    enabled: bool = True


@dataclass
class ExternalController:
    """External controller mapping"""

    controller_id: str
    name: str
    controller_type: str  # pedal, midi_cc, control_switch
    source: str  # external input source
    min_value: float
    max_value: float
    curve: str  # linear, log, exp, s_curve
    invert: bool
    enabled: bool = True


@dataclass
class Modifier:
    """Modifier that can be applied to parameters"""

    modifier_id: str
    name: str
    controller_type: ControllerType
    controller_id: str
    target_parameter: str
    target_block: str
    min_range: float
    max_range: float
    enabled: bool = True


class ControllersModifiers:
    """Controllers and Modifiers system for FM9"""

    def __init__(self):
        self.lfos: Dict[int, LFO] = {}
        self.adsrs: Dict[int, ADSR] = {}
        self.envelope_followers: Dict[str, EnvelopeFollower] = {}
        self.sequencers: Dict[str, Sequencer] = {}
        self.pitch_detectors: Dict[str, PitchDetector] = {}
        self.external_controllers: Dict[str, ExternalController] = {}
        self.modifiers: Dict[str, Modifier] = {}

        # Initialize default controllers
        self._initialize_default_lfos()
        self._initialize_default_adsrs()
        self._initialize_default_envelope_followers()
        self._initialize_default_sequencers()
        self._initialize_default_pitch_detectors()
        self._initialize_default_external_controllers()
        self._initialize_default_modifiers()

    def _initialize_default_lfos(self):
        """Initialize 2 default LFOs"""
        lfo1 = LFO(
            lfo_id=1,
            name="LFO 1 - Chorus",
            rate=2.5,
            depth=75.0,
            waveform=Waveform.SINE,
            phase=0.0,
            sync=False,
            tempo_sync=True,
            tempo_division="eighth",
        )

        lfo2 = LFO(
            lfo_id=2,
            name="LFO 2 - Tremolo",
            rate=6.0,
            depth=60.0,
            waveform=Waveform.TRIANGLE,
            phase=90.0,
            sync=False,
            tempo_sync=True,
            tempo_division="quarter",
        )

        self.lfos[1] = lfo1
        self.lfos[2] = lfo2

    def _initialize_default_adsrs(self):
        """Initialize 2 default ADSRs"""
        adsr1 = ADSR(
            adsr_id=1,
            name="ADSR 1 - Filter",
            attack=50.0,
            decay=200.0,
            sustain=60.0,
            release=800.0,
            curve="exponential",
        )

        adsr2 = ADSR(
            adsr_id=2,
            name="ADSR 2 - Volume",
            attack=10.0,
            decay=100.0,
            sustain=80.0,
            release=500.0,
            curve="linear",
        )

        self.adsrs[1] = adsr1
        self.adsrs[2] = adsr2

    def _initialize_default_envelope_followers(self):
        """Initialize default envelope follower"""
        env_follower = EnvelopeFollower(
            name="Envelope Follower - Auto Wah",
            attack=5.0,
            release=50.0,
            sensitivity=75.0,
            scale=80.0,
            invert=False,
        )

        self.envelope_followers["env_follower_1"] = env_follower

    def _initialize_default_sequencers(self):
        """Initialize default sequencer"""
        # Create a 16-step sequencer with random values
        sequencer_values = [random.uniform(0, 100) for _ in range(16)]

        sequencer = Sequencer(
            name="Sequencer - Filter Sweep",
            steps=16,
            rate=1.0,
            values=sequencer_values,
            sync=True,
            tempo_sync=True,
            tempo_division="sixteenth",
            loop=True,
        )

        self.sequencers["seq_1"] = sequencer

    def _initialize_default_pitch_detectors(self):
        """Initialize default pitch detector"""
        pitch_detector = PitchDetector(
            name="Pitch Detector - Harmonizer",
            tracking_mode="mono",
            key="C",
            scale="major",
            formant_preservation=True,
        )

        self.pitch_detectors["pitch_1"] = pitch_detector

    def _initialize_default_external_controllers(self):
        """Initialize default external controllers"""
        controllers = [
            ExternalController(
                controller_id="pedal_1",
                name="Expression Pedal 1",
                controller_type="pedal",
                source="pedal_1",
                min_value=0.0,
                max_value=100.0,
                curve="linear",
                invert=False,
            ),
            ExternalController(
                controller_id="pedal_2",
                name="Expression Pedal 2",
                controller_type="pedal",
                source="pedal_2",
                min_value=0.0,
                max_value=100.0,
                curve="log",
                invert=False,
            ),
            ExternalController(
                controller_id="midi_cc_1",
                name="MIDI CC 1",
                controller_type="midi_cc",
                source="midi_cc_1",
                min_value=0.0,
                max_value=127.0,
                curve="linear",
                invert=False,
            ),
        ]

        for controller in controllers:
            self.external_controllers[controller.controller_id] = controller

    def _initialize_default_modifiers(self):
        """Initialize default modifiers"""
        modifiers = [
            Modifier(
                modifier_id="mod_1",
                name="Chorus Rate",
                controller_type=ControllerType.LFO,
                controller_id="1",
                target_parameter="rate",
                target_block="modulation",
                min_range=0.1,
                max_range=10.0,
            ),
            Modifier(
                modifier_id="mod_2",
                name="Filter Cutoff",
                controller_type=ControllerType.ADSR,
                controller_id="1",
                target_parameter="cutoff",
                target_block="filter",
                min_range=200.0,
                max_range=8000.0,
            ),
            Modifier(
                modifier_id="mod_3",
                name="Wah Frequency",
                controller_type=ControllerType.ENVELOPE_FOLLOWER,
                controller_id="env_follower_1",
                target_parameter="frequency",
                target_block="filter",
                min_range=200.0,
                max_range=2000.0,
            ),
            Modifier(
                modifier_id="mod_4",
                name="Delay Time",
                controller_type=ControllerType.EXTERNAL,
                controller_id="pedal_1",
                target_parameter="time",
                target_block="delay",
                min_range=100.0,
                max_range=1000.0,
            ),
        ]

        for modifier in modifiers:
            self.modifiers[modifier.modifier_id] = modifier

    def create_lfo(
        self,
        lfo_id: int,
        name: str,
        rate: float,
        depth: float,
        waveform: Waveform,
        **kwargs
    ) -> bool:
        """Create a new LFO"""
        if lfo_id not in self.lfos:
            lfo = LFO(
                lfo_id=lfo_id,
                name=name,
                rate=rate,
                depth=depth,
                waveform=waveform,
                phase=kwargs.get("phase", 0.0),
                sync=kwargs.get("sync", False),
                tempo_sync=kwargs.get("tempo_sync", True),
                tempo_division=kwargs.get("tempo_division", "quarter"),
            )
            self.lfos[lfo_id] = lfo
            return True
        return False

    def create_adsr(
        self,
        adsr_id: int,
        name: str,
        attack: float,
        decay: float,
        sustain: float,
        release: float,
        **kwargs
    ) -> bool:
        """Create a new ADSR"""
        if adsr_id not in self.adsrs:
            adsr = ADSR(
                adsr_id=adsr_id,
                name=name,
                attack=attack,
                decay=decay,
                sustain=sustain,
                release=release,
                curve=kwargs.get("curve", "linear"),
            )
            self.adsrs[adsr_id] = adsr
            return True
        return False

    def create_sequencer(self, name: str, steps: int, rate: float, **kwargs) -> bool:
        """Create a new sequencer"""
        if name not in self.sequencers:
            values = kwargs.get(
                "values", [random.uniform(0, 100) for _ in range(steps)]
            )
            sequencer = Sequencer(
                name=name,
                steps=steps,
                rate=rate,
                values=values,
                sync=kwargs.get("sync", True),
                tempo_sync=kwargs.get("tempo_sync", True),
                tempo_division=kwargs.get("tempo_division", "quarter"),
                loop=kwargs.get("loop", True),
            )
            self.sequencers[name] = sequencer
            return True
        return False

    def create_modifier(
        self,
        modifier_id: str,
        name: str,
        controller_type: ControllerType,
        controller_id: str,
        target_parameter: str,
        target_block: str,
        min_range: float,
        max_range: float,
    ) -> bool:
        """Create a new modifier"""
        if modifier_id not in self.modifiers:
            modifier = Modifier(
                modifier_id=modifier_id,
                name=name,
                controller_type=controller_type,
                controller_id=controller_id,
                target_parameter=target_parameter,
                target_block=target_block,
                min_range=min_range,
                max_range=max_range,
            )
            self.modifiers[modifier_id] = modifier
            return True
        return False

    def get_lfo_value(self, lfo_id: int, time: float) -> float:
        """Get current LFO value at given time"""
        if lfo_id not in self.lfos:
            return 0.0

        lfo = self.lfos[lfo_id]
        if not lfo.enabled:
            return 0.0

        # Calculate phase
        phase = (lfo.phase + (time * lfo.rate * 360)) % 360

        # Generate waveform
        if lfo.waveform == Waveform.SINE:
            value = math.sin(math.radians(phase))
        elif lfo.waveform == Waveform.TRIANGLE:
            value = 2 * abs(phase / 180 - 1) - 1
        elif lfo.waveform == Waveform.SAWTOOTH:
            value = (phase / 180) - 1
        elif lfo.waveform == Waveform.SQUARE:
            value = 1 if phase < 180 else -1
        else:  # RANDOM
            value = random.uniform(-1, 1)

        # Apply depth
        return value * (lfo.depth / 100.0)

    def get_adsr_value(self, adsr_id: int, time: float, gate: bool) -> float:
        """Get current ADSR value at given time"""
        if adsr_id not in self.adsrs:
            return 0.0

        adsr = self.adsrs[adsr_id]
        if not adsr.enabled:
            return 0.0

        # Simplified ADSR calculation
        if gate:
            if time < adsr.attack:
                # Attack phase
                return (time / adsr.attack) * 100
            elif time < adsr.attack + adsr.decay:
                # Decay phase
                decay_time = time - adsr.attack
                decay_progress = decay_time / adsr.decay
                return 100 - (decay_progress * (100 - adsr.sustain))
            else:
                # Sustain phase
                return adsr.sustain
        else:
            # Release phase
            release_time = time
            if release_time < adsr.release:
                release_progress = release_time / adsr.release
                return adsr.sustain * (1 - release_progress)
            else:
                return 0.0

    def get_sequencer_value(self, sequencer_name: str, time: float) -> float:
        """Get current sequencer value at given time"""
        if sequencer_name not in self.sequencers:
            return 0.0

        sequencer = self.sequencers[sequencer_name]
        if not sequencer.enabled:
            return 0.0

        # Calculate current step
        step_time = 1.0 / sequencer.rate
        current_step = int((time / step_time) % sequencer.steps)

        return sequencer.values[current_step]

    def apply_modifier(
        self, modifier_id: str, base_value: float, time: float, gate: bool = True
    ) -> float:
        """Apply a modifier to a base value"""
        if modifier_id not in self.modifiers:
            return base_value

        modifier = self.modifiers[modifier_id]
        if not modifier.enabled:
            return base_value

        # Get controller value
        if modifier.controller_type == ControllerType.LFO:
            controller_value = self.get_lfo_value(int(modifier.controller_id), time)
        elif modifier.controller_type == ControllerType.ADSR:
            controller_value = self.get_adsr_value(
                int(modifier.controller_id), time, gate
            )
        elif modifier.controller_type == ControllerType.ENVELOPE_FOLLOWER:
            # Simplified envelope follower
            controller_value = random.uniform(0, 1)  # Placeholder
        elif modifier.controller_type == ControllerType.SEQUENCER:
            controller_value = self.get_sequencer_value(modifier.controller_id, time)
        else:
            controller_value = 0.0

        # Map controller value to parameter range
        mapped_value = modifier.min_range + (
            controller_value * (modifier.max_range - modifier.min_range)
        )

        # Apply to base value (simplified)
        return base_value + (mapped_value * 0.1)  # 10% modulation depth

    def get_controller_summary(self) -> Dict[str, Any]:
        """Get summary of all controllers"""
        return {
            "lfos": {
                lfo_id: {
                    "name": lfo.name,
                    "rate": lfo.rate,
                    "depth": lfo.depth,
                    "waveform": lfo.waveform.value,
                    "enabled": lfo.enabled,
                }
                for lfo_id, lfo in self.lfos.items()
            },
            "adsrs": {
                adsr_id: {
                    "name": adsr.name,
                    "attack": adsr.attack,
                    "decay": adsr.decay,
                    "sustain": adsr.sustain,
                    "release": adsr.release,
                    "enabled": adsr.enabled,
                }
                for adsr_id, adsr in self.adsrs.items()
            },
            "sequencers": {
                name: {"steps": seq.steps, "rate": seq.rate, "enabled": seq.enabled}
                for name, seq in self.sequencers.items()
            },
            "modifiers": {
                mod_id: {
                    "name": mod.name,
                    "controller_type": mod.controller_type.value,
                    "target_parameter": mod.target_parameter,
                    "target_block": mod.target_block,
                    "enabled": mod.enabled,
                }
                for mod_id, mod in self.modifiers.items()
            },
        }

    def export_controllers(self) -> Dict[str, Any]:
        """Export all controller settings"""
        return {
            "lfos": {lfo_id: lfo.__dict__ for lfo_id, lfo in self.lfos.items()},
            "adsrs": {adsr_id: adsr.__dict__ for adsr_id, adsr in self.adsrs.items()},
            "envelope_followers": {
                name: env.__dict__ for name, env in self.envelope_followers.items()
            },
            "sequencers": {name: seq.__dict__ for name, seq in self.sequencers.items()},
            "pitch_detectors": {
                name: pitch.__dict__ for name, pitch in self.pitch_detectors.items()
            },
            "external_controllers": {
                ctrl_id: ctrl.__dict__
                for ctrl_id, ctrl in self.external_controllers.items()
            },
            "modifiers": {
                mod_id: mod.__dict__ for mod_id, mod in self.modifiers.items()
            },
        }

    def save_to_file(self, filepath: str):
        """Save controller settings to file"""
        data = self.export_controllers()
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filepath: str):
        """Load controller settings from file"""
        with open(filepath, "r") as f:
            data = json.load(f)

        # Reconstruct controllers
        self.lfos = {
            int(lfo_id): LFO(**lfo_data)
            for lfo_id, lfo_data in data.get("lfos", {}).items()
        }
        self.adsrs = {
            int(adsr_id): ADSR(**adsr_data)
            for adsr_id, adsr_data in data.get("adsrs", {}).items()
        }
        self.envelope_followers = {
            name: EnvelopeFollower(**env_data)
            for name, env_data in data.get("envelope_followers", {}).items()
        }
        self.sequencers = {
            name: Sequencer(**seq_data)
            for name, seq_data in data.get("sequencers", {}).items()
        }
        self.pitch_detectors = {
            name: PitchDetector(**pitch_data)
            for name, pitch_data in data.get("pitch_detectors", {}).items()
        }
        self.external_controllers = {
            ctrl_id: ExternalController(**ctrl_data)
            for ctrl_id, ctrl_data in data.get("external_controllers", {}).items()
        }
        self.modifiers = {
            mod_id: Modifier(**mod_data)
            for mod_id, mod_data in data.get("modifiers", {}).items()
        }
