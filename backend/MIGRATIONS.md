# Guia de Migrações com Alembic

Este documento descreve como usar o Alembic para gerenciar migrações de banco de dados no projeto.

## Configuração

O Alembic foi configurado para trabalhar com o projeto usando:
- **Configuração**: `alembic.ini` - arquivo de configuração principal
- **Environment**: `alembic/env.py` - configuração do ambiente de migração
- **Migrações**: `alembic/versions/` - diretório com arquivos de migração

### Configuração do Banco de Dados

O Alembic está configurado para:
- Usar a variável de ambiente `DATABASE_URL` para conexão
- Converter automaticamente URLs `postgresql+asyncpg://` para `postgresql://` (necessário para migrações síncronas)
- Importar automaticamente os modelos do projeto para detecção de mudanças

## Comandos Principais

### Criar uma Nova Migração

```bash
# Migração com autogenerate (detecta mudanças automaticamente)
docker exec -it project_backend alembic revision --autogenerate -m "Descrição da migração"

# Migração manual (arquivo vazio para edição)
docker exec -it project_backend alembic revision -m "Descrição da migração"
```

### Aplicar Migrações

```bash
# Aplicar todas as migrações pendentes
docker exec -it project_backend alembic upgrade head

# Aplicar até uma revisão específica
docker exec -it project_backend alembic upgrade <revision_id>

# Aplicar próxima migração
docker exec -it project_backend alembic upgrade +1
```

### Reverter Migrações

```bash
# Reverter todas as migrações
docker exec -it project_backend alembic downgrade base

# Reverter até uma revisão específica
docker exec -it project_backend alembic downgrade <revision_id>

# Reverter uma migração
docker exec -it project_backend alembic downgrade -1
```

### Verificar Status

```bash
# Ver histórico de migrações
docker exec -it project_backend alembic history

# Ver migração atual
docker exec -it project_backend alembic current

# Ver migrações pendentes
docker exec -it project_backend alembic show <revision_id>
```

## Estrutura de Arquivos

```
backend/
├── alembic.ini              # Configuração principal
├── alembic/
│   ├── env.py              # Configuração do ambiente
│   ├── script.py.mako      # Template para novas migrações
│   └── versions/           # Arquivos de migração
│       └── xxxx_description.py
```

## Boas Práticas

### 1. Sempre Revisar Migrações Autogenerate

O autogenerate pode não detectar todas as mudanças. Sempre revise o arquivo gerado:

```python
def upgrade() -> None:
    # Revisar comandos gerados
    op.create_table('nova_tabela', ...)
    
def downgrade() -> None:
    # Garantir que o downgrade funciona
    op.drop_table('nova_tabela')
```

### 2. Testar Upgrade e Downgrade

Sempre teste ambos os processos:

```bash
# Aplicar migração
docker exec -it project_backend alembic upgrade head

# Testar rollback
docker exec -it project_backend alembic downgrade -1

# Aplicar novamente
docker exec -it project_backend alembic upgrade head
```

### 3. Backup Antes de Migrações em Produção

```bash
# Fazer backup do banco antes de aplicar migrações
pg_dump -h localhost -U admin -d project_management_db > backup_pre_migration.sql
```

### 4. Migrações de Dados

Para migrações que envolvem transformação de dados:

```python
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Criar nova coluna
    op.add_column('users', sa.Column('full_name', sa.String()))
    
    # Migrar dados
    connection = op.get_bind()
    connection.execute(
        "UPDATE users SET full_name = first_name || ' ' || last_name"
    )
    
    # Remover colunas antigas (opcional)
    # op.drop_column('users', 'first_name')
    # op.drop_column('users', 'last_name')
```

## Problemas Comuns

### 1. Erro de ENUMs Duplicados

Se encontrar erro "type already exists":

```python
# No downgrade, remover ENUMs manualmente
def downgrade() -> None:
    op.drop_table('tabela')
    op.execute('DROP TYPE IF EXISTS enum_name CASCADE')
```

### 2. Conflitos de Migração

Se duas pessoas criarem migrações simultaneamente:

```bash
# Mesclar migrações
docker exec -it project_backend alembic merge -m "Merge migrations" <rev1> <rev2>
```

### 3. Resetar Migrações (Desenvolvimento)

```bash
# CUIDADO: Isso remove todos os dados
docker exec -it project_backend alembic downgrade base
# Recriar migração inicial
docker exec -it project_backend alembic revision --autogenerate -m "Initial migration"
docker exec -it project_backend alembic upgrade head
```

## Integração com CI/CD

### Script de Deploy

```bash
#!/bin/bash
# deploy.sh

echo "Aplicando migrações..."
docker exec -it project_backend alembic upgrade head

if [ $? -eq 0 ]; then
    echo "Migrações aplicadas com sucesso"
else
    echo "Erro ao aplicar migrações"
    exit 1
fi
```

### Verificação de Migrações Pendentes

```bash
# Verificar se há migrações pendentes
PENDING=$(docker exec -it project_backend alembic current | grep -c "head")
if [ "$PENDING" -eq 0 ]; then
    echo "Há migrações pendentes!"
    exit 1
fi
```

## Monitoramento

### Log de Migrações

O Alembic registra todas as migrações na tabela `alembic_version`:

```sql
SELECT * FROM alembic_version;
```

### Auditoria de Mudanças

Considere adicionar campos de auditoria aos modelos:

```python
class BaseModel:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String)  # ID do usuário
```

## Contato

Para dúvidas sobre migrações, consulte:
- Documentação oficial: https://alembic.sqlalchemy.org/
- Time de desenvolvimento