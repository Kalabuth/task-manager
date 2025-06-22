from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.infrastructure.models.task_list_model import TaskListModel
from app.infrastructure.models.task_model import TaskModel
from app.schemas.task_list import TaskListCreate, TaskListUpdate


class TaskListRepository:
    def __init__(self, db: Session = SessionLocal()):
        self.db = db

    def create(self, task_list: TaskListCreate, user_id: int):
        db_list = TaskListModel(**task_list.model_dump(), owner_id=user_id)
        self.db.add(db_list)
        self.db.commit()
        self.db.refresh(db_list)
        return db_list

    def get_tasks_by_list(
        self, list_id: int, completed: bool = None, priority: int = None
    ):
        query = self.db.query(TaskModel).filter(TaskModel.task_list_id == list_id)

        if completed is not None:
            query = query.filter(TaskModel.completed == completed)
        if priority is not None:
            query = query.filter(TaskModel.priority == priority)

        tasks = query.all()
        total_all = (
            self.db.query(TaskModel).filter(TaskModel.task_list_id == list_id).count()
        )
        completed_all = (
            self.db.query(TaskModel)
            .filter(TaskModel.task_list_id == list_id, TaskModel.completed == True)
            .count()
        )
        percentage = (completed_all / total_all) * 100 if total_all else 0

        return {"tasks": tasks, "completion_percentage": percentage}

    def get_all_by_owner(self, user_id: int):
        return self.db.query(TaskListModel).filter_by(owner_id=user_id).all()

    def get_by_id_and_owner(self, list_id: int, user_id: int):
        return (
            self.db.query(TaskListModel).filter_by(id=list_id, owner_id=user_id).first()
        )

    def update(self, db_list: TaskListModel, task_list: TaskListUpdate):
        for key, value in task_list.model_dump().items():
            setattr(db_list, key, value)
        self.db.commit()
        self.db.refresh(db_list)
        return db_list

    def delete(self, db_list: TaskListModel):
        self.db.delete(db_list)
        self.db.commit()
