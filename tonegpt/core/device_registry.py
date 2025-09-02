"""
Device Registry for ToneGPT System

TL;DR: Device registry stub for future multi-device support (currently FM9-only).
- Provides device abstraction layer for future expansion
- Currently contains only FM9 device configuration
- Designed for drop-in expansion when FEATURE_MULTI_DEVICE is enabled
- All device-specific logic isolated in adapters

Constraints:
- FM9 single-mode only (docs/ground-truth.md#Invariants)
- No network calls (pure function)
- Device registry in adapters only (docs/ground-truth.md#Future-proofing)
- Raises ValueError if device not supported (cite file+key)
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json

from .flags import FEATURE_MULTI_DEVICE


class DeviceRegistry:
    """
    Registry for supported Fractal Audio devices.

    Currently FM9-only, but designed for future expansion to other Fractal devices
    when FEATURE_MULTI_DEVICE is enabled.
    """

    def __init__(self):
        """Initialize device registry with FM9-only configuration."""
        self._devices: Dict[str, Dict[str, Any]] = {}
        self._load_fm9_device()

    def _load_fm9_device(self) -> None:
        """Load FM9 device configuration."""
        self._devices["fm9"] = {
            "name": "Fractal Audio FM9",
            "model": "FM9",
            "version": "1.0",
            "supported_blocks": [
                "amp",
                "cab",
                "drive",
                "mod",
                "delay",
                "reverb",
                "pitch",
                "dynamics",
                "eq",
                "utility",
            ],
            "parameter_source": "data/fm9_comprehensive_reference.json",
            "config_source": "data/fm9_config.json",
            "blocks_source": "tonegpt/core/blocks_with_footswitch.json",
            "max_blocks": 512,
            "description": "Fractal Audio FM9 - Flagship floor modeler",
        }

    def get_device(self, device_id: str) -> Dict[str, Any]:
        """
        Get device configuration by ID.

        Args:
            device_id: Device identifier (e.g., 'fm9')

        Returns:
            Device configuration dictionary

        Raises:
            ValueError: If device not supported
        """
        if device_id not in self._devices:
            raise ValueError(
                f"Device '{device_id}' not supported. "
                f"Available devices: {list(self._devices.keys())}. "
                f"See docs/ground-truth.md#Future-proofing for expansion info."
            )
        return self._devices[device_id]

    def list_devices(self) -> List[str]:
        """
        List all supported device IDs.

        Returns:
            List of device identifiers
        """
        return list(self._devices.keys())

    def get_default_device(self) -> str:
        """
        Get the default device ID.

        Returns:
            Default device identifier (currently 'fm9')
        """
        return "fm9"

    def is_device_supported(self, device_id: str) -> bool:
        """
        Check if device is supported.

        Args:
            device_id: Device identifier

        Returns:
            True if device is supported
        """
        return device_id in self._devices

    def get_device_parameter_source(self, device_id: str) -> str:
        """
        Get the parameter source file for a device.

        Args:
            device_id: Device identifier

        Returns:
            Path to parameter source file

        Raises:
            ValueError: If device not supported
        """
        device = self.get_device(device_id)
        return device["parameter_source"]

    def get_device_config_source(self, device_id: str) -> str:
        """
        Get the config source file for a device.

        Args:
            device_id: Device identifier

        Returns:
            Path to config source file

        Raises:
            ValueError: If device not supported
        """
        device = self.get_device(device_id)
        return device["config_source"]

    def get_device_blocks_source(self, device_id: str) -> str:
        """
        Get the blocks source file for a device.

        Args:
            device_id: Device identifier

        Returns:
            Path to blocks source file

        Raises:
            ValueError: If device not supported
        """
        device = self.get_device(device_id)
        return device["blocks_source"]

    def get_supported_blocks(self, device_id: str) -> List[str]:
        """
        Get list of supported block types for a device.

        Args:
            device_id: Device identifier

        Returns:
            List of supported block types

        Raises:
            ValueError: If device not supported
        """
        device = self.get_device(device_id)
        return device["supported_blocks"]

    def get_max_blocks(self, device_id: str) -> int:
        """
        Get maximum number of blocks for a device.

        Args:
            device_id: Device identifier

        Returns:
            Maximum number of blocks

        Raises:
            ValueError: If device not supported
        """
        device = self.get_device(device_id)
        return device["max_blocks"]


# Global device registry instance
_device_registry: Optional[DeviceRegistry] = None


def get_device_registry() -> DeviceRegistry:
    """
    Get the global device registry instance.

    Returns:
        Device registry instance
    """
    global _device_registry
    if _device_registry is None:
        _device_registry = DeviceRegistry()
    return _device_registry


def get_current_device() -> str:
    """
    Get the current device ID based on feature flags.

    Returns:
        Current device identifier
    """
    if FEATURE_MULTI_DEVICE:
        # Future: Allow device selection when multi-device is enabled
        # For now, still default to FM9
        return "fm9"
    else:
        # Single-mode: Always FM9
        return "fm9"


def validate_device_compatibility(device_id: str) -> None:
    """
    Validate that a device is compatible with current system configuration.

    Args:
        device_id: Device identifier to validate

    Raises:
        ValueError: If device not compatible
    """
    registry = get_device_registry()

    if not registry.is_device_supported(device_id):
        raise ValueError(
            f"Device '{device_id}' not supported. "
            f"Available devices: {registry.list_devices()}. "
            f"See docs/ground-truth.md#Future-proofing for expansion info."
        )

    if not FEATURE_MULTI_DEVICE and device_id != "fm9":
        raise ValueError(
            f"Multi-device support disabled. "
            f"Only FM9 is supported in single-mode. "
            f"Enable FEATURE_MULTI_DEVICE for multi-device support. "
            f"See docs/ground-truth.md#Future-proofing."
        )
