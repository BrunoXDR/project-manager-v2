import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ...domain.models import AuditLog, User


async def create_audit_log(
    db: AsyncSession,
    action: str,
    user: Optional[User] = None,
    details: Optional[dict] = None
):
    """
    Cria um log de auditoria para registrar ações críticas do sistema.
    
    Args:
        db: Sessão do banco de dados
        action: Ação realizada (ex: "USER_LOGIN", "PROJECT_CREATED")
        user: Usuário que realizou a ação (opcional para eventos do sistema)
        details: Detalhes contextuais da ação em formato JSON
    """
    user_id = user.id if user else None
    log_entry = AuditLog(user_id=user_id, action=action, details=details)
    db.add(log_entry)
    await db.commit()
    return log_entry