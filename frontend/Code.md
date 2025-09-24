# Documentação Detalhada do Código - Sistema de Gestão de Projetos

## Visão Geral do Código

Esta documentação detalha minuciosamente toda a implementação do código do Sistema de Gestão de Projetos, incluindo estrutura de arquivos, componentes, lógica de negócio, tipos de dados e padrões implementados.

## 1. Estrutura de Tipos de Dados

### 1.1 Arquivo: `src/types/project.ts`

Este arquivo define toda a tipagem TypeScript do sistema, estabelecendo contratos claros para todas as entidades.

```typescript
// Enums para fases do projeto
export type ProjectPhase = 'inception' | 'definition' | 'built' | 'deploy' | 'close';

// Enums para status do projeto  
export type ProjectStatus = 'active' | 'hold' | 'completed' | 'cancelled';

// Enums para status de tarefas
export type TaskStatus = 'todo' | 'in-progress' | 'done' | 'hold';
```

**Interface Principal - Project**
```typescript
export interface Project {
  // Identificação única e básica
  id: string;                    // UUID único do projeto
  name: string;                  // Nome descritivo do projeto
  client: string;                // Cliente responsável
  
  // Informações comerciais
  orderValue: string;            // Valor do pedido (formato moeda)
  proposal: string;              // Número da proposta
  pct: string;                   // Estimativa de horas (PCT)
  
  // Status e controle
  phase: ProjectPhase;           // Fase atual do projeto
  status: ProjectStatus;         // Status operacional
  
  // Recursos humanos (opcionais até alocação)
  projectManager?: string;       // Gerente de Projeto designado
  technicalLead?: string;        // Líder Técnico designado
  team: string[];               // Array com nomes da equipe
  
  // Controle temporal
  startDate: string;            // Data de início (ISO string)
  estimatedEndDate: string;     // Data estimada de conclusão
  actualEndDate?: string;       // Data real de conclusão (opcional)
  
  // Metadados
  description: string;          // Descrição detalhada do projeto
  createdAt: string;           // Timestamp de criação
  updatedAt: string;           // Timestamp da última atualização
  
  // Relacionamentos (arrays de entidades relacionadas)
  documents: Document[];        // Documentos anexados
  tasks: Task[];               // Tarefas do projeto
  comments: Comment[];         // Comentários e discussões
}
```

**Interface de Documentos**
```typescript
export interface Document {
  id: string;                   // Identificador único
  name: string;                 // Nome do arquivo/documento
  type: string;                 // Tipo (BRD, LLD, As-Built, etc.)
  phase: ProjectPhase;          // Fase à qual pertence
  
  // Controle de status com workflow
  status: 'pending' | 'uploaded' | 'approved' | 'rejected';
  
  // Metadados de arquivo
  url?: string;                 // URL de download/visualização
  version: number;              // Controle de versioning
  comments?: string;            // Comentários da aprovação/rejeição
  
  // Auditoria de upload
  uploadedAt?: string;          // Timestamp do upload
  uploadedBy?: string;          // Usuário que fez upload
  
  // Auditoria de aprovação
  approvedAt?: string;          // Timestamp da aprovação
  approvedBy?: string;          // Usuário que aprovou
}
```

**Interface de Tarefas**
```typescript
export interface Task {
  // Identificação e descrição
  id: string;                   // UUID único da tarefa
  title: string;               // Título conciso da tarefa
  description?: string;        // Descrição detalhada (opcional)
  
  // Estado e atribuição
  status: TaskStatus;          // Status atual (todo, in-progress, done, hold)
  assignedTo?: string;         // Pessoa responsável (opcional)
  phase: ProjectPhase;         // Fase do projeto à qual pertence
  priority: 'low' | 'medium' | 'high' | 'critical'; // Prioridade
  
  // Controle temporal
  dueDate?: string;            // Data de vencimento (opcional)
  createdAt: string;           // Data de criação
  completedAt?: string;        // Data de conclusão (quando aplicável)
  
  // Dependências entre tarefas
  dependencies?: string[];      // IDs de tarefas pré-requisito
}
```

**Interface de Comentários**
```typescript
export interface Comment {
  id: string;                   // Identificador único
  content: string;             // Conteúdo do comentário
  author: string;              // Autor do comentário
  createdAt: string;           // Timestamp de criação
  
  // Funcionalidades avançadas
  mentions?: string[];         // Usuários mencionados (@usuario)
  
  // Categorização por tipo
  type: 'comment' | 'status-change' | 'document-upload' | 'approval';
}
```

**Labels para Interface**
```typescript
// Mapeamento de fases para exibição em português
export const PHASE_LABELS: Record<ProjectPhase, string> = {
  inception: 'Inception',
  definition: 'Definition', 
  built: 'Built',
  deploy: 'Deploy',
  close: 'Close'
};

// Mapeamento de status para exibição em português
export const STATUS_LABELS: Record<ProjectStatus, string> = {
  active: 'Ativo',
  hold: 'Em Espera',
  completed: 'Finalizado',
  cancelled: 'Cancelado'
};
```

