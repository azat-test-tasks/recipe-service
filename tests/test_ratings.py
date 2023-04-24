from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from models.ratings import Rating

client = TestClient(app)


def test_create_rating_for_recipe(db: Session):
    # Test creating a rating for a recipe
    with client:
        # Login as a user
        data = {"username": "testuser", "password": "testpassword"}
        response = client.post("/login", data=data)
        assert response.status_code == 200

        # Create a rating
        data = {"value": 3}
        response = client.post(
            "/1/ratings",
            json=data,
            headers={"Authorization": f"Bearer {response.json()['access_token']}"},
        )
        assert response.status_code == 200

        # Check that the rating was created
        db_rating = db.query(Rating).filter(Rating.id == response.json()["id"]).first()
        assert db_rating is not None
        assert db_rating.recipe_id == 1
        assert db_rating.user_id == 1
        assert db_rating.rating == 3


def test_create_rating_for_recipe_already_rated(db: Session):
    # Test creating a rating for a recipe that has already been rated by the user
    with client:
        # Login as a user
        data = {"username": "testuser", "password": "testpassword"}
        response = client.post("/login", data=data)
        assert response.status_code == 200

        # Create an initial rating
        data = {"value": 3}
        response = client.post(
            "/1/ratings",
            json=data,
            headers={"Authorization": f"Bearer {response.json()['access_token']}"},
        )
        assert response.status_code == 200

        # Attempt to create another rating
        data = {"value": 4}
        response = client.post(
            "/1/ratings",
            json=data,
            headers={"Authorization": f"Bearer {response.json()['access_token']}"},
        )
        assert response.status_code == 400


def test_get_ratings_for_recipe(db: Session):
    # Test getting ratings for a recipe
    with client:
        # Create some ratings
        for i in range(5):
            db_rating = Rating(rating=3, recipe_id=1, user_id=i)
            db.add(db_rating)
        db.commit()

        # Get the ratings
        response = client.get("/1/ratings")
        assert response.status_code == 200

        # Check the response
        assert len(response.json()) == 5
        for rating in response.json():
            assert rating["recipe_id"] == 1
            assert rating["value"] == 3
