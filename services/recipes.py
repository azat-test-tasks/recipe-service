from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.recipes import Recipe
from schemas.recipes import RecipeCreateRequest, RecipeUpdateRequest


async def get_all_recipes(db: Session, skip: int = 0, limit: int = 100) -> List[Recipe]:
    result = db.execute(select(Recipe).offset(skip).limit(limit))
    return result.scalars().all()


async def get_recipe_by_id(db: Session, recipe_id: int) -> Optional[Recipe]:
    result = db.execute(select(Recipe).filter(Recipe.id == recipe_id))
    return result.scalars().first()


async def create_recipe(db: Session, recipe: RecipeCreateRequest) -> Recipe:
    recipe_db = Recipe(
        name=recipe.name,
        description=recipe.description,
        ingredients=recipe.ingredients,
        steps=recipe.steps
    )
    db.add(recipe_db)
    db.commit()
    db.refresh(recipe_db)
    return recipe_db


async def update_recipe(db: Session, recipe_id: int, recipe: RecipeUpdateRequest) -> Optional[Recipe]:
    if not recipe.dict(exclude_unset=True):
        raise ValueError("No fields provided for update")

    result = db.execute(select(Recipe).filter(Recipe.id == recipe_id))
    recipe_db = result.scalars().first()
    if recipe_db:
        for field, value in recipe:
            if value is not None:
                setattr(recipe_db, field, value)
        db.commit()
        db.refresh(recipe_db)
    return recipe_db


async def delete_recipe(db: Session, recipe_id: int) -> Optional[Recipe]:
    result = db.execute(select(Recipe).filter(Recipe.id == recipe_id))
    recipe_db = result.scalars().first()
    if recipe_db:
        db.delete(recipe_db)
        db.commit()
    return recipe_db
