from tests.conftest import make_user


def test_register_user(client, mock_user_service):
    user = make_user(email="test@example.com")
    mock_user_service.register.return_value = user

    payload = {"email": "test@example.com", "password": "12345678"}

    r = client.post("/users/register", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == "test@example.com"
    assert "id" in data