import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.orm import selectinload
from project_management_api.domain.models import Task
from project_management_api.application.schemas import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_project(self, project_id: uuid.UUID) -> List[Task]:
        from sqlalchemy.orm import selectinload
        
        result = await self.db.execute(
            select(Task)
            .options(
                selectinload(Task.project),
                selectinload(Task.assigned_to)
            )
            .filter(Task.project_id == str(project_id))
        )
        return result.scalars().all()

    async def get_by_id(self, task_id: uuid.UUID) -> Optional[Task]:
        result = await self.db.execute(
            select(Task)
            .options(selectinload(Task.assigned_to))
            .filter(Task.id == task_id)
        )
        return result.scalars().first()

    async def create_for_project(self, project_id: uuid.UUID, task: TaskCreate) -> Task:
        db_task = Task(**task.model_dump(), project_id=project_id)
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        
        # Recarregar a tarefa com os relacionamentos
        return await self.get_by_id(db_task.id)

    async def update(self, task_id: uuid.UUID, task: TaskUpdate) -> Optional[Task]:
        update_data = task.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_by_id(task_id)
        
        q = sqlalchemy_update(Task).where(Task.id == task_id).values(update_data)
        await self.db.execute(q)
        await self.db.commit()
        
        # Recarregar a tarefa com os relacionamentos
        return await self.get_by_id(task_id)
        
    async def delete(self, task_id: uuid.UUID) -> bool:
        q = sqlalchemy_delete(Task).where(Task.id == task_id)
        res = await self.db.execute(q)
        await self.db.commit()
        return res.rowcount > 0