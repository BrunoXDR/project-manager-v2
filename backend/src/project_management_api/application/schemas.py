import uuid
from datetime import date, datetime
from pydantic import BaseModel, computed_field, Field
from typing import Optional, Any, Generic, TypeVar, List
from project_management_api.domain.models import ProjectPhase, ProjectStatus, UserRole, TaskStatus, TaskPriority, DocumentStatus

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    total: int = Field(..., description="Número total de itens disponíveis na consulta", example=150)
    page: int = Field(..., gt=0, description="Número da página atual (baseado em 1)", example=2)
    size: int = Field(..., gt=0, description="Número de itens por página", example=20)
    pages: int = Field(..., description="Número total de páginas disponíveis", example=8)
    items: List[T] = Field(..., description="Lista de itens para a página atual")


# Schema for representing a user within a project context
class UserInProject(BaseModel):
    id: str = Field(..., description="Identificador único do usuário", example="550e8400-e29b-41d4-a716-446655440000")
    email: str = Field(..., description="Endereço de email do usuário", example="joao.silva@empresa.com")
    
    class Config:
        from_attributes = True


# Schema for representing a user within a task context
class UserInTask(BaseModel):
    id: uuid.UUID = Field(..., description="Identificador único do usuário", example="550e8400-e29b-41d4-a716-446655440000")
    email: str = Field(..., description="Endereço de email do usuário", example="maria.santos@empresa.com")
    
    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str = Field(..., description="Nome descritivo do projeto", example="Implementação Microsoft 365")
    client: str = Field(..., description="Nome do cliente para o qual o projeto é executado", example="Empresa ABC Ltda")
    startDate: date = Field(..., description="Data de início do projeto", example="2025-01-15")
    estimatedEndDate: date = Field(..., description="Data estimada para conclusão do projeto", example="2025-06-30")
    orderValue: Optional[str] = Field(None, description="Valor do contrato/ordem de serviço", example="R$ 150.000,00")
    proposal: Optional[str] = Field(None, description="Número ou referência da proposta comercial", example="PROP-2024-001")
    pct: Optional[str] = Field(None, description="Número do PCT (Plano de Controle de Trabalho)", example="PCT-2024-MS365-001")
    phase: ProjectPhase = Field(ProjectPhase.INCEPTION, description="Fase atual do projeto no ciclo de vida", example="INCEPTION")
    status: ProjectStatus = Field(ProjectStatus.ACTIVE, description="Status operacional do projeto", example="ACTIVE")
    project_manager_id: Optional[str] = Field(None, description="ID do gerente de projeto responsável", example="550e8400-e29b-41d4-a716-446655440001")
    technical_lead_id: Optional[str] = Field(None, description="ID do líder técnico do projeto", example="550e8400-e29b-41d4-a716-446655440002")


class ProjectRead(ProjectBase):
    id: str = Field(..., description="Identificador único do projeto", example="550e8400-e29b-41d4-a716-446655440003")
    project_manager: Optional[UserInProject] = Field(None, description="Dados do gerente de projeto")
    technical_lead: Optional[UserInProject] = Field(None, description="Dados do líder técnico")
    
    class Config:
        from_attributes = True


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Novo nome do projeto", example="Implementação Microsoft 365 - Fase 2")
    client: Optional[str] = Field(None, description="Novo nome do cliente", example="Empresa XYZ Ltda")
    startDate: Optional[date] = Field(None, description="Nova data de início", example="2025-02-01")
    estimatedEndDate: Optional[date] = Field(None, description="Nova data estimada de conclusão", example="2025-08-31")
    orderValue: Optional[str] = Field(None, description="Novo valor do contrato", example="R$ 200.000,00")
    proposal: Optional[str] = Field(None, description="Nova referência da proposta", example="PROP-2024-002")
    pct: Optional[str] = Field(None, description="Novo número do PCT", example="PCT-2024-MS365-002")
    phase: Optional[ProjectPhase] = Field(None, description="Nova fase do projeto", example="ELABORATION")
    status: Optional[ProjectStatus] = Field(None, description="Novo status do projeto", example="HOLD")
    project_manager_id: Optional[str] = Field(None, description="Novo ID do gerente de projeto", example="550e8400-e29b-41d4-a716-446655440004")
    technical_lead_id: Optional[str] = Field(None, description="Novo ID do líder técnico", example="550e8400-e29b-41d4-a716-446655440005")


class UserBase(BaseModel):
    email: str = Field(..., description="Endereço de email único do usuário", example="usuario@empresa.com")


class UserCreate(UserBase):
    password: str = Field(..., description="Senha do usuário (será criptografada)", example="MinhaSenh@123")
    role: UserRole = Field(UserRole.MEMBER, description="Papel/função do usuário no sistema", example="MEMBER")


class UserRead(UserBase):
    id: uuid.UUID = Field(..., description="Identificador único do usuário", example="550e8400-e29b-41d4-a716-446655440006")
    role: UserRole = Field(..., description="Papel/função atual do usuário", example="MANAGER")
    
    class Config:
        from_attributes = True


