# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências
COPY pyproject.toml .
RUN pip install "fastapi[all]" uvicorn sqlalchemy "asyncpg" alembic python-dotenv

# Copiar o código da aplicação
COPY ./src /app/src

# Definir PYTHONPATH para incluir o diretório src
ENV PYTHONPATH=/app/src