### 1.2 Quality Gates Interface
```typescript
export interface QualityGate {
  phase: ProjectPhase;          // Fase à qual se aplica
  requirements: {
    documents: string[];        // Documentos obrigatórios
    tasks: string[];           // Tarefas que devem estar concluídas
    approvals: string[];       // Aprovações necessárias
  };
  completed: boolean;          // Status de completude
}
```

## 2. Camada de Dados Mock

### 2.1 Arquivo: `src/data/mockData.ts`

Este arquivo implementa dados de exemplo e funções utilitárias para simulação do backend.

**Dados Mock Completos**
```typescript
export const mockProjects: Project[] = [
  {
    // Projeto 1: Microsoft 365 Implementation
    id: "1",
    name: "Implementação Microsoft 365",
    client: "Empresa ABC Ltda",
    orderValue: "R$ 75.000,00",
    proposal: "PROP-2024-001",
    pct: "45h",
    phase: "built",                    // Fase atual: Built
    status: "active",                  // Status: Ativo
    projectManager: "João Silva",
    technicalLead: "Maria Santos",
    team: ["João Silva", "Maria Santos", "Pedro Costa"],
    startDate: "2024-01-15",
    estimatedEndDate: "2024-03-30",
    description: "Migração completa do ambiente de e-mail e colaboração para Microsoft 365",
    createdAt: "2024-01-10",
    updatedAt: "2024-02-20",
    
    // Documentos com diferentes status
    documents: [
      {
        id: "doc1",
        name: "BRD v1.2",
        type: "Business Requirements Document",
        phase: "definition",
        status: "approved",            // Documento aprovado
        version: 2,                    // Segunda versão
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
        status: "pending",             // Aguardando aprovação
        version: 1,
        uploadedAt: "2024-02-15",
        uploadedBy: "Pedro Costa"
      }
    ],
    
    // Tarefas com dependências e diferentes status
    tasks: [
      {
        id: "task1",
        title: "Elaborar LLD",
        description: "Criar documento de design detalhado",
        status: "in-progress",         // Em progresso
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
        status: "todo",                // Aguardando início
        assignedTo: "Pedro Costa",
        phase: "built", 
        priority: "medium",
        dueDate: "2024-02-28",
        createdAt: "2024-02-10",
        dependencies: ["task1"]        // Depende da task1
      }
    ],
    
    // Histórico de comentários
    comments: [
      {
        id: "comm1",
        content: "BRD aprovado. Podem prosseguir para a próxima fase.",
        author: "João Silva",
        createdAt: "2024-01-25T10:30:00Z",
        type: "approval"               // Comentário de aprovação
      }
    ]
  },
  
  // Projeto 2: Exchange Online Migration (estrutura similar)
  {
    id: "2", 
    name: "Migração Exchange Online",
    client: "Tech Corp",
    orderValue: "R$ 120.000,00",
    proposal: "PROP-2024-002",
    pct: "80h",
    phase: "deploy",                   // Fase: Deploy
    status: "active",
    projectManager: "Ana Costa",
    technicalLead: "Carlos Oliveira",
    team: ["Ana Costa", "Carlos Oliveira", "Lucas Lima"],
    startDate: "2024-02-01",
    estimatedEndDate: "2024-04-15", 
    description: "Migração de 500 caixas postais para Exchange Online",
    createdAt: "2024-01-25",
    updatedAt: "2024-02-18",
    documents: [],                     // Sem documentos ainda
    tasks: [],                         // Sem tarefas ainda
    comments: []                       // Sem comentários ainda
  },
  
  // Projeto 3: SharePoint Implementation
  {
    id: "3",
    name: "Implementação SharePoint", 
    client: "Indústrias XYZ",
    orderValue: "R$ 95.000,00",
    proposal: "PROP-2024-003",
    pct: "60h",
    phase: "definition",               // Fase: Definition
    status: "hold",                    // Status: Em espera
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
```

**Funções Utilitárias**
```typescript
// Busca projeto por ID específico
export const getProjectById = (id: string): Project | undefined => {
  return mockProjects.find(project => project.id === id);
};

// Filtra projetos por status
export const getProjectsByStatus = (status: string) => {
  return mockProjects.filter(project => project.status === status);
};

// Filtra projetos por fase
export const getProjectsByPhase = (phase: string) => {
  return mockProjects.filter(project => project.phase === phase);
};
```

## 3. Sistema de Design e Estilização

### 3.1 Arquivo: `src/index.css`

Define todo o sistema de design através de CSS custom properties e classes utilitárias.

**Design Tokens Base**
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
@tailwind base;
@tailwind components; 
@tailwind utilities;

