#!/usr/bin/env python3
"""
Script de seed para popular o banco de dados com dados de amostra.
Este script é idempotente - pode ser executado múltiplas vezes sem criar duplicatas.
"""

import asyncio
import sys
import os
from datetime import datetime, date, timedelta
from typing import List
from faker import Faker

# Adicionar o diretório src ao path para importar os módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Importar a engine do DB, a SessionLocal, e todos os modelos
from project_management_api.infrastructure.db.database import engine, AsyncSessionLocal
from project_management_api.domain.models import (
    Base, User, Project, Task, Document, Notification,
    UserRole, ProjectPhase, ProjectStatus, TaskStatus, TaskPriority, DocumentStatus
)
from project_management_api.infrastructure.api.security import get_password_hash

# Configurar Faker para português brasileiro
fake = Faker('pt_BR')

class DataSeeder:
    def __init__(self):
        self.users = []
        self.projects = []
        self.tasks = []
        self.documents = []

    async def check_if_data_exists(self, db: AsyncSession) -> bool:
        """Verifica se já existem dados no banco."""
        result = await db.execute(select(User))
        users = result.scalars().all()
        return len(users) > 0

    async def create_users(self, db: AsyncSession) -> List[User]:
        """Cria usuários com diferentes papéis."""
        print("📝 Criando usuários...")
        
        users_data = [
            {
                "email": "admin@planomaster.com",
                "password": "admin123",
                "role": UserRole.ADMIN
            },
            {
                "email": "gerente@planomaster.com", 
                "password": "gerente123",
                "role": UserRole.MANAGER
            },
            {
                "email": "membro@planomaster.com",
                "password": "membro123", 
                "role": UserRole.MEMBER
            },
            {
                "email": "carlos.silva@planomaster.com",
                "password": "carlos123",
                "role": UserRole.MANAGER
            },
            {
                "email": "ana.santos@planomaster.com",
                "password": "ana123",
                "role": UserRole.MEMBER
            },
            {
                "email": "pedro.oliveira@planomaster.com",
                "password": "pedro123",
                "role": UserRole.MEMBER
            },
            {
                "email": "maria.costa@planomaster.com",
                "password": "maria123",
                "role": UserRole.MEMBER
            }
        ]

        created_users = []
        for user_data in users_data:
            user = User(
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
                role=user_data["role"]
            )
            db.add(user)
            created_users.append(user)

        await db.commit()
        
        # Refresh para obter os IDs
        for user in created_users:
            await db.refresh(user)
            
        self.users = created_users
        print(f"✅ {len(created_users)} usuários criados")
        return created_users

    async def create_projects(self, db: AsyncSession) -> List[Project]:
        """Cria projetos variados com diferentes fases e status."""
        print("🏗️ Criando projetos...")
        
        # Dados realistas de projetos
        projects_data = [
            {
                "name": "Implementação Microsoft 365",
                "client": "Empresa ABC Ltda",
                "orderValue": "R$ 150.000,00",
                "proposal": "PROP-2024-001",
                "pct": "PCT-2024-MS365-001",
                "phase": ProjectPhase.BUILT,
                "status": ProjectStatus.ACTIVE,
                "days_offset": -30
            },
            {
                "name": "Migração para AWS Cloud",
                "client": "TechCorp Solutions",
                "orderValue": "R$ 280.000,00", 
                "proposal": "PROP-2024-002",
                "pct": "PCT-2024-AWS-002",
                "phase": ProjectPhase.DEFINITION,
                "status": ProjectStatus.ACTIVE,
                "days_offset": -15
            },
            {
                "name": "Sistema de Gestão Financeira",
                "client": "Financeira XYZ",
                "orderValue": "R$ 320.000,00",
                "proposal": "PROP-2024-003", 
                "pct": "PCT-2024-FIN-003",
                "phase": ProjectPhase.INCEPTION,
                "status": ProjectStatus.ACTIVE,
                "days_offset": -5
            },
            {
                "name": "Modernização de Infraestrutura",
                "client": "Indústria Moderna S.A.",
                "orderValue": "R$ 450.000,00",
                "proposal": "PROP-2024-004",
                "pct": "PCT-2024-INF-004", 
                "phase": ProjectPhase.DEPLOY,
                "status": ProjectStatus.ACTIVE,
                "days_offset": -60
            },
            {
                "name": "Portal de Atendimento ao Cliente",
                "client": "Serviços Premium Ltda",
                "orderValue": "R$ 180.000,00",
                "proposal": "PROP-2024-005",
                "pct": "PCT-2024-POR-005",
                "phase": ProjectPhase.CLOSE,
                "status": ProjectStatus.COMPLETED,
                "days_offset": -90
            },
            {
                "name": "Integração de Sistemas ERP",
                "client": "Corporação Global",
                "orderValue": "R$ 380.000,00",
                "proposal": "PROP-2024-006",
                "pct": "PCT-2024-ERP-006",
                "phase": ProjectPhase.BUILT,
                "status": ProjectStatus.HOLD,
                "days_offset": -45
            },
            {
                "name": "Plataforma de E-commerce",
                "client": "Varejo Digital Ltda",
                "orderValue": "R$ 220.000,00",
                "proposal": "PROP-2024-007",
                "pct": "PCT-2024-ECO-007",
                "phase": ProjectPhase.DEFINITION,
                "status": ProjectStatus.ACTIVE,
                "days_offset": -10
            },
            {
                "name": "Sistema de Monitoramento IoT",
                "client": "Smart Industries",
                "orderValue": "R$ 290.000,00",
                "proposal": "PROP-2024-008",
                "pct": "PCT-2024-IOT-008",
                "phase": ProjectPhase.INCEPTION,
                "status": ProjectStatus.ACTIVE,
                "days_offset": 0
            },
            {
                "name": "Automação de Processos RPA",
                "client": "Eficiência Corp",
                "orderValue": "R$ 160.000,00",
                "proposal": "PROP-2024-009",
                "pct": "PCT-2024-RPA-009",
                "phase": ProjectPhase.BUILT,
                "status": ProjectStatus.ACTIVE,
                "days_offset": -25
            },
            {
                "name": "Segurança Cibernética Avançada",
                "client": "SecureTech Ltda",
                "orderValue": "R$ 340.000,00",
                "proposal": "PROP-2024-010",
                "pct": "PCT-2024-SEC-010",
                "phase": ProjectPhase.DEFINITION,
                "status": ProjectStatus.ACTIVE,
                "days_offset": -20
            }
        ]

        created_projects = []
        managers = [u for u in self.users if u.role in [UserRole.ADMIN, UserRole.MANAGER]]
        members = [u for u in self.users if u.role == UserRole.MEMBER]

        for i, project_data in enumerate(projects_data):
            start_date = date.today() + timedelta(days=project_data["days_offset"])
            end_date = start_date + timedelta(days=fake.random_int(min=60, max=180))
            
            project = Project(
                name=project_data["name"],
                client=project_data["client"],
                orderValue=project_data["orderValue"],
                proposal=project_data["proposal"],
                pct=project_data["pct"],
                phase=project_data["phase"],
                status=project_data["status"],
                startDate=start_date,
                estimatedEndDate=end_date,
                project_manager_id=fake.random_element(managers).id if managers else None,
                technical_lead_id=fake.random_element(members).id if members else None
            )
            db.add(project)
            created_projects.append(project)

        await db.commit()
        
        # Refresh para obter os IDs
        for project in created_projects:
            await db.refresh(project)
            
        self.projects = created_projects
        print(f"✅ {len(created_projects)} projetos criados")
        return created_projects

    async def create_tasks(self, db: AsyncSession) -> List[Task]:
        """Cria tarefas para cada projeto."""
        print("📋 Criando tarefas...")
        
        task_templates = {
            ProjectPhase.INCEPTION: [
                "Levantamento de requisitos iniciais",
                "Análise de viabilidade técnica", 
                "Definição do escopo do projeto",
                "Identificação dos stakeholders",
                "Criação do cronograma preliminar"
            ],
            ProjectPhase.DEFINITION: [
                "Elaboração do documento de requisitos",
                "Definição da arquitetura do sistema",
                "Criação dos wireframes e mockups",
                "Planejamento detalhado das sprints",
                "Configuração do ambiente de desenvolvimento",
                "Definição dos critérios de aceite"
            ],
            ProjectPhase.BUILT: [
                "Desenvolvimento do módulo principal",
                "Implementação da interface de usuário",
                "Integração com sistemas externos",
                "Desenvolvimento de testes unitários",
                "Configuração do pipeline CI/CD",
                "Implementação de logs e monitoramento",
                "Otimização de performance"
            ],
            ProjectPhase.DEPLOY: [
                "Preparação do ambiente de produção",
                "Execução dos testes de aceitação",
                "Deploy em ambiente de homologação",
                "Treinamento dos usuários finais",
                "Deploy em produção",
                "Monitoramento pós-deploy"
            ],
            ProjectPhase.CLOSE: [
                "Documentação final do projeto",
                "Transferência de conhecimento",
                "Avaliação de lições aprendidas",
                "Encerramento de contratos",
                "Arquivamento da documentação"
            ]
        }

        created_tasks = []
        members = [u for u in self.users if u.role in [UserRole.MEMBER, UserRole.MANAGER]]

        for project in self.projects:
            phase_tasks = task_templates.get(project.phase, [])
            num_tasks = fake.random_int(min=5, max=min(10, len(phase_tasks)))
            selected_tasks = fake.random_elements(elements=phase_tasks, length=num_tasks, unique=True)
            
            for task_title in selected_tasks:
                # Determinar status baseado na fase do projeto
                if project.phase == ProjectPhase.CLOSE:
                    status = TaskStatus.DONE
                elif project.phase == ProjectPhase.DEPLOY:
                    status = fake.random_element([TaskStatus.DONE, TaskStatus.IN_PROGRESS])
                elif project.phase == ProjectPhase.BUILT:
                    status = fake.random_element([TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE])
                else:
                    status = fake.random_element([TaskStatus.TODO, TaskStatus.IN_PROGRESS])

                due_date = project.estimatedEndDate - timedelta(days=fake.random_int(min=1, max=30))
                
                task = Task(
                    title=task_title,
                    description=f"Descrição detalhada para: {task_title}",
                    status=status,
                    priority=fake.random_element([TaskPriority.LOW, TaskPriority.MEDIUM, TaskPriority.HIGH, TaskPriority.CRITICAL]),
                    dueDate=due_date,
                    project_id=project.id,
                    assigned_to_id=fake.random_element(members).id if fake.boolean(chance_of_getting_true=80) else None
                )
                db.add(task)
                created_tasks.append(task)

        await db.commit()
        
        # Refresh para obter os IDs
        for task in created_tasks:
            await db.refresh(task)
            
        self.tasks = created_tasks
        print(f"✅ {len(created_tasks)} tarefas criadas")
        return created_tasks

    async def create_documents(self, db: AsyncSession) -> List[Document]:
        """Cria documentos para alguns projetos."""
        print("📄 Criando documentos...")
        
        document_types = [
            ("BRD", "Business Requirements Document"),
            ("LLD", "Low Level Design"),
            ("Proposta Técnica", "Proposta Técnica"),
            ("Manual do Usuário", "Manual do Usuário"),
            ("Plano de Testes", "Plano de Testes"),
            ("Arquitetura", "Documento de Arquitetura")
        ]
        
        file_extensions = ["pdf", "docx", "xlsx", "pptx"]
        
        created_documents = []
        
        # Criar 2-3 documentos para cada projeto
        for project in self.projects:
            num_docs = fake.random_int(min=2, max=3)
            selected_types = fake.random_elements(elements=document_types, length=num_docs, unique=True)
            
            for doc_type, doc_description in selected_types:
                file_ext = fake.random_element(file_extensions)
                file_name = f"{doc_type}_{project.name.replace(' ', '_')}_v{fake.random_int(min=1, max=3)}.{file_ext}"
                
                # Status baseado na fase do projeto
                if project.phase in [ProjectPhase.CLOSE, ProjectPhase.DEPLOY]:
                    status = DocumentStatus.APPROVED
                elif project.phase == ProjectPhase.BUILT:
                    status = fake.random_element([DocumentStatus.UPLOADED, DocumentStatus.APPROVED])
                else:
                    status = DocumentStatus.UPLOADED
                
                document = Document(
                    name=file_name,
                    type=doc_type,
                    file_path=f"/app/uploads/{project.id}/{file_name}",
                    file_type=file_ext,
                    version=fake.random_int(min=1, max=3),
                    status=status,
                    project_id=project.id
                )
                db.add(document)
                created_documents.append(document)

        await db.commit()
        
        # Refresh para obter os IDs
        for document in created_documents:
            await db.refresh(document)
            
        self.documents = created_documents
        print(f"✅ {len(created_documents)} documentos criados")
        return created_documents

    async def create_notifications(self, db: AsyncSession) -> List[Notification]:
        """Cria algumas notificações para os usuários."""
        print("🔔 Criando notificações...")
        
        notification_templates = [
            "Você foi atribuído à tarefa '{task_title}'",
            "O projeto '{project_name}' mudou de fase",
            "Nova tarefa criada no projeto '{project_name}'",
            "Documento '{doc_name}' foi aprovado",
            "Prazo da tarefa '{task_title}' está próximo"
        ]
        
        created_notifications = []
        members = [u for u in self.users if u.role == UserRole.MEMBER]
        
        # Criar algumas notificações para cada membro
        for user in members:
            num_notifications = fake.random_int(min=2, max=5)
            
            for _ in range(num_notifications):
                template = fake.random_element(notification_templates)
                
                if '{task_title}' in template and self.tasks:
                    task = fake.random_element(self.tasks)
                    message = template.format(task_title=task.title)
                    link = f"/projects/{task.project_id}/tasks/{task.id}"
                elif '{project_name}' in template and self.projects:
                    project = fake.random_element(self.projects)
                    message = template.format(project_name=project.name)
                    link = f"/projects/{project.id}"
                elif '{doc_name}' in template and self.documents:
                    doc = fake.random_element(self.documents)
                    message = template.format(doc_name=doc.name)
                    link = f"/projects/{doc.project_id}/documents/{doc.id}"
                else:
                    message = "Você tem uma nova notificação no sistema"
                    link = "/dashboard"
                
                notification = Notification(
                    user_id=user.id,
                    message=message,
                    is_read=fake.boolean(chance_of_getting_true=30),
                    link=link
                )
                db.add(notification)
                created_notifications.append(notification)

        await db.commit()
        print(f"✅ {len(created_notifications)} notificações criadas")
        return created_notifications

