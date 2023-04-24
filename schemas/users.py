from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    name: constr(min_length=2, max_length=50)
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class DisplayUser(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
