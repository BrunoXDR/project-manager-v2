import { Project, Task, Document, Comment } from "@/types/project";

export const mockProjects: Project[] = [
  {
    id: "1",
    name: "Implementação Microsoft 365",
    client: "Empresa ABC Ltda",
    orderValue: "R$ 75.000,00",
    proposal: "PROP-2024-001",
    pct: "45h",
    phase: "built",
    status: "active",
    projectManager: "João Silva",
    technicalLead: "Maria Santos",
    team: ["João Silva", "Maria Santos", "Pedro Costa"],
    startDate: "2024-01-15",
    estimatedEndDate: "2024-03-30",
    description: "Migração completa do ambiente de e-mail e colaboração para Microsoft 365",
    createdAt: "2024-01-10",
    updatedAt: "2024-02-20",
    documents: [
      {
        id: "doc1",
        name: "BRD v1.2",
        type: "Business Requirements Document",
        phase: "definition",
        status: "approved",
        version: 2,
        uploadedAt: "2024-01-20",
        uploadedBy: "Maria Santos",
        approvedAt: "2024-01-25",
        approvedBy: "João Silva"
      },
      {
        id: "doc2",
        name: "LLD v1.0",
        type: "Low Level Design",
        phase: "built",
        status: "pending",
        version: 1,
        uploadedAt: "2024-02-15",
        uploadedBy: "Pedro Costa"
      }
    ],
    tasks: [
      {
        id: "task1",
        title: "Elaborar LLD",
        description: "Criar documento de design detalhado",
        status: "in-progress",
        assignedTo: "Pedro Costa",
        phase: "built",
        priority: "high",
        dueDate: "2024-02-25",
        createdAt: "2024-02-10"
      },
      {
        id: "task2",
        title: "Submeter LLD para Aprovação",
        description: "Enviar LLD para aprovação do GP",
        status: "todo",
        assignedTo: "Pedro Costa",
        phase: "built",
        priority: "medium",
        dueDate: "2024-02-28",
        createdAt: "2024-02-10",
        dependencies: ["task1"]
      }
    ],
    comments: [
      {
        id: "comm1",
        content: "BRD aprovado. Podem prosseguir para a próxima fase.",
        author: "João Silva",
        createdAt: "2024-01-25T10:30:00Z",
        type: "approval"
      }
    ]
  },
  {
    id: "2",
    name: "Migração Exchange Online",
    client: "Tech Corp",
    orderValue: "R$ 120.000,00",
    proposal: "PROP-2024-002",
    pct: "80h",
    phase: "deploy",
    status: "active",
    projectManager: "Ana Costa",
    technicalLead: "Carlos Oliveira",
    team: ["Ana Costa", "Carlos Oliveira", "Lucas Lima"],
    startDate: "2024-02-01",
    estimatedEndDate: "2024-04-15",
    description: "Migração de 500 caixas postais para Exchange Online",
    createdAt: "2024-01-25",
    updatedAt: "2024-02-18",
    documents: [],
    tasks: [],
    comments: []
  },
  {
    id: "3",
    name: "Implementação SharePoint",
    client: "Indústrias XYZ",
    orderValue: "R$ 95.000,00",
    proposal: "PROP-2024-003",
    pct: "60h",
    phase: "definition",
    status: "hold",
    projectManager: "Roberto Lima",
    technicalLead: "Fernanda Silva",
    team: ["Roberto Lima", "Fernanda Silva"],
    startDate: "2024-02-10",
    estimatedEndDate: "2024-05-20",
    description: "Implementação de portal colaborativo com SharePoint Online",
    createdAt: "2024-02-05",
    updatedAt: "2024-02-15",
    documents: [],
    tasks: [],
    comments: []
  }
];

export const getProjectById = (id: string): Project | undefined => {
  return mockProjects.find(project => project.id === id);
};

export const getProjectsByStatus = (status: string) => {
  return mockProjects.filter(project => project.status === status);
};

export const getProjectsByPhase = (phase: string) => {
  return mockProjects.filter(project => project.phase === phase);
};