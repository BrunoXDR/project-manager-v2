import asyncio
import sys
import os
sys.path.append('/home/toor/project-manager-v1/backend/src')

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from project_management_api.domain.models import User

async def check_users():
    engine = create_async_engine("sqlite+aiosqlite:///database.db")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        print(f"Total de usuários: {len(users)}")
        for user in users:
            print(f"ID: {user.id}, Email: {user.email}, Role: {user.role}")

if __name__ == "__main__":
    asyncio.run(check_users())
