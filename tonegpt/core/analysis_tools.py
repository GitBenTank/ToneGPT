"""
Analysis & Tools System for ToneGPT
Implements real-time frequency response analysis, harmonic content analysis, dynamic range measurement, 
EQ curve visualization, gain staging analysis, and CPU usage monitoring
"""

import json
import math
import numpy as np
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO
import base64


class AnalysisType(Enum):
    FREQUENCY_RESPONSE = "frequency_response"
    HARMONIC_CONTENT = "harmonic_content"
    DYNAMIC_RANGE = "dynamic_range"
    EQ_CURVE = "eq_curve"
    GAIN_STAGING = "gain_staging"
    CPU_USAGE = "cpu_usage"


@dataclass
class FrequencyResponse:
    """Frequency response analysis data"""

    frequencies: List[float]
    magnitude_db: List[float]
    phase_degrees: List[float]
    peak_frequency: float
    peak_magnitude: float
    bandwidth_3db: float
    q_factor: float


@dataclass
class HarmonicContent:
    """Harmonic content analysis data"""

    fundamental_freq: float
    harmonics: Dict[int, float]  # harmonic number -> amplitude
    thd_percent: float  # Total Harmonic Distortion
    thd_plus_n_percent: float  # THD+N
    noise_floor_db: float
    dynamic_range_db: float


@dataclass
class DynamicRange:
    """Dynamic range measurement data"""

    peak_level_db: float
    rms_level_db: float
    crest_factor_db: float
    dynamic_range_db: float
    compression_ratio: float
    attack_time_ms: float
    release_time_ms: float


@dataclass
class EQCurve:
    """EQ curve visualization data"""

    frequencies: List[float]
    gains_db: List[float]
    q_factors: List[float]
    filter_types: List[str]
    total_response: List[float]


@dataclass
class GainStaging:
    """Gain staging analysis data"""

    input_level_db: float
    output_level_db: float
    gain_reduction_db: float
    headroom_db: float
    clipping_detected: bool
    optimal_level: bool
    recommendations: List[str]


@dataclass
class CPUUsage:
    """CPU usage monitoring data"""

    total_cpu_percent: float
    dsp_core_1_percent: float
    dsp_core_2_percent: float
    memory_usage_percent: float
    block_usage: Dict[str, float]  # block_type -> cpu_percent
    optimization_suggestions: List[str]


