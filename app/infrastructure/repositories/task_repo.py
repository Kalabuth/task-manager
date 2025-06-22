from typing import Optional

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.infrastructure.models.task_model import TaskModel
from app.schemas.task import TaskCreate


class TaskRepository:
    def __init__(self, db: Session = SessionLocal()):
        self.db = db

    def create(self, task: TaskCreate):
        db_task = TaskModel(**task.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def list(self, status: Optional[bool] = None, priority: Optional[int] = None):
        query = self.db.query(TaskModel)
        if status is not None:
            query = query.filter(TaskModel.completed == status)
        if priority is not None:
            query = query.filter(TaskModel.priority == priority)
        return query.all()

    def update(self, task_id: int, task: TaskCreate):
        db_task = self.db.get(TaskModel, task_id)
        if db_task:
            for key, value in task.model_dump().items():
                setattr(db_task, key, value)
            self.db.commit()
            self.db.refresh(db_task)
        return db_task

    def delete(self, task_id: int):
        db_task = self.db.get(TaskModel, task_id)
        if db_task:
            self.db.delete(db_task)
            self.db.commit()
        return {"deleted": bool(db_task)}

    def toggle_status(self, task_id: int):
        db_task = self.db.get(TaskModel, task_id)
        if db_task:
            db_task.completed = not db_task.completed
            self.db.commit()
            self.db.refresh(db_task)
        return db_task
