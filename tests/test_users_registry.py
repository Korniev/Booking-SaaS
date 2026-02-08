def test_register_user(client):
    payload = {"email": "test@example.com", "password": "12345678"}

    r = client.post("/users/register", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "test@example.com"
    assert "id" in data