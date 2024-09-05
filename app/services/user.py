from datetime import datetime
from uuid import UUID
import uuid

from fastapi import utils
from models import company, user
from schemas.user import User, get_password_hash
from sqlalchemy import false, select
from sqlalchemy.orm import Session

from services.exception import InvalidInputError
from services.utils import get_current_utc_time
from services import company as CompanyService

def get_user_by_id(db: Session, owner_id: UUID) -> User:
    return db.scalars(select(User).filter(User.id == owner_id)).first()

def add_new_user(db: Session, data: user.UserModel) -> User:
    # Check if a user with the same username already exists
    existing_user = db.query(User).filter(User.username == data.username).first()
    if existing_user:
        raise InvalidInputError("A user with this username already exists.")
    
    # Check existing company
    existing_company = CompanyService.get_company_by_id(db, data.company_id)
    if not existing_company:
        raise InvalidInputError("A company {company_id} does not exists.}")
        
    hashed_password = get_password_hash(data.password)
    
    new_user = User(
            id=uuid.uuid4(),
            username= data.username,
            first_name= data.first_name,
            last_name = data.last_name,
            email = data.email,
            hashed_password = hashed_password,
            is_active = True,
            is_admin = False,
            company_id = data.company_id,
            created_at = get_current_utc_time(),
            updated_at= get_current_utc_time()
        )

    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
