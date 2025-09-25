# Documentação da API - Project Manager

Esta pasta contém os artefatos de documentação da API do Project Manager gerados durante o Sprint 21.

## Arquivos Disponíveis

### 📄 openapi.json
Especificação OpenAPI 3.0 completa da API, contendo:
- **28 endpoints** documentados com descrições detalhadas
- **22 rotas** organizadas por funcionalidade
- Schemas Pydantic enriquecidos com exemplos
- Definições de autenticação e autorização
- Códigos de resposta e modelos de erro

**Uso:**
- Importar em ferramentas como Swagger Editor
- Gerar clientes SDK automaticamente
- Validação de contratos de API

### 📮 postman_collection.json
Coleção Postman completa com todas as requisições da API, organizada em:
- **9 pastas** por funcionalidade:
  - Authentication
  - Projects
  - Users
  - Tasks
  - Documents
  - Analytics
  - Notifications
  - Admin: Audit Logs
  - Health

**Características:**
- Variáveis de ambiente configuradas (`baseUrl`, `token`)
- Autenticação Bearer Token automática
- Exemplos de body para requisições POST/PUT
- Parâmetros de query pré-configurados

**Como usar:**
1. Importar o arquivo no Postman
2. Configurar a variável `baseUrl` (padrão: http://localhost:8002)
3. Fazer login no endpoint `/auth/token` para obter o token
4. Copiar o token para a variável `token`
5. Testar os endpoints

## Documentação Interativa

A documentação Swagger UI está disponível em:
- **Swagger UI:** http://localhost:8002/docs
- **ReDoc:** http://localhost:8002/redoc

## Geração dos Arquivos

Os arquivos são gerados automaticamente através dos scripts:
- `../generate_openapi.py` - Gera o openapi.json
- `../generate_postman.py` - Gera a coleção Postman

Para regenerar a documentação:
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Gerar OpenAPI
PYTHONPATH=src python3 generate_openapi.py

# Gerar Postman Collection
python3 generate_postman.py
```

## Melhorias Implementadas no Sprint 21

✅ **Schemas Pydantic Enriquecidos**
- Descrições detalhadas para todos os campos
- Exemplos realistas para facilitar testes
- Validações documentadas

✅ **Endpoints Documentados**
- Summary e description para todos os 28 endpoints
- Códigos de resposta explicados
- Requisitos de autenticação clarificados

✅ **Organização por Funcionalidade**
- Agrupamento lógico por tags
- Estrutura consistente na coleção Postman
- Navegação intuitiva na documentação

---

*Documentação gerada automaticamente durante o Sprint 21 - API Documentation*