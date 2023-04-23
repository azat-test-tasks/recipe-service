from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user
from starlette.responses import FileResponse

from api import deps
from models import images as models
from models.recipes import Recipe
from schemas import images as schema

router = APIRouter()


@router.post("/{recipe_id}/image", response_model=schema.Image)
async def upload_recipe_image(
        recipe_id: int,
        image_type: schema.ImageType,
        image: UploadFile = File(...),
        db: Session = Depends(deps.get_db),
):
    # Check if recipe exists
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Check if user is allowed to update the recipe
    if not recipe.owner == current_user:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Check if image type is valid
    if not image_type in schema.ImageType:
        raise HTTPException(status_code=400, detail="Invalid image type")

    # Save the image to disk
    filename = f"{recipe_id}_{image_type.value}.jpg"
    with open(filename, "wb") as f:
        f.write(image.file.read())

    # Create a new image object
    db_image = models.Image(
        recipe_id=recipe_id,
        image_type=image_type,
        filename=filename,
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    return db_image


@router.get("/recipes/{recipe_id}/image", response_class=FileResponse)
async def get_recipe_image(
        recipe_id: int,
        image_type: schema.ImageType,
        db: Session = Depends(deps.get_db),
):
    # Check if recipe exists
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Check if image type is valid
    if not image_type in schema.ImageType:
        raise HTTPException(status_code=400, detail="Invalid image type")

    db_image = db.query(models.Image).filter(
        models.Image.recipe_id == recipe_id, models.Image.image_type == image_type
    ).first()
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(db_image.filename)
