from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm import Session

from api import deps
from main import app
from schemas.users import User, UserCreate

client = TestClient(app)


@fixture
def test_db() -> Session:
    yield deps.get_db()


def test_login(test_db: Session):
    # Создаем тестового пользователя
    user = User(email="test@example.com", password="password")
    test_db.add(user)
    test_db.commit()

    # Проверяем успешную аутентификацию
    response = client.post(
        "/login", data={"username": "test@example.com", "password": "password"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    # Проверяем неудачную аутентификацию
    response = client.post(
        "/login", data={"username": "test@example.com", "password": "wrong_password"}
    )
    assert response.status_code == 400
    assert "detail" in response.json()


def test_create_user(test_db: Session):
    # Создаем тестового пользователя
    user_in = UserCreate(email="test@example.com", password="password")

    # Проверяем успешную регистрацию
    response = client.post("/registration", json=user_in.dict())
    assert response.status_code == 200
    user = User(**response.json())
    assert user.email == user_in.email

    # Проверяем неудачную регистрацию
    response = client.post("/registration", json=user_in.dict())
    assert response.status_code == 400
    assert "detail" in response.json()
