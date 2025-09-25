# backend/tests/test_projects_api.py
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_create_and_read_project(authenticated_client: AsyncClient):
    """Teste básico de criação e leitura de projeto."""
    project_data = {
        "name": "Projeto de Teste",
        "client": "Cliente de Teste",
        "startDate": "2025-01-01",
        "estimatedEndDate": "2025-12-31"
    }
    
    # Teste de Criação (POST)
    response = await authenticated_client.post("/api/projects/", json=project_data)
    assert response.status_code == 201
    created_project = response.json()
    assert created_project["name"] == project_data["name"]
    assert created_project["client"] == project_data["client"]

    # Teste de Leitura (GET All)
    response = await authenticated_client.get("/api/projects/")
    assert response.status_code == 200
    projects_list = response.json()
    assert len(projects_list) >= 1
    
    # Verificar se o projeto criado está na lista
    project_ids = [p["id"] for p in projects_list]
    assert created_project["id"] in project_ids

async def test_get_project_by_id(authenticated_client: AsyncClient):
    """Teste de busca de projeto por ID."""
    # Primeiro criar um projeto
    project_data = {
        "name": "Projeto para Busca",
        "client": "Cliente para Busca",
        "startDate": "2025-01-01",
        "estimatedEndDate": "2025-12-31"
    }
    
    response = await authenticated_client.post("/api/projects/", json=project_data)
    created_project = response.json()
    project_id = created_project["id"]
    
    # Buscar o projeto por ID
    response = await authenticated_client.get(f"/api/projects/{project_id}")
    assert response.status_code == 200
    retrieved_project = response.json()
    assert retrieved_project["id"] == project_id
    assert retrieved_project["name"] == project_data["name"]