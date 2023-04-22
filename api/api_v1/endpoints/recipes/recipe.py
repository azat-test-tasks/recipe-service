from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import deps
from schemas import recipes as schemas
from services import recipes as services

router = APIRouter()


@router.post("/", response_model=schemas.RecipeResponse)
async def create_recipe(recipe: schemas.RecipeCreateRequest, db: Session = Depends(deps.get_db)):
    return await services.create_recipe(db=db, recipe=recipe)


@router.get("/", response_model=List[schemas.RecipeResponse])
async def read_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    recipes = await services.get_all_recipes(db, skip=skip, limit=limit)
    return recipes


@router.get("/{recipe_id}", response_model=schemas.RecipeResponse)
async def read_recipe(recipe_id: int, db: Session = Depends(deps.get_db)):
    recipe = await services.get_recipe_by_id(db, recipe_id=recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.put("/{recipe_id}", response_model=schemas.RecipeResponse)
async def update_recipe(recipe_id: int, recipe: schemas.RecipeUpdateRequest, db: Session = Depends(deps.get_db)):
    updated_recipe = await services.update_recipe(db, recipe_id=recipe_id, recipe=recipe)
    if updated_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated_recipe


@router.delete("/{recipe_id}", response_model=schemas.RecipeResponse)
async def delete_recipe(recipe_id: int, db: Session = Depends(deps.get_db)):
    deleted_recipe = await services.delete_recipe(db, recipe_id=recipe_id)
    if deleted_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return deleted_recipe
