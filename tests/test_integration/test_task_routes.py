import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_create_task():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com", "password": "123456"},
        )
        login = await ac.post(
            "/api/v1/auth/login",
            data={"username": "test@example.com", "password": "123456"},
        )
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        task_list = await ac.post(
            "/api/v1/task-lists/", json={"name": "My List"}, headers=headers
        )
        list_id = task_list.json()["id"]

        response = await ac.post(
            "/api/v1/tasks/",
            json={
                "title": "Test Task",
                "description": "Do something",
                "priority": 2,
                "task_list_id": list_id,
            },
            headers=headers,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "Test Task"


@pytest.mark.asyncio
async def test_get_tasks():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        login = await ac.post(
            "/api/v1/auth/login",
            data={"username": "test@example.com", "password": "123456"},
        )
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await ac.get("/api/v1/tasks/", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_toggle_task_status():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        login = await ac.post(
            "/api/v1/auth/login",
            data={"username": "test@example.com", "password": "123456"},
        )
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        tasks = await ac.get("/api/v1/tasks/", headers=headers)
        task_id = tasks.json()[0]["id"]

        toggle = await ac.patch(f"/api/v1/tasks/{task_id}/toggle", headers=headers)
        assert toggle.status_code == status.HTTP_200_OK
        assert isinstance(toggle.json()["completed"], bool)


@pytest.mark.asyncio
async def test_user_me():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        login = await ac.post(
            "/api/v1/auth/login",
            data={"username": "test@example.com", "password": "123456"},
        )
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await ac.get("/api/v1/users/me", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_assign_user_to_task():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(
            "/api/v1/auth/register",
            json={"email": "assigner@example.com", "password": "123456"},
        )
        await ac.post(
            "/api/v1/auth/register",
            json={"email": "assignee@example.com", "password": "123456"},
        )

        login = await ac.post(
            "/api/v1/auth/login",
            data={"username": "assigner@example.com", "password": "123456"},
        )
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        me_resp = await ac.get("/api/v1/users/me", headers=headers)
        assignee_id = me_resp.json()["id"]

        task_list = await ac.post(
            "/api/v1/task-lists/", json={"name": "AssignedTasks"}, headers=headers
        )
        list_id = task_list.json()["id"]

        task = await ac.post(
            "/api/v1/tasks/",
            json={
                "title": "Review PR",
                "description": "Code review",
                "priority": 1,
                "task_list_id": list_id,
                "assigned_user_id": assignee_id,
            },
            headers=headers,
        )
        assert task.status_code == status.HTTP_200_OK
        assert task.json()["assigned_user_id"] == assignee_id
