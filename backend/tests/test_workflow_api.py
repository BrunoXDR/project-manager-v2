# backend/tests/test_workflow_api.py
import pytest
from httpx import AsyncClient
import io

# Importe o helper do conftest ou defina-o localmente
# from .conftest import create_test_project

pytestmark = pytest.mark.asyncio

# Reutilize o helper para criar projetos de teste
async def create_test_project(client: AsyncClient) -> dict:
    project_data = {
        "name": "Projeto de Teste Workflow",
        "client": "Cliente Teste",
        "startDate": "2025-01-01",
        "estimatedEndDate": "2025-12-31"
    }
    response = await client.post("/api/projects/", json=project_data)
    assert response.status_code == 201
    return response.json()

async def test_advance_phase_failure_due_to_quality_gate(authenticated_client: AsyncClient):
    """
    Testa se o Quality Gate bloqueia o avanço quando os requisitos não são atendidos.
    """
    project = await create_test_project(authenticated_client)
    project_id = project['id']
    
    # Avança de INCEPTION para DEFINITION (deve funcionar)
    response = await authenticated_client.post(f"/api/projects/{project_id}/advance-phase")
    assert response.status_code == 200
    assert response.json()["phase"] == "definition"

    # Tenta avançar de DEFINITION para BUILT (deve falhar, pois falta o BRD aprovado)
    response = await authenticated_client.post(f"/api/projects/{project_id}/advance-phase")
    assert response.status_code == 400
    error_details = response.json()["detail"]
    assert "Quality Gate para a fase 'definition' falhou." in error_details["message"]
    assert "Documento obrigatório: Tipo 'BRD' com status 'approved'." in error_details["missing"]

async def test_advance_phase_success_after_meeting_requirements(authenticated_client: AsyncClient, temp_upload_dir):
    """
    Testa se o avanço de fase funciona após os requisitos do Quality Gate serem atendidos.
    """
    project = await create_test_project(authenticated_client)
    project_id = project['id']
    await authenticated_client.post(f"/api/projects/{project_id}/advance-phase")  # -> Vai para DEFINITION

    # 1. Upload e configuração do documento para atender ao requisito
    files = {"file": ("brd.pdf", io.BytesIO(b"conteudo"), "application/pdf")}
    response = await authenticated_client.post(f"/api/projects/{project_id}/documents/upload", files=files)
    doc_id = response.json()["id"]
    update_data = {"type": "BRD", "status": "approved"}
    await authenticated_client.put(f"/api/projects/{project_id}/documents/{doc_id}", json=update_data)

    # 2. Tenta avançar a fase novamente (agora deve funcionar)
    response = await authenticated_client.post(f"/api/projects/{project_id}/advance-phase")
    assert response.status_code == 200
    assert response.json()["phase"] == "built"

async def test_advance_phase_triggers_task_creation(authenticated_client: AsyncClient):
    """
    Testa se o avanço de fase aciona a criação de tarefas a partir de um template.
    """
    # 1. Setup: Criar um template para a fase 'DEFINITION'
    template_data = {
        "name": "Template de Teste Workflow",
        "applies_to_phase": "definition",
        "items": [{"title": "Tarefa Automatica 1"}]
    }
    await authenticated_client.post("/api/admin/task-templates/", json=template_data)

    # 2. Execução: Criar um projeto e avançá-lo para a fase 'DEFINITION'
    project = await create_test_project(authenticated_client)
    project_id = project['id']
    response = await authenticated_client.post(f"/api/projects/{project_id}/advance-phase")
    assert response.status_code == 200
    assert response.json()["phase"] == "definition"

    # 3. Verificação: Checar se a tarefa foi criada
    response = await authenticated_client.get(f"/api/projects/{project_id}/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Tarefa Automatica 1"