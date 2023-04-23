from typing import List, Optional

from fastapi import HTTPException, status

from models.users import User
from schemas.users import UserCreate


async def new_user_register(request, database) -> UserCreate:
    new_user = User(name=request.name, email=request.email, password=request.password)
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user


async def all_users(database) -> List[User]:
    users = database.query(User).all()
    return users


async def get_user_by_id(user_id, database) -> Optional[User]:
    user_info = database.query(User).get(user_id)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Not Found !")
    return user_info


async def delete_user_by_id(user_id, database):
    database.query(User).filter(User.id == user_id).delete()
    database.commit()
