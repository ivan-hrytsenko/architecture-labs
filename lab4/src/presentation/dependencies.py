from fastapi import Depends
from sqlalchemy.orm import Session
from src.infrastructure.database import SessionLocal
from src.infrastructure.repositories import SQLAlchemyUserRepository, SQLAlchemyProductRepository
from src.notifications.service import NotificationService
from src.application.common.event_bus import EventBus
from src.notifications.consumers import NotificationConsumer
from src.domain.events.user_events import UserRegisteredEvent
from src.domain.events.product_events import ProductCreatedEvent
from src.application.commands.register_user import RegisterUserHandler
from src.application.commands.create_product import CreateProductHandler
from src.application.queries.get_all_products import GetAllProductsHandler

_event_bus_instance = EventBus()
_notification_service_instance = NotificationService(fail_safely=False)
_consumer = NotificationConsumer(_notification_service_instance)

_event_bus_instance.subscribe(UserRegisteredEvent, _consumer.handle_user_registered)
_event_bus_instance.subscribe(ProductCreatedEvent, _consumer.handle_product_created)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_event_bus() -> EventBus:
    return _event_bus_instance

def get_notification_service(fail_safely: bool = False) -> NotificationService:
    _notification_service_instance._fail_safely = fail_safely
    return _notification_service_instance

def get_register_user_handler(
    db: Session = Depends(get_db),
    notification_service: NotificationService = Depends(get_notification_service),
    event_bus: EventBus = Depends(get_event_bus)
):
    return lambda mode="sync": RegisterUserHandler(
        user_repo=SQLAlchemyUserRepository(db),
        notification_service=notification_service,
        event_bus=event_bus,
        mode=mode
    )

def get_create_product_handler(
    db: Session = Depends(get_db),
    notification_service: NotificationService = Depends(get_notification_service),
    event_bus: EventBus = Depends(get_event_bus)
):
    return lambda mode="sync": CreateProductHandler(
        product_repo=SQLAlchemyProductRepository(db),
        user_repo=SQLAlchemyUserRepository(db),
        notification_service=notification_service,
        event_bus=event_bus,
        mode=mode
    )

def get_all_products_handler(db: Session = Depends(get_db)):
    return GetAllProductsHandler(db)