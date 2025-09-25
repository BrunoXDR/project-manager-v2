# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências
COPY pyproject.toml .
RUN pip install "fastapi[all]" uvicorn sqlalchemy "asyncpg" alembic python-dotenv "passlib[bcrypt]" "python-jose[cryptography]" psycopg2-binary

# Copiar o código da aplicação
COPY ./src /app/src

# Copiar arquivos do Alembic
COPY alembic.ini /app/
COPY alembic /app/alembic

# Definir PYTHONPATH para incluir o diretório src
ENV PYTHONPATH=/app/src