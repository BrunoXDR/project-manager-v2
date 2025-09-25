# infrastructure/repositories/notification_repository.py
import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ...domain.models import Notification


class NotificationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_unread_for_user(self, user_id: uuid.UUID) -> List[Notification]:
        q = select(Notification).filter_by(user_id=user_id, is_read=False).order_by(Notification.created_at.desc())
        res = await self.db.execute(q)
        return res.scalars().all()

    async def get_by_id(self, notif_id: uuid.UUID) -> Optional[Notification]:
        return await self.db.get(Notification, notif_id)

    async def mark_as_read(self, notification: Notification) -> Notification:
        notification.is_read = True
        await self.db.commit()
        await self.db.refresh(notification)
        return notification