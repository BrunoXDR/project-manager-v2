import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { projectsAPI, Project } from "@/lib/apiClient";
import { BarChart3, TrendingUp, Clock, AlertTriangle, Users, Target } from "lucide-react";

const Analytics = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await projectsAPI.getProjects();
        setProjects(response.items);
      } catch (err) {
        console.error('Erro ao carregar projetos:', err);
        setError('Erro ao carregar dados dos projetos');
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-foreground mb-2">Carregando...</h2>
          <p className="text-text-secondary">Buscando dados de analytics</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-foreground mb-2">Erro ao carregar dados</h2>
          <p className="text-text-secondary">{error}</p>
        </div>
      </div>
    );
  }

  // Calculate analytics data
  const totalProjects = projects.length;
  const activeProjects = projects.filter(p => p.status === 'active').length;
  const completedProjects = projects.filter(p => p.status === 'completed').length;
  const projectsOnHold = projects.filter(p => p.status === 'hold').length;
  
  // Projects by status
  const projectsByStatus = projects.reduce((acc, project) => {
    acc[project.status] = (acc[project.status] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // Performance metrics - Note: API projects don't have estimatedEndDate, using end_date
  const overdueProjects = projects.filter(p => 
    p.end_date && new Date(p.end_date) < new Date() && p.status === 'active'
  ).length;

  const metrics = [
    {
      title: "Total de Projetos",
      value: totalProjects,
      description: "Projetos no sistema",
      icon: Target,
      color: "text-primary"
    },
    {
      title: "Taxa de Sucesso",
      value: totalProjects > 0 ? `${Math.round((completedProjects / totalProjects) * 100)}%` : "0%",
      description: "Projetos finalizados",
      icon: TrendingUp,
      color: "text-success"
    },
    {
      title: "Projetos Ativos",
      value: activeProjects,
      description: "Em andamento",
      icon: Clock,
      color: "text-info"
    },
    {
      title: "Projetos Atrasados",
      value: overdueProjects,
      description: "Requerem atenção",
      icon: AlertTriangle,
      color: "text-danger"
    }
  ];

  const getStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      active: 'Ativo',
      hold: 'Em Espera',
      completed: 'Finalizado',
      cancelled: 'Cancelado'
    };
    return labels[status] || status;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">Analytics</h1>
        <p className="text-text-secondary mt-2">
          Insights e métricas dos seus projetos
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {metrics.map((metric, index) => {
          const Icon = metric.icon;
          return (
            <Card key={index} className="border-card-border">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-text-secondary">
                  {metric.title}
                </CardTitle>
                <Icon className={`h-4 w-4 ${metric.color}`} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-foreground">{metric.value}</div>
                <p className="text-xs text-text-tertiary">
                  {metric.description}
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Project Status Distribution */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card className="border-card-border">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-foreground">
              <BarChart3 className="h-5 w-5" />
              Distribuição por Status
            </CardTitle>
            <CardDescription className="text-text-secondary">
              Projetos organizados por status atual
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {Object.entries(projectsByStatus).map(([status, count]) => (
              <div key={status} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Badge variant="outline" className="text-xs">
                    {getStatusLabel(status)}
                  </Badge>
                </div>
                <div className="flex items-center gap-2">
                  <div className="text-sm font-medium text-foreground">{count}</div>
                  <div className="text-xs text-text-tertiary">
                    ({totalProjects > 0 ? Math.round((count / totalProjects) * 100) : 0}%)
                  </div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Project Performance */}
        <Card className="border-card-border">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-foreground">
              <TrendingUp className="h-5 w-5" />
              Performance dos Projetos
            </CardTitle>
            <CardDescription className="text-text-secondary">
              Métricas de desempenho e produtividade
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-text-secondary">Projetos no Prazo</span>
              <span className="text-sm font-medium text-foreground">
                {totalProjects - overdueProjects} de {totalProjects}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-text-secondary">Taxa de Conclusão</span>
              <span className="text-sm font-medium text-foreground">
                {totalProjects > 0 ? Math.round((completedProjects / totalProjects) * 100) : 0}%
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-text-secondary">Projetos Ativos</span>
              <span className="text-sm font-medium text-foreground">
                {activeProjects}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-text-secondary">Projetos em Espera</span>
              <span className="text-sm font-medium text-foreground">
                {projectsOnHold}
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Projects Activity */}
      <Card className="border-card-border">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-foreground">
            <Users className="h-5 w-5" />
            Projetos Recentes
          </CardTitle>
          <CardDescription className="text-text-secondary">
            Últimos projetos atualizados no sistema
          </CardDescription>
        </CardHeader>
        <CardContent>
          {projects.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-text-secondary">Nenhum projeto encontrado</p>
            </div>
          ) : (
            <div className="space-y-4">
              {projects.slice(0, 5).map((project) => (
                <div key={project.id} className="flex items-center justify-between p-3 rounded-lg border border-card-border">
                  <div className="flex-1">
                    <h4 className="font-medium text-foreground">{project.name}</h4>
                    <p className="text-sm text-text-secondary line-clamp-1">
                      {project.description}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="outline" className="text-xs">
                      {getStatusLabel(project.status)}
                    </Badge>
                    <Badge variant="outline" className="text-xs">
                      {project.priority}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Analytics;