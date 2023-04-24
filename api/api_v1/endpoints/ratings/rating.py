from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from api import deps
from core.security import get_current_user
from models import ratings as models
from models.users import User
from schemas import ratings as schemas

router = APIRouter()


@router.post("/{recipe_id}/ratings", response_model=schemas.Rating)
def create_rating_for_recipe(
    recipe_id: int,
    rating: schemas.RatingCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(get_current_user),
):
    # Check if user already rated the recipe
    db_rating = (
        db.query(models.Rating)
        .filter(
            models.Rating.recipe_id == recipe_id,
            models.Rating.user_id == current_user.id,
        )
        .first()
    )

    if db_rating:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already rated this recipe",
        )

    # Create a new rating object
    db_rating = models.Rating(
        rating=rating.value,
        recipe_id=recipe_id,
        user_id=current_user.id,
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)

    return db_rating


@router.get("/{recipe_id}/ratings", response_model=List[schemas.Rating])
def get_ratings_for_recipe(
    recipe_id: int,
    db: Session = Depends(deps.get_db),
    limit: int = Query(20, gt=0, le=100),
    offset: int = Query(0, ge=0),
    sort_by: Optional[str] = Query(None, regex="^(id|value)$"),
    sort_desc: Optional[bool] = Query(True),
):
    query = db.query(models.Rating).filter(
        models.Rating.recipe_id == recipe_id,
    )

    if sort_by is not None:
        sort_column = getattr(models.Rating, sort_by)
        if sort_desc:
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(sort_column)

    ratings = query.offset(offset).limit(limit).all()
    return ratings
