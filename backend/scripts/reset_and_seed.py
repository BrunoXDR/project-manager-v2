#!/usr/bin/env python3
"""
Script para resetar o banco de dados e executar o seed.
ATENÇÃO: Este script apaga TODOS os dados existentes!
"""

import asyncio
import sys
import os

# Adicionar o diretório src ao path para importar os módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from project_management_api.infrastructure.db.database import engine
from project_management_api.domain.models import Base
from seed import DataSeeder, AsyncSessionLocal

async def reset_and_seed():
    """Reseta o banco de dados e executa o seed."""
    print("🔥 ATENÇÃO: Este script irá APAGAR todos os dados existentes!")
    print("=" * 60)
    
    # Recriar todas as tabelas (drop + create)
    async with engine.begin() as conn:
        print("🗑️  Removendo todas as tabelas...")
        await conn.run_sync(Base.metadata.drop_all)
        print("🏗️  Recriando estrutura do banco...")
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Banco de dados resetado com sucesso!")
    print()
    
    # Executar o seed
    async with AsyncSessionLocal() as db:
        seeder = DataSeeder()
        
        print("📊 Iniciando população do banco...")
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
            print("🎉 Banco de dados resetado e populado com sucesso!")
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
            print(f"❌ Erro durante o reset e seed: {str(e)}")
            raise

if __name__ == "__main__":
    asyncio.run(reset_and_seed())