import pytest
from src.domain.factory import DomainFactory
from src.domain.exceptions import InvalidValueError, InvariantViolationError

def test_create_valid_user():
    user = DomainFactory.create_user(None, "farmer1", "farmer@example.com", "farmer")
    assert user.username == "farmer1"
    assert user.role == "farmer"

def test_create_user_invalid_email():
    with pytest.raises(InvalidValueError):
        DomainFactory.create_user(None, "farmer1", "invalid-email", "farmer")

def test_create_user_invalid_role():
    with pytest.raises(InvalidValueError):
        DomainFactory.create_user(None, "farmer1", "farmer@example.com", "admin")

def test_create_valid_product():
    product = DomainFactory.create_product(None, "Tomato", "Fresh", 10.5, 100, 1)
    assert product.title == "Tomato"
    assert product.price.amount == 10.5
    assert product.quantity.value == 100

def test_create_product_negative_price():
    with pytest.raises(InvalidValueError):
        DomainFactory.create_product(None, "Tomato", "Fresh", -5.0, 100, 1)

def test_product_reduce_stock():
    product = DomainFactory.create_product(None, "Tomato", "Fresh", 10.5, 100, 1)
    product.reduce_stock(30)
    assert product.quantity.value == 70

def test_product_reduce_stock_insufficient():
    product = DomainFactory.create_product(None, "Tomato", "Fresh", 10.5, 100, 1)
    with pytest.raises(InvariantViolationError):
        product.reduce_stock(150)