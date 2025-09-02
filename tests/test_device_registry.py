"""
Tests for Device Registry Architecture

Tests the device registry system for future multi-device support.
Currently FM9-only, but designed for expansion when FEATURE_MULTI_DEVICE is enabled.
"""

import pytest
from pathlib import Path
from tonegpt.core.device_registry import (
    DeviceRegistry,
    get_device_registry,
    get_current_device,
    validate_device_compatibility,
)
from tonegpt.core.flags import FEATURE_MULTI_DEVICE


class TestDeviceRegistry:
    """Test device registry functionality."""

    def test_device_registry_initialization(self):
        """Test that device registry initializes with FM9 device."""
        registry = DeviceRegistry()

        # Should have FM9 device
        assert "fm9" in registry.list_devices()
        assert len(registry.list_devices()) == 1

        # Should have FM9 as default
        assert registry.get_default_device() == "fm9"

    def test_fm9_device_configuration(self):
        """Test FM9 device configuration is correct."""
        registry = DeviceRegistry()
        fm9_config = registry.get_device("fm9")

        # Check required fields
        assert fm9_config["name"] == "Fractal Audio FM9"
        assert fm9_config["model"] == "FM9"
        assert fm9_config["version"] == "1.0"

        # Check data sources
        assert fm9_config["parameter_source"] == "data/fm9_comprehensive_reference.json"
        assert fm9_config["config_source"] == "data/fm9_config.json"
        assert fm9_config["blocks_source"] == "tonegpt/core/blocks_with_footswitch.json"

        # Check capabilities
        assert fm9_config["max_blocks"] == 512
        assert "amp" in fm9_config["supported_blocks"]
        assert "cab" in fm9_config["supported_blocks"]
        assert "drive" in fm9_config["supported_blocks"]

    def test_get_device_raises_error_for_unsupported(self):
        """Test that getting unsupported device raises ValueError."""
        registry = DeviceRegistry()

        with pytest.raises(ValueError) as exc_info:
            registry.get_device("unsupported_device")

        error_msg = str(exc_info.value)
        assert "Device 'unsupported_device' not supported" in error_msg
        assert "Available devices: ['fm9']" in error_msg
        assert "docs/ground-truth.md#Future-proofing" in error_msg

    def test_device_parameter_sources(self):
        """Test device parameter source methods."""
        registry = DeviceRegistry()

        # Test parameter source
        param_source = registry.get_device_parameter_source("fm9")
        assert param_source == "data/fm9_comprehensive_reference.json"

        # Test config source
        config_source = registry.get_device_config_source("fm9")
        assert config_source == "data/fm9_config.json"

        # Test blocks source
        blocks_source = registry.get_device_blocks_source("fm9")
        assert blocks_source == "tonegpt/core/blocks_with_footswitch.json"

    def test_supported_blocks(self):
        """Test supported blocks for FM9."""
        registry = DeviceRegistry()
        supported_blocks = registry.get_supported_blocks("fm9")

        expected_blocks = [
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
        ]

        for block in expected_blocks:
            assert block in supported_blocks

    def test_max_blocks(self):
        """Test maximum blocks for FM9."""
        registry = DeviceRegistry()
        max_blocks = registry.get_max_blocks("fm9")
        assert max_blocks == 512

    def test_is_device_supported(self):
        """Test device support checking."""
        registry = DeviceRegistry()

        assert registry.is_device_supported("fm9") is True
        assert registry.is_device_supported("unsupported") is False


class TestGlobalDeviceRegistry:
    """Test global device registry functions."""

    def test_get_device_registry_singleton(self):
        """Test that get_device_registry returns singleton instance."""
        registry1 = get_device_registry()
        registry2 = get_device_registry()

        assert registry1 is registry2

    def test_get_current_device(self):
        """Test get_current_device returns FM9."""
        current_device = get_current_device()
        assert current_device == "fm9"

    def test_validate_device_compatibility_fm9(self):
        """Test device compatibility validation for FM9."""
        # Should not raise for FM9
        validate_device_compatibility("fm9")

    def test_validate_device_compatibility_unsupported(self):
        """Test device compatibility validation for unsupported device."""
        with pytest.raises(ValueError) as exc_info:
            validate_device_compatibility("unsupported_device")

        error_msg = str(exc_info.value)
        assert "Device 'unsupported_device' not supported" in error_msg
        assert "Available devices: ['fm9']" in error_msg
        assert "docs/ground-truth.md#Future-proofing" in error_msg


class TestFeatureFlagIntegration:
    """Test integration with feature flags."""

    def test_feature_multi_device_default_false(self):
        """Test that FEATURE_MULTI_DEVICE defaults to False."""
        assert FEATURE_MULTI_DEVICE is False

    def test_current_device_with_feature_flag(self):
        """Test that current device is FM9 regardless of feature flag."""
        # Even if FEATURE_MULTI_DEVICE were True, should still default to FM9
        current_device = get_current_device()
        assert current_device == "fm9"

    def test_device_registry_fm9_only(self):
        """Test that device registry only contains FM9."""
        registry = get_device_registry()
        devices = registry.list_devices()

        assert devices == ["fm9"]
        assert len(devices) == 1


class TestFutureExpansion:
    """Test architecture for future expansion."""

    def test_device_registry_extensible(self):
        """Test that device registry is designed for extension."""
        registry = DeviceRegistry()

        # Should have methods for adding devices (even if not implemented yet)
        assert hasattr(registry, "get_device")
        assert hasattr(registry, "list_devices")
        assert hasattr(registry, "is_device_supported")

    def test_parameter_source_abstraction(self):
        """Test that parameter sources are abstracted."""
        registry = DeviceRegistry()

        # Should be able to get parameter source without hardcoding
        param_source = registry.get_device_parameter_source("fm9")
        assert isinstance(param_source, str)
        assert param_source.endswith(".json")

    def test_device_configuration_structure(self):
        """Test that device configuration has consistent structure."""
        registry = DeviceRegistry()
        fm9_config = registry.get_device("fm9")

        # Should have all required fields for device configuration
        required_fields = [
            "name",
            "model",
            "version",
            "supported_blocks",
            "parameter_source",
            "config_source",
            "blocks_source",
            "max_blocks",
            "description",
        ]

        for field in required_fields:
            assert field in fm9_config, f"Missing required field: {field}"

    def test_error_messages_include_documentation(self):
        """Test that error messages include documentation references."""
        registry = DeviceRegistry()

        with pytest.raises(ValueError) as exc_info:
            registry.get_device("invalid")

        error_msg = str(exc_info.value)
        assert "docs/ground-truth.md#Future-proofing" in error_msg
