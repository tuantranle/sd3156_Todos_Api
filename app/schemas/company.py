import uuid, enum
from database import Base
from sqlalchemy import Column, String, Uuid, Enum, SmallInteger
from sqlalchemy.orm import relationship
from .base_entity import BaseEntity

class CompanyMode(enum.Enum):
    B2B = "B2B"
    B2C = "B2C"
    SAAS = "SaaS"

class Company(Base, BaseEntity):
    __tablename__ = "companies"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String)
    mode = Column(Enum(CompanyMode), nullable=False, default=CompanyMode.B2B)  
    rating = Column(SmallInteger, nullable=False, default=0)
    
    #users = relationship()"User", back_populates="company")
