# src/project_management_api/infrastructure/api/routes/analytics.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project_management_api.infrastructure.db.database import get_db
from project_management_api.application import schemas
from project_management_api.domain.models import User
from project_management_api.infrastructure.api import security
from project_management_api.infrastructure.repositories.project_repository import ProjectRepository

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/projects-by-status", response_model=List[schemas.AnalyticsStat])
async def get_projects_by_status(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    repo = ProjectRepository(db)
    stats_tuples = await repo.count_by_status()
    return [schemas.AnalyticsStat(category=status.value, count=count) for status, count in stats_tuples]

@router.get("/projects-by-phase", response_model=List[schemas.AnalyticsStat])
async def get_projects_by_phase(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    repo = ProjectRepository(db)
    stats_tuples = await repo.count_by_phase()
    return [schemas.AnalyticsStat(category=phase.value, count=count) for phase, count in stats_tuples]

@router.get("/projects-by-pm", response_model=List[schemas.AnalyticsStat])
async def get_projects_by_project_manager(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    repo = ProjectRepository(db)
    stats_tuples = await repo.count_by_project_manager()
    return [schemas.AnalyticsStat(category=email or "Unassigned", count=count) for email, count in stats_tuples]

@router.get("/projects-by-tl", response_model=List[schemas.AnalyticsStat])
async def get_projects_by_technical_lead(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    repo = ProjectRepository(db)
    stats_tuples = await repo.count_by_technical_lead()
    return [schemas.AnalyticsStat(category=email or "Unassigned", count=count) for email, count in stats_tuples]

@router.get("/projects-by-client", response_model=List[schemas.AnalyticsStat])
async def get_projects_by_client(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    repo = ProjectRepository(db)
    stats_tuples = await repo.count_by_client()
    return [schemas.AnalyticsStat(category=client, count=count) for client, count in stats_tuples]

@router.get("/overdue-projects", response_model=List[schemas.ProjectRead])
async def get_overdue_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    """
    Retorna uma lista de projetos em atraso.
    Um projeto é considerado em atraso se a data de término estimada passou
    e seu status ainda é 'ativo' ou 'em espera'.
    """
    repo = ProjectRepository(db)
    return await repo.get_overdue_projects()