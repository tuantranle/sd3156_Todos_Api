from telnetlib import STATUS
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from models import UserBaseModel
from schemas import TaskPriority, TaskStatus


class SearchTaskModel():
    def __init__(self, summary, owner_id, page, size) -> None:
        self.summary = summary
        self.owner_id = owner_id
        self.page = page
        self.size = size

class TaskModel(BaseModel):
    summary: str
    description: Optional[str]
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    owner_id: Optional[UUID] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "Task 1",
                "description": "Description for Task 1",
                "status": TaskStatus.PENDING,
                "priority": TaskPriority.MEDIUM,
                "owner_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        }

class TaskViewModel(BaseModel):
    id: UUID
    summary: str
    description: str | None = None
    status: TaskStatus
    priority: TaskPriority
    owner_id: UUID | None = None
    owner: UserBaseModel | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        from_attributes = True
