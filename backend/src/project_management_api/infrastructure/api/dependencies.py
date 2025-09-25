# src/project_management_api/infrastructure/api/dependencies.py
from fastapi import Query
from typing import Dict

def get_pagination_params(
    page: int = Query(1, gt=0, description="Número da página"),
    size: int = Query(20, gt=0, le=100, description="Tamanho da página")
) -> Dict[str, int]:
    return {"page": page, "size": size}