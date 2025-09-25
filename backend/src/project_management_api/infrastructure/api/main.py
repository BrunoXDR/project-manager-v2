# backend/src/project_management_api/infrastructure/api/main.py
from fastapi import FastAPI
import sentry_sdk
import os
from .routes import projects, users, auth, tasks, documents, analytics
from .middleware import LoggingMiddleware

# Inicializar Sentry se o DSN estiver disponível
sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

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
app.include_router(documents.router)
app.include_router(analytics.router)

# Adicionar middleware de logging
app.add_middleware(LoggingMiddleware)

@app.get("/api/health", tags=["Health"])
def health_check():
    """Verifica se a API está operacional."""
    return {"status": "ok"}