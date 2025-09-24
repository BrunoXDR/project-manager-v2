import uuid
import enum
from datetime import datetime, date
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, Date as SQLDate
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

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
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.MEMBER)