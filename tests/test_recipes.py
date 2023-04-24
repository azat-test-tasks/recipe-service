import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from models.recipes import Recipe
from models.users import User
from services.recipes import create_recipe

pytestmark = pytest.mark.asyncio


async def test_create_recipe(client: AsyncClient, db: Session, test_user: User):
    # Создаем мок рецепта
    recipe_data = {
        "name": "Омлет",
        "description": "Быстрый и простой завтрак",
        "ingredients": [
            {"name": "Яйца", "quantity": 3},
            {"name": "Молоко", "quantity": "50 мл"},
            {"name": "Соль", "quantity": "по вкусу"},
            {"name": "Масло растительное", "quantity": "2 ст. л."},
        ],
        "steps": [
            {"description": "Смешать яйца, молоко и соль в миске", "time": 5},
            {
                "description": "Вылить яичную смесь на сковороду и готовить до золотистой корочки",
                "time": 10,
            },
        ],
    }
    # Создаем рецепт в базе данных
    created_recipe = await create_recipe(db, recipe_data, test_user)
    # Получаем ответ от API
    response = await client.post("/recipes/", json=recipe_data)
    # Проверяем, что статус код ответа равен 200
    assert response.status_code == 200
    # Проверяем, что данные в ответе соответствуют созданному рецепту
    assert response.json() == created_recipe


async def test_get_all_recipes(client: AsyncClient):
    response = await client.get("/recipes/")
    assert response.status_code == 200


async def test_get_recipe(client: AsyncClient, db: Session, test_recipe: Recipe):
    response = await client.get(f"/recipes/{test_recipe.id}")
    assert response.status_code == 200
    assert response.json() == test_recipe


async def test_update_recipe(
    client: AsyncClient, db: Session, test_recipe: Recipe, test_user: User
):
    updated_recipe_data = {"title": "New Test Recipe Title"}
    response = await client.put(f"/recipes/{test_recipe.id}", json=updated_recipe_data)
    assert response.status_code == 200
    updated_recipe = db.query(Recipe).get(test_recipe.id)
    assert updated_recipe.title == updated_recipe_data["title"]


async def test_delete_recipe(client: AsyncClient, db: Session, test_recipe: Recipe):
    response = await client.delete(f"/recipes/{test_recipe.id}")
    assert response.status_code == 200
    deleted_recipe = db.query(Recipe).get(test_recipe.id)
    assert deleted_recipe is None


async def test_search_recipes(client: AsyncClient):
    response = await client.get("/recipes/search?sort_by_time=True")
    assert response.status_code == 200
    assert len(response.json()) > 0
