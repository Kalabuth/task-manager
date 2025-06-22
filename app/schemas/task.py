from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
    priority: int = 1
    task_list_id: int
    assigned_user_id: Optional[int] = None


class TaskRead(TaskCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
