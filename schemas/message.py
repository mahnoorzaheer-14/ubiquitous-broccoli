from datetime import datetime, timezone

from pydantic import BaseModel, Field, computed_field


class GridState(BaseModel):
    """Total power at the grid connection."""
    active_power_W: float = Field(..., description="Total grid active power in Watts")

class State(BaseModel):
    """Different states but this validates the grid only."""
    grid: GridState

class FeedbackFields(BaseModel):
    """Energy 'fields' in the feedback message."""
    state: State

class MQTTFeedbackMessage(BaseModel):
    """Parsed MQTT feedback message. Only fields needed for S2 PowerMeasurement are validated."""

    time: int = Field(..., description="Unix timestamp when the values were measured")
    fields: FeedbackFields

    @computed_field
    @property
    def measurement_timestamp(self) -> datetime:
        """Timezone-aware datetime for S2 measurement_timestamp (UTC)."""
        return datetime.fromtimestamp(self.time, tz=timezone.utc)
