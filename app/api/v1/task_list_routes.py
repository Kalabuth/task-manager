from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status

from app.aplication.services.task_list_service import TaskListService
from app.core.security import get_current_user
from app.schemas.task_list import TaskListCreate, TaskListRead, TaskListUpdate

router = APIRouter()


@router.post("/", response_model=TaskListRead)
def create_task_list(
    task_list: TaskListCreate,
    service: TaskListService = Depends(TaskListService),
    current_user=Depends(get_current_user),
):
    return service.create(task_list, current_user)


@router.get("/{list_id}/tasks")
def get_tasks_by_list(
    list_id: int,
    completed: Optional[bool] = Query(None),
    priority: Optional[int] = Query(None),
    service: TaskListService = Depends(TaskListService),
    current_user=Depends(get_current_user),
):
    return service.get_tasks_by_list(list_id, completed=completed, priority=priority)


@router.get("/", response_model=List[TaskListRead])
def get_task_lists(
    service: TaskListService = Depends(TaskListService),
    current_user=Depends(get_current_user),
):
    return service.get_all(current_user.id)


@router.put("/{list_id}", response_model=TaskListRead)
def update_task_list(
    list_id: int,
    task_list: TaskListUpdate,
    service: TaskListService = Depends(TaskListService),
    current_user=Depends(get_current_user),
):
    return service.update(list_id=list_id, task_list=task_list, user_id=current_user.id)


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_list(
    list_id: int,
    service: TaskListService = Depends(TaskListService),
    current_user=Depends(get_current_user),
):
    service.delete(list_id=list_id, user_id=current_user.id)
