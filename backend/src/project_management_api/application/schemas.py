import uuid
from datetime import date, datetime
from pydantic import BaseModel, computed_field
from typing import Optional
from project_management_api.domain.models import ProjectPhase, ProjectStatus, UserRole, TaskStatus, TaskPriority, DocumentStatus


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
    id: uuid.UUID
    project_id: uuid.UUID
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
    file_type: Optional[str] = None
    version: int = 1
    status: DocumentStatus = DocumentStatus.UPLOADED


class DocumentRead(DocumentBase):
    id: uuid.UUID
    project_id: uuid.UUID
    
    @computed_field
    @property
    def download_url(self) -> str:
        # O nome do arquivo salvo é o seu ID para evitar colisões e ofuscar nomes.
        # O NGINX servirá o arquivo a partir desta URL.
        file_id_str = str(self.id)
        return f"/uploads/{file_id_str}"
    
    class Config:
        from_attributes = True


class DocumentUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[DocumentStatus] = None
    # No futuro, poderemos adicionar outros campos como 'type' ou 'description'