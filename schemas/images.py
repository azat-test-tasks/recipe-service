from enum import Enum

from pydantic import BaseModel


class ImageType(str, Enum):
    recipe = "recipe"
    step = "step"


class ImageBase(BaseModel):
    recipe_id: int
    image_type: ImageType


class ImageCreate(ImageBase):
    filename: str


class Image(ImageBase):
    id: int
    filename: str

    class Config:
        orm_mode = True