# Token schemas for JWT authentication
class Token(BaseModel):
    access_token: str = Field(..., description="Token JWT para autenticação", example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(..., description="Tipo do token de autenticação", example="bearer")


class TokenData(BaseModel):
    email: Optional[str] = Field(None, description="Email extraído do token JWT", example="usuario@empresa.com")


# Task schemas for task management
class TaskBase(BaseModel):
    title: str = Field(..., description="Título descritivo da tarefa", example="Configurar Active Directory")
    description: Optional[str] = Field(None, description="Descrição detalhada da tarefa", example="Configurar estrutura organizacional do AD com OUs e grupos de segurança")
    status: TaskStatus = Field(TaskStatus.TODO, description="Status atual da tarefa", example="TODO")
    priority: TaskPriority = Field(TaskPriority.MEDIUM, description="Prioridade da tarefa", example="HIGH")
    dueDate: Optional[date] = Field(None, description="Data limite para conclusão da tarefa", example="2025-02-15")
    assigned_to_id: Optional[uuid.UUID] = Field(None, description="ID do usuário responsável pela tarefa", example="550e8400-e29b-41d4-a716-446655440007")


class TaskRead(TaskBase):
    id: str = Field(..., description="Identificador único da tarefa", example="550e8400-e29b-41d4-a716-446655440008")
    project_id: str = Field(..., description="ID do projeto ao qual a tarefa pertence", example="550e8400-e29b-41d4-a716-446655440003")
    createdAt: datetime = Field(..., description="Data e hora de criação da tarefa", example="2025-01-15T10:30:00Z")
    assigned_to: Optional[UserInTask] = Field(None, description="Dados do usuário responsável pela tarefa")
    
    class Config:
        from_attributes = True


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Novo título da tarefa", example="Configurar Active Directory - Atualizado")
    description: Optional[str] = Field(None, description="Nova descrição da tarefa", example="Configurar AD com integração ao Azure AD")
    status: Optional[TaskStatus] = Field(None, description="Novo status da tarefa", example="IN_PROGRESS")
    priority: Optional[TaskPriority] = Field(None, description="Nova prioridade da tarefa", example="URGENT")
    dueDate: Optional[date] = Field(None, description="Nova data limite", example="2025-02-20")
    assigned_to_id: Optional[uuid.UUID] = Field(None, description="Novo responsável pela tarefa", example="550e8400-e29b-41d4-a716-446655440009")


class DocumentBase(BaseModel):
    name: str = Field(..., description="Nome do arquivo/documento", example="BRD_Microsoft365_v1.0.pdf")
    type: Optional[str] = Field(None, description="Tipo/categoria do documento", example="BRD")
    file_type: Optional[str] = Field(None, description="Extensão do arquivo", example="pdf")
    version: int = Field(1, description="Versão do documento", example=2)
    status: DocumentStatus = Field(DocumentStatus.UPLOADED, description="Status atual do documento", example="APPROVED")


class DocumentRead(DocumentBase):
    id: str = Field(..., description="Identificador único do documento", example="550e8400-e29b-41d4-a716-446655440010")
    project_id: str = Field(..., description="ID do projeto ao qual o documento pertence", example="550e8400-e29b-41d4-a716-446655440003")
    uploadedAt: datetime = Field(..., description="Data e hora do upload do documento", example="2025-01-15T14:20:00Z")
    
    class Config:
        from_attributes = True


class DocumentUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Novo nome do documento", example="BRD_Microsoft365_v2.0.pdf")
    type: Optional[str] = Field(None, description="Novo tipo do documento", example="LLD")
    status: Optional[DocumentStatus] = Field(None, description="Novo status do documento", example="UNDER_REVIEW")


# Analytics schemas for dashboard metrics
class AnalyticsStat(BaseModel):
    category: Any = Field(..., description="Categoria ou dimensão da estatística", example="Empresa ABC Ltda")
    count: int = Field(..., description="Quantidade/contagem para a categoria", example=5)


# Notification schemas
class NotificationRead(BaseModel):
    id: uuid.UUID = Field(..., description="Identificador único da notificação", example="550e8400-e29b-41d4-a716-446655440011")
    message: str = Field(..., description="Conteúdo da mensagem de notificação", example="Projeto 'Implementação MS365' avançou para fase de Elaboração")
    is_read: bool = Field(..., description="Indica se a notificação foi lida pelo usuário", example=False)
    link: Optional[str] = Field(None, description="Link relacionado à notificação", example="/projects/550e8400-e29b-41d4-a716-446655440003")
    created_at: datetime = Field(..., description="Data e hora de criação da notificação", example="2025-01-15T16:45:00Z")
    
    class Config:
        from_attributes = True


class AuditLogRead(BaseModel):
    id: str = Field(..., description="Identificador único do log de auditoria", example="550e8400-e29b-41d4-a716-446655440012")
    user: Optional[UserInProject] = Field(None, description="Dados do usuário que executou a ação")
    action: str = Field(..., description="Tipo de ação executada", example="PROJECT_CREATED")
    details: Optional[dict] = Field(None, description="Detalhes contextuais da ação", example={"project_name": "Implementação MS365", "client": "Empresa ABC"})
    timestamp: datetime = Field(..., description="Data e hora da execução da ação", example="2025-01-15T10:30:00Z")
    
    class Config:
        from_attributes = True