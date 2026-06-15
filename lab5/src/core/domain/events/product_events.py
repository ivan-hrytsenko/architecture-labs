from dataclasses import dataclass
from src.core.domain.events.base import IntegrationEvent

@dataclass(frozen=True, kw_only=True)
class ProductCreatedEvent(IntegrationEvent):
    product_id: int
    title: str
    price: float
    quantity: int
    farmer_id: int