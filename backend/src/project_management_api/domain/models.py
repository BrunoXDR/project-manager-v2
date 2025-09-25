import uuid
import enum
from datetime import datetime, date
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, Date as SQLDate, ForeignKey, Text, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class ProjectPhase(str, enum.Enum):
    INCEPTION = "inception"
    DEFINITION = "definition"
    BUILT = "built"
    DEPLOY = "deploy"
    CLOSE = "close"


class ProjectStatus(str, enum.Enum):
    ACTIVE = "active"
    HOLD = "hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    client = Column(String, nullable=False)
    orderValue = Column(String)
    proposal = Column(String)
    pct = Column(String)
    phase = Column(SQLEnum(ProjectPhase), nullable=False, default=ProjectPhase.INCEPTION)
    status = Column(SQLEnum(ProjectStatus), nullable=False, default=ProjectStatus.ACTIVE)
    startDate = Column(SQLDate, nullable=False)
    estimatedEndDate = Column(SQLDate, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys for project manager and technical lead
    project_manager_id = Column(String, ForeignKey("users.id"), nullable=True)
    technical_lead_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    project_manager = relationship("User", foreign_keys=[project_manager_id])
    technical_lead = relationship("User", foreign_keys=[technical_lead_id])


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.MEMBER)


class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"
    HOLD = "hold"


class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DocumentStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    APPROVED = "approved"
    REJECTED = "rejected"


class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    priority = Column(SQLEnum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM)
    dueDate = Column(SQLDate)
    createdAt = Column(DateTime, default=datetime.utcnow)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    assigned_to_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    project = relationship("Project")
    assigned_to = relationship("User")


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    link = Column(String, nullable=True)  # Ex: /projects/{project_id}
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")


class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    type = Column(String(100), nullable=True)  # Ex: "BRD", "LLD", "Proposta Técnica"
    file_path = Column(String, nullable=False, unique=True)
    file_type = Column(String)
    version = Column(Integer, default=1)
    status = Column(SQLEnum(DocumentStatus), nullable=False, default=DocumentStatus.UPLOADED)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project")