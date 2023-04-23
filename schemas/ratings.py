from typing import Optional

from pydantic import BaseModel, Field


class RatingBase(BaseModel):
    value: int = Field(..., ge=1, le=5)

    class Config:
        orm_mode = True


class RatingCreate(RatingBase):
    pass


class Rating(RatingBase):
    id: int
    recipe_id: int
    user_id: int

    class Config:
        orm_mode = True
