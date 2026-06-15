import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database import Base
from src.presentation.main import app
from src.presentation.dependencies import get_db
from src.infrastructure.models import ProductORM

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_lab3.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_get_all_products_query_returns_correct_read_models(db_session, client):
    product1 = ProductORM(title="Сир", description="Домашній сир", price=120.0, quantity=5, farmer_id=1)
    product2 = ProductORM(title="Мед", description="Липовий мед", price=250.0, quantity=2, farmer_id=1)
    db_session.add(product1)
    db_session.add(product2)
    db_session.commit()

    response = client.get("/products")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Сир"
    assert data[1]["title"] == "Мед"
    assert "farmer_id" in data[0]