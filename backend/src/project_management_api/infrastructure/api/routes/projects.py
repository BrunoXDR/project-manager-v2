import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from project_management_api.infrastructure.db.database import get_db
from project_management_api.application.schemas import ProjectRead, ProjectCreate, ProjectUpdate
from project_management_api.infrastructure.repositories.project_repository import ProjectRepository
from project_management_api.domain.models import User
from project_management_api.infrastructure.api import security
from project_management_api.application.services.project_workflow_service import ProjectWorkflowService, QualityGateNotPassedError
from project_management_api.infrastructure.repositories.document_repository import DocumentRepository
from project_management_api.application import schemas

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.get("/", response_model=List[ProjectRead])
async def get_all_projects(db: AsyncSession = Depends(get_db), current_user: User = Depends(security.get_current_user)):
    return await ProjectRepository(db).get_all()


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(security.get_current_user)):
    project = await ProjectRepository(db).get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(p: ProjectCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(security.get_current_user)):
    return await ProjectRepository(db).create(p)


@router.put("/{p_id}", response_model=ProjectRead)
async def update_project(p_id: uuid.UUID, p: ProjectUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(security.get_current_user)):
    proj = await ProjectRepository(db).update(p_id, p)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj


@router.delete("/{p_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(p_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(security.get_current_user)):
    deleted = await ProjectRepository(db).delete(p_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")


@router.post("/{project_id}/advance-phase", response_model=schemas.ProjectRead)
async def advance_project_phase(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    project_repo = ProjectRepository(db)
    doc_repo = DocumentRepository(db)
    
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Busca os documentos que serão usados na validação
    documents = await doc_repo.get_by_project(project_id)
    workflow_service = ProjectWorkflowService()

    try:
        # Chama o serviço completo, que agora pode lançar uma exceção
        updated_project = workflow_service.advance_phase(project, documents)
        
        # Se a validação passar, o serviço modifica o objeto. Agora, salvamos.
        return await project_repo.update(project_id, schemas.ProjectUpdate(phase=updated_project.phase))

    except QualityGateNotPassedError as e:
        # Se o Quality Gate falhar, retorna um erro 400 com os detalhes
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.args[0], "missing": e.missing_requirements}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))