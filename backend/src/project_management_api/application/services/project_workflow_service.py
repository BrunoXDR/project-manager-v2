from typing import List
from ...domain.models import Project, ProjectPhase, Document
from .quality_gates import PHASE_ORDER, QUALITY_GATE_RULES

# 1. Defina uma exceção customizada para falhas de Quality Gate
class QualityGateNotPassedError(Exception):
    def __init__(self, message: str, missing_requirements: List[str]):
        super().__init__(message)
        self.missing_requirements = missing_requirements

class ProjectWorkflowService:
    # 2. Implemente o método privado de validação
    def _validate_gate(self, project: Project, documents: List[Document]):
        """Verifica se os pré-requisitos da fase atual foram atendidos."""
        current_phase = project.phase
        if current_phase not in QUALITY_GATE_RULES:
            return  # Nenhuma regra para esta fase, passagem livre

        rules = QUALITY_GATE_RULES[current_phase]
        missing_reqs = []

        # Valida documentos obrigatórios
        for req_doc in rules.get("required_docs", []):
            is_doc_found = any(
                doc.type == req_doc["type"] and doc.status == req_doc["status"]
                for doc in documents
            )
            if not is_doc_found:
                missing_reqs.append(
                    f"Documento obrigatório: Tipo '{req_doc['type']}' com status '{req_doc['status'].value}'."
                )
        
        # Futuramente, podemos adicionar validação de tarefas aqui.
        
        if missing_reqs:
            raise QualityGateNotPassedError(
                message=f"Quality Gate para a fase '{current_phase.value}' falhou.",
                missing_requirements=missing_reqs
            )

    # 3. Atualize o método principal para usar a validação
    def advance_phase(self, project: Project, documents: List[Document]) -> Project:
        """Tenta avançar o projeto para a próxima fase após validar o Quality Gate."""
        if project.phase == ProjectPhase.CLOSE:
            return project

        # Chama a nova lógica de validação antes de qualquer ação
        self._validate_gate(project, documents)

        try:
            current_index = PHASE_ORDER.index(project.phase)
            if current_index < len(PHASE_ORDER) - 1:
                next_phase = PHASE_ORDER[current_index + 1]
                project.phase = next_phase
        except ValueError:
            raise ValueError("Fase atual do projeto é inválida ou não sequenciada.")
            
        return project