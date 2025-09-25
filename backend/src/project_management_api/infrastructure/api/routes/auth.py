from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from project_management_api.infrastructure.api import security
from project_management_api.application import schemas
from project_management_api.infrastructure.db.database import get_db
from project_management_api.infrastructure.repositories.user_repository import UserRepository
from project_management_api.application.services import audit_service

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/token", response_model=schemas.Token,
    summary="Autenticação de Usuário",
    description="Realiza login do usuário no sistema usando email e senha. Retorna um token JWT para autenticação em endpoints protegidos. Registra automaticamente um log de auditoria do login."
)
async def login_for_access_token(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    repo = UserRepository(db)
    user = await repo.get_by_email(email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Registrar log de auditoria para login bem-sucedido
    await audit_service.create_audit_log(
        db, 
        user=user, 
        action="USER_LOGIN", 
        details={"email": user.email, "user_id": str(user.id)}
    )
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}