from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr

from app.aplication.services.email_service import send_invite_email

router = APIRouter()


class InviteRequest(BaseModel):
    email: EmailStr


@router.post("/invite", status_code=status.HTTP_200_OK)
def invite_user(request: InviteRequest):
    message = send_invite_email(request.email)
    return {"message": message}
