import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from project_management_api.domain.models import Project
from project_management_api.application.schemas import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[Project]:
        result = await self.db.execute(select(Project))
        return result.scalars().all()

    async def get_by_id(self, project_id: uuid.UUID) -> Optional[Project]:
        result = await self.db.execute(select(Project).filter(Project.id == project_id))
        return result.scalars().first()

    async def create(self, p_data: ProjectCreate) -> Project:
        p = Project(**p_data.model_dump())
        self.db.add(p)
        await self.db.commit()
        await self.db.refresh(p)
        return p

    async def update(self, p_id: uuid.UUID, p_data: ProjectUpdate) -> Optional[Project]:
        update_data = p_data.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_by_id(p_id)
        
        q = sqlalchemy_update(Project).where(Project.id == p_id).values(update_data).returning(Project)
        res = await self.db.execute(q)
        await self.db.commit()
        return res.scalars().first()

    async def delete(self, p_id: uuid.UUID) -> bool:
        q = sqlalchemy_delete(Project).where(Project.id == p_id)
        res = await self.db.execute(q)
        await self.db.commit()
        return res.rowcount > 0