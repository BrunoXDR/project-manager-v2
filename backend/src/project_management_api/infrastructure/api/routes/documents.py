import uuid
import shutil
import os
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from project_management_api.infrastructure.db.database import get_db
from project_management_api.application import schemas
from project_management_api.domain.models import User, Document
from project_management_api.infrastructure.api import security
from project_management_api.infrastructure.repositories.document_repository import DocumentRepository

router = APIRouter(prefix="/api/projects/{project_id}/documents", tags=["Documents"])
UPLOAD_DIR = "/app/uploads"


@router.post("/upload", response_model=schemas.DocumentRead, status_code=201)
async def upload_document(
    project_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(security.allow_all_authenticated)
):
    repo = DocumentRepository(db)
    doc_id = uuid.uuid4()
    file_location = f"{UPLOAD_DIR}/{doc_id}"
    
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    db_doc = Document(
        id=str(uuid.uuid4()),
        name=file.filename,
        file_path=file_location,
        file_type=file.content_type,
        project_id=project_id
    )
    return await repo.create(db_doc)


@router.get("/", response_model=List[schemas.DocumentRead])
async def get_documents(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(security.allow_all_authenticated)
):
    return await DocumentRepository(db).get_by_project(project_id)


@router.put("/{document_id}", response_model=schemas.DocumentRead)
async def update_document_metadata(
    project_id: str, document_id: str,
    doc_data: schemas.DocumentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.allow_managers_and_admins)
):
    repo = DocumentRepository(db)
    doc_to_update = await repo.get_by_id(document_id)
    if not doc_to_update or doc_to_update.project_id != project_id:
        raise HTTPException(status_code=404, detail="Document not found in this project")
    
    return await repo.update(document_id, doc_data)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    project_id: uuid.UUID, document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.allow_managers_and_admins)
):
    repo = DocumentRepository(db)
    doc_to_delete = await repo.get_by_id(document_id)
    if not doc_to_delete or doc_to_delete.project_id != project_id:
        raise HTTPException(status_code=404, detail="Document not found in this project")

    # Excluir o arquivo físico
    try:
        os.remove(doc_to_delete.file_path)
    except FileNotFoundError:
        # Se o arquivo não existir, prosseguimos para apagar o registro do DB mesmo assim
        pass
    except Exception as e:
        # Para outros erros de IO, pode ser prudente parar e logar
        raise HTTPException(status_code=500, detail=f"Error removing file: {e}")

    # Excluir o registro do banco de dados
    await repo.delete(doc_to_delete)