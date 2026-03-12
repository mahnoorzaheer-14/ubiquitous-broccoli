import asyncio
import logging

import aiomqtt
import websockets

from core.config import settings
from core.logging import configure_logging
from eniris_rm.message_processing import process_mqtt_payload

logger = logging.getLogger(__name__)

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
