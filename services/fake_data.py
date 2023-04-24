import json

from sqlalchemy.orm import Session

from models.recipes import Recipe


def create_default_recipes(db: Session):
    recipes = []
    for i in range(100):
        name = f"Recipe {i}"
        description = f"This is the description for recipe {i}"
        ingredients = json.dumps(["ingredient1", "ingredient2", "ingredient3"])
        recipe = Recipe(
            name=name, description=description, ingredients=ingredients, owner_id=1
        )
        db.add(recipe)
        recipes.append(recipe)
    db.commit()
    return recipes
