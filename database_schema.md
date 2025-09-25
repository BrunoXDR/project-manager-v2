# Database Schema - Project Manager v1

Este documento descreve o esquema completo do banco de dados do sistema Project Manager v1, incluindo todas as tabelas, relacionamentos, índices e constraints.

## 📊 Visão Geral

O banco de dados utiliza **PostgreSQL** como SGBD principal e é gerenciado através do **SQLAlchemy ORM** com migrações **Alembic**. O schema é projetado para suportar um sistema completo de gerenciamento de projetos com controle de acesso baseado em roles.

## 🗂️ Tabelas

### 1. users
Tabela principal para armazenamento de informações dos usuários do sistema.

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| id | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Identificador único do usuário |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email do usuário (usado para login) |
| hashed_password | VARCHAR(255) | NOT NULL | Senha criptografada com bcrypt |
| full_name | VARCHAR(255) | NOT NULL | Nome completo do usuário |
| role | ENUM(UserRole) | NOT NULL, DEFAULT 'developer' | Role do usuário no sistema |
| is_active | BOOLEAN | NOT NULL, DEFAULT true | Status ativo/inativo do usuário |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Data de criação do registro |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Data da última atualização |

**Enum UserRole:**
- `admin`: Administrador do sistema
- `project_manager`: Gerente de projeto
- `technical_lead`: Líder técnico
- `developer`: Desenvolvedor
- `stakeholder`: Stakeholder/Cliente

**Índices:**
- `idx_users_email` (UNIQUE) - Otimização para login
- `idx_users_role` - Filtros por role
- `idx_users_is_active` - Filtros por status

### 2. projects
Tabela para armazenamento dos projetos do sistema.

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| id | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Identificador único do projeto |
| name | VARCHAR(255) | NOT NULL | Nome do projeto |
| description | TEXT | NULL | Descrição detalhada do projeto |
| start_date | DATE | NOT NULL | Data de início do projeto |
| end_date | DATE | NULL | Data de término planejada |
| actual_end_date | DATE | NULL | Data real de término |
| status | ENUM(ProjectStatus) | NOT NULL, DEFAULT 'planning' | Status atual do projeto |
| phase | ENUM(ProjectPhase) | NOT NULL, DEFAULT 'initiation' | Fase atual do projeto |
| budget | DECIMAL(15,2) | NULL | Orçamento do projeto |
| project_manager_id | UUID | FOREIGN KEY → users(id) | Gerente responsável pelo projeto |
| technical_lead_id | UUID | FOREIGN KEY → users(id) | Líder técnico do projeto |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Data de criação |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Data da última atualização |

**Enum ProjectStatus:**
- `planning`: Em planejamento
- `active`: Ativo/Em andamento
- `on_hold`: Pausado
- `completed`: Concluído
- `cancelled`: Cancelado

**Enum ProjectPhase:**
- `initiation`: Iniciação
- `planning`: Planejamento
- `execution`: Execução
- `monitoring`: Monitoramento
- `closure`: Encerramento

**Relacionamentos:**
- `project_manager_id` → `users.id` (Many-to-One)
- `technical_lead_id` → `users.id` (Many-to-One)

**Índices:**
- `idx_projects_status` - Filtros por status
- `idx_projects_phase` - Filtros por fase
- `idx_projects_manager` - Projetos por gerente
- `idx_projects_dates` - Consultas por período

### 3. tasks
Tabela para armazenamento das tarefas dos projetos.

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| id | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Identificador único da tarefa |
| title | VARCHAR(255) | NOT NULL | Título da tarefa |
| description | TEXT | NULL | Descrição detalhada da tarefa |
| status | ENUM(TaskStatus) | NOT NULL, DEFAULT 'todo' | Status atual da tarefa |
| priority | ENUM(TaskPriority) | NOT NULL, DEFAULT 'medium' | Prioridade da tarefa |
| estimated_hours | INTEGER | NULL | Horas estimadas para conclusão |
| actual_hours | INTEGER | NULL | Horas reais gastas |
| due_date | DATE | NULL | Data limite para conclusão |
| completed_at | TIMESTAMP | NULL | Data/hora de conclusão |
| project_id | UUID | NOT NULL, FOREIGN KEY → projects(id) | Projeto ao qual a tarefa pertence |
| assigned_to | UUID | FOREIGN KEY → users(id) | Usuário responsável pela tarefa |
| created_by | UUID | NOT NULL, FOREIGN KEY → users(id) | Usuário que criou a tarefa |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Data de criação |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Data da última atualização |

**Enum TaskStatus:**
- `todo`: A fazer
- `in_progress`: Em progresso
- `in_review`: Em revisão
- `done`: Concluída
- `blocked`: Bloqueada

**Enum TaskPriority:**
- `low`: Baixa
- `medium`: Média
- `high`: Alta
- `critical`: Crítica

**Relacionamentos:**
- `project_id` → `projects.id` (Many-to-One)
- `assigned_to` → `users.id` (Many-to-One)
- `created_by` → `users.id` (Many-to-One)

**Índices:**
- `idx_tasks_project` - Tarefas por projeto
- `idx_tasks_assigned` - Tarefas por responsável
- `idx_tasks_status` - Filtros por status
- `idx_tasks_priority` - Filtros por prioridade
- `idx_tasks_due_date` - Ordenação por prazo

