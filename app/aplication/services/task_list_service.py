from fastapi import HTTPException

from app.infrastructure.repositories.task_list_repo import TaskListRepository
from app.schemas.task_list import TaskListCreate, TaskListUpdate


class TaskListService:
    def __init__(self):
        self.repo = TaskListRepository()

    def create(self, task_list: TaskListCreate, user):
        return self.repo.create(task_list, user_id=user.id)

    def get_tasks_by_list(
        self, list_id: int, completed: bool = None, priority: int = None
    ):
        return self.repo.get_tasks_by_list(list_id, completed, priority)

    def get_all(self, user_id: int):
        return self.repo.get_all_by_owner(user_id)

    def update(self, list_id: int, task_list: TaskListUpdate, user_id: int):
        db_list = self.repo.get_by_id_and_owner(list_id, user_id)
        if not db_list:
            raise HTTPException(status_code=404, detail="Task list not found")

        updated = self.repo.update(db_list, task_list)
        return updated

    def delete(self, list_id: int, user_id: int):
        db_list = self.repo.get_by_id_and_owner(list_id, user_id)
        if not db_list:
            raise HTTPException(status_code=404, detail="Task list not found")
        self.repo.delete(db_list)
