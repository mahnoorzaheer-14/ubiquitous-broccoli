from pydantic import WebsocketUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mqtt_broker: str = "broker.hivemq.com"
    mqtt_username: str | None = None
    mqtt_password: str | None = None
    mqtt_port: int =  8884
    controller_sn: str = ""
    s2_websocket_endpoint: WebsocketUrl = WebsocketUrl('ws://localhost:8080/s2')

    model_config = SettingsConfigDict(env_file='.env', extra="ignore")


def get_settings() -> Settings:
    return Settings()
