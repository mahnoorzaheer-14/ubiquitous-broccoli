"""Transform MQTT feedback payloads into S2 PowerMeasurement messages."""

import json
import logging
import uuid

from pydantic import ValidationError
from s2python.common import PowerMeasurement, PowerValue
from s2python.generated.gen_s2 import CommodityQuantity

from schemas.message import MQTTFeedbackMessage

logger = logging.getLogger(__name__)

def transform_message(feedback: MQTTFeedbackMessage) -> PowerMeasurement:
    """Build S2 PowerMeasurement Message from validated MQTT feedback."""
    power_value = PowerValue(
        commodity_quantity=CommodityQuantity.ELECTRIC_POWER_3_PHASE_SYMMETRIC,
        value=feedback.fields.state.grid.active_power_W,
    )
    return PowerMeasurement(
        message_id=uuid.uuid4(),
        message_type="PowerMeasurement",
        measurement_timestamp=feedback.measurement_timestamp,
        values=[power_value],
    )

# This function validates and parses the incoming message from the broker before transforming it into a PowerMeasurement message using a Pydantic model. This approach is used because:
# 1) It is a more pythonic and maintainable way of parsing and validating than the dict-based approach in the commented-out transform_message below. Pydantic may add some parsing overhead, but with no strict latency requirement specified, it is a reasonable trade-off.
# 2) The power measurement payload is relatively small, so Pydantic is practical here. If message size or throughput grows and latency becomes critical, we could switch to the lighter-weight dict-based approach.

def process_mqtt_payload(payload_str: str) -> PowerMeasurement | None:
    """Parse and validate MQTT payload, transform to S2."""
    try:
        feedback = MQTTFeedbackMessage.model_validate_json(payload_str)
    except (ValidationError, json.JSONDecodeError) as e:
        logger.error("Invalid or incomplete MQTT feedback: %s", e)
        return None
    return transform_message(feedback)


# def transform_message(payload: dict) -> PowerMeasurement:
#     time = payload.get("time")
#     timestamp = datetime.fromtimestamp(time, tz=timezone.utc)
#     grid = payload.get("fields", {}).get("state", {}).get("grid", {})
#     active_power = grid.get("active_power_W")
#     if not active_power:
#         # add log here. This message can be sent back to the publisher or to a DLQ of sort to process/analyze later
#         return None
#     power_value = PowerValue(
#         commodity_quantity="ELECTRIC.POWER.3_PHASE_SYMMETRIC",
#         value=active_power
#     )
#     return PowerMeasurement(
#         message_id=uuid.uuid4(),
#         message_type="PowerMeasurement",
#         measurement_timestamp=timestamp,
#         values=[power_value]
#     )