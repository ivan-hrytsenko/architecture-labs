from src.common.event_bus import EventBus
from src.core.domain.events.user_events import UserRegisteredEvent
from src.core.domain.events.product_events import ProductCreatedEvent
from src.analytics.infrastructure.repositories import AnalyticsRepository
from src.analytics.application.consumers import UserRegisteredConsumer, ProductCreatedConsumer

class AnalyticsACL:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def register_subscriptions(self, event_bus: EventBus) -> None:
        event_bus.subscribe(UserRegisteredEvent, self.handle_user_registered)
        event_bus.subscribe(ProductCreatedEvent, self.handle_product_created)

    def handle_user_registered(self, event: UserRegisteredEvent) -> None:
        session = self._session_factory()
        try:
            repo = AnalyticsRepository(session)
            consumer = UserRegisteredConsumer(repo)
            consumer.execute(role=event.role)
        finally:
            session.close()

    def handle_product_created(self, event: ProductCreatedEvent) -> None:
        session = self._session_factory()
        try:
            repo = AnalyticsRepository(session)
            consumer = ProductCreatedConsumer(repo)
            consumer.execute(price=event.price)
        finally:
            session.close()