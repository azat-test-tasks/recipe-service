from fastapi.testclient import TestClient

from models import users as models


def test_get_current_user(client: TestClient, user: models.User, token: str):
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["email"] == user.email


def test_get_all_users(client: TestClient, users: list[models.User], token: str):
    response = client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(users)
    for i, user in enumerate(users):
        assert data[i]["id"] == user.id
        assert data[i]["email"] == user.email


def test_get_user_by_id(client: TestClient, user: models.User, token: str):
    response = client.get(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["email"] == user.email


def test_delete_user_by_id(client: TestClient, user: models.User, token: str):
    response = client.delete(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

    response = client.get(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
