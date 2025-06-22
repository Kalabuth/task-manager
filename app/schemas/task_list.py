from pydantic import BaseModel, ConfigDict


class TaskListCreate(BaseModel):
    name: str


class TaskListRead(TaskListCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TaskListUpdate(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)
