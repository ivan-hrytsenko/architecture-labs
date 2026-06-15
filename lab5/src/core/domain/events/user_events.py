from dataclasses import dataclass
from src.core.domain.events.base import IntegrationEvent

@dataclass(frozen=True, kw_only=True)
class UserRegisteredEvent(IntegrationEvent):
    user_id: int
    username: str
    email: str
    role: str