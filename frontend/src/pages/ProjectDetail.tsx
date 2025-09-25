import { useParams, Link } from "react-router-dom";
import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { StatusBadge } from "@/components/ui/status-badge";
import { projectsAPI, Project } from "@/lib/apiClient";
import { ProjectStatus } from "@/types/project";
import { 
  ArrowLeft, 
  Calendar, 
  DollarSign, 
  Users, 
  FileText, 
  MessageSquare,
  Settings,
  CheckCircle,
  Clock,
  AlertTriangle,
  Target,
  TrendingUp
} from "lucide-react";

const ProjectDetail = () => {
  const { id } = useParams<{ id: string }>();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProject = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError(null);
        
        const projectData = await projectsAPI.getProject(id);
        setProject(projectData);
      } catch (err) {
        console.error('Erro ao carregar projeto:', err);
        setError('Erro ao carregar dados do projeto');
      } finally {
        setLoading(false);
      }
    };

    fetchProject();
  }, [id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-foreground mb-2">Carregando...</h2>
          <p className="text-text-secondary">Buscando dados do projeto</p>
        </div>
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-foreground mb-2">Projeto não encontrado</h2>
          <p className="text-text-secondary mb-4">{error || 'O projeto solicitado não existe ou foi removido.'}</p>
          <Link to="/projects">
            <Button>Voltar para Projetos</Button>
          </Link>
        </div>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const getInitials = (name: string) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  };

  const isOverdue = new Date(project.end_date) < new Date() && project.status === 'active';

  // Simular dados de fases para demonstração (já que a API real não tem)
  const phases = ['Inception', 'Definition', 'Built', 'Deploy', 'Close'];
  const currentPhaseIndex = Math.floor(Math.random() * phases.length); // Simulado
  const currentPhase = phases[currentPhaseIndex];

  const getPhaseProgress = () => {
    return ((currentPhaseIndex + 1) / phases.length) * 100;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link to="/projects">
            <Button variant="outline" size="sm">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Voltar
            </Button>
          </Link>
          <div>
            <div className="flex items-center space-x-3">
              <h1 className="text-3xl font-bold text-foreground">{project.name}</h1>
              <StatusBadge status={project.status as ProjectStatus} />
              <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                {currentPhase}
              </Badge>
              {isOverdue && (
                <Badge className="bg-danger text-danger-foreground">
                  <AlertTriangle className="mr-1 h-3 w-3" />
                  Atrasado
                </Badge>
              )}
            </div>
            <p className="text-text-secondary mt-1">Cliente: {project.description}</p>
          </div>
        </div>
        <Button variant="outline">
          <Settings className="mr-2 h-4 w-4" />
          Configurações
        </Button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="border-card-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-text-secondary">Valor OV</CardTitle>
            <DollarSign className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">R$ 150.000</div>
            <p className="text-xs text-text-tertiary">Valor do projeto</p>
          </CardContent>
        </Card>

        <Card className="border-card-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-text-secondary">PCT</CardTitle>
            <Clock className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">480h</div>
            <p className="text-xs text-text-tertiary">Horas planejadas</p>
          </CardContent>
        </Card>

        <Card className="border-card-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-text-secondary">Início</CardTitle>
            <Calendar className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">{formatDate(project.start_date)}</div>
            <p className="text-xs text-text-tertiary">Data de início</p>
          </CardContent>
        </Card>

        <Card className="border-card-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-text-secondary">Previsão</CardTitle>
            <Calendar className={`h-4 w-4 ${isOverdue ? 'text-danger' : 'text-primary'}`} />
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${isOverdue ? 'text-danger' : 'text-foreground'}`}>
              {formatDate(project.end_date)}
            </div>
            <p className="text-xs text-text-tertiary">Data estimada</p>
          </CardContent>
        </Card>
      </div>

      {/* Progress Bar das Fases */}
      <Card className="border-card-border">
        <CardHeader>
          <CardTitle className="text-foreground">Progresso do Projeto</CardTitle>
          <CardDescription className="text-text-secondary">
            Fase atual: {currentPhase} • {getPhaseProgress().toFixed(0)}% concluído
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="w-full bg-surface-secondary rounded-full h-3 mb-4">
            <div 
              className="bg-primary h-3 rounded-full transition-all duration-300" 
              style={{ width: `${getPhaseProgress()}%` }}
            />
          </div>
          <div className="flex justify-between text-sm">
            {phases.map((phase, index) => (
              <div key={phase} className="flex flex-col items-center">
                <div className={`w-3 h-3 rounded-full mb-1 ${
                  index <= currentPhaseIndex ? 'bg-primary' : 'bg-surface-secondary'
                }`} />
                <span className={`text-xs ${
                  index <= currentPhaseIndex ? 'text-foreground font-medium' : 'text-text-tertiary'
                }`}>
                  {phase}
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Tabs Section */}
      <Tabs defaultValue="kanban" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="kanban">Kanban</TabsTrigger>
          <TabsTrigger value="documents">Documentos</TabsTrigger>
          <TabsTrigger value="team">Equipe</TabsTrigger>
          <TabsTrigger value="communication">Comunicação</TabsTrigger>
        </TabsList>

        <TabsContent value="kanban" className="space-y-4">
          <Card className="border-card-border">
            <CardHeader>
              <CardTitle className="text-foreground">Kanban Board</CardTitle>
              <CardDescription className="text-text-secondary">
                Visualização das tarefas do projeto
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-text-tertiary">
                <Target className="mx-auto h-12 w-12 mb-4" />
                <p className="text-lg font-medium mb-2">Kanban em breve...</p>
                <p className="text-sm">Esta funcionalidade será implementada em sprints futuras</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="documents" className="space-y-4">
          <Card className="border-card-border">
            <CardHeader>
              <CardTitle className="text-foreground">Documentos do Projeto</CardTitle>
              <CardDescription className="text-text-secondary">
                Gerencie todos os documentos e artefatos
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-text-tertiary">
                <FileText className="mx-auto h-12 w-12 mb-4" />
                <p className="text-lg font-medium mb-2">Documentos em breve...</p>
                <p className="text-sm">Esta funcionalidade será implementada em sprints futuras</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="team" className="space-y-4">
          <Card className="border-card-border">
            <CardHeader>
              <CardTitle className="text-foreground">Equipe do Projeto</CardTitle>
              <CardDescription className="text-text-secondary">
                Membros ativos no projeto
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {project.manager && (
                  <div className="flex items-center space-x-3 p-4 border border-card-border rounded-lg bg-blue-50/50">
                    <Avatar>
                      <AvatarFallback className="bg-blue-100 text-blue-700">
                        {getInitials(project.manager.full_name)}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <h4 className="font-medium text-foreground">{project.manager.full_name}</h4>
                      <p className="text-sm text-text-secondary">Gerente de Projetos</p>
                      <p className="text-xs text-text-tertiary">{project.manager.username}</p>
                    </div>
                    <Badge variant="outline" className="bg-blue-100 text-blue-700 border-blue-200">
                      Gerente
                    </Badge>
                  </div>
                )}
                
                {/* Líder Técnico simulado */}
                <div className="flex items-center space-x-3 p-4 border border-card-border rounded-lg bg-green-50/50">
                  <Avatar>
                    <AvatarFallback className="bg-green-100 text-green-700">
                      TL
                    </AvatarFallback>
                  </Avatar>
                  <div className="flex-1">
                    <h4 className="font-medium text-foreground">Tech Lead</h4>
                    <p className="text-sm text-text-secondary">Líder Técnico</p>
                    <p className="text-xs text-text-tertiary">tech.lead@empresa.com</p>
                  </div>
                  <Badge variant="outline" className="bg-green-100 text-green-700 border-green-200">
                    Líder Técnico
                  </Badge>
                </div>

                {/* Membros da equipe simulados */}
                {['Desenvolvedor Frontend', 'Desenvolvedor Backend', 'Designer UX/UI'].map((role, index) => (
                  <div key={index} className="flex items-center space-x-3 p-4 border border-card-border rounded-lg">
                    <Avatar>
                      <AvatarFallback>
                        {role.split(' ').map(n => n[0]).join('').slice(0, 2)}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <h4 className="font-medium text-foreground">{role}</h4>
                      <p className="text-sm text-text-secondary">Membro da Equipe</p>
                      <p className="text-xs text-text-tertiary">{role.toLowerCase().replace(/\s+/g, '.')}@empresa.com</p>
                    </div>
                    <Badge variant="outline">
                      Técnico
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="communication" className="space-y-4">
          <Card className="border-card-border">
            <CardHeader>
              <CardTitle className="text-foreground">Centro de Comunicação</CardTitle>
              <CardDescription className="text-text-secondary">
                Timeline de atividades e histórico do projeto
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* Timeline simulada de atividades */}
                {[
                  {
                    id: 1,
                    author: project.manager?.full_name || 'Sistema',
                    action: 'criou o projeto',
                    date: project.created_at,
                    type: 'creation'
                  },
                  {
                    id: 2,
                    author: project.manager?.full_name || 'Gerente',
                    action: 'atualizou o status para ' + project.status,
                    date: project.updated_at,
                    type: 'status-change'
                  },
                  {
                    id: 3,
                    author: 'Tech Lead',
                    action: 'avançou o projeto para a fase ' + currentPhase,
                    date: new Date().toISOString(),
                    type: 'phase-change'
                  }
                ].map((activity) => (
                  <div key={activity.id} className="flex space-x-3 p-4 border border-card-border rounded-lg">
                    <Avatar>
                      <AvatarFallback>{getInitials(activity.author)}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        <h4 className="font-medium text-foreground">{activity.author}</h4>
                        <span className="text-xs text-text-tertiary">
                          {formatDate(activity.date)}
                        </span>
                        {activity.type === 'creation' && (
                          <Badge className="bg-blue-100 text-blue-700 border-blue-200">
                            <Target className="mr-1 h-3 w-3" />
                            Criação
                          </Badge>
                        )}
                        {activity.type === 'status-change' && (
                          <Badge className="bg-yellow-100 text-yellow-700 border-yellow-200">
                            <TrendingUp className="mr-1 h-3 w-3" />
                            Status
                          </Badge>
                        )}
                        {activity.type === 'phase-change' && (
                          <Badge className="bg-green-100 text-green-700 border-green-200">
                            <CheckCircle className="mr-1 h-3 w-3" />
                            Fase
                          </Badge>
                        )}
                      </div>
                      <p className="text-sm text-text-secondary">{activity.action}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ProjectDetail;