from typing import List
from uuid import UUID
from schemas.task import TaskStatus
from services.exception import InvalidInputError, ResourceNotFoundError
from services.utils import get_current_utc_time
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from models.task import SearchTaskModel, TaskModel
from services import user as UserService
from schemas import Task

def get_tasks(db: Session, conds: SearchTaskModel) -> List[Task]:
    # Default of joinedload is LEFT OUTER JOIN
    query = select(Task).options(
        joinedload(Task.owner, innerjoin=True))
    
    if conds.summary is not None:
        query = query.filter(Task.title.like(f"{conds.summary}%"))
    if conds.owner_id is not None:
        query = query.filter(Task.author_id == conds.owner_id)
    
    query.offset((conds.page-1)*conds.size).limit(conds.size)
    
    return db.scalars(query).all()

def get_task_by_id(db: Session, id: UUID, /, joined_load = False) -> Task:
    query = select(Task).filter(Task.id == id)
    
    if joined_load:
        query.options(joinedload(Task.owner, innerjoin = True))
        
    return db.scalars(query).first()

def get_tasks_by_status(db: Session, status: TaskStatus, page, size) -> List[Task]:
    # Ensure the status is valid
    if not isinstance(status, TaskStatus):
        raise ValueError("Invalid status value.")
    
    # Calculate the offset for pagination
    offset = (page - 1) * size
        
    # Query tasks by status with pagination
    query = (
        select(Task)
        .filter(Task.status == status)
        .offset(offset)
        .limit(size)
    )
        
    return db.scalars(query).all()
    

def add_new_task(db: Session, data: TaskModel) -> Task:
    # Validate that the owner exists
    user = UserService.get_user_by_id(db, data.owner_id)
    if user is None:
        raise InvalidInputError("Invalid owner task information")
    
    # Validate required fields
    if not data.summary:
        raise InvalidInputError("Summary cannot be empty.")
    if not data.status:
        raise InvalidInputError("Status must be provided.")
    if not data.priority:
        raise InvalidInputError("Priority must be provided.")
    
    # Check for duplicate tasks (e.g., based on summary and owner_id)
    existing_task = db.query(Task).filter(Task.summary == data.summary, Task.owner_id == data.owner_id).first()
    if existing_task:
        raise InvalidInputError("A task with the same summary already exists for this user.")
    
    # Create the new task
    task = Task(**data.model_dump())
    task.created_at = get_current_utc_time()
    task.updated_at = get_current_utc_time()
    
    # Add the task to the session and commit
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task
    
def update_task(db: Session, id: UUID, data: TaskModel) -> Task:
    # Retrieve the existing task
    task = get_task_by_id(db, id)

    # Validate that the task exists
    if task is None:
        raise ResourceNotFoundError(f"Task with ID {id} not found.")

    if data.owner_id != task.owner_id:
        owner = UserService.get_user_by_id(db, data.owner_id)
        if owner is None:
            raise InvalidInputError("Invalid owner task information")
        
     # Validate required fields
    if not data.summary:
        raise InvalidInputError("Summary cannot be empty.")
    if not data.status:
        raise InvalidInputError("Status must be provided.")
    if not data.priority:
        raise InvalidInputError("Priority must be provided.")
    
    # Update only if the values are different
    if data.summary != task.summary:
        task.summary = data.summary
    if data.description != task.description:
        task.description = data.description
    if data.status != task.status:
        task.status = data.status
    if data.priority != task.priority:
        task.priority = data.priority
    if data.owner_id != task.owner_id:
        task.owner_id = data.owner_id
        
    # Update the timestamp
    task.updated_at = get_current_utc_time()
    
    # Commit the transaction
    db.commit()
    db.refresh(task)
    
    return task

def delete_task(db: Session, task_id: UUID) -> None:
    # Fetch the task from the database
    task = db.query(Task).filter(Task.id == task_id).first()
        
    # If the task does not exist, raise an error
    if task is None:
        raise ResourceNotFoundError(f"Task with ID {task_id} not found.")
        
    # Delete the task
    db.delete(task)
        
    # Commit the transaction to save changes
    db.commit()
    
    