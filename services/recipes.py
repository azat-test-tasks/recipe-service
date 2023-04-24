from typing import List

from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from models.recipes import Recipe, Step
from models.users import User
from schemas.recipes import RecipeCreateRequest, RecipeUpdateRequest


async def create_recipe(
    db: Session, recipe: RecipeCreateRequest, current_user: User
) -> Recipe:
    user_info = db.query(User).filter(User.email == current_user.email).first()
    db_recipe = Recipe(
        name=recipe.name,
        description=recipe.description,
        ingredients=recipe.ingredients,
        owner_id=user_info.id,
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    for step in recipe.steps:
        db_step = Step(**step.dict(), recipe_id=db_recipe.id)
        db.add(db_step)
        db.commit()

    return db_recipe


async def get_all_recipes(db: Session, skip: int = 0, limit: int = 100) -> List[Recipe]:
    return db.query(Recipe).offset(skip).limit(limit).all()


async def get_recipe(db: Session, recipe_id: int) -> Recipe:
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return db_recipe


async def update_recipe(
    db: Session, recipe_id: int, recipe: RecipeUpdateRequest, current_user: User
) -> Recipe:
    db_recipe = await get_recipe(db, recipe_id)

    if db_recipe.owner != current_user:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this recipe"
        )

    if recipe.name:
        db_recipe.name = recipe.name

    if recipe.description:
        db_recipe.description = recipe.description

    if recipe.ingredients:
        db_recipe.ingredients = recipe.ingredients

    if recipe.steps:
        db_steps = db_recipe.steps

        for i, step in enumerate(recipe.steps):
            if i < len(db_steps):
                db_step = db_steps[i]
                db_step.description = step.description
                db_step.time = step.time
            else:
                db_steps.append(Step(**step.dict(), recipe_id=db_recipe.id))

        if len(db_steps) > len(recipe.steps):
            db.session.delete(db_steps[len(recipe.steps) :])

        db_recipe.steps = db_steps

    db.commit()
    db.refresh(db_recipe)

    return db_recipe


async def delete_recipe(db: Session, recipe_id: int, current_user: User):
    db_recipe = await get_recipe(db, recipe_id)

    if db_recipe.owner != current_user:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this recipe"
        )

    db.delete(db_recipe)
    db.commit()


async def get_recipes_by_ingredients(
    db: Session, ingredients: List[str], skip: int = 0, limit: int = 100
) -> List[Recipe]:
    recipes = (
        db.query(Recipe)
        .filter(
            or_(
                *[
                    Recipe.ingredients.ilike(f"%{ingredient}%")
                    for ingredient in ingredients
                ]
            )
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
    return recipes


async def get_recipes_sorted_by_time(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Recipe]:
    recipes = (
        db.query(Recipe)
        .join(Step)
        .group_by(Recipe.id)
        .order_by(func.sum(Step.time).desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return recipes
