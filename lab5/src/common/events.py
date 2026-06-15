import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass(frozen=True, kw_only=True)
class IntegrationEvent:
    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))