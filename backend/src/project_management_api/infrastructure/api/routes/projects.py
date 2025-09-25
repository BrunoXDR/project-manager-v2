import uuid
import math
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from project_management_api.infrastructure.db.database import get_db
from project_management_api.application.schemas import ProjectRead, ProjectCreate, ProjectUpdate
from project_management_api.infrastructure.repositories.project_repository import ProjectRepository
from project_management_api.domain.models import User, ProjectStatus
from project_management_api.infrastructure.api import security
from project_management_api.infrastructure.api.dependencies import get_pagination_params
from project_management_api.application.services.project_workflow_service import ProjectWorkflowService, QualityGateNotPassedError
from project_management_api.infrastructure.repositories.document_repository import DocumentRepository
from project_management_api.application import schemas
from project_management_api.application.services.notification_service import create_notification
from project_management_api.application.services import audit_service

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.get("/", response_model=schemas.PaginatedResponse[schemas.ProjectRead])
async def read_projects(
    pagination: dict = Depends(get_pagination_params),
    status: Optional[ProjectStatus] = Query(None, description="Filtrar por status do projeto"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    page = pagination["page"]
    size = pagination["size"]
    skip = (page - 1) * size

    repo = ProjectRepository(db)
    items, total = await repo.get_all(skip=skip, limit=size, status=status)
    
    return schemas.PaginatedResponse(
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if total > 0 else 1,
        items=items
    )


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(security.allow_all_authenticated)):
    project = await ProjectRepository(db).get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(p: ProjectCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(security.allow_managers_and_admins)):
    repo = ProjectRepository(db)
    new_project = await repo.create(p)
    
    # Registrar log de auditoria para criação de projeto
    await audit_service.create_audit_log(
        db, 
        user=current_user, 
        action="PROJECT_CREATED", 
        details={"project_id": str(new_project.id), "project_name": new_project.name}
    )
    
    return new_project


@router.put("/{p_id}", response_model=ProjectRead)
async def update_project(p_id: uuid.UUID, p: ProjectUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(security.allow_managers_and_admins)):
    # Buscar o projeto atual para comparar mudanças
    project_repo = ProjectRepository(db)
    current_project = await project_repo.get_by_id(p_id)
    if not current_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Atualizar o projeto
    proj = await project_repo.update(p_id, p)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Registrar log de auditoria para atualização de projeto
    await audit_service.create_audit_log(
        db, 
        user=current_user, 
        action="PROJECT_UPDATED", 
        details={"project_id": str(p_id), "project_name": proj.name}
    )
    
    # Verificar se houve mudança no Project Manager (GP)
    if p.project_manager_id and p.project_manager_id != current_project.project_manager_id:
        await create_notification(
            db=db,
            user_id=p.project_manager_id,
            message=f"Você foi designado como Gerente de Projeto (GP) do projeto '{proj.name}'",
            link=f"/projects/{proj.id}"
        )
    
    # Verificar se houve mudança no Technical Lead (LT)
    if p.technical_lead_id and p.technical_lead_id != current_project.technical_lead_id:
        await create_notification(
            db=db,
            user_id=p.technical_lead_id,
            message=f"Você foi designado como Líder Técnico (LT) do projeto '{proj.name}'",
            link=f"/projects/{proj.id}"
        )
    
    return proj


@router.delete("/{p_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(p_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(security.allow_only_admins)):
    project_repo = ProjectRepository(db)
    project = await project_repo.get_by_id(p_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Registrar log de auditoria antes de deletar o projeto
    await audit_service.create_audit_log(
        db, 
        user=current_user, 
        action="PROJECT_DELETED", 
        details={"project_id": str(p_id), "project_name": project.name}
    )
    
    deleted = await project_repo.delete(p_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")


@router.post("/{project_id}/advance-phase", response_model=schemas.ProjectRead)
async def advance_project_phase(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.allow_managers_and_admins)
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
        result = await project_repo.update(project_id, schemas.ProjectUpdate(phase=updated_project.phase))
        
        # Registrar log de auditoria para avanço de fase
        await audit_service.create_audit_log(
            db, 
            user=current_user, 
            action="PROJECT_PHASE_ADVANCED", 
            details={
                "project_id": str(project_id), 
                "project_name": project.name,
                "old_phase": project.phase.value,
                "new_phase": updated_project.phase.value
            }
        )
        
        return result

    except QualityGateNotPassedError as e:
        # Se o Quality Gate falhar, retorna um erro 400 com os detalhes
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.args[0], "missing": e.missing_requirements}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))