import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_invite_user():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/email/invite", json={"email": "invitee@gmail.com"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Invite sent to invitee@gmail.com"
