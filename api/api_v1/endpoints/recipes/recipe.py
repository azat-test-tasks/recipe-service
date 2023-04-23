from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import deps
from core.security import get_current_user
from models.recipes import Recipe
from schemas import recipes as schemas
from schemas.users import User
from services import recipes as services

router = APIRouter()


@router.post("/", response_model=schemas.RecipeResponse)
async def create_recipe(recipe: schemas.RecipeCreateRequest,
                        db: Session = Depends(deps.get_db), current_user: User = Depends(get_current_user),):
    return await services.create_recipe(db, recipe, current_user)


@router.get("/", response_model=List[schemas.RecipeResponse])
async def read_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    recipes = await services.get_all_recipes(db, skip=skip, limit=limit)
    return recipes


@router.get("/{recipe_id}", response_model=schemas.RecipeResponse)
async def read_recipe(recipe_id: int, db: Session = Depends(deps.get_db)):
    recipe = await services.get_recipe(db, recipe_id=recipe_id)
    return recipe


@router.put("/{recipe_id}", response_model=schemas.RecipeResponse)
async def update_recipe(recipe_id: int, recipe: schemas.RecipeUpdateRequest,
                        db: Session = Depends(deps.get_db), current_user: User = Depends(get_current_user)):
    updated_recipe = await services.update_recipe(db, recipe_id, recipe, current_user)
    return updated_recipe


@router.delete("/{recipe_id}", response_model=schemas.RecipeResponse)
async def delete_recipe(recipe_id: int, db: Session = Depends(deps.get_db),
                        current_user: User = Depends(get_current_user)):
    deleted_recipe = await services.delete_recipe(db, recipe_id, current_user)
    return deleted_recipe


@router.get("/search", response_model=List[schemas.RecipeResponse])
async def search_recipes(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        ingredients: List[str] = None,
        sort_by_time: bool = False,
) -> List[schemas.RecipeResponse]:
    if ingredients:
        recipes = await services.get_recipes_by_ingredients(db, ingredients, skip=skip, limit=limit)
    elif sort_by_time:
        recipes = await services.get_recipes_sorted_by_time(db, skip=skip, limit=limit)
    else:
        recipes = db.query(Recipe).offset(skip).limit(limit).all()
    return recipes
