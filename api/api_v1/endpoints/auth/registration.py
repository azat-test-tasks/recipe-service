from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import deps
from core.security import verify_email_exist
from schemas.users import UserCreate, User
from services.users import new_user_register

router = APIRouter()


@router.post("/registration", response_model=User)
async def create_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = await verify_email_exist(user_in.email, db)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await new_user_register(user_in, db)
    return user
