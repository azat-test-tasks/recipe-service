from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from db.base import Base
from models.users import User


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    ingredients = Column(JSONB)
    owner_id = Column(
        Integer,
        ForeignKey(User.id, ondelete="CASCADE"),
    )

    owner = relationship("User", back_populates="recipes")
    steps = relationship("Step", backref="recipe_steps")
    ratings = relationship("Rating", back_populates="recipe")
    images = relationship("Image", back_populates="recipe")


class Step(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    time = Column(Integer)

    recipe_id = Column(Integer, ForeignKey("recipes.id"))
