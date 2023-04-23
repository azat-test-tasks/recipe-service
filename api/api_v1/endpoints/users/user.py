from typing import List

from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from api import deps
from core.security import get_current_user, verify_email_exist
from schemas import users as schema
from services import users as services

router = APIRouter()


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
