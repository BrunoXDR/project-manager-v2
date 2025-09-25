import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from project_management_api.domain.models import Document
from project_management_api.application.schemas import DocumentUpdate


class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, doc: Document) -> Document:
        self.db.add(doc)
        await self.db.commit()
        await self.db.refresh(doc)
        return doc
    
    async def get_by_project(self, project_id: uuid.UUID) -> List[Document]:
        from sqlalchemy.orm import selectinload
        
        result = await self.db.execute(
            select(Document)
            .options(selectinload(Document.project))
            .filter(Document.project_id == project_id)
        )
        return result.scalars().all()
    
    async def get_by_id(self, doc_id: uuid.UUID) -> Optional[Document]:
        res = await self.db.execute(select(Document).filter(Document.id == doc_id))
        return res.scalars().first()
    
    async def update(self, doc_id: uuid.UUID, doc_data: DocumentUpdate) -> Optional[Document]:
        update_data = doc_data.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_by_id(doc_id)
        
        q = sqlalchemy_update(Document).where(Document.id == doc_id).values(update_data).returning(Document)
        res = await self.db.execute(q)
        await self.db.commit()
        return res.scalars().first()
        
    async def delete(self, doc: Document) -> None:
        await self.db.delete(doc)
        await self.db.commit()