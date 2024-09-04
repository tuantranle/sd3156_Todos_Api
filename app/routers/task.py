from uuid import UUID
from fastapi import APIRouter, Response, status, Depends, Query
from typing import List
from database import get_db_context
from schemas.task import TaskStatus
from services.exception import AccessDeniedError
from sqlalchemy.orm import Session
from services import task as TaskService
from services import auth as AuthService
from models.task import TaskViewModel
from schemas import User
from models import TaskModel, TaskViewModel, SearchTaskModel
from services.exception import ResourceNotFoundError

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[TaskViewModel])
async def get_all_tasks(
        summary: str = Query(default=None),
        owner_id: UUID = Query(default=None),
        page: int = Query(ge=1,default=1),
        size: int = Query(ge=1, le=50, default=10),
        db: Session = Depends(get_db_context),
        user: User = Depends(AuthService.token_interceptor),
    ):
    if not user.is_admin:
        raise AccessDeniedError()
        
    conds = SearchTaskModel(summary, owner_id, page, size)
    return TaskService.get_tasks(db, conds)

@router.get("/{task_id}", response_model=TaskViewModel)
async def get_task_detail(task_id: UUID, db: Session=Depends(get_db_context)):
    task = TaskService.get_task_by_id(db, task_id, joined_load=True)
    
    if task is None:
        raise ResourceNotFoundError()

    return task

@router.get("/status/{status}", response_model=List[TaskViewModel])
async def get_tasks_by_status(
        status: TaskStatus,
        page: int = Query(ge=1, default=1),
        size: int = Query(ge=1, le=50, default=10),
        db: Session = Depends(get_db_context),
        user: User = Depends(AuthService.token_interceptor),
    ):
    if not user.is_admin:
        raise AccessDeniedError()

    tasks = TaskService.get_tasks_by_status(db, status, page, size)
    return tasks
    
@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskViewModel)
async def create_task(
    request: TaskModel, 
        user: User = Depends(AuthService.token_interceptor),
        db: Session = Depends(get_db_context),
    ):
    
    if not user:
        raise AccessDeniedError()
        
    request.owner_id = user.id

    return TaskService.add_new_task(db, request)



@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def update_task(
        task_id: UUID,
        request: TaskModel,
        db: Session=Depends(get_db_context),
    ):
    
    return TaskService.update_task(db, task_id, request)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: UUID,
        db: Session = Depends(get_db_context),
        user: User = Depends(AuthService.token_interceptor),
    ):
    if not user.is_admin:
        raise AccessDeniedError()

    task = TaskService.get_task_by_id(db, task_id)
    
    if task is None:
        raise ResourceNotFoundError()

    TaskService.delete_task(db, task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)