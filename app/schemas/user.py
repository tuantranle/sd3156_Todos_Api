import uuid
from sqlalchemy import Boolean, Column, String, Uuid
from database import Base
from .base_entity import BaseEntity
from passlib.context import CryptContext
from sqlalchemy.orm import relationship

bcrypt_context = CryptContext(schemes=["bcrypt"])

class User(BaseEntity, Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    tasks = relationship("Task", back_populates="owner")


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hased_password):
    return bcrypt_context.verify(plain_password, hased_password)
