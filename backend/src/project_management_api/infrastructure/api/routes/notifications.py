import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from project_management_api.infrastructure.db.database import get_db
from project_management_api.application import schemas
from project_management_api.domain.models import User
from project_management_api.infrastructure.api import security
from project_management_api.infrastructure.repositories.notification_repository import NotificationRepository

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("/me", response_model=List[schemas.NotificationRead],
    summary="Minhas Notificações",
    description="Retorna todas as notificações não lidas do usuário autenticado. Requer autenticação de qualquer usuário válido."
)
async def get_my_notifications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    repo = NotificationRepository(db)
    return await repo.get_unread_for_user(user_id=current_user.id)


@router.post("/{notification_id}/mark-as-read", response_model=schemas.NotificationRead,
    summary="Marcar Notificação como Lida",
    description="Marca uma notificação específica como lida. Valida se a notificação pertence ao usuário autenticado. Requer autenticação de qualquer usuário válido."
)
async def mark_notification_as_read(
    notification_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    repo = NotificationRepository(db)
    notif = await repo.get_by_id(notification_id)
    if not notif or notif.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notif.is_read:
        return notif  # Já está lida, apenas retorna
    return await repo.mark_as_read(notif)