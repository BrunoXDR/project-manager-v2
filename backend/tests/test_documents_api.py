# backend/tests/test_documents_api.py
import pytest
from httpx import AsyncClient
import io

pytestmark = pytest.mark.asyncio

async def test_upload_and_read_document(authenticated_client: AsyncClient, create_test_project, temp_upload_dir):
    """Teste de upload e leitura de documentos."""
    project_id = await create_test_project()

    # Simula um arquivo em memória
    file_content = b"Este eh um arquivo de teste."
    file_to_upload = io.BytesIO(file_content)

    # Teste de Upload (POST)
    files = {"file": ("test_document.txt", file_to_upload, "text/plain")}
    response = await authenticated_client.post(
        f"/api/projects/{project_id}/documents/upload", files=files
    )
    assert response.status_code == 201
    uploaded_doc = response.json()
    assert uploaded_doc["name"] == "test_document.txt"
    assert uploaded_doc["project_id"] == project_id

    # Teste de Leitura (GET All)
    response = await authenticated_client.get(f"/api/projects/{project_id}/documents/")
    assert response.status_code == 200
    docs_list = response.json()
    assert len(docs_list) == 1
    assert docs_list[0]["id"] == uploaded_doc["id"]
    assert docs_list[0]["download_url"] is not None

async def test_update_and_delete_document(authenticated_client: AsyncClient, create_test_project, temp_upload_dir):
    """Teste de atualização e exclusão de documentos."""
    project_id = await create_test_project()

    # Upload de um arquivo para manipular
    files = {"file": ("doc_to_update.txt", io.BytesIO(b"content"), "text/plain")}
    response = await authenticated_client.post(
        f"/api/projects/{project_id}/documents/upload", files=files
    )
    doc_id = response.json()["id"]

    # Teste de Atualização (PUT)
    update_data = {"name": "Nome do Arquivo Atualizado", "status": "approved"}
    response = await authenticated_client.put(
        f"/api/projects/{project_id}/documents/{doc_id}", json=update_data
    )
    assert response.status_code == 200
    updated_doc = response.json()
    assert updated_doc["name"] == "Nome do Arquivo Atualizado"
    assert updated_doc["status"] == "approved"

    # Teste de Exclusão (DELETE)
    response = await authenticated_client.delete(
        f"/api/projects/{project_id}/documents/{doc_id}"
    )
    assert response.status_code == 204

    # Verificação da Exclusão
    response = await authenticated_client.get(f"/api/projects/{project_id}/documents/")
    assert response.status_code == 200
    assert len(response.json()) == 0