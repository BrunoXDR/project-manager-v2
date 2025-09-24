import uuid
from datetime import date
from pydantic import BaseModel
from typing import Optional
from project_management_api.domain.models import ProjectPhase, ProjectStatus, UserRole


class ProjectBase(BaseModel):
    name: str
    client: str
    startDate: date
    estimatedEndDate: date
    orderValue: Optional[str] = None
    proposal: Optional[str] = None
    pct: Optional[str] = None
    phase: ProjectPhase = ProjectPhase.INCEPTION
    status: ProjectStatus = ProjectStatus.ACTIVE


class ProjectRead(ProjectBase):
    id: uuid.UUID
    
    class Config:
        from_attributes = True


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    client: Optional[str] = None
    startDate: Optional[date] = None
    estimatedEndDate: Optional[date] = None
    orderValue: Optional[str] = None
    proposal: Optional[str] = None
    pct: Optional[str] = None
    phase: Optional[ProjectPhase] = None
    status: Optional[ProjectStatus] = None


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.MEMBER


class UserRead(UserBase):
    id: uuid.UUID
    role: UserRole
    
    class Config:
        from_attributes = True