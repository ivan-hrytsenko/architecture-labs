from src.domain.events.user_events import UserRegisteredEvent
from src.domain.events.product_events import ProductCreatedEvent
from src.notifications.interface import NotificationComponent

class NotificationConsumer:
    def __init__(self, notification_service: NotificationComponent):
        self._notification_service = notification_service

    def handle_user_registered(self, event: UserRegisteredEvent) -> None:
        self._notification_service.send_welcome_notification(
            email=event.email,
            username=event.username
        )

    def handle_product_created(self, event: ProductCreatedEvent) -> None:
        self._notification_service.send_product_created_notification(
            title=event.title,
            price=event.price
        )