from uuid import UUID
from models import user
from schemas.user import User
from sqlalchemy import select
from sqlalchemy.orm import Session

def get_user_by_id(db: Session, owner_id: UUID) -> User:
    return db.scalars(select(User).filter(User.id == owner_id)).first()