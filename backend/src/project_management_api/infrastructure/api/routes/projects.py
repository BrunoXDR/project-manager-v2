import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from project_management_api.infrastructure.db.database import get_db
from project_management_api.application.schemas import ProjectRead, ProjectCreate, ProjectUpdate
from project_management_api.infrastructure.repositories.project_repository import ProjectRepository

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.get("/", response_model=List[ProjectRead])
async def get_all_projects(db: AsyncSession = Depends(get_db)):
    return await ProjectRepository(db).get_all()


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    project = await ProjectRepository(db).get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(p: ProjectCreate, db: AsyncSession = Depends(get_db)):
    return await ProjectRepository(db).create(p)


@router.put("/{p_id}", response_model=ProjectRead)
async def update_project(p_id: uuid.UUID, p: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    proj = await ProjectRepository(db).update(p_id, p)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj


@router.delete("/{p_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(p_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    deleted = await ProjectRepository(db).delete(p_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")