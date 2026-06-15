def test_api_workflow(client):
    reg_response = client.post("/register", json={
        "username": "farmer_joe",
        "email": "joe@example.com",
        "role": "farmer"
    })
    assert reg_response.status_code == 201

    login_response = client.post("/login", json={
        "email": "joe@example.com"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    prod_response = client.post("/products", headers=headers, json={
        "title": "Potatoes",
        "description": "Organic potatoes",
        "price": 2.5,
        "quantity": 200
    })
    assert prod_response.status_code == 201
    assert prod_response.json()["title"] == "Potatoes"

    get_response = client.get("/products")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 1