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

## Project Structure

```
eniris_rm/
├── __init__.py
├── __main__.py          # Entry point
├── config.py            # Configuration using pydantic-settings
├── models.py            # Pydantic models for MQTT and S2 messages
├── mqtt_client.py       # MQTT client implementation
├── s2_client.py         # S2 WebSocket client (bonus)
└── transformer.py       # Data transformation logic

tests/
├── __init__.py
└── test_transformer.py  # Unit tests
```

## References

- [Eniris MQTT documentation](https://docs.eniris.be/en/Controller/External%20Signals/MQTT/eniris-mqtt)
- [S2 PowerMeasurement documentation](https://docs.s2standard.org/model-reference/Common/PowerMeasurement/)
- [s2-python library](https://github.com/flexiblepower/s2-python)
