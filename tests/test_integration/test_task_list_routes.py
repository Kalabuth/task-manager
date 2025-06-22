import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_create_get_update_delete_task_list():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(
            "/api/v1/auth/register",
            json={"email": "listuser@example.com", "password": "123456"},
        )
        login = await ac.post(
            "/api/v1/auth/login",
            data={"username": "listuser@example.com", "password": "123456"},
        )
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        create = await ac.post(
            "/api/v1/task-lists/", json={"name": "Project"}, headers=headers
        )
        assert create.status_code == status.HTTP_200_OK
        list_id = create.json()["id"]

        get_all = await ac.get("/api/v1/task-lists/", headers=headers)
        assert get_all.status_code == status.HTTP_200_OK

        update = await ac.put(
            f"/api/v1/task-lists/{list_id}",
            json={"name": "Updated Project"},
            headers=headers,
        )
        assert update.status_code == status.HTTP_200_OK
        assert update.json()["name"] == "Updated Project"

        delete = await ac.delete(f"/api/v1/task-lists/{list_id}", headers=headers)
        assert delete.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_get_tasks_by_list_with_filters():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Registro y login
        await ac.post(
            "/api/v1/auth/register",
            json={"email": "filteruser@example.com", "password": "123456"},
        )
        login = await ac.post(
            "/api/v1/auth/login",
            data={"username": "filteruser@example.com", "password": "123456"},
        )
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Crear una lista de tareas
        create_list = await ac.post(
            "/api/v1/task-lists/", json={"name": "Filter List"}, headers=headers
        )
        list_id = create_list.json()["id"]

        # Crear tareas con diferentes estados y prioridades
        await ac.post(
            "/api/v1/tasks/",
            json={
                "title": "Tarea 1",
                "task_list_id": list_id,
                "completed": False,
                "priority": 1,
            },
            headers=headers,
        )
        await ac.post(
            "/api/v1/tasks/",
            json={
                "title": "Tarea 2",
                "task_list_id": list_id,
                "completed": True,
                "priority": 2,
            },
            headers=headers,
        )
        await ac.post(
            "/api/v1/tasks/",
            json={
                "title": "Tarea 3",
                "task_list_id": list_id,
                "completed": True,
                "priority": 1,
            },
            headers=headers,
        )

        # Obtener todas las tareas sin filtros
        res = await ac.get(f"/api/v1/task-lists/{list_id}/tasks", headers=headers)
        assert res.status_code == 200
        data = res.json()
        assert len(data["tasks"]) == 3
        assert data["completion_percentage"] == pytest.approx(66.66, rel=1e-2)

        # Filtro por completed=true
        res_completed = await ac.get(
            f"/api/v1/task-lists/{list_id}/tasks?completed=true", headers=headers
        )
        assert res_completed.status_code == 200
        assert len(res_completed.json()["tasks"]) == 2

        # Filtro por priority=1
        res_priority = await ac.get(
            f"/api/v1/task-lists/{list_id}/tasks?priority=1", headers=headers
        )
        assert res_priority.status_code == 200
        assert len(res_priority.json()["tasks"]) == 2

        # Filtro combinado completed=true & priority=1
        res_combined = await ac.get(
            f"/api/v1/task-lists/{list_id}/tasks?completed=true&priority=1",
            headers=headers,
        )
        assert res_combined.status_code == 200
        assert len(res_combined.json()["tasks"]) == 1
