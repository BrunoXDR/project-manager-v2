export type ProjectPhase = 'inception' | 'definition' | 'built' | 'deploy' | 'close';

export type ProjectStatus = 'active' | 'hold' | 'completed' | 'cancelled';

export type TaskStatus = 'todo' | 'in-progress' | 'done' | 'hold';

export interface Project {
  id: string;
  name: string;
  client: string;
  orderValue: string;
  proposal: string;
  pct: string;
  phase: ProjectPhase;
  status: ProjectStatus;
  projectManager?: string;
  technicalLead?: string;
  team: string[];
  startDate: string;
  estimatedEndDate: string;
  actualEndDate?: string;
  description: string;
  createdAt: string;
  updatedAt: string;
  documents: Document[];
  tasks: Task[];
  comments: Comment[];
}

export interface Document {
  id: string;
  name: string;
  type: string;
  phase: ProjectPhase;
  status: 'pending' | 'uploaded' | 'approved' | 'rejected';
  url?: string;
  uploadedAt?: string;
  uploadedBy?: string;
  approvedAt?: string;
  approvedBy?: string;
  version: number;
  comments?: string;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: TaskStatus;
  assignedTo?: string;
  phase: ProjectPhase;
  priority: 'low' | 'medium' | 'high' | 'critical';
  dueDate?: string;
  createdAt: string;
  completedAt?: string;
  dependencies?: string[];
}

export interface Comment {
  id: string;
  content: string;
  author: string;
  createdAt: string;
  mentions?: string[];
  type: 'comment' | 'status-change' | 'document-upload' | 'approval';
}

export interface QualityGate {
  phase: ProjectPhase;
  requirements: {
    documents: string[];
    tasks: string[];
    approvals: string[];
  };
  completed: boolean;
}

export const PHASE_LABELS: Record<ProjectPhase, string> = {
  inception: 'Inception',
  definition: 'Definition', 
  built: 'Built',
  deploy: 'Deploy',
  close: 'Close'
};

export const STATUS_LABELS: Record<ProjectStatus, string> = {
  active: 'Ativo',
  hold: 'Em Espera',
  completed: 'Finalizado',
  cancelled: 'Cancelado'
};