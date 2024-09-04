from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

from schemas.company import CompanyMode

class CompanyModel(BaseModel):
    name: str = Field(min_length=2)

class CompanyViewModel(BaseModel):
    id: UUID 
    name: str
    created_at: datetime | None = None
    mode: CompanyMode = Field(default=CompanyMode.B2B)
    rating: int
    class Config:
        from_attributes = True