@layer base {
  :root {
    /* Sistema de cores semânticas usando HSL */
    --background: 0 0% 100%;              /* Fundo principal branco */
    --foreground: 240 10% 3.9%;          /* Texto principal escuro */
    
    /* Cores primárias da marca */
    --primary: 240 5.9% 10%;             /* Azul escuro principal */
    --primary-foreground: 0 0% 98%;      /* Texto sobre primário */
    
    /* Cores secundárias */  
    --secondary: 240 4.8% 95.9%;         /* Cinza claro */
    --secondary-foreground: 240 5.9% 10%; /* Texto sobre secundário */
    
    /* Cores de destaque */
    --accent: 240 4.8% 95.9%;            /* Accent neutro */
    --accent-foreground: 240 5.9% 10%;   /* Texto sobre accent */
    
    /* Estados e feedback */
    --destructive: 0 84.2% 60.2%;        /* Vermelho para ações destrutivas */
    --destructive-foreground: 0 0% 98%;   /* Texto sobre destrutivo */
    
    /* Elementos de UI */
    --border: 240 5.9% 90%;              /* Bordas padrão */
    --input: 240 5.9% 90%;               /* Fundo de inputs */
    --ring: 240 5% 64.9%;                /* Cor de foco */
    
    /* Componentes específicos */
    --card: 0 0% 100%;                   /* Fundo de cards */
    --card-foreground: 240 10% 3.9%;    /* Texto em cards */
    --popover: 0 0% 100%;                /* Fundo de popovers */
    --popover-foreground: 240 10% 3.9%;  /* Texto em popovers */
    
    /* Elementos mutáveis */
    --muted: 240 4.8% 95.9%;            /* Elementos sem destaque */
    --muted-foreground: 240 3.8% 46.1%;  /* Texto sem destaque */
    
    /* Raio de bordas padrão */
    --radius: 0.5rem;                    /* 8px em rem */
  }

  /* Tema escuro (dark mode) */
  .dark {
    --background: 240 10% 3.9%;          /* Fundo escuro */
    --foreground: 0 0% 98%;              /* Texto claro */
    
    --primary: 0 0% 98%;                 /* Primário invertido */
    --primary-foreground: 240 5.9% 10%;  /* Texto sobre primário */
    
    --secondary: 240 3.7% 15.9%;         /* Secundário escuro */
    --secondary-foreground: 0 0% 98%;     /* Texto sobre secundário */
    
    --accent: 240 3.7% 15.9%;           /* Accent escuro */ 
    --accent-foreground: 0 0% 98%;       /* Texto sobre accent */
    
    --destructive: 0 62.8% 30.6%;       /* Destrutivo mais escuro */
    --destructive-foreground: 0 85.7% 97.3%; /* Texto sobre destrutivo */
    
    --border: 240 3.7% 15.9%;           /* Bordas escuras */
    --input: 240 3.7% 15.9%;            /* Input escuro */
    --ring: 240 4.9% 83.9%;             /* Ring claro */
    
    --card: 240 10% 3.9%;               /* Card escuro */
    --card-foreground: 0 0% 98%;         /* Texto em card */
    --popover: 240 10% 3.9%;            /* Popover escuro */
    --popover-foreground: 0 0% 98%;      /* Texto em popover */
    
    --muted: 240 3.7% 15.9%;            /* Muted escuro */
    --muted-foreground: 240 5% 64.9%;    /* Texto muted */
  }
}

