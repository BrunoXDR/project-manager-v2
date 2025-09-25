#!/usr/bin/env python3
"""
Script para gerar o arquivo OpenAPI JSON da API do Project Manager.
Este script extrai a especificação OpenAPI da aplicação FastAPI e salva em formato JSON.
"""

import json
import sys
import os
from pathlib import Path

# Adicionar o diretório src ao PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / "src"))

from project_management_api.infrastructure.api.main import app

def generate_openapi_json():
    """Gera o arquivo openapi.json a partir da aplicação FastAPI."""
    try:
        # Obter a especificação OpenAPI da aplicação
        openapi_schema = app.openapi()
        
        # Criar diretório docs se não existir
        docs_dir = Path(__file__).parent / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        # Salvar o arquivo OpenAPI JSON
        openapi_file = docs_dir / "openapi.json"
        with open(openapi_file, "w", encoding="utf-8") as f:
            json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Arquivo OpenAPI gerado com sucesso: {openapi_file}")
        print(f"📊 Total de endpoints documentados: {len([path for path in openapi_schema.get('paths', {}).values() for method in path.values()])}")
        
        # Mostrar estatísticas
        paths = openapi_schema.get('paths', {})
        total_endpoints = sum(len(methods) for methods in paths.values())
        print(f"📈 Total de rotas: {len(paths)}")
        print(f"🔗 Total de endpoints: {total_endpoints}")
        
        # Listar tags (grupos de endpoints)
        tags = openapi_schema.get('tags', [])
        if tags:
            print(f"🏷️  Tags disponíveis: {', '.join([tag['name'] for tag in tags])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar OpenAPI JSON: {e}")
        return False

if __name__ == "__main__":
    success = generate_openapi_json()
    sys.exit(0 if success else 1)