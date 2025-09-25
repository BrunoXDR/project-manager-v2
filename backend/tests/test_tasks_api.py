# backend/tests/test_tasks_api.py
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_create_and_read_task(authenticated_client: AsyncClient, create_test_project):
    project_id = await create_test_project()
    task_data = {
        "title": "Nova Tarefa de Teste",
        "description": "Descrição da tarefa.",
        "status": "todo",
        "priority": "high"
    }
    
    # Teste de Criação (POST)
    response = await authenticated_client.post(f"/api/projects/{project_id}/tasks/", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    assert created_task["title"] == task_data["title"]
    assert created_task["project_id"] == project_id

    # Teste de Leitura (GET All)
    response = await authenticated_client.get(f"/api/projects/{project_id}/tasks/")
    assert response.status_code == 200
    tasks_list = response.json()
    assert len(tasks_list) == 1
    assert tasks_list[0]["id"] == created_task["id"]

async def test_update_and_delete_task(authenticated_client: AsyncClient, create_test_project):
    project_id = await create_test_project()
    task_data = {"title": "Tarefa para Atualizar e Deletar"}
    response = await authenticated_client.post(f"/api/projects/{project_id}/tasks/", json=task_data)
    task_id = response.json()["id"]

    # Teste de Atualização (PUT)
    update_data = {"status": "done", "priority": "low"}
    response = await authenticated_client.put(f"/api/projects/{project_id}/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["status"] == "done"
    assert updated_task["priority"] == "low"

    # Teste de Exclusão (DELETE)
    response = await authenticated_client.delete(f"/api/projects/{project_id}/tasks/{task_id}")
    assert response.status_code == 204

    # Verificação da Exclusão
    response = await authenticated_client.get(f"/api/projects/{project_id}/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 0