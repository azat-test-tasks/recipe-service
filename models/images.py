from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base
from schemas.images import ImageType


class Image(Base):
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    image_type = Column(Enum(ImageType))
    filename = Column(String)

    recipe = relationship("Recipe", back_populates="images")
