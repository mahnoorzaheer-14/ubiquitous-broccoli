# MQTT to S2 PowerMeasurement Bridge

This application receives power measurement data from the Eniris SmartGrid Home Energy Management System via MQTT and forwards it as S2 PowerMeasurement messages.

## Assignment

This project is part of a technical interview assignment. See the full assignment details in the Notion page.

## Requirements

- Python 3.12+
- Poetry for dependency management

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Copy `.env.example` to `.env` and configure your settings:
```bash
cp .env.example .env
```

3. Edit `.env` with your MQTT broker credentials and controller serial number.

## Running the Application

```bash
poetry run python -m eniris_rm
```

## Testing

Run the test suite:
```bash
poetry run pytest
```

With coverage:
```bash
poetry run pytest --cov
```

## Development

Install pre-commit hooks:
```bash
poetry run pre-commit install
```

Run linting:
```bash
poetry run ruff check .
```

Run type checking:
```bash
poetry run pyright
```

## Important Libraries
- [pydantic](https://docs.pydantic.dev/)
- [pydantic settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [python mqtt client library](https://aiomqtt.bo3hm.com/subscribing-to-a-topic)

## References

- [Eniris MQTT documentation](https://docs.eniris.be/en/Controller/External%20Signals/MQTT/eniris-mqtt)
- [S2 PowerMeasurement documentation](https://docs.s2standard.org/model-reference/Common/PowerMeasurement/)

## MQTT
- [Public mqtt broker](https://www.mqtt-dashboard.com/)
- [basics of MQTT](https://www.hivemq.com/mqtt/)
- [webbased MQTT client](https://www.hivemq.com/demos/websocket-client/)

# Dummy WebSocket Server

This is a simple WebSocket server for testing purposes. It accepts all connections on `/s2` and prints any messages it receives, formatting them prettily if they are JSON.

## How to run

1. Make sure you have installed dependencies with Poetry:

	poetry install

2. Start the server:

	poetry run ws_server

The server will listen on `ws://0.0.0.0:8000/s2`.

Any message sent to this endpoint will be printed to the console. JSON messages will be pretty-printed.
