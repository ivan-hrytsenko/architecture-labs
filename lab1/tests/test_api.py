from fastapi import status
from lab1.src.models.product import Category

def test_user_registration_and_login(client):
    user_payload = {
        "email": "customer@example.com",
        "password": "securepassword",
        "full_name": "John Doe",
        "role": "customer"
    }
    response = client.post("/register", json=user_payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == "customer@example.com"

    login_payload = {
        "email": "customer@example.com",
        "password": "securepassword",
        "full_name": "John Doe",
        "role": "customer"
    }
    response = client.post("/login", json=login_payload)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

def test_farmer_can_create_product(client, db):
    category = Category(name="Vegetables", description="Fresh vegetables")
    db.add(category)
    db.commit()

    farmer_payload = {
        "email": "farmer@example.com",
        "password": "password123",
        "full_name": "Farmer Joe",
        "role": "farmer"
    }
    client.post("/register", json=farmer_payload)
    login_response = client.post("/login", json=farmer_payload)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    product_payload = {
        "category_id": category.id,
        "name": "Carrot",
        "description": "Sweet carrot",
        "price": 2.50,
        "stock_quantity": 50
    }
    response = client.post("/products", json=product_payload, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED

def test_customer_cannot_create_product(client, db):
    category = Category(name="Vegetables", description="Fresh vegetables")
    db.add(category)
    db.commit()

    customer_payload = {
        "email": "hacker@example.com",
        "password": "password123",
        "full_name": "Not A Farmer",
        "role": "customer"
    }
    client.post("/register", json=customer_payload)
    login_response = client.post("/login", json=customer_payload)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    product_payload = {
        "category_id": category.id,
        "name": "Carrot",
        "description": "Sweet carrot",
        "price": 2.50,
        "stock_quantity": 50
    }
    response = client.post("/products", json=product_payload, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN