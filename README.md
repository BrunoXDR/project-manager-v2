# Project Manager v1

Sistema completo de gerenciamento de projetos desenvolvido com FastAPI (backend) e React (frontend), oferecendo funcionalidades robustas para gestão de projetos, tarefas, usuários e documentos.

## 🚀 Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e de alta performance
- **SQLAlchemy** - ORM para Python com suporte assíncrono
- **PostgreSQL** - Banco de dados relacional
- **Alembic** - Ferramenta de migração de banco de dados
- **Uvicorn** - Servidor ASGI de alta performance
- **Python-Jose** - Biblioteca para JWT
- **Passlib** - Biblioteca para hash de senhas
- **Sentry** - Monitoramento de erros

### Frontend
- **React 18** - Biblioteca para interfaces de usuário
- **TypeScript** - Superset tipado do JavaScript
- **Vite** - Build tool e dev server
- **React Router DOM** - Roteamento para React
- **React Hook Form** - Gerenciamento de formulários
- **TanStack Query** - Gerenciamento de estado servidor
- **Radix UI** - Componentes acessíveis
- **Tailwind CSS** - Framework CSS utilitário
- **Axios** - Cliente HTTP
- **Zod** - Validação de esquemas

### Infraestrutura
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers
- **Nginx** - Proxy reverso e servidor web

## 📋 Pré-requisitos

- Docker 20.10+
- Docker Compose 2.0+
- Node.js 18+ (para desenvolvimento local)
- Python 3.11+ (para desenvolvimento local)

## 🏃‍♂️ Execução

### Usando Docker Compose (Recomendado)

1. Clone o repositório:
```bash
git clone <repository-url>
cd project-manager-v1
```

2. Execute o sistema completo:
```bash
docker-compose up -d
```

### Execução Manual

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -e .
alembic upgrade head
uvicorn project_management_api.infrastructure.api.main:app --reload --host 0.0.0.0 --port 8002
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🌐 URLs de Acesso

- **Frontend**: http://localhost:8081
- **Backend API**: http://localhost:8002
- **Documentação API**: http://localhost:8002/docs
- **OpenAPI Schema**: http://localhost:8002/openapi.json

## 🔐 Credenciais de Teste

### Usuário Administrador
- **Email**: admin@example.com
- **Senha**: admin123

### Usuário Gerente de Projeto
- **Email**: manager@example.com
- **Senha**: manager123

### Usuário Desenvolvedor
- **Email**: developer@example.com
- **Senha**: developer123

## 🏗️ Estrutura do Projeto

```
project-manager-v1/
├── backend/                    # API FastAPI
│   ├── src/
│   │   └── project_management_api/
│   │       ├── application/    # Camada de aplicação
│   │       ├── domain/         # Modelos de domínio
│   │       └── infrastructure/ # Infraestrutura
│   ├── alembic/               # Migrações do banco
│   ├── tests/                 # Testes automatizados
│   └── docs/                  # Documentação da API
├── frontend/                  # Aplicação React
│   ├── src/
│   │   ├── components/        # Componentes reutilizáveis
│   │   ├── pages/            # Páginas da aplicação
│   │   ├── contexts/         # Contextos React
│   │   ├── hooks/            # Hooks customizados
│   │   └── types/            # Definições TypeScript
│   └── public/               # Arquivos estáticos
└── docker-compose.yml        # Orquestração dos serviços
```

## 🧪 Testes

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm test
```

## 📊 Funcionalidades Principais

### Gestão de Projetos
- Criação, edição e exclusão de projetos
- Controle de fases e status
- Atribuição de gerentes e líderes técnicos
- Métricas e analytics

### Gestão de Tarefas
- Criação e atribuição de tarefas
- Controle de prioridades e status
- Comentários e atualizações
- Rastreamento de progresso

### Gestão de Usuários
- Sistema de autenticação JWT
- Controle de acesso baseado em roles (RBAC)
- Perfis de usuário
- Notificações

### Gestão de Documentos
- Upload e download de arquivos
- Versionamento de documentos
- Controle de acesso
- Organização por projeto

### Sistema de Notificações
- Notificações em tempo real
- Histórico de notificações
- Marcação de lidas/não lidas

### Auditoria
- Log de todas as ações do sistema
- Rastreamento de alterações
- Histórico completo de atividades

## 🔧 Desenvolvimento

### Configuração do Ambiente

1. **Backend**:
   - Configure as variáveis de ambiente no arquivo `.env`
   - Execute as migrações: `alembic upgrade head`
   - Popule o banco com dados de teste: `python scripts/seed.py`

2. **Frontend**:
   - Configure as variáveis de ambiente no arquivo `.env.local`
   - Instale as dependências: `npm install`

### Comandos Úteis

```bash
# Backend
cd backend
python scripts/reset_and_seed.py  # Reset e popular banco
alembic revision --autogenerate -m "description"  # Nova migração
python generate_openapi.py        # Gerar OpenAPI spec
python generate_postman.py        # Gerar collection Postman

# Frontend
cd frontend
npm run build                     # Build de produção
npm run preview                   # Preview do build
npm run lint                      # Linting
```

## 📈 Monitoramento

O sistema inclui integração com Sentry para monitoramento de erros e performance. Configure a variável `SENTRY_DSN` no ambiente de produção.

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte e dúvidas, entre em contato através dos issues do GitHub ou email: support@projectmanager.com