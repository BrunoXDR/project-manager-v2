# src/project_management_api/infrastructure/api/security.py
import os
from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from project_management_api.application.schemas import TokenData
from project_management_api.domain.models import User, UserRole
from project_management_api.infrastructure.db.database import get_db
from project_management_api.infrastructure.repositories.user_repository import UserRepository

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "a_super_secret_key_for_dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = await UserRepository(db).get_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


# Role-based authorization
class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user does not have enough privileges for this action"
            )
        return current_user


# Criar instâncias específicas para os casos de uso mais comuns
allow_all_authenticated = RoleChecker([UserRole.ADMIN, UserRole.MANAGER, UserRole.MEMBER])
allow_managers_and_admins = RoleChecker([UserRole.ADMIN, UserRole.MANAGER])
allow_only_admins = RoleChecker([UserRole.ADMIN])


# Função para compatibilidade com código existente
async def get_current_admin_user(current_user: User = Depends(allow_only_admins)):
    return current_user