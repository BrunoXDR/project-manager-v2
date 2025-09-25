# src/project_management_api/application/services/quality_gates.py
from project_management_api.domain.models import ProjectPhase, DocumentStatus, TaskStatus

# Esta estrutura define os pré-requisitos para SAIR de uma fase e ir para a próxima.
QUALITY_GATE_RULES = {
    ProjectPhase.DEFINITION: {
        "required_docs": [
            {"type": "BRD", "status": DocumentStatus.APPROVED},
        ],
        "required_tasks_status": [
            # Exemplo: Adicionar aqui tarefas que devem estar 'DONE'
        ]
    },
    ProjectPhase.BUILT: {
        "required_docs": [
            {"type": "LLD", "status": DocumentStatus.APPROVED},
        ],
    },
    # Adicionar outras regras para INCEPTION, DEPLOY, etc. conforme a necessidade.
}

# Ordem de progressão das fases
PHASE_ORDER = [
    ProjectPhase.INCEPTION,
    ProjectPhase.DEFINITION,
    ProjectPhase.BUILT,
    ProjectPhase.DEPLOY,
    ProjectPhase.CLOSE,
]