from fastapi import APIRouter, Depends, Query

from app.aplication.services.task_service import TaskService
from app.core.security import get_current_user
from app.schemas.task import TaskCreate, TaskRead

router = APIRouter()


@router.post("/", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    service: TaskService = Depends(TaskService),
    current_user=Depends(get_current_user),
):
    return service.create_task(task)


@router.get("/", response_model=list[TaskRead])
def list_tasks(
    status: bool | None = Query(None),
    priority: int | None = Query(None),
    service: TaskService = Depends(TaskService),
    current_user=Depends(get_current_user),
):
    return service.list_tasks(status=status, priority=priority)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task: TaskCreate,
    service: TaskService = Depends(TaskService),
    current_user=Depends(get_current_user),
):
    return service.update_task(task_id, task)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    service: TaskService = Depends(TaskService),
    current_user=Depends(get_current_user),
):
    return service.delete_task(task_id)


@router.patch("/{task_id}/toggle")
def toggle_task_completion(
    task_id: int,
    service: TaskService = Depends(TaskService),
    current_user=Depends(get_current_user),
):
    return service.toggle_task_status(task_id)
