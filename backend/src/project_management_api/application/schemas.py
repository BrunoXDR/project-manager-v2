import uuid
from datetime import date, datetime
from pydantic import BaseModel, computed_field
from typing import Optional, Any
from project_management_api.domain.models import ProjectPhase, ProjectStatus, UserRole, TaskStatus, TaskPriority, DocumentStatus


# Schema for representing a user within a project context
class UserInProject(BaseModel):
    id: str
    email: str
    
    class Config:
        from_attributes = True


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
    project_manager_id: Optional[str] = None
    technical_lead_id: Optional[str] = None


class ProjectRead(ProjectBase):
    id: str
    project_manager: Optional[UserInProject] = None
    technical_lead: Optional[UserInProject] = None
    
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
    project_manager_id: Optional[str] = None
    technical_lead_id: Optional[str] = None


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


# Token schemas for JWT authentication
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# Task schemas for task management
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    dueDate: Optional[date] = None


class TaskRead(TaskBase):
    id: str
    project_id: str
    createdAt: datetime
    
    class Config:
        from_attributes = True


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    dueDate: Optional[date] = None


class DocumentBase(BaseModel):
    name: str
    type: Optional[str] = None  # Ex: "BRD", "LLD", "Proposta Técnica"
    file_type: Optional[str] = None
    version: int = 1
    status: DocumentStatus = DocumentStatus.UPLOADED


class DocumentRead(DocumentBase):
    id: str
    project_id: str
    uploadedAt: datetime
    
    class Config:
        from_attributes = True


class DocumentUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None  # Ex: "BRD", "LLD", "Proposta Técnica"
    status: Optional[DocumentStatus] = None
    # No futuro, poderemos adicionar outros campos como 'description'


# Analytics schemas for dashboard metrics
class AnalyticsStat(BaseModel):
    category: Any
    count: int