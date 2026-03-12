"""Tests for MQTT feedback → S2 PowerMeasurement transformation and validation."""

import json
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError
from pytest import LogCaptureFixture
from s2python.generated.gen_s2 import CommodityQuantity

from eniris_rm.__main__ import process_mqtt_payload, transform_message
from schemas.message import MQTTFeedbackMessage


def test_transform_message_produces_expected_timestamp_and_grid_power(
    sample_mqtt_feedback_json: str,
) -> None:
    """Given sample MQTT feedback, S2 PowerMeasurement has expected timestamp and grid active power."""
    feedback = MQTTFeedbackMessage.model_validate_json(sample_mqtt_feedback_json)
    pm = transform_message(feedback)
    expected_ts = datetime(2024, 5, 2, 12, 14, 6, tzinfo=timezone.utc)
    assert pm.measurement_timestamp == expected_ts
    assert pm.message_type == "PowerMeasurement"
    assert len(pm.values) == 1
    assert pm.values[0].commodity_quantity is CommodityQuantity.ELECTRIC_POWER_3_PHASE_SYMMETRIC
    assert isinstance(pm.values[0].value, float)
    assert pm.values[0].value == 742.3


def test_model_validate_json_raises_on_malformed_json(malformed_mqtt_json: str) -> None:
    """Malformed JSON raises ValidationError or JSONDecodeError."""
    with pytest.raises((ValidationError, json.JSONDecodeError)):
        MQTTFeedbackMessage.model_validate_json(malformed_mqtt_json)


def test_model_validate_json_raises_on_incomplete_json(incomplete_mqtt_json: str) -> None:
    """Incomplete JSON (missing required fields) raises ValidationError."""
    with pytest.raises(ValidationError):
        MQTTFeedbackMessage.model_validate_json(incomplete_mqtt_json)


def test_process_mqtt_payload_handles_malformed_gracefully(
    caplog: LogCaptureFixture,
    malformed_mqtt_json: str,
) -> None:
    """Process malformed JSON: no crash, error logged."""
    result = process_mqtt_payload(malformed_mqtt_json)
    assert result is None
    assert "error" in caplog.text.lower() or "invalid" in caplog.text.lower()


def test_process_mqtt_payload_handles_incomplete_gracefully(
    caplog: LogCaptureFixture,
    incomplete_mqtt_json: str,
) -> None:
    """Process incomplete JSON: no crash, error logged."""
    result = process_mqtt_payload(incomplete_mqtt_json)
    assert result is None
    assert "error" in caplog.text.lower() or "invalid" in caplog.text.lower()


def test_process_mqtt_payload_returns_s2_message_for_valid_payload(
    sample_mqtt_feedback_json: str,
) -> None:
    """Valid payload returns PowerMeasurement with correct grid power."""
    result = process_mqtt_payload(sample_mqtt_feedback_json)
    assert result is not None
    assert result.values[0].value == 742.3
