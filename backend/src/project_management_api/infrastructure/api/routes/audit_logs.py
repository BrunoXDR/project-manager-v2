import math
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from project_management_api.infrastructure.db.database import get_db
from project_management_api.infrastructure.api import security
from project_management_api.application import schemas
from project_management_api.domain.models import User
from project_management_api.infrastructure.repositories.audit_log_repository import AuditLogRepository
from project_management_api.infrastructure.api.dependencies import get_pagination_params

router = APIRouter(prefix="/api/admin/audit-logs", tags=["Admin: Audit Logs"])


@router.get("/", response_model=schemas.PaginatedResponse[schemas.AuditLogRead])
async def get_audit_logs(
    pagination: dict = Depends(get_pagination_params),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(security.get_current_admin_user)
):
    """
    Endpoint para consulta de logs de auditoria (apenas para administradores).
    
    Retorna uma lista paginada de todos os logs de auditoria do sistema,
    incluindo informações sobre o usuário que realizou a ação, a ação executada,
    detalhes contextuais e timestamp.
    """
    repo = AuditLogRepository(db)
    skip = (pagination["page"] - 1) * pagination["size"]
    
    items, total = await repo.get_all(skip=skip, limit=pagination["size"])
    
    return schemas.PaginatedResponse(
        total=total,
        page=pagination["page"],
        size=pagination["size"],
        pages=math.ceil(total / pagination["size"]) if total > 0 else 1,
        items=items
    )