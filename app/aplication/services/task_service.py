from app.infrastructure.repositories.task_repo import TaskRepository
from app.schemas.task import TaskCreate


class TaskService:
    def __init__(self):
        self.repo = TaskRepository()

    def create_task(self, task: TaskCreate):
        return self.repo.create(task)

    def list_tasks(self, status=None, priority=None):
        return self.repo.list(status=status, priority=priority)

    def update_task(self, task_id: int, task: TaskCreate):
        return self.repo.update(task_id, task)

    def delete_task(self, task_id: int):
        return self.repo.delete(task_id)

    def toggle_task_status(self, task_id: int):
        return self.repo.toggle_status(task_id)
