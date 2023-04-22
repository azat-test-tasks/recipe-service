from sqlalchemy import Column, Integer, String, ARRAY

from db.base import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    ingredients = Column(ARRAY(String))
    steps = Column(ARRAY(String))
