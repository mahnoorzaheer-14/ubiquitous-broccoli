import asyncio
import json
import logging
import uuid

import aiomqtt
import websockets
from pydantic import ValidationError
from s2python.common import PowerMeasurement, PowerValue
from s2python.generated.gen_s2 import CommodityQuantity

from core.config import get_settings
from schemas.message import MQTTFeedbackMessage

settings = get_settings()
logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Configure root logger format and level."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


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


def transform_message(feedback: MQTTFeedbackMessage) -> PowerMeasurement:
    """Build S2 PowerMeasurement from validated MQTT feedback. Uses feedback.measurement_timestamp from schema."""
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


def process_mqtt_payload(payload_str: str) -> PowerMeasurement | None:
    """Parse and validate MQTT payload, transform to S2. On error log and return None."""
    try:
        feedback = MQTTFeedbackMessage.model_validate_json(payload_str)
    except (ValidationError, json.JSONDecodeError) as e:
        logger.error("Invalid or incomplete MQTT feedback: %s", e)
        return None
    return transform_message(feedback)


async def main():
    configure_logging()
    logger.info("The app has started")
    try:
        async with websockets.connect(str(settings.s2_websocket_endpoint)) as ws:
            async with aiomqtt.Client(hostname=settings.mqtt_broker, port=settings.mqtt_port) as client:
                await client.subscribe(f"standard1/outbound/remoteControlMetrics/feedback/{settings.controller_sn}")
                async for message in client.messages:
                    payload_str = message.payload.decode()
                    s2_msg = process_mqtt_payload(payload_str)
                    if s2_msg is not None:
                        json_str = s2_msg.model_dump_json()
                        logger.info(json_str)
                        await ws.send(json_str)
                    else:
                        logger.warning("Skipping message due to validation error")
    except Exception as e:
        logger.error("WebSocket connection failed: %s", e)
        raise


if __name__ == "__main__":
    asyncio.run(main())
