# backend/src/project_management_api/infrastructure/api/main.py
from fastapi import FastAPI
from .routes import projects, users, auth, tasks

app = FastAPI(
    title="Sistema de Gestão de Projetos API",
    version="1.0.0",
    description="API para gerenciar o ciclo de vida de projetos.",
    openapi_url="/api/openapi.json",  # Garante que a documentação fique sob /api
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Include routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/api/health", tags=["Health"])
def health_check():
    """Verifica se a API está operacional."""
    return {"status": "ok"}