### 4. notifications
Tabela para sistema de notificações dos usuários.

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| id | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Identificador único da notificação |
| user_id | UUID | NOT NULL, FOREIGN KEY → users(id) | Usuário destinatário |
| message | TEXT | NOT NULL | Conteúdo da notificação |
| link | VARCHAR(500) | NULL | Link relacionado à notificação |
| is_read | BOOLEAN | NOT NULL, DEFAULT false | Status de leitura |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Data de criação |

**Relacionamentos:**
- `user_id` → `users.id` (Many-to-One)

**Índices:**
- `idx_notifications_user` - Notificações por usuário
- `idx_notifications_unread` - Notificações não lidas
- `idx_notifications_created` - Ordenação por data

### 5. documents
Tabela para gerenciamento de documentos dos projetos.

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| id | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Identificador único do documento |
| filename | VARCHAR(255) | NOT NULL | Nome original do arquivo |
| file_path | VARCHAR(500) | NOT NULL | Caminho do arquivo no sistema |
| file_size | BIGINT | NOT NULL | Tamanho do arquivo em bytes |
| mime_type | VARCHAR(100) | NOT NULL | Tipo MIME do arquivo |
| status | ENUM(DocumentStatus) | NOT NULL, DEFAULT 'active' | Status do documento |
| version | INTEGER | NOT NULL, DEFAULT 1 | Versão do documento |
| project_id | UUID | NOT NULL, FOREIGN KEY → projects(id) | Projeto ao qual pertence |
| uploaded_by | UUID | NOT NULL, FOREIGN KEY → users(id) | Usuário que fez upload |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Data de upload |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Data da última atualização |

**Enum DocumentStatus:**
- `active`: Ativo
- `archived`: Arquivado
- `deleted`: Excluído (soft delete)

**Relacionamentos:**
- `project_id` → `projects.id` (Many-to-One)
- `uploaded_by` → `users.id` (Many-to-One)

**Índices:**
- `idx_documents_project` - Documentos por projeto
- `idx_documents_uploader` - Documentos por usuário
- `idx_documents_status` - Filtros por status
- `idx_documents_filename` - Busca por nome

### 6. audit_logs
Tabela para auditoria e rastreamento de ações no sistema.

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| id | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Identificador único do log |
| user_id | UUID | FOREIGN KEY → users(id) | Usuário que executou a ação |
| action | VARCHAR(100) | NOT NULL | Tipo de ação executada |
| details | JSONB | NULL | Detalhes da ação em formato JSON |
| timestamp | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Data/hora da ação |

**Relacionamentos:**
- `user_id` → `users.id` (Many-to-One)

**Índices:**
- `idx_audit_user` - Logs por usuário
- `idx_audit_action` - Logs por tipo de ação
- `idx_audit_timestamp` - Ordenação temporal
- `idx_audit_details` (GIN) - Busca em campos JSON

## 🔗 Relacionamentos Principais

### Hierarquia de Entidades
```
users (1) ←→ (N) projects
    ↓
projects (1) ←→ (N) tasks
    ↓
projects (1) ←→ (N) documents
    ↓
users (1) ←→ (N) notifications
    ↓
users (1) ←→ (N) audit_logs
```

### Relacionamentos Detalhados

1. **User → Projects**: Um usuário pode ser gerente ou líder técnico de múltiplos projetos
2. **Project → Tasks**: Um projeto pode ter múltiplas tarefas
3. **User → Tasks**: Um usuário pode ser responsável por múltiplas tarefas
4. **Project → Documents**: Um projeto pode ter múltiplos documentos
5. **User → Notifications**: Um usuário pode ter múltiplas notificações
6. **User → Audit Logs**: Um usuário pode ter múltiplos logs de auditoria

## 🔒 Constraints e Validações

### Constraints de Integridade Referencial
- Todas as foreign keys possuem `ON DELETE CASCADE` ou `ON DELETE SET NULL` conforme apropriado
- Constraints de unicidade em campos críticos (email, combinações específicas)

### Validações de Negócio
- Datas de fim devem ser posteriores às datas de início
- Status e fases seguem fluxos específicos
- Roles possuem permissões específicas definidas na aplicação

## 📈 Considerações de Performance

### Índices Estratégicos
- Índices compostos para consultas frequentes
- Índices parciais para filtros específicos
- Índices GIN para campos JSONB

### Otimizações
- Uso de UUIDs para distribuição e segurança
- Campos de timestamp para auditoria temporal
- Soft deletes para preservação de histórico

## 🔄 Migrações

O sistema utiliza **Alembic** para controle de versão do schema:

```bash
# Gerar nova migração
alembic revision --autogenerate -m "description"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1
```

### Histórico de Migrações Principais
- `001_create_audit_logs_table.py` - Criação da tabela de auditoria
- `d92223d91a68_create_notifications_table.py` - Criação da tabela de notificações
- Migrações automáticas para ajustes de schema

## 🛡️ Segurança

### Proteção de Dados
- Senhas armazenadas com hash bcrypt
- UUIDs para prevenir enumeration attacks
- Soft deletes para preservação de dados críticos

### Auditoria
- Log completo de todas as ações críticas
- Rastreamento de alterações com timestamp
- Detalhes em formato JSON para flexibilidade

## 📊 Métricas e Analytics

O schema suporta extração de métricas através de:
- Contadores por status de projetos e tarefas
- Análise temporal de atividades
- Relatórios de produtividade por usuário
- Estatísticas de uso do sistema

## 🔧 Manutenção

### Limpeza Periódica
- Arquivamento de logs antigos
- Limpeza de notificações lidas antigas
- Otimização de índices

### Backup e Recuperação
- Backup completo diário
- Backup incremental a cada 4 horas
- Testes de recuperação mensais