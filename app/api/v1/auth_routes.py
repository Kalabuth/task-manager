from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import (create_access_token, get_password_hash,
                               verify_password)
from app.infrastructure.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate

router = APIRouter()


@router.post("/register")
def register(user: UserCreate):
    repo = UserRepository()
    existing = repo.get_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = get_password_hash(user.password)
    return repo.create(user)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    repo = UserRepository()
    user = repo.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
