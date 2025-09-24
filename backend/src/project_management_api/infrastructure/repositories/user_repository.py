from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from project_management_api.domain.models import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_email(self, email: str):
        res = await self.db.execute(select(User).filter(User.email == email))
        return res.scalars().first()