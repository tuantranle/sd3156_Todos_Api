from typing import List
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from database import get_db_context
from models.user import UserModel
from schemas import User
from models import UserViewModel, UserBaseModel
from services.exception import AccessDeniedError
from services import auth as AuthService
from services import user as UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[UserBaseModel])
async def get_users(db: Session = Depends(get_db_context)) -> List[UserViewModel]:
    return db.query(User).filter(User.is_active == True).all()

@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserViewModel)
async def create_user(
    request: UserModel, 
        user: User = Depends(AuthService.token_interceptor),
        db: Session = Depends(get_db_context)
    ):
    
    if not user:
        raise AccessDeniedError()
        
    return UserService.add_new_user(db, request)