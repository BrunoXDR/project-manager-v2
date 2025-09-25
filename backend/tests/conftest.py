# backend/tests/conftest.py
import os
import sys
import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Set DATABASE_URL for testing before importing modules
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from project_management_api.infrastructure.api.main import app
from project_management_api.infrastructure.db.database import get_db
from project_management_api.domain.models import Base, User
from project_management_api.infrastructure.api import security

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def test_engine():
    """Create a test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture
async def test_session(test_engine):
    """Create a test database session."""
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

@pytest_asyncio.fixture
async def test_user(test_session):
    """Create a test user."""
    from project_management_api.infrastructure.repositories.user_repository import UserRepository
    user_repo = UserRepository(test_session)
    user_data = {
        "email": "test@example.com",
        "hashed_password": security.get_password_hash("testpassword"),
        "role": "admin"
    }
    user = User(**user_data)
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user

@pytest_asyncio.fixture
async def client(test_session):
    """Create a test client with database dependency override."""
    from httpx import AsyncClient, ASGITransport
    
    async def override_get_db():
        yield test_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def authenticated_client(client, test_user):
    """Create an authenticated test client."""
    # Create access token for the test user
    access_token = security.create_access_token(data={"sub": test_user.email})
    
    # Set the authorization header
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    
    return client

@pytest_asyncio.fixture
async def create_test_project(authenticated_client):
    """Helper fixture para criar um projeto e retornar seu ID."""
    async def _create_project():
        project_data = {
            "name": "Projeto para Teste",
            "client": "Cliente de Teste",
            "startDate": "2025-01-01",
            "estimatedEndDate": "2025-12-31"
        }
        response = await authenticated_client.post("/api/projects/", json=project_data)
        assert response.status_code == 201
        return response.json()["id"]
    return _create_project

@pytest_asyncio.fixture
async def temp_upload_dir(monkeypatch):
    """Fixture para criar um diretório temporário para uploads durante os testes."""
    import tempfile
    import shutil
    
    # Criar diretório temporário
    temp_dir = tempfile.mkdtemp()
    
    # Monkeypatch do UPLOAD_DIR na rota de documentos
    monkeypatch.setattr("project_management_api.infrastructure.api.routes.documents.UPLOAD_DIR", temp_dir)
    
    yield temp_dir
    
    # Cleanup: remover diretório temporário após o teste
    shutil.rmtree(temp_dir, ignore_errors=True)