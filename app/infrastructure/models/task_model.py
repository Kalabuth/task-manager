from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Integer, default=1)
    completed = Column(Boolean, default=False)
    task_list_id = Column(Integer, ForeignKey("task_lists.id"))
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    task_list = relationship("TaskListModel", back_populates="tasks")
    assigned_user = relationship("UserModel", back_populates="assigned_tasks")