@layer base {
  /* Reset e configurações base */
  * {
    @apply border-border;                /* Aplica cor de borda padrão */
  }
  
  body {
    @apply bg-background text-foreground; /* Aplica cores base */
    font-feature-settings: "rlig" 1, "calt" 1; /* Ligaduras tipográficas */
  }
}
```

**Classes Utilitárias Customizadas**
```css
@layer utilities {
  /* Animação de entrada suave */
  .animate-fade-in {
    animation: fade-in 0.3s ease-out;
  }
  
  @keyframes fade-in {
    from {
      opacity: 0;
      transform: translateY(8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  /* Gradientes personalizados */
  .gradient-primary {
    background: linear-gradient(135deg, hsl(var(--primary)), hsl(var(--primary) / 0.8));
  }
}
```

### 3.2 Arquivo: `tailwind.config.ts`

Configuração do Tailwind CSS integrada com o sistema de design.

```typescript
import type { Config } from "tailwindcss"

const config = {
  // Dark mode baseado em classe
  darkMode: ["class"],
  
  // Arquivos para purging de CSS não utilizado
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  
  prefix: "",    // Sem prefixo para classes
  
  theme: {
    container: {
      center: true,                      // Container centralizado
      padding: "2rem",                   // Padding interno
      screens: {
        "2xl": "1400px",                 // Largura máxima em telas grandes
      },
    },
    
    extend: {
      // Extensão de cores baseada nas CSS custom properties
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))", 
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      
      // Border radius baseado na custom property
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      
      // Animações customizadas
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  
  // Plugins do Tailwind
  plugins: [require("tailwindcss-animate")],
} satisfies Config

export default config
```

## 4. Componentes de Interface

### 4.1 Sistema de Componentes Base (UI Components)

#### 4.1.1 Button Component (`src/components/ui/button.tsx`)

```typescript
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

// Definição de variantes usando CVA (Class Variance Authority)
const buttonVariants = cva(
  // Classes base aplicadas a todos os botões
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      // Variantes de estilo
      variant: {
        default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline: "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      
      // Variantes de tamanho
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs", 
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    
    // Variantes padrão quando não especificadas
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

// Interface para props do componente
export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean    // Permite renderizar como outro elemento
}

// Componente Button com forwardRef para referências
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    // Usa Slot se asChild for true, senão usa button normal
    const Comp = asChild ? Slot : "button"
    
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)

Button.displayName = "Button"

export { Button, buttonVariants }
```

#### 4.1.2 Status Badge Component (`src/components/ui/status-badge.tsx`)

```typescript
import { cn } from "@/lib/utils"
import { cva, type VariantProps } from "class-variance-authority"

// Variantes específicas para badges de status
const statusBadgeVariants = cva(
  "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
  {
    variants: {
      variant: {
        // Status de projetos
        active: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
        hold: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300", 
        completed: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300",
        cancelled: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
        
        // Fases do projeto
        inception: "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300",
        definition: "bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-300",
        built: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300",
        deploy: "bg-teal-100 text-teal-800 dark:bg-teal-900 dark:text-teal-300",
        close: "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300",
        
        // Status de tarefas
        todo: "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300",
        "in-progress": "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300",
        done: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
        
        // Prioridades
        low: "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300",
        medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
        high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300", 
        critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
      },
    },
    defaultVariants: {
      variant: "active",
    },
  }
)

// Props interface com variantes
interface StatusBadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof statusBadgeVariants> {
  children: React.ReactNode
}

// Componente funcional exportado
export function StatusBadge({ className, variant, children, ...props }: StatusBadgeProps) {
  return (
    <div className={cn(statusBadgeVariants({ variant }), className)} {...props}>
      {children}
    </div>
  )
}
```

### 4.2 Componentes de Layout

#### 4.2.1 Navigation Component (`src/components/layout/Navigation.tsx`)

```typescript
import { Link, useLocation } from "react-router-dom"
import { cn } from "@/lib/utils"
import { 
  LayoutDashboard, 
  FolderOpen, 
  BarChart3, 
  Settings,
  Menu,
  X 
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { useState } from "react"

// Definição dos itens de navegação
const navigationItems = [
  {
    name: "Dashboard",
    href: "/dashboard", 
    icon: LayoutDashboard,
    description: "Visão geral do sistema"
  },
  {
    name: "Projetos",
    href: "/projects",
    icon: FolderOpen,
    description: "Gestão de projetos"
  },
  {
    name: "Analytics", 
    href: "/analytics",
    icon: BarChart3,
    description: "Relatórios e métricas"
  },
  {
    name: "Administração",
    href: "/admin",
    icon: Settings,
    description: "Configurações do sistema"
  }
]

export function Navigation() {
  const location = useLocation()          // Hook para rota atual
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  return (
    <nav className="bg-white dark:bg-gray-900 shadow-sm border-b">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          
          {/* Logo e marca */}
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0 flex items-center">
              <div className="h-8 w-8 bg-primary rounded-lg flex items-center justify-center">
                <span className="text-primary-foreground font-bold text-sm">GP</span>
              </div>
              <span className="ml-2 text-xl font-semibold text-gray-900 dark:text-white">
                Gestão de Projetos
              </span>
            </Link>
          </div>

          {/* Navegação desktop */}
          <div className="hidden md:flex md:items-center md:space-x-4">
            {navigationItems.map((item) => {
              const isActive = location.pathname === item.href
              const Icon = item.icon
              
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    "flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors",
                    isActive
                      ? "bg-primary text-primary-foreground"      // Ativo
                      : "text-gray-600 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-300 dark:hover:text-white dark:hover:bg-gray-800"  // Inativo
                  )}
                  title={item.description}
                >
                  <Icon className="h-4 w-4 mr-2" />
                  {item.name}
                </Link>
              )
            })}
          </div>

          {/* Botão do menu mobile */}
          <div className="md:hidden flex items-center">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              aria-label="Abrir menu"
            >
              {isMobileMenuOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </Button>
          </div>
        </div>

        {/* Menu mobile expandido */}
        {isMobileMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              {navigationItems.map((item) => {
                const isActive = location.pathname === item.href
                const Icon = item.icon
                
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={cn(
                      "flex items-center px-3 py-2 rounded-md text-base font-medium transition-colors",
                      isActive
                        ? "bg-primary text-primary-foreground"
                        : "text-gray-600 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-300 dark:hover:text-white dark:hover:bg-gray-800"
                    )}
                    onClick={() => setIsMobileMenuOpen(false)}  // Fecha menu ao clicar
                  >
                    <Icon className="h-5 w-5 mr-3" />
                    <div>
                      <div>{item.name}</div>
                      <div className="text-xs opacity-75">{item.description}</div>
                    </div>
                  </Link>
                )
              })}
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
```

#### 4.2.2 Layout Component (`src/components/layout/Layout.tsx`)

```typescript
import { Outlet } from "react-router-dom"
import { Navigation } from "./Navigation"
import { Toaster } from "@/components/ui/sonner"

// Layout principal que envolve todas as páginas
export function Layout() {
  return (
    <div className="min-h-screen bg-background">
      {/* Navegação fixa no topo */}
      <Navigation />
      
      {/* Conteúdo principal das páginas */}
      <main className="flex-1">
        <Outlet />  {/* Renderiza o componente da rota atual */}
      </main>
      
      {/* Sistema de notificações toast */}
      <Toaster />
    </div>
  )
}
```

### 4.3 Componentes Específicos de Domínio

#### 4.3.1 Kanban Board Component (`src/components/kanban/KanbanBoard.tsx`)

```typescript
import { Task } from "@/types/project"
import { StatusBadge } from "@/components/ui/status-badge"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Calendar, User, AlertCircle } from "lucide-react"
import { format } from "date-fns"
import { ptBR } from "date-fns/locale"

// Props do componente Kanban
interface KanbanBoardProps {
  tasks: Task[]                          // Array de tarefas para exibir
  onTaskUpdate?: (task: Task) => void    // Callback para atualizações
}

// Definição das colunas do Kanban
const columns = [
  { id: 'todo', title: 'A Fazer', status: 'todo' as const },
  { id: 'in-progress', title: 'Em Progresso', status: 'in-progress' as const },
  { id: 'done', title: 'Concluído', status: 'done' as const },
  { id: 'hold', title: 'Em Espera', status: 'hold' as const },
]

export function KanbanBoard({ tasks, onTaskUpdate }: KanbanBoardProps) {
  
  // Função para filtrar tarefas por status
  const getTasksByStatus = (status: string) => {
    return tasks.filter(task => task.status === status)
  }
  
  // Função para determinar se a tarefa está atrasada
  const isTaskOverdue = (task: Task) => {
    if (!task.dueDate) return false
    return new Date(task.dueDate) < new Date() && task.status !== 'done'
  }
  
  // Função para obter cor da prioridade
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'destructive'
      case 'high': return 'default'
      case 'medium': return 'secondary'
      case 'low': return 'outline'
      default: return 'secondary'
    }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 p-6">
      {columns.map((column) => {
        const columnTasks = getTasksByStatus(column.status)
        
        return (
          <div key={column.id} className="flex flex-col">
            {/* Cabeçalho da coluna */}
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-lg">{column.title}</h3>
              <Badge variant="secondary" className="ml-2">
                {columnTasks.length}
              </Badge>
            </div>
            
            {/* Lista de tarefas da coluna */}
            <div className="flex-1 space-y-3">
              {columnTasks.length === 0 ? (
                // Estado vazio
                <div className="text-center py-8 text-muted-foreground">
                  <p className="text-sm">Nenhuma tarefa</p>
                </div>
              ) : (
                // Renderização das tarefas
                columnTasks.map((task) => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    isOverdue={isTaskOverdue(task)}
                    priorityColor={getPriorityColor(task.priority)}
                    onUpdate={onTaskUpdate}
                  />
                ))
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}

// Componente para card individual de tarefa
interface TaskCardProps {
  task: Task
  isOverdue: boolean
  priorityColor: string
  onUpdate?: (task: Task) => void
}

function TaskCard({ task, isOverdue, priorityColor, onUpdate }: TaskCardProps) {
  return (
    <Card className={`cursor-pointer transition-all hover:shadow-md ${
      isOverdue ? 'border-destructive bg-destructive/5' : ''
    }`}>
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between">
          <CardTitle className="text-sm font-medium line-clamp-2">
            {task.title}
          </CardTitle>
          {isOverdue && (
            <AlertCircle className="h-4 w-4 text-destructive flex-shrink-0 ml-2" />
          )}
        </div>
        
        {task.description && (
          <CardDescription className="text-xs line-clamp-2">
            {task.description}
          </CardDescription>
        )}
      </CardHeader>
      
      <CardContent className="pt-0">
        <div className="space-y-2">
          
          {/* Badge de prioridade */}
          <div className="flex items-center gap-2">
            <StatusBadge variant={task.priority as any}>
              {task.priority.toUpperCase()}
            </StatusBadge>
            <StatusBadge variant={task.phase as any}>
              {task.phase}
            </StatusBadge>
          </div>
          
          {/* Informações adicionais */}
          <div className="space-y-1 text-xs text-muted-foreground">
            
            {/* Responsável */}
            {task.assignedTo && (
              <div className="flex items-center gap-1">
                <User className="h-3 w-3" />
                <span>{task.assignedTo}</span>
              </div>
            )}
            
            {/* Data de vencimento */}
            {task.dueDate && (
              <div className={`flex items-center gap-1 ${
                isOverdue ? 'text-destructive' : ''
              }`}>
                <Calendar className="h-3 w-3" />
                <span>
                  {format(new Date(task.dueDate), 'dd/MM/yyyy', { locale: ptBR })}
                </span>
              </div>
            )}
          </div>
          
          {/* Indicador de dependências */}
          {task.dependencies && task.dependencies.length > 0 && (
            <div className="text-xs text-muted-foreground">
              <span>Depende de {task.dependencies.length} tarefa(s)</span>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
```

## 5. Páginas Principais

### 5.1 Dashboard (`src/pages/Dashboard.tsx`)

```typescript
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { StatusBadge } from "@/components/ui/status-badge"
import { Button } from "@/components/ui/button"
import { mockProjects } from "@/data/mockData"
import { Project } from "@/types/project"
import { 
  FolderOpen, 
  Users, 
  Clock, 
  AlertTriangle,
  TrendingUp,
  CheckCircle,
  Plus
} from "lucide-react"
import { Link } from "react-router-dom"

export function Dashboard() {
  
  // Cálculos de métricas baseadas nos dados mock
  const totalProjects = mockProjects.length
  const activeProjects = mockProjects.filter(p => p.status === 'active').length
  const completedProjects = mockProjects.filter(p => p.status === 'completed').length
  const onHoldProjects = mockProjects.filter(p => p.status === 'hold').length
  
  // Projetos recentes (ordenados por data de atualização)
  const recentProjects = [...mockProjects]
    .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
    .slice(0, 5)
  
  // Projetos com possível atraso (estimativa próxima ou passada)
  const projectsAtRisk = mockProjects.filter(project => {
    if (project.status === 'completed') return false
    const estimatedEnd = new Date(project.estimatedEndDate)
    const today = new Date()
    const daysUntilDeadline = Math.ceil((estimatedEnd.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
    return daysUntilDeadline <= 30 && daysUntilDeadline >= 0
  })

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      
      {/* Cabeçalho da página */}
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <div className="flex items-center space-x-2">
          <Button asChild>
            <Link to="/projects">
              <Plus className="mr-2 h-4 w-4" />
              Novo Projeto
            </Link>
          </Button>
        </div>
      </div>
      
      {/* Cards de métricas */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        
        {/* Total de Projetos */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Projetos</CardTitle>
            <FolderOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalProjects}</div>
            <p className="text-xs text-muted-foreground">
              Em todo o portfólio
            </p>
          </CardContent>
        </Card>
        
        {/* Projetos Ativos */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Projetos Ativos</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{activeProjects}</div>
            <p className="text-xs text-muted-foreground">
              Em execução
            </p>
          </CardContent>
        </Card>
        
        {/* Projetos Finalizados */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Finalizados</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{completedProjects}</div>
            <p className="text-xs text-muted-foreground">
              Entregues com sucesso
            </p>
          </CardContent>
        </Card>
        
        {/* Projetos em Espera */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Em Espera</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{onHoldProjects}</div>
            <p className="text-xs text-muted-foreground">
              Aguardando liberação
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        
        {/* Lista de Projetos Recentes */}
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Projetos Recentes</CardTitle>
            <CardDescription>
              Últimas atualizações nos projetos
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentProjects.map((project) => (
                <ProjectRow key={project.id} project={project} />
              ))}
            </div>
          </CardContent>
        </Card>
        
        {/* Alertas e Projetos de Atenção */}
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-yellow-500" />
              Projetos de Atenção
            </CardTitle>
            <CardDescription>
              Projetos com prazo próximo ou outros alertas
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {projectsAtRisk.length === 0 ? (
                <div className="text-sm text-muted-foreground text-center py-4">
                  Nenhum projeto requer atenção especial no momento.
                </div>
              ) : (
                projectsAtRisk.map((project) => (
                  <div key={project.id} className="flex items-center space-x-3 p-3 rounded-lg border">
                    <div className="flex-1 space-y-1">
                      <p className="text-sm font-medium">{project.name}</p>
                      <p className="text-xs text-muted-foreground">{project.client}</p>
                      <StatusBadge variant={project.phase as any}>
                        {project.phase}
                      </StatusBadge>
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

// Componente para linha de projeto na lista
interface ProjectRowProps {
  project: Project
}

function ProjectRow({ project }: ProjectRowProps) {
  return (
    <div className="flex items-center space-x-4 p-4 rounded-lg border hover:bg-muted/50 transition-colors">
      <div className="flex-1 space-y-1">
        <div className="flex items-center justify-between">
          <Link 
            to={`/projects/${project.id}`}
            className="text-sm font-medium hover:underline"
          >
            {project.name}
          </Link>
          <StatusBadge variant={project.status as any}>
            {project.status}
          </StatusBadge>
        </div>
        
        <div className="flex items-center space-x-4 text-xs text-muted-foreground">
          <span>{project.client}</span>
          <span>•</span>
          <span>{project.orderValue}</span>
          <span>•</span>
          <StatusBadge variant={project.phase as any}>
            {project.phase}
          </StatusBadge>
        </div>
        
        <div className="flex items-center space-x-2 text-xs text-muted-foreground">
          {project.projectManager && (
            <>
              <Users className="h-3 w-3" />
              <span>GP: {project.projectManager}</span>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
```

## 6. Utilitários e Configurações

### 6.1 Utilitários (`src/lib/utils.ts`)

```typescript
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

// Função utilitária para combinar classes CSS de forma inteligente
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Função para formatação de datas em português
export function formatDate(date: string | Date): string {
  const d = new Date(date)
  return d.toLocaleDateString('pt-BR', {
    year: 'numeric',
    month: '2-digit', 
    day: '2-digit'
  })
}

// Função para calcular dias entre duas datas
export function daysBetween(date1: string | Date, date2: string | Date): number {
  const d1 = new Date(date1)
  const d2 = new Date(date2)
  const diffTime = Math.abs(d2.getTime() - d1.getTime())
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
}

// Função para verificar se data está no futuro
export function isFutureDate(date: string | Date): boolean {
  return new Date(date) > new Date()
}

// Função para gerar ID único simples
export function generateId(): string {
  return Math.random().toString(36).substr(2, 9)
}

// Função para truncar texto
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text
  return text.substr(0, maxLength) + '...'
}

// Função para validar email
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

// Função para capitalizar primeira letra
export function capitalize(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1)
}

// Função para converter string para slug
export function slugify(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')
    .replace(/[^\w\-]+/g, '')
    .replace(/\-\-+/g, '-')
}
```

### 6.2 Configuração Principal (`src/App.tsx`)

```typescript
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import { Layout } from "./components/layout/Layout"
import { Index } from "./pages/Index"
import { Dashboard } from "./pages/Dashboard"
import { Projects } from "./pages/Projects"
import { ProjectDetail } from "./pages/ProjectDetail"
import { Analytics } from "./pages/Analytics"
import { Admin } from "./pages/Admin"
import { NotFound } from "./pages/NotFound"

// Configuração completa do roteamento
const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,                     // Layout wrapper para todas as rotas
    children: [
      {
        index: true,                         // Rota raiz "/"
        element: <Index />,
      },
      {
        path: "dashboard",                   // "/dashboard"
        element: <Dashboard />,
      },
      {
        path: "projects",                    // "/projects"
        element: <Projects />,
      },
      {
        path: "projects/:id",               // "/projects/1", "/projects/2", etc.
        element: <ProjectDetail />,
      },
      {
        path: "analytics",                   // "/analytics"
        element: <Analytics />,
      },
      {
        path: "admin",                       // "/admin"
        element: <Admin />,
      },
    ],
  },
  {
    path: "*",                              // Catch-all para 404
    element: <NotFound />,
  },
])

// Componente principal da aplicação
function App() {
  return <RouterProvider router={router} />
}

export default App
```

### 6.3 Ponto de Entrada (`src/main.tsx`)

```typescript
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'

// Renderização da aplicação no DOM
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

## 7. Configurações de Build e Desenvolvimento

### 7.1 Configuração Vite (`vite.config.ts`)

```typescript
import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),  // Alias para imports absolutos
    },
  },
})
```

### 7.2 Configuração HTML (`index.html`)

```html
<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Sistema completo de gestão de projetos com controle de qualidade e automatização de fluxos" />
    <meta name="keywords" content="gestão projetos, qualidade, automação, workflow" />
    <title>Sistema de Gestão de Projetos</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

## 8. Padrões e Convenções Implementados

### 8.1 Padrões de Nomenclatura

**Arquivos e Pastas**
- Componentes: PascalCase (`Dashboard.tsx`, `ProjectDetail.tsx`)
- Utilitários: camelCase (`utils.ts`, `mockData.ts`)
- Pastas: kebab-case quando apropriado, PascalCase para componentes

**Variáveis e Funções**
- Variáveis: camelCase (`projectManager`, `estimatedEndDate`)
- Constantes: UPPER_SNAKE_CASE (`PHASE_LABELS`, `STATUS_LABELS`)
- Funções: camelCase (`getProjectById`, `formatDate`)
- Componentes: PascalCase (`Dashboard`, `KanbanBoard`)

**Interfaces e Types**
- Interfaces: PascalCase (`Project`, `Task`, `Document`)
- Union Types: camelCase (`ProjectPhase`, `ProjectStatus`)
- Props Interfaces: PascalCase + "Props" suffix (`ButtonProps`, `KanbanBoardProps`)

### 8.2 Estrutura de Componentes

**Padrão de Organização Interna**
```typescript
// 1. Imports externos
import React from 'react'
import { Link } from 'react-router-dom'

// 2. Imports internos (UI components)
import { Button } from '@/components/ui/button'

// 3. Imports de tipos
import { Project } from '@/types/project'

// 4. Imports de utilitários
import { cn } from '@/lib/utils'

// 5. Definição de interfaces
interface ComponentProps {
  // ...
}

// 6. Componente principal
export function Component({ ...props }: ComponentProps) {
  // ...
}

// 7. Sub-componentes (se houver)
function SubComponent() {
  // ...
}
```

### 8.3 Padrões de Estado e Props

**Gerenciamento de Estado Local**
```typescript
// Estado simples
const [projects, setProjects] = useState<Project[]>([])

// Estado com tipo explícito
const [loading, setLoading] = useState<boolean>(false)

// Estado com valor inicial baseado em dados
const [activeTab, setActiveTab] = useState<string>('overview')
```

**Passagem de Props**
```typescript
// Props obrigatórias e opcionais claramente definidas
interface Props {
  project: Project              // Obrigatória
  onUpdate?: (p: Project) => void  // Opcional
  className?: string           // Opcional com padrão
}

// Desestruturação com valores padrão
function Component({ 
  project, 
  onUpdate, 
  className = "" 
}: Props) {
  // ...
}
```

### 8.4 Tratamento de Erros e Loading States

**Estados de Loading**
```typescript
function Component() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  if (loading) return <div>Carregando...</div>
  if (error) return <div>Erro: {error}</div>
  
  return <div>{/* Conteúdo normal */}</div>
}
```

**Estados Vazios**
```typescript
{projects.length === 0 ? (
  <div className="text-center py-8">
    <p className="text-muted-foreground">Nenhum projeto encontrado</p>
  </div>
) : (
  <div>{/* Lista de projetos */}</div>
)}
```

## 9. Performance e Otimizações Implementadas

### 9.1 Otimizações de Renderização

**Memoização de Componentes**
```typescript
import { memo } from 'react'

// Componente memorizado para evitar re-renders desnecessários
const TaskCard = memo(({ task, onUpdate }: TaskCardProps) => {
  // ...
})
```

**Callbacks Otimizados**
```typescript
import { useCallback } from 'react'

function Component() {
  // Callback memorizado para evitar re-criação
  const handleTaskUpdate = useCallback((task: Task) => {
    // lógica de atualização
  }, [/* dependências */])
  
  return <TaskCard onUpdate={handleTaskUpdate} />
}
```

### 9.2 Otimizações de Bundle

**Code Splitting por Rota**
```typescript
// Carregamento lazy de páginas grandes
const Analytics = lazy(() => import('./pages/Analytics'))
const Admin = lazy(() => import('./pages/Admin'))

// Wrapper com Suspense
<Suspense fallback={<div>Carregando...</div>}>
  <Analytics />
</Suspense>
```

**Tree Shaking**
- Imports específicos: `import { Button } from '@/components/ui/button'`
- Evitar imports de barrel: `import * as utils from './utils'`

### 9.3 Otimizações de CSS

**Purging de CSS não utilizado**
- Tailwind configurado para remover classes não utilizadas
- Classes dinâmicas em safelist quando necessário

**CSS-in-JS minimizado**
- Uso de class-variance-authority para variantes
- Merge inteligente de classes com tailwind-merge

## 10. Considerações de Acessibilidade

### 10.1 Semântica HTML

**Uso correto de elementos semânticos**
```html
<nav>          <!-- Navegação -->
<main>         <!-- Conteúdo principal -->
<section>      <!-- Seções de conteúdo -->
<article>      <!-- Artigos independentes -->
<aside>        <!-- Conteúdo relacionado -->
<header>       <!-- Cabeçalho -->
<footer>       <!-- Rodapé -->
```

### 10.2 ARIA e Acessibilidade

**Atributos ARIA implementados**
```typescript
// Labels descritivos
<Button aria-label="Abrir menu de navegação">
  <Menu className="h-6 w-6" />
</Button>

// Estados de componentes
<div role="tabpanel" aria-labelledby="tab-projects">
  {/* Conteúdo */}
</div>
```

### 10.3 Navegação por Teclado

**Focus management**
- Ordem de tab lógica e intuitiva
- Indicadores visuais de foco
- Escape para fechar modals e menus

**Shortcuts implementados**
- Enter/Space para ativação de botões
- Arrow keys para navegação em listas
- Escape para cancelar ações

Este documento representa uma visão completa e detalhada de toda a implementação do código do Sistema de Gestão de Projetos, desde os tipos de dados fundamentais até as otimizações de performance e acessibilidade.