import pytest
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database import Base
from src.infrastructure.repositories import SQLAlchemyUserRepository, SQLAlchemyProductRepository
from src.notifications.service import NotificationService
from src.application.common.event_bus import EventBus
from src.application.commands.register_user import RegisterUserHandler, RegisterUserCommand
from src.application.commands.create_product import CreateProductHandler, CreateProductCommand
from src.domain.exceptions import InvariantViolationError

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

def test_sync_registration_success(db_session):
    user_repo = SQLAlchemyUserRepository(db_session)
    notification_service = NotificationService(fail_safely=False)
    event_bus = EventBus()
    
    handler = RegisterUserHandler(user_repo, notification_service, event_bus, mode="sync")
    command = RegisterUserCommand(username="ivan_farmer", email="ivan@example.com", role="farmer")
    
    start_time = time.perf_counter()
    user_id = handler.handle(command)
    end_time = time.perf_counter()
    
    assert user_id is not None
    assert user_repo.get_by_id(user_id) is not None
    assert (end_time - start_time) < 0.1

def test_sync_registration_failure_on_notification_error(db_session):
    user_repo = SQLAlchemyUserRepository(db_session)
    notification_service = NotificationService(fail_safely=True)
    event_bus = EventBus()
    
    handler = RegisterUserHandler(user_repo, notification_service, event_bus, mode="sync")
    command = RegisterUserCommand(username="bad_sync", email="bad@example.com", role="customer")
    
    with pytest.raises(InvariantViolationError) as exc_info:
        handler.handle(command)
        
    assert "Registration aborted due to notification system failure" in str(exc_info.value)
    assert user_repo.get_by_email("bad@example.com") is None

def test_sync_product_creation_ignores_notification_error(db_session):
    user_repo = SQLAlchemyUserRepository(db_session)
    product_repo = SQLAlchemyProductRepository(db_session)
    notification_service = NotificationService(fail_safely=True)
    event_bus = EventBus()
    
    from src.domain.factory import DomainFactory
    farmer = DomainFactory.create_user(id=None, username="farmer1", email="f1@ex.com", role="farmer")
    saved_farmer = user_repo.save(farmer)
    
    handler = CreateProductHandler(product_repo, user_repo, notification_service, event_bus, mode="sync")
    command = CreateProductCommand(title="Tomato", description="Fresh", price=50.0, quantity=10, farmer_id=saved_farmer.id)
    
    product_id = handler.handle(command)
    
    assert product_id is not None
    assert product_repo.get_by_id(product_id) is not None