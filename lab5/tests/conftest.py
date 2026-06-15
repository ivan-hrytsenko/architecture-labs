import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.common.database import Base
from src.core.infrastructure.models import UserORM, ProductORM
from src.analytics.infrastructure.models import UserStatsORM, ProductMetricsORM
from src.presentation.dependencies import get_event_bus

@pytest.fixture(scope="function")
def test_db_setup():
    engine = create_engine(
        "sqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    yield TestingSessionLocal
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(test_db_setup):
    session = test_db_setup()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function", autouse=True)
def clean_event_bus():
    bus = get_event_bus()
    bus._listeners.clear()
    yield