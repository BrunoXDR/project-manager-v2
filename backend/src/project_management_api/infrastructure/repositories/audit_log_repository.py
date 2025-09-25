from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from project_management_api.domain.models import AuditLog


class AuditLogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, *, skip: int = 0, limit: int = 20) -> Tuple[List[AuditLog], int]:
        """
        Busca logs de auditoria com paginação, ordenados por timestamp decrescente.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            
        Returns:
            Tupla contendo (lista de logs, total de registros)
        """
        # Query para os itens paginados com join do usuário
        query = (
            select(AuditLog)
            .options(joinedload(AuditLog.user))
            .order_by(AuditLog.timestamp.desc())
        )
        
        # Query para a contagem total
        count_query = select(func.count()).select_from(AuditLog)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        paginated_query = query.offset(skip).limit(limit)
        items_result = await self.db.execute(paginated_query)
        items = items_result.scalars().all()
        
        return items, total