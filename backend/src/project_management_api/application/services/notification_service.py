# application/services/notification_service.py
import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ...domain.models import Notification


async def create_notification(db: AsyncSession, user_id: uuid.UUID, message: str, link: Optional[str] = None):
    notification = Notification(user_id=user_id, message=message, link=link)
    db.add(notification)
    await db.commit()
    return notification  # Retorna o objeto para possíveis testes