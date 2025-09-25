import uuid
from typing import List, Optional, Tuple
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func
from project_management_api.domain.models import Project, ProjectStatus
from project_management_api.application.schemas import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, *, skip: int = 0, limit: int = 20, status: Optional[ProjectStatus] = None) -> Tuple[List[Project], int]:
        # Query para os itens paginados e filtrados
        query = select(Project).order_by(Project.createdAt.desc())
        if status:
            query = query.filter(Project.status == status)
        
        # Query para a contagem total (com os mesmos filtros)
        count_query = select(func.count()).select_from(Project)
        if status:
            count_query = count_query.filter(Project.status == status)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        paginated_query = query.offset(skip).limit(limit)
        items_result = await self.db.execute(paginated_query)
        items = items_result.scalars().all()
        
        return items, total

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

    async def count_by_status(self) -> List[Tuple[str, int]]:
        query = select(Project.status, func.count(Project.id)).group_by(Project.status)
        result = await self.db.execute(query)
        return result.all()

    async def count_by_phase(self) -> List[Tuple[str, int]]:
        query = select(Project.phase, func.count(Project.id)).group_by(Project.phase)
        result = await self.db.execute(query)
        return result.all()

    async def count_by_project_manager(self) -> List[Tuple[str, int]]:
        from project_management_api.domain.models import User
        query = select(User.email, func.count(Project.id)).join(
            User, Project.project_manager_id == User.id, isouter=True
        ).group_by(User.email)
        result = await self.db.execute(query)
        return result.all()

    async def count_by_technical_lead(self) -> List[Tuple[str, int]]:
        from project_management_api.domain.models import User
        query = select(User.email, func.count(Project.id)).join(
            User, Project.technical_lead_id == User.id, isouter=True
        ).group_by(User.email)
        result = await self.db.execute(query)
        return result.all()

    async def count_by_client(self) -> List[Tuple[str, int]]:
        query = select(Project.client, func.count(Project.id)).group_by(Project.client)
        result = await self.db.execute(query)
        return result.all()

    async def get_overdue_projects(self) -> List[Project]:
        """
        Retorna projetos cuja data estimada de término já passou e que não estão
        em um estado final (concluído ou cancelado).
        """
        today = date.today()
        query = (
            select(Project)
            .filter(
                Project.estimatedEndDate < today,
                Project.status.in_([ProjectStatus.ACTIVE, ProjectStatus.HOLD])
            )
        )
        result = await self.db.execute(query)
        return result.scalars().all()