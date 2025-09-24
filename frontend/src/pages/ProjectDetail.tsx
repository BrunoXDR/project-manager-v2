import { useParams, Link } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { StatusBadge, PhaseBadge } from "@/components/ui/status-badge";
import { getProjectById } from "@/data/mockData";
import KanbanBoard from "@/components/kanban/KanbanBoard";
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
  AlertTriangle
} from "lucide-react";

const ProjectDetail = () => {
  const { id } = useParams<{ id: string }>();
  const project = id ? getProjectById(id) : null;

  if (!project) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-foreground mb-2">Projeto não encontrado</h2>
          <p className="text-text-secondary mb-4">O projeto solicitado não existe ou foi removido.</p>
          <Link to="/projects">
            <Button>Voltar para Projetos</Button>
          </Link>
        </div>
      </div>
    );
  }

  const getPhaseProgress = () => {
    const phases = ['inception', 'definition', 'built', 'deploy', 'close'];
    const currentIndex = phases.indexOf(project.phase);
    return ((currentIndex + 1) / phases.length) * 100;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const getInitials = (name: string) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  };

  const isOverdue = new Date(project.estimatedEndDate) < new Date() && project.status === 'active';

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
              <StatusBadge status={project.status} />
              <PhaseBadge phase={project.phase} />
              {isOverdue && (
                <Badge className="bg-danger text-danger-foreground">
                  <AlertTriangle className="mr-1 h-3 w-3" />
                  Atrasado
                </Badge>
              )}
            </div>
            <p className="text-text-secondary mt-1">{project.client}</p>
          </div>
        </div>
        <Button variant="outline">
          <Settings className="mr-2 h-4 w-4" />
          Configurações
        </Button>
      </div>

      {/* Project Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="border-card-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-text-secondary">Valor OV</CardTitle>
            <DollarSign className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">{project.orderValue}</div>
            <p className="text-xs text-text-tertiary">Proposta: {project.proposal}</p>
          </CardContent>
        </Card>

        <Card className="border-card-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-text-secondary">PCT</CardTitle>
            <Clock className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">{project.pct}</div>
            <p className="text-xs text-text-tertiary">Horas planejadas</p>
          </CardContent>
        </Card>

        <Card className="border-card-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-text-secondary">Início</CardTitle>
            <Calendar className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">{formatDate(project.startDate)}</div>
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
              {formatDate(project.estimatedEndDate)}
            </div>
            <p className="text-xs text-text-tertiary">Data estimada</p>
          </CardContent>
        </Card>
      </div>

      {/* Progress Bar */}
      <Card className="border-card-border">
        <CardHeader>
          <CardTitle className="text-foreground">Progresso do Projeto</CardTitle>
          <CardDescription className="text-text-secondary">
            Fase atual: {project.phase} • {getPhaseProgress().toFixed(0)}% concluído
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="w-full bg-surface-secondary rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-primary to-primary-light h-2 rounded-full transition-all duration-300"
              style={{ width: `${getPhaseProgress()}%` }}
            />
          </div>
          <div className="flex justify-between mt-2 text-xs text-text-secondary">
            <span>Inception</span>
            <span>Definition</span>
            <span>Built</span>
            <span>Deploy</span>
            <span>Close</span>
          </div>
        </CardContent>
      </Card>

      {/* Main Content Tabs */}
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
              <CardTitle className="text-foreground">Quadro Kanban</CardTitle>
              <CardDescription className="text-text-secondary">
                Gerencie as tarefas do projeto por status
              </CardDescription>
            </CardHeader>
            <CardContent>
              <KanbanBoard tasks={project.tasks} />
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
              {project.documents.length > 0 ? (
                <div className="space-y-3">
                  {project.documents.map((doc) => (
                    <div key={doc.id} className="flex items-center justify-between p-4 border border-card-border rounded-lg">
                      <div className="flex items-center space-x-3">
                        <FileText className="h-5 w-5 text-primary" />
                        <div>
                          <h4 className="font-medium text-foreground">{doc.name}</h4>
                          <p className="text-sm text-text-secondary">{doc.type} • v{doc.version}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <StatusBadge status={doc.status === 'approved' ? 'completed' : doc.status === 'uploaded' ? 'active' : 'hold'} />
                        <Button variant="outline" size="sm">Ver</Button>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-text-tertiary">
                  <FileText className="mx-auto h-12 w-12 mb-4" />
                  <p>Nenhum documento anexado ainda</p>
                </div>
              )}
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
                {project.projectManager && (
                  <div className="flex items-center space-x-3 p-3 border border-card-border rounded-lg">
                    <Avatar>
                      <AvatarFallback>{getInitials(project.projectManager)}</AvatarFallback>
                    </Avatar>
                    <div>
                      <h4 className="font-medium text-foreground">{project.projectManager}</h4>
                      <p className="text-sm text-text-secondary">Gerente de Projetos</p>
                    </div>
                  </div>
                )}
                
                {project.technicalLead && (
                  <div className="flex items-center space-x-3 p-3 border border-card-border rounded-lg">
                    <Avatar>
                      <AvatarFallback>{getInitials(project.technicalLead)}</AvatarFallback>
                    </Avatar>
                    <div>
                      <h4 className="font-medium text-foreground">{project.technicalLead}</h4>
                      <p className="text-sm text-text-secondary">Líder Técnico</p>
                    </div>
                  </div>
                )}

                {project.team.filter(member => member !== project.projectManager && member !== project.technicalLead).map((member, index) => (
                  <div key={index} className="flex items-center space-x-3 p-3 border border-card-border rounded-lg">
                    <Avatar>
                      <AvatarFallback>{getInitials(member)}</AvatarFallback>
                    </Avatar>
                    <div>
                      <h4 className="font-medium text-foreground">{member}</h4>
                      <p className="text-sm text-text-secondary">Técnico</p>
                    </div>
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
                Timeline de atividades e comentários
              </CardDescription>
            </CardHeader>
            <CardContent>
              {project.comments.length > 0 ? (
                <div className="space-y-4">
                  {project.comments.map((comment) => (
                    <div key={comment.id} className="flex space-x-3 p-4 border border-card-border rounded-lg">
                      <Avatar>
                        <AvatarFallback>{getInitials(comment.author)}</AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <h4 className="font-medium text-foreground">{comment.author}</h4>
                          <span className="text-xs text-text-tertiary">
                            {new Date(comment.createdAt).toLocaleDateString('pt-BR')}
                          </span>
                          {comment.type === 'approval' && (
                            <Badge className="bg-success text-success-foreground">
                              <CheckCircle className="mr-1 h-3 w-3" />
                              Aprovação
                            </Badge>
                          )}
                        </div>
                        <p className="text-sm text-text-secondary">{comment.content}</p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-text-tertiary">
                  <MessageSquare className="mx-auto h-12 w-12 mb-4" />
                  <p>Nenhuma comunicação registrada ainda</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ProjectDetail;