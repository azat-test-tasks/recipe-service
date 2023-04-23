from typing import List

from fastapi import APIRouter, Depends, status, Response, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from api import deps
from core.config import settings
from core.security import oauth2_scheme
from models import users as models
from schemas import users as schema
from schemas.auth import TokenData
from services import users as services

router = APIRouter()


@router.get("/me", response_model=schema.DisplayUser)
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(deps.get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        token_data = TokenData(email=email)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    return user


@router.get('/', response_model=List[schema.DisplayUser])
async def get_all_users(database: Session = Depends(deps.get_db),
                        current_user: schema.UserBase = Depends(get_current_user)):
    return await services.all_users(database)


@router.get('/{user_id}', response_model=schema.DisplayUser)
async def get_user_by_id(user_id: int, database: Session = Depends(deps.get_db),
                         current_user: schema.UserBase = Depends(get_current_user)):
    return await services.get_user_by_id(user_id, database)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_user_by_id(user_id: int, database: Session = Depends(deps.get_db),
                            current_user: schema.UserBase = Depends(get_current_user)):
    return await services.delete_user_by_id(user_id, database)