async def seed_data():
    """Função principal para popular o banco de dados."""
    print("🌱 Iniciando processo de seed do banco de dados...")
    print("=" * 60)
    
    # Criar as tabelas se não existirem
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as db:
        seeder = DataSeeder()
        
        # Verificar se já existem dados
        if await seeder.check_if_data_exists(db):
            print("⚠️  Banco de dados já contém dados.")
            print("   Para recriar os dados, execute: docker-compose exec backend python scripts/reset_and_seed.py")
            return
        
        print("📊 Banco de dados vazio. Iniciando população...")
        print()
        
        try:
            # Criar dados em ordem de dependência
            await seeder.create_users(db)
            await seeder.create_projects(db)
            await seeder.create_tasks(db)
            await seeder.create_documents(db)
            await seeder.create_notifications(db)
            
            print()
            print("=" * 60)
            print("🎉 Banco de dados populado com sucesso!")
            print()
            print("📈 Resumo dos dados criados:")
            print(f"   👥 Usuários: {len(seeder.users)}")
            print(f"   🏗️  Projetos: {len(seeder.projects)}")
            print(f"   📋 Tarefas: {len(seeder.tasks)}")
            print(f"   📄 Documentos: {len(seeder.documents)}")
            print()
            print("🔑 Credenciais de acesso:")
            print("   Admin: admin@planomaster.com / admin123")
            print("   Gerente: gerente@planomaster.com / gerente123")
            print("   Membro: membro@planomaster.com / membro123")
            print()
            print("🚀 Agora você pode testar a API com dados realistas!")
            
        except Exception as e:
            print(f"❌ Erro durante o seed: {str(e)}")
            raise

def run():
    """Função de entrada para o comando poetry."""
    asyncio.run(seed_data())

if __name__ == "__main__":
    asyncio.run(seed_data())