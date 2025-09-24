from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from project_management_api.infrastructure.db.database import get_db
from project_management_api.infrastructure.api import security
from project_management_api.application import schemas
from project_management_api.domain.models import User
from project_management_api.infrastructure.repositories.user_repository import UserRepository

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    db_user = await repo.get_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = security.get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user