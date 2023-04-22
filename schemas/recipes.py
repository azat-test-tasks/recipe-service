from typing import List, Optional, Dict

from pydantic import BaseModel


class RecipeCreateRequest(BaseModel):
    name: str
    description: str
    ingredients: List[Dict[str, str | int]]
    steps: List[Dict[str, str | int]]

    class Config:
        orm_mode = True


class RecipeUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[List[Dict[str, str | int]]] = None
    steps: Optional[List[Dict[str, str | int]]] = None

    class Config:
        orm_mode = True


class RecipeResponse(BaseModel):
    id: int
    name: str
    description: str
    ingredients: List[Dict[str, str | int]]
    steps: List[Dict[str, str | int]]

    class Config:
        orm_mode = True
