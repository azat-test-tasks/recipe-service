from typing import List, Optional

from pydantic import BaseModel


class RecipeCreateRequest(BaseModel):
    name: str
    description: str
    ingredients: List[str]
    steps: List[str]

    class Config:
        orm_mode = True


class RecipeUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[List[str]] = None
    steps: Optional[List[str]] = None

    class Config:
        orm_mode = True


class RecipeResponse(BaseModel):
    id: int
    name: str
    description: str
    ingredients: List[str]
    steps: List[str]

    class Config:
        orm_mode = True
