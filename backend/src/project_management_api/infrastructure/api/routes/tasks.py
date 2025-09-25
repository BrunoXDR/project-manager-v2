import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from project_management_api.infrastructure.db.database import get_db
from project_management_api.application import schemas
from project_management_api.domain.models import User
from project_management_api.infrastructure.api import security
from project_management_api.infrastructure.repositories.task_repository import TaskRepository
from project_management_api.application.services.notification_service import create_notification

router = APIRouter(prefix="/api/projects/{project_id}/tasks", tags=["Tasks"])


@router.get("/", response_model=List[schemas.TaskRead],
    summary="Lista Tarefas do Projeto",
    description="Retorna todas as tarefas associadas a um projeto específico. Requer autenticação de qualquer usuário válido."
)
async def get_tasks_for_project(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.allow_all_authenticated)
):
    return await TaskRepository(db).get_by_project(project_id)


@router.get("/{task_id}", response_model=schemas.TaskRead,
    summary="Busca Tarefa por ID",
    description="Retorna os detalhes de uma tarefa específica dentro de um projeto. Valida se a tarefa pertence ao projeto informado. Requer autenticação de qualquer usuário válido."
)
async def get_task(
    project_id: uuid.UUID,
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.allow_all_authenticated)
):
    task = await TaskRepository(db).get_by_id(task_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found in this project")
    return task


@router.post("/", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED,
    summary="Cria Nova Tarefa",
    description="Cria uma nova tarefa dentro de um projeto específico. Envia notificação automática se um usuário for atribuído à tarefa. Requer autenticação de qualquer usuário válido."
)
async def create_task(
    project_id: uuid.UUID,
    task: schemas.TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.allow_all_authenticated)
):
    created_task = await TaskRepository(db).create_for_project(project_id, task)
    
    # Criar notificação se um usuário foi atribuído à tarefa
    if task.assigned_to_id:
        await create_notification(
            db=db,
            user_id=task.assigned_to_id,
            message=f"Você foi atribuído à tarefa '{created_task.title}'",
            link=f"/projects/{project_id}/tasks/{created_task.id}"
        )
    
    return created_task


@router.put("/{task_id}", response_model=schemas.TaskRead,
    summary="Atualiza Tarefa Existente",
    description="Atualiza os dados de uma tarefa existente dentro de um projeto. Envia notificação automática se houver mudança na atribuição de usuário. Requer autenticação de qualquer usuário válido."
)
async def update_task(
    project_id: uuid.UUID,
    task_id: uuid.UUID,
    task: schemas.TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.allow_all_authenticated)
):
    repo = TaskRepository(db)
    # Validação extra para garantir que a tarefa pertence ao projeto
    task_to_update = await repo.get_by_id(task_id)
    if not task_to_update or task_to_update.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found in this project")
    
    # Salvar o assigned_to_id original antes da atualização
    original_assigned_to_id = task_to_update.assigned_to_id
    
    updated_task = await repo.update(task_id, task)
    
    # Criar notificação se houve mudança na atribuição de usuário
    if task.assigned_to_id and task.assigned_to_id != original_assigned_to_id:
        await create_notification(
            db=db,
            user_id=task.assigned_to_id,
            message=f"Você foi atribuído à tarefa '{updated_task.title}'",
            link=f"/projects/{project_id}/tasks/{updated_task.id}"
        )
    
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT,
    summary="Exclui uma Tarefa",
    description="Remove permanentemente uma tarefa de um projeto. Valida se a tarefa pertence ao projeto informado. Requer permissão de MANAGER ou ADMIN."
)
async def delete_task(
    project_id: uuid.UUID,
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.allow_managers_and_admins)
):
    repo = TaskRepository(db)
    # Validação extra
    task_to_delete = await repo.get_by_id(task_id)
    if not task_to_delete or task_to_delete.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found in this project")

    await repo.delete(task_id)