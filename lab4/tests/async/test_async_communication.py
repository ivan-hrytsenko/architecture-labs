import pytest
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database import Base
from src.infrastructure.repositories import SQLAlchemyUserRepository, SQLAlchemyProductRepository
from src.notifications.service import NotificationService
from src.application.common.event_bus import EventBus
from src.notifications.consumers import NotificationConsumer
from src.domain.events.user_events import UserRegisteredEvent
from src.application.commands.register_user import RegisterUserHandler, RegisterUserCommand

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_async_registration_non_blocking_and_eventual_consistency(db_session):
    user_repo = SQLAlchemyUserRepository(db_session)
    notification_service = NotificationService(fail_safely=False)
    event_bus = EventBus()
    consumer = NotificationConsumer(notification_service)
    
    event_bus.subscribe(UserRegisteredEvent, consumer.handle_user_registered)
    
    handler = RegisterUserHandler(user_repo, notification_service, event_bus, mode="async")
    command = RegisterUserCommand(username="async_user", email="async@example.com", role="customer")
    
    start_time = time.perf_counter()
    user_id = handler.handle(command)
    end_time = time.perf_counter()
    
    assert user_id is not None
    assert (end_time - start_time) < 0.05
    
    time.sleep(0.1)
    assert user_repo.get_by_id(user_id) is not None

def test_async_registration_does_not_fail_main_flow_on_broker_error(db_session):
    user_repo = SQLAlchemyUserRepository(db_session)
    notification_service = NotificationService(fail_safely=True)
    event_bus = EventBus()
    consumer = NotificationConsumer(notification_service)
    
    event_bus.subscribe(UserRegisteredEvent, consumer.handle_user_registered)
    
    handler = RegisterUserHandler(user_repo, notification_service, event_bus, mode="async")
    command = RegisterUserCommand(username="async_fail", email="async_fail@example.com", role="customer")
    
    user_id = handler.handle(command)
    
    assert user_id is not None
    time.sleep(0.1)
    assert user_repo.get_by_id(user_id) is not None