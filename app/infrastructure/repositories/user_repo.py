from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.infrastructure.models.user_model import UserModel
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, db: Session = SessionLocal()):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def create(self, user: UserCreate):
        db_user = UserModel(email=user.email, hashed_password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
