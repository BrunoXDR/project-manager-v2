#!/usr/bin/env python3
"""
Script de teste para verificar a implementação do RBAC (Role-Based Access Control)
Sprint 17 - Advanced RBAC Implementation
"""

import sys
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar variáveis de ambiente para teste se não estiverem definidas
if not os.getenv('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'postgresql+asyncpg://user:password@localhost:5432/project_manager_test'
if not os.getenv('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'test_secret_key_for_development_only'

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from project_management_api.infrastructure.api.security import (
    RoleChecker, 
    allow_all_authenticated, 
    allow_managers_and_admins, 
    allow_only_admins
)
from project_management_api.domain.models import User, UserRole
from fastapi import HTTPException
import asyncio
import uuid

def create_test_user(role: UserRole, email: str = None) -> User:
    """Cria um usuário de teste com o papel especificado."""
    if email is None:
        email = f"test_{role.value.lower()}@example.com"
    
    user = User(
        id=str(uuid.uuid4()),
        email=email,
        role=role,
        hashed_password="test_hash"
    )
    return user

async def test_role_checker():
    """Testa a funcionalidade do RoleChecker."""
    print("🔐 Testando implementação do RBAC - Sprint 17")
    print("=" * 60)
    
    # Criar usuários de teste
    member_user = create_test_user(UserRole.MEMBER, "member@test.com")
    manager_user = create_test_user(UserRole.MANAGER, "manager@test.com")
    admin_user = create_test_user(UserRole.ADMIN, "admin@test.com")
    
    print(f"👤 Usuários de teste criados:")
    print(f"   - MEMBER: {member_user.email}")
    print(f"   - MANAGER: {manager_user.email}")
    print(f"   - ADMIN: {admin_user.email}")
    print()
    
    # Teste 1: allow_all_authenticated
    print("📋 Teste 1: allow_all_authenticated")
    print("   Deve permitir acesso para todos os usuários autenticados")
    
    try:
        result_member = allow_all_authenticated(member_user)
        result_manager = allow_all_authenticated(manager_user)
        result_admin = allow_all_authenticated(admin_user)
        
        print(f"   ✅ MEMBER permitido: {result_member.email}")
        print(f"   ✅ MANAGER permitido: {result_manager.email}")
        print(f"   ✅ ADMIN permitido: {result_admin.email}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()
    
    # Teste 2: allow_managers_and_admins
    print("📋 Teste 2: allow_managers_and_admins")
    print("   Deve permitir apenas MANAGER e ADMIN")
    
    # Teste com MEMBER (deve falhar)
    try:
        allow_managers_and_admins(member_user)
        print(f"   ❌ MEMBER foi permitido (deveria falhar)")
    except HTTPException as e:
        print(f"   ✅ MEMBER bloqueado corretamente: {e.detail}")
    except Exception as e:
        print(f"   ❌ Erro inesperado: {e}")
    
    # Teste com MANAGER (deve passar)
    try:
        result_manager = allow_managers_and_admins(manager_user)
        print(f"   ✅ MANAGER permitido: {result_manager.email}")
    except Exception as e:
        print(f"   ❌ MANAGER bloqueado incorretamente: {e}")
    
    # Teste com ADMIN (deve passar)
    try:
        result_admin = allow_managers_and_admins(admin_user)
        print(f"   ✅ ADMIN permitido: {result_admin.email}")
    except Exception as e:
        print(f"   ❌ ADMIN bloqueado incorretamente: {e}")
    
    print()
    
    # Teste 3: allow_only_admins
    print("📋 Teste 3: allow_only_admins")
    print("   Deve permitir apenas ADMIN")
    
    # Teste com MEMBER (deve falhar)
    try:
        allow_only_admins(member_user)
        print(f"   ❌ MEMBER foi permitido (deveria falhar)")
    except HTTPException as e:
        print(f"   ✅ MEMBER bloqueado corretamente: {e.detail}")
    except Exception as e:
        print(f"   ❌ Erro inesperado: {e}")
    
    # Teste com MANAGER (deve falhar)
    try:
        allow_only_admins(manager_user)
        print(f"   ❌ MANAGER foi permitido (deveria falhar)")
    except HTTPException as e:
        print(f"   ✅ MANAGER bloqueado corretamente: {e.detail}")
    except Exception as e:
        print(f"   ❌ Erro inesperado: {e}")
    
    # Teste com ADMIN (deve passar)
    try:
        result_admin = allow_only_admins(admin_user)
        print(f"   ✅ ADMIN permitido: {result_admin.email}")
    except Exception as e:
        print(f"   ❌ ADMIN bloqueado incorretamente: {e}")
    
    print()
    
    # Teste 4: RoleChecker customizado
    print("📋 Teste 4: RoleChecker customizado")
    print("   Testando criação de checker personalizado")
    
    # Criar um checker que permite apenas MEMBER e MANAGER
    custom_checker = RoleChecker([UserRole.MEMBER, UserRole.MANAGER])
    
    try:
        result_member = custom_checker(member_user)
        print(f"   ✅ MEMBER permitido no checker customizado: {result_member.email}")
    except Exception as e:
        print(f"   ❌ MEMBER bloqueado incorretamente: {e}")
    
    try:
        result_manager = custom_checker(manager_user)
        print(f"   ✅ MANAGER permitido no checker customizado: {result_manager.email}")
    except Exception as e:
        print(f"   ❌ MANAGER bloqueado incorretamente: {e}")
    
    try:
        custom_checker(admin_user)
        print(f"   ❌ ADMIN foi permitido (deveria falhar)")
    except HTTPException as e:
        print(f"   ✅ ADMIN bloqueado corretamente: {e.detail}")
    except Exception as e:
        print(f"   ❌ Erro inesperado: {e}")
    
    print()
    print("🎉 Testes de RBAC concluídos!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_role_checker())