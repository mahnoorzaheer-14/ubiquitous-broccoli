"""Pytest fixtures."""

import pytest

SAMPLE_MQTT_JSON = """
{
  "time": 1714652046,
  "fields": {
    "state": {
      "grid": {
        "active_power_W": 742.3,
        "today_imported_energy_Wh": 3850.0,
        "today_exported_energy_Wh": 120.0,
        "import_limit_W": 6000.0,
        "export_limit_W": 0.0
      },
      "vpp_id": "example-vpp",
      "storage": {},
      "solar": {},
      "heat_pump": {},
      "switched_load": {}
    },
    "response_code": 0
  }
}
"""


MALFORMED_MQTT_JSON = '{"time": 1714652046, invalid}'
INCOMPLETE_MQTT_JSON = '{"time": 1714652046}'


@pytest.fixture
def sample_mqtt_feedback_json():
    """Valid sample MQTT feedback payload (string)."""
    return SAMPLE_MQTT_JSON.strip()


@pytest.fixture
def malformed_mqtt_json():
    """Malformed JSON (invalid syntax)."""
    return MALFORMED_MQTT_JSON


@pytest.fixture
def incomplete_mqtt_json():
    """Incomplete JSON (missing required fields e.g. fields.state.grid)."""
    return INCOMPLETE_MQTT_JSON
