import logging
from dataclasses import dataclass
from src.domain.interfaces import UserRepository, ProductRepository
from src.domain.factory import DomainFactory
from src.domain.exceptions import InvariantViolationError
from src.application.commands.base import CommandHandler
from src.application.common.event_bus import EventBus
from src.notifications.interface import NotificationComponent
from src.domain.events.product_events import ProductCreatedEvent

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class CreateProductCommand:
    title: str
    description: str
    price: float
    quantity: int
    farmer_id: int

class CreateProductHandler(CommandHandler[CreateProductCommand, int]):
    def __init__(
        self, 
        product_repo: ProductRepository, 
        user_repo: UserRepository,
        notification_service: NotificationComponent,
        event_bus: EventBus,
        mode: str = "sync"
    ):
        self._product_repo = product_repo
        self._user_repo = user_repo
        self._notification_service = notification_service
        self._event_bus = event_bus
        self._mode = mode

    def handle(self, command: CreateProductCommand) -> int:
        farmer = self._user_repo.get_by_id(command.farmer_id)
        if not farmer:
            raise InvariantViolationError("Farmer not found")
        
        if farmer.role != "farmer":
            raise InvariantViolationError("Only users with the 'farmer' role can create products")

        product = DomainFactory.create_product(
            None,
            command.title,
            command.description,
            command.price,
            command.quantity,
            command.farmer_id
        )
        saved_product = self._product_repo.save(product)

        if self._mode == "sync":
            try:
                self._notification_service.send_product_created_notification(
                    title=saved_product.title,
                    price=saved_product.price.value
                )
            except Exception as e:
                logger.error(f"[Sync Notification Warning] Side effect failed but ignored: {e}")
                pass
        
        elif self._mode == "async":
            event = ProductCreatedEvent(
                product_id=saved_product.id,
                title=saved_product.title,
                price=saved_product.price.value,
                quantity=saved_product.quantity.value,
                farmer_id=saved_product.farmer_id
            )
            self._event_bus.publish(event)

        return saved_product.id