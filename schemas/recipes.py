from typing import Dict, List, Optional

from pydantic import BaseModel


class StepBase(BaseModel):
    description: str
    time: int


class RecipeBase(BaseModel):
    name: str
    description: str
    ingredients: List[Dict[str, str | int]]
    steps: List[StepBase]


class RecipeCreateRequest(RecipeBase):
    pass


class RecipeUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[List[Dict[str, str | int]]] = None
    steps: Optional[List[StepBase]] = None


class StepResponse(StepBase):
    id: int

    class Config:
        orm_mode = True


class RecipeResponse(RecipeBase):
    id: int
    owner_id: int
    steps: List[StepResponse]

    class Config:
        orm_mode = True
