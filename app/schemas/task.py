import enum, uuid
from sqlalchemy import Column, ForeignKey, SmallInteger, String, Uuid, Enum
from sqlalchemy.orm import relationship
from database import Base
from .base_entity import BaseEntity

class TaskStatus(enum.Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"
    CANCELLED = "Cancelled"
    
class TaskPriority(enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class Task(BaseEntity, Base):
    __tablename__ = "tasks"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    summary = Column(String)
    description = Column(String)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING)  
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM)  
    owner_id = Column(Uuid, ForeignKey("users.id"), nullable=True)

    owner = relationship("User")
