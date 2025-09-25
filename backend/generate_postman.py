#!/usr/bin/env python3
"""
Script para gerar uma coleção Postman a partir do arquivo OpenAPI JSON.
Este script converte a especificação OpenAPI em uma coleção Postman utilizável.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List
import uuid

def convert_openapi_to_postman(openapi_spec: Dict[str, Any]) -> Dict[str, Any]:
    """Converte especificação OpenAPI para formato de coleção Postman."""
    
    # Informações básicas da coleção
    collection = {
        "info": {
            "name": openapi_spec.get("info", {}).get("title", "API Collection"),
            "description": openapi_spec.get("info", {}).get("description", ""),
            "version": openapi_spec.get("info", {}).get("version", "1.0.0"),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [],
        "variable": [
            {
                "key": "baseUrl",
                "value": "http://localhost:8002",
                "type": "string"
            },
            {
                "key": "token",
                "value": "",
                "type": "string"
            }
        ]
    }
    
    # Agrupar endpoints por tags
    paths = openapi_spec.get("paths", {})
    folders = {}
    
    for path, methods in paths.items():
        for method, details in methods.items():
            if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                # Determinar pasta (tag)
                tags = details.get("tags", ["Default"])
                folder_name = tags[0] if tags else "Default"
                
                if folder_name not in folders:
                    folders[folder_name] = {
                        "name": folder_name,
                        "item": []
                    }
                
                # Criar item da requisição
                request_item = create_postman_request(path, method, details, openapi_spec)
                folders[folder_name]["item"].append(request_item)
    
    # Adicionar pastas à coleção
    collection["item"] = list(folders.values())
    
    return collection

def create_postman_request(path: str, method: str, details: Dict[str, Any], openapi_spec: Dict[str, Any]) -> Dict[str, Any]:
    """Cria um item de requisição Postman."""
    
    # Substituir parâmetros de path por variáveis Postman
    postman_path = path.replace("{", ":").replace("}", "")
    
    request = {
        "name": details.get("summary", f"{method.upper()} {path}"),
        "request": {
            "method": method.upper(),
            "header": [],
            "url": {
                "raw": "{{baseUrl}}" + postman_path,
                "host": ["{{baseUrl}}"],
                "path": [p for p in postman_path.strip("/").split("/") if p]
            }
        },
        "response": []
    }
    
    # Adicionar descrição se disponível
    if details.get("description"):
        request["request"]["description"] = details["description"]
    
    # Adicionar autenticação se necessário
    if details.get("security") or any("Authorization" in str(param) for param in details.get("parameters", [])):
        request["request"]["auth"] = {
            "type": "bearer",
            "bearer": [
                {
                    "key": "token",
                    "value": "{{token}}",
                    "type": "string"
                }
            ]
        }
    
    # Adicionar parâmetros de query
    parameters = details.get("parameters", [])
    query_params = [p for p in parameters if p.get("in") == "query"]
    if query_params:
        request["request"]["url"]["query"] = []
        for param in query_params:
            request["request"]["url"]["query"].append({
                "key": param["name"],
                "value": param.get("example", ""),
                "description": param.get("description", ""),
                "disabled": not param.get("required", False)
            })
    
    # Adicionar body para métodos POST/PUT/PATCH
    if method.upper() in ["POST", "PUT", "PATCH"]:
        request_body = details.get("requestBody")
        if request_body:
            content = request_body.get("content", {})
            if "application/json" in content:
                request["request"]["header"].append({
                    "key": "Content-Type",
                    "value": "application/json"
                })
                
                # Tentar gerar exemplo do body
                schema = content["application/json"].get("schema", {})
                example_body = generate_example_from_schema(schema, openapi_spec)
                
                request["request"]["body"] = {
                    "mode": "raw",
                    "raw": json.dumps(example_body, indent=2),
                    "options": {
                        "raw": {
                            "language": "json"
                        }
                    }
                }
            elif "multipart/form-data" in content:
                request["request"]["body"] = {
                    "mode": "formdata",
                    "formdata": [
                        {
                            "key": "file",
                            "type": "file",
                            "src": []
                        }
                    ]
                }
    
    return request

def generate_example_from_schema(schema: Dict[str, Any], openapi_spec: Dict[str, Any]) -> Any:
    """Gera um exemplo a partir de um schema OpenAPI."""
    
    if "$ref" in schema:
        # Resolver referência
        ref_path = schema["$ref"].replace("#/", "").split("/")
        ref_schema = openapi_spec
        for part in ref_path:
            ref_schema = ref_schema.get(part, {})
        return generate_example_from_schema(ref_schema, openapi_spec)
    
    schema_type = schema.get("type", "object")
    
    if schema_type == "object":
        example = {}
        properties = schema.get("properties", {})
        for prop_name, prop_schema in properties.items():
            if "example" in prop_schema:
                example[prop_name] = prop_schema["example"]
            else:
                example[prop_name] = generate_example_from_schema(prop_schema, openapi_spec)
        return example
    
    elif schema_type == "array":
        items_schema = schema.get("items", {})
        return [generate_example_from_schema(items_schema, openapi_spec)]
    
    elif schema_type == "string":
        return schema.get("example", "string")
    
    elif schema_type == "integer":
        return schema.get("example", 0)
    
    elif schema_type == "number":
        return schema.get("example", 0.0)
    
    elif schema_type == "boolean":
        return schema.get("example", True)
    
    else:
        return schema.get("example", None)

def generate_postman_collection():
    """Gera a coleção Postman a partir do arquivo OpenAPI JSON."""
    try:
        # Ler arquivo OpenAPI
        openapi_file = Path(__file__).parent / "docs" / "openapi.json"
        if not openapi_file.exists():
            print("❌ Arquivo openapi.json não encontrado. Execute primeiro o generate_openapi.py")
            return False
        
        with open(openapi_file, "r", encoding="utf-8") as f:
            openapi_spec = json.load(f)
        
        # Converter para Postman
        postman_collection = convert_openapi_to_postman(openapi_spec)
        
        # Salvar coleção Postman
        postman_file = Path(__file__).parent / "docs" / "postman_collection.json"
        with open(postman_file, "w", encoding="utf-8") as f:
            json.dump(postman_collection, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Coleção Postman gerada com sucesso: {postman_file}")
        print(f"📁 Total de pastas: {len(postman_collection['item'])}")
        
        total_requests = sum(len(folder['item']) for folder in postman_collection['item'])
        print(f"🔗 Total de requisições: {total_requests}")
        
        # Listar pastas
        folder_names = [folder['name'] for folder in postman_collection['item']]
        print(f"📂 Pastas criadas: {', '.join(folder_names)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar coleção Postman: {e}")
        return False

if __name__ == "__main__":
    success = generate_postman_collection()
    sys.exit(0 if success else 1)