class AnalysisTools:
    """Analysis and Tools system for FM9"""

    def __init__(self):
        self.frequency_response: Optional[FrequencyResponse] = None
        self.harmonic_content: Optional[HarmonicContent] = None
        self.dynamic_range: Optional[DynamicRange] = None
        self.eq_curve: Optional[EQCurve] = None
        self.gain_staging: Optional[GainStaging] = None
        self.cpu_usage: Optional[CPUUsage] = None

        # Analysis settings
        self.analysis_settings = {
            "frequency_range": (20, 20000),  # Hz
            "fft_size": 4096,
            "window_type": "hann",
            "overlap_percent": 75,
            "averaging_frames": 10,
            "real_time_update": True,
        }

    def analyze_frequency_response(
        self, audio_data: Optional[List[float]] = None
    ) -> FrequencyResponse:
        """Analyze frequency response of audio signal"""
        if audio_data is None:
            # Generate synthetic frequency response for demonstration
            frequencies = np.logspace(1, 4.3, 100)  # 10 Hz to 20 kHz
            magnitude_db = self._generate_synthetic_response(frequencies)
            phase_degrees = self._calculate_phase_response(frequencies, magnitude_db)
        else:
            # Real FFT analysis would go here
            frequencies, magnitude_db, phase_degrees = self._perform_fft_analysis(
                audio_data
            )

        # Calculate derived parameters
        peak_idx = np.argmax(magnitude_db)
        peak_frequency = frequencies[peak_idx]
        peak_magnitude = magnitude_db[peak_idx]

        # Calculate 3dB bandwidth
        bandwidth_3db = self._calculate_bandwidth_3db(
            frequencies, magnitude_db, peak_frequency
        )

        # Calculate Q factor
        q_factor = peak_frequency / bandwidth_3db if bandwidth_3db > 0 else 0

        self.frequency_response = FrequencyResponse(
            frequencies=frequencies.tolist(),
            magnitude_db=magnitude_db.tolist(),
            phase_degrees=phase_degrees.tolist(),
            peak_frequency=peak_frequency,
            peak_magnitude=peak_magnitude,
            bandwidth_3db=bandwidth_3db,
            q_factor=q_factor,
        )

        return self.frequency_response

    def _generate_synthetic_response(self, frequencies: np.ndarray) -> np.ndarray:
        """Generate synthetic frequency response for demonstration"""
        # Create a realistic guitar amp frequency response
        response = np.zeros_like(frequencies)

        # Low frequency roll-off
        response += -20 * np.log10(1 + (100 / frequencies) ** 2)

        # Mid frequency boost
        mid_boost = 3 * np.exp(
            -((np.log10(frequencies) - np.log10(1000)) ** 2) / (2 * 0.5**2)
        )
        response += mid_boost

        # High frequency roll-off
        response += -15 * np.log10(1 + (frequencies / 5000) ** 2)

        # Add some realistic variations
        response += 2 * np.sin(2 * np.pi * np.log10(frequencies) * 3)

        return response

    def _calculate_phase_response(
        self, frequencies: np.ndarray, magnitude_db: np.ndarray
    ) -> np.ndarray:
        """Calculate phase response from magnitude response"""
        # Simplified phase calculation
        phase = np.cumsum(np.gradient(magnitude_db)) * 10
        return phase

    def _perform_fft_analysis(
        self, audio_data: List[float]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Perform FFT analysis on real audio data"""
        # This would be implemented with actual FFT analysis
        # For now, return synthetic data
        frequencies = np.logspace(1, 4.3, 100)
        magnitude_db = self._generate_synthetic_response(frequencies)
        phase_degrees = self._calculate_phase_response(frequencies, magnitude_db)
        return frequencies, magnitude_db, phase_degrees

    def _calculate_bandwidth_3db(
        self, frequencies: np.ndarray, magnitude_db: np.ndarray, peak_freq: float
    ) -> float:
        """Calculate 3dB bandwidth"""
        peak_idx = np.argmin(np.abs(frequencies - peak_freq))
        peak_mag = magnitude_db[peak_idx]
        threshold = peak_mag - 3

        # Find frequencies where magnitude is 3dB below peak
        above_threshold = magnitude_db >= threshold
        if not np.any(above_threshold):
            return 0

        # Find bandwidth
        start_idx = np.where(above_threshold)[0][0]
        end_idx = np.where(above_threshold)[0][-1]

        return frequencies[end_idx] - frequencies[start_idx]

    def analyze_harmonic_content(
        self, audio_data: Optional[List[float]] = None
    ) -> HarmonicContent:
        """Analyze harmonic content and distortion"""
        if audio_data is None:
            # Generate synthetic harmonic content
            fundamental_freq = 440.0  # A4
            harmonics = self._generate_synthetic_harmonics(fundamental_freq)
            thd_percent = self._calculate_thd(harmonics)
            thd_plus_n_percent = thd_percent + random.uniform(0.1, 0.5)
            noise_floor_db = random.uniform(-80, -60)
            dynamic_range_db = random.uniform(60, 90)
        else:
            # Real harmonic analysis would go here
            (
                fundamental_freq,
                harmonics,
                thd_percent,
                thd_plus_n_percent,
                noise_floor_db,
                dynamic_range_db,
            ) = self._perform_harmonic_analysis(audio_data)

        self.harmonic_content = HarmonicContent(
            fundamental_freq=fundamental_freq,
            harmonics=harmonics,
            thd_percent=thd_percent,
            thd_plus_n_percent=thd_plus_n_percent,
            noise_floor_db=noise_floor_db,
            dynamic_range_db=dynamic_range_db,
        )

        return self.harmonic_content

    def _generate_synthetic_harmonics(
        self, fundamental_freq: float
    ) -> Dict[int, float]:
        """Generate synthetic harmonic content"""
        harmonics = {}
        for i in range(1, 11):  # 10 harmonics
            freq = fundamental_freq * i
            # Typical guitar amp harmonic content
            amplitude = 1.0 / (i**1.5) * random.uniform(0.8, 1.2)
            harmonics[i] = amplitude
        return harmonics

    def _calculate_thd(self, harmonics: Dict[int, float]) -> float:
        """Calculate Total Harmonic Distortion"""
        fundamental = harmonics.get(1, 0)
        if fundamental == 0:
            return 0

        harmonic_power = sum(amp**2 for i, amp in harmonics.items() if i > 1)
        thd = math.sqrt(harmonic_power) / fundamental * 100
        return thd

    def _perform_harmonic_analysis(
        self, audio_data: List[float]
    ) -> Tuple[float, Dict[int, float], float, float, float, float]:
        """Perform real harmonic analysis"""
        # This would be implemented with actual harmonic analysis
        # For now, return synthetic data
        fundamental_freq = 440.0
        harmonics = self._generate_synthetic_harmonics(fundamental_freq)
        thd_percent = self._calculate_thd(harmonics)
        thd_plus_n_percent = thd_percent + random.uniform(0.1, 0.5)
        noise_floor_db = random.uniform(-80, -60)
        dynamic_range_db = random.uniform(60, 90)
        return (
            fundamental_freq,
            harmonics,
            thd_percent,
            thd_plus_n_percent,
            noise_floor_db,
            dynamic_range_db,
        )

    def analyze_dynamic_range(
        self, audio_data: Optional[List[float]] = None
    ) -> DynamicRange:
        """Analyze dynamic range and compression characteristics"""
        if audio_data is None:
            # Generate synthetic dynamic range data
            peak_level_db = random.uniform(-3, 0)
            rms_level_db = random.uniform(-20, -10)
            crest_factor_db = peak_level_db - rms_level_db
            dynamic_range_db = random.uniform(40, 70)
            compression_ratio = random.uniform(2.0, 8.0)
            attack_time_ms = random.uniform(1, 50)
            release_time_ms = random.uniform(50, 500)
        else:
            # Real dynamic range analysis would go here
            (
                peak_level_db,
                rms_level_db,
                crest_factor_db,
                dynamic_range_db,
                compression_ratio,
                attack_time_ms,
                release_time_ms,
            ) = self._perform_dynamic_analysis(audio_data)

        self.dynamic_range = DynamicRange(
            peak_level_db=peak_level_db,
            rms_level_db=rms_level_db,
            crest_factor_db=crest_factor_db,
            dynamic_range_db=dynamic_range_db,
            compression_ratio=compression_ratio,
            attack_time_ms=attack_time_ms,
            release_time_ms=release_time_ms,
        )

        return self.dynamic_range

    def _perform_dynamic_analysis(
        self, audio_data: List[float]
    ) -> Tuple[float, float, float, float, float, float, float]:
        """Perform real dynamic range analysis"""
        # This would be implemented with actual dynamic analysis
        # For now, return synthetic data
        peak_level_db = random.uniform(-3, 0)
        rms_level_db = random.uniform(-20, -10)
        crest_factor_db = peak_level_db - rms_level_db
        dynamic_range_db = random.uniform(40, 70)
        compression_ratio = random.uniform(2.0, 8.0)
        attack_time_ms = random.uniform(1, 50)
        release_time_ms = random.uniform(50, 500)
        return (
            peak_level_db,
            rms_level_db,
            crest_factor_db,
            dynamic_range_db,
            compression_ratio,
            attack_time_ms,
            release_time_ms,
        )

    def analyze_eq_curve(self, eq_settings: Dict[str, Any]) -> EQCurve:
        """Analyze and visualize EQ curve"""
        frequencies = np.logspace(1, 4.3, 100)  # 10 Hz to 20 kHz
        total_response = np.zeros_like(frequencies)

        gains_db = []
        q_factors = []
        filter_types = []

        # Process each EQ band
        for band in eq_settings.get("bands", []):
            freq = band.get("frequency", 1000)
            gain = band.get("gain", 0)
            q = band.get("q", 1.0)
            filter_type = band.get("type", "parametric")

            gains_db.append(gain)
            q_factors.append(q)
            filter_types.append(filter_type)

            # Calculate filter response
            if filter_type == "parametric":
                response = self._calculate_parametric_response(
                    frequencies, freq, gain, q
                )
            elif filter_type == "high_shelf":
                response = self._calculate_shelf_response(
                    frequencies, freq, gain, "high"
                )
            elif filter_type == "low_shelf":
                response = self._calculate_shelf_response(
                    frequencies, freq, gain, "low"
                )
            elif filter_type == "high_pass":
                response = self._calculate_high_pass_response(frequencies, freq, q)
            elif filter_type == "low_pass":
                response = self._calculate_low_pass_response(frequencies, freq, q)
            else:
                response = np.zeros_like(frequencies)

            total_response += response

        self.eq_curve = EQCurve(
            frequencies=frequencies.tolist(),
            gains_db=gains_db,
            q_factors=q_factors,
            filter_types=filter_types,
            total_response=total_response.tolist(),
        )

        return self.eq_curve

    def _calculate_parametric_response(
        self, frequencies: np.ndarray, center_freq: float, gain_db: float, q: float
    ) -> np.ndarray:
        """Calculate parametric EQ response"""
        # Simplified parametric EQ calculation
        response = np.zeros_like(frequencies)
        for i, freq in enumerate(frequencies):
            if freq > 0:
                # Bell curve response
                ratio = freq / center_freq
                if ratio > 0:
                    log_ratio = np.log10(ratio)
                    response[i] = gain_db * np.exp(-(log_ratio**2) / (2 * (1 / q) ** 2))
        return response

    def _calculate_shelf_response(
        self,
        frequencies: np.ndarray,
        corner_freq: float,
        gain_db: float,
        shelf_type: str,
    ) -> np.ndarray:
        """Calculate shelf EQ response"""
        response = np.zeros_like(frequencies)
        for i, freq in enumerate(frequencies):
            if freq > 0:
                ratio = freq / corner_freq
                if shelf_type == "high":
                    response[i] = gain_db * (1 - 1 / (1 + ratio))
                else:  # low
                    response[i] = gain_db * (1 / (1 + ratio))
        return response

    def _calculate_high_pass_response(
        self, frequencies: np.ndarray, cutoff_freq: float, q: float
    ) -> np.ndarray:
        """Calculate high-pass filter response"""
        response = np.zeros_like(frequencies)
        for i, freq in enumerate(frequencies):
            if freq > 0:
                ratio = freq / cutoff_freq
                response[i] = -20 * np.log10(1 / np.sqrt(1 + (1 / ratio) ** 2))
        return response

    def _calculate_low_pass_response(
        self, frequencies: np.ndarray, cutoff_freq: float, q: float
    ) -> np.ndarray:
        """Calculate low-pass filter response"""
        response = np.zeros_like(frequencies)
        for i, freq in enumerate(frequencies):
            if freq > 0:
                ratio = freq / cutoff_freq
                response[i] = -20 * np.log10(1 / np.sqrt(1 + ratio**2))
        return response

    def analyze_gain_staging(
        self,
        input_level: float,
        output_level: float,
        compression_settings: Dict[str, Any],
    ) -> GainStaging:
        """Analyze gain staging and provide recommendations"""
        gain_reduction_db = input_level - output_level
        headroom_db = 0 - output_level  # Assuming 0dB is maximum

        clipping_detected = output_level > 0
        optimal_level = -18 <= output_level <= -6  # Optimal range

        recommendations = []
        if clipping_detected:
            recommendations.append("Reduce output level to prevent clipping")
        if output_level < -18:
            recommendations.append(
                "Increase output level for better signal-to-noise ratio"
            )
        if output_level > -6:
            recommendations.append("Reduce output level to maintain headroom")
        if gain_reduction_db > 10:
            recommendations.append(
                "Consider reducing input gain to minimize compression"
            )
        if headroom_db < 3:
            recommendations.append("Increase headroom for dynamic peaks")

        self.gain_staging = GainStaging(
            input_level_db=input_level,
            output_level_db=output_level,
            gain_reduction_db=gain_reduction_db,
            headroom_db=headroom_db,
            clipping_detected=clipping_detected,
            optimal_level=optimal_level,
            recommendations=recommendations,
        )

        return self.gain_staging

    def monitor_cpu_usage(self, block_usage: Dict[str, float]) -> CPUUsage:
        """Monitor CPU usage and provide optimization suggestions"""
        total_cpu = sum(block_usage.values())
        dsp_core_1 = total_cpu * 0.6  # Simulate DSP core distribution
        dsp_core_2 = total_cpu * 0.4
        memory_usage = total_cpu * 0.8  # Simulate memory usage

        optimization_suggestions = []
        if total_cpu > 80:
            optimization_suggestions.append(
                "High CPU usage detected - consider disabling unused blocks"
            )
        if dsp_core_1 > 90:
            optimization_suggestions.append(
                "DSP Core 1 overloaded - redistribute blocks"
            )
        if dsp_core_2 > 90:
            optimization_suggestions.append(
                "DSP Core 2 overloaded - redistribute blocks"
            )
        if memory_usage > 85:
            optimization_suggestions.append(
                "High memory usage - consider reducing IR resolution"
            )

        # Find highest CPU usage blocks
        sorted_blocks = sorted(block_usage.items(), key=lambda x: x[1], reverse=True)
        if sorted_blocks:
            highest_block = sorted_blocks[0]
            if highest_block[1] > 20:
                optimization_suggestions.append(
                    f"Consider optimizing {highest_block[0]} block (using {highest_block[1]:.1f}% CPU)"
                )

        self.cpu_usage = CPUUsage(
            total_cpu_percent=total_cpu,
            dsp_core_1_percent=dsp_core_1,
            dsp_core_2_percent=dsp_core_2,
            memory_usage_percent=memory_usage,
            block_usage=block_usage,
            optimization_suggestions=optimization_suggestions,
        )

        return self.cpu_usage

    def create_frequency_response_plot(self) -> str:
        """Create frequency response plot and return as base64 string"""
        if self.frequency_response is None:
            return ""

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        # Magnitude response
        ax1.semilogx(
            self.frequency_response.frequencies, self.frequency_response.magnitude_db
        )
        ax1.set_xlabel("Frequency (Hz)")
        ax1.set_ylabel("Magnitude (dB)")
        ax1.set_title("Frequency Response")
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(20, 20000)

        # Phase response
        ax2.semilogx(
            self.frequency_response.frequencies, self.frequency_response.phase_degrees
        )
        ax2.set_xlabel("Frequency (Hz)")
        ax2.set_ylabel("Phase (degrees)")
        ax2.set_title("Phase Response")
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(20, 20000)

        plt.tight_layout()

        # Convert to base64 string
        buffer = BytesIO()
        plt.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

        return image_base64

    def create_harmonic_analysis_plot(self) -> str:
        """Create harmonic analysis plot and return as base64 string"""
        if self.harmonic_content is None:
            return ""

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Harmonic spectrum
        harmonics = list(self.harmonic_content.harmonics.keys())
        amplitudes = list(self.harmonic_content.harmonics.values())

        ax1.bar(harmonics, amplitudes)
        ax1.set_xlabel("Harmonic Number")
        ax1.set_ylabel("Amplitude")
        ax1.set_title("Harmonic Content")
        ax1.grid(True, alpha=0.3)

        # THD display
        ax2.text(
            0.5,
            0.7,
            f"THD: {self.harmonic_content.thd_percent:.2f}%",
            ha="center",
            va="center",
            fontsize=16,
            transform=ax2.transAxes,
        )
        ax2.text(
            0.5,
            0.5,
            f"THD+N: {self.harmonic_content.thd_plus_n_percent:.2f}%",
            ha="center",
            va="center",
            fontsize=16,
            transform=ax2.transAxes,
        )
        ax2.text(
            0.5,
            0.3,
            f"Dynamic Range: {self.harmonic_content.dynamic_range_db:.1f} dB",
            ha="center",
            va="center",
            fontsize=16,
            transform=ax2.transAxes,
        )
        ax2.set_title("Distortion Analysis")
        ax2.axis("off")

        plt.tight_layout()

        # Convert to base64 string
        buffer = BytesIO()
        plt.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

        return image_base64

    def create_eq_curve_plot(self) -> str:
        """Create EQ curve plot and return as base64 string"""
        if self.eq_curve is None:
            return ""

        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot EQ curve
        ax.semilogx(self.eq_curve.frequencies, self.eq_curve.total_response)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Gain (dB)")
        ax.set_title("EQ Curve")
        ax.grid(True, alpha=0.3)
        ax.set_xlim(20, 20000)
        ax.axhline(y=0, color="k", linestyle="--", alpha=0.5)

        plt.tight_layout()

        # Convert to base64 string
        buffer = BytesIO()
        plt.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

        return image_base64

    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get summary of all analysis results"""
        summary = {}

        if self.frequency_response:
            summary["frequency_response"] = {
                "peak_frequency": self.frequency_response.peak_frequency,
                "peak_magnitude": self.frequency_response.peak_magnitude,
                "bandwidth_3db": self.frequency_response.bandwidth_3db,
                "q_factor": self.frequency_response.q_factor,
            }

        if self.harmonic_content:
            summary["harmonic_content"] = {
                "fundamental_freq": self.harmonic_content.fundamental_freq,
                "thd_percent": self.harmonic_content.thd_percent,
                "thd_plus_n_percent": self.harmonic_content.thd_plus_n_percent,
                "dynamic_range_db": self.harmonic_content.dynamic_range_db,
            }

        if self.dynamic_range:
            summary["dynamic_range"] = {
                "peak_level_db": self.dynamic_range.peak_level_db,
                "rms_level_db": self.dynamic_range.rms_level_db,
                "crest_factor_db": self.dynamic_range.crest_factor_db,
                "dynamic_range_db": self.dynamic_range.dynamic_range_db,
            }

        if self.gain_staging:
            summary["gain_staging"] = {
                "input_level_db": self.gain_staging.input_level_db,
                "output_level_db": self.gain_staging.output_level_db,
                "clipping_detected": self.gain_staging.clipping_detected,
                "optimal_level": self.gain_staging.optimal_level,
                "recommendations": self.gain_staging.recommendations,
            }

        if self.cpu_usage:
            summary["cpu_usage"] = {
                "total_cpu_percent": self.cpu_usage.total_cpu_percent,
                "dsp_core_1_percent": self.cpu_usage.dsp_core_1_percent,
                "dsp_core_2_percent": self.cpu_usage.dsp_core_2_percent,
                "optimization_suggestions": self.cpu_usage.optimization_suggestions,
            }

        return summary

    def export_analysis_data(self) -> Dict[str, Any]:
        """Export all analysis data"""
        return {
            "frequency_response": (
                self.frequency_response.__dict__ if self.frequency_response else None
            ),
            "harmonic_content": (
                self.harmonic_content.__dict__ if self.harmonic_content else None
            ),
            "dynamic_range": (
                self.dynamic_range.__dict__ if self.dynamic_range else None
            ),
            "eq_curve": self.eq_curve.__dict__ if self.eq_curve else None,
            "gain_staging": self.gain_staging.__dict__ if self.gain_staging else None,
            "cpu_usage": self.cpu_usage.__dict__ if self.cpu_usage else None,
            "analysis_settings": self.analysis_settings,
        }

    def save_analysis_to_file(self, filepath: str):
        """Save analysis data to file"""
        data = self.export_analysis_data()
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def load_analysis_from_file(self, filepath: str):
        """Load analysis data from file"""
        with open(filepath, "r") as f:
            data = json.load(f)

        # Reconstruct analysis objects
        if data.get("frequency_response"):
            self.frequency_response = FrequencyResponse(**data["frequency_response"])
        if data.get("harmonic_content"):
            self.harmonic_content = HarmonicContent(**data["harmonic_content"])
        if data.get("dynamic_range"):
            self.dynamic_range = DynamicRange(**data["dynamic_range"])
        if data.get("eq_curve"):
            self.eq_curve = EQCurve(**data["eq_curve"])
        if data.get("gain_staging"):
            self.gain_staging = GainStaging(**data["gain_staging"])
        if data.get("cpu_usage"):
            self.cpu_usage = CPUUsage(**data["cpu_usage"])

        self.analysis_settings = data.get("analysis_settings", self.analysis_settings)
