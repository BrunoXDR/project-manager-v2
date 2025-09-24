import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { mockProjects } from "@/data/mockData";
import { BarChart3, TrendingUp, Clock, AlertTriangle, Users, Target } from "lucide-react";

const Analytics = () => {
  // Calculate analytics data
  const totalProjects = mockProjects.length;
  const activeProjects = mockProjects.filter(p => p.status === 'active').length;
  const completedProjects = mockProjects.filter(p => p.status === 'completed').length;
  const projectsOnHold = mockProjects.filter(p => p.status === 'hold').length;
  
  // Projects by phase
  const projectsByPhase = mockProjects.reduce((acc, project) => {
    acc[project.phase] = (acc[project.phase] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // Projects by status
  const projectsByStatus = mockProjects.reduce((acc, project) => {
    acc[project.status] = (acc[project.status] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // Performance metrics
  const overdueProjects = mockProjects.filter(p => 
    new Date(p.estimatedEndDate) < new Date() && p.status === 'active'
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
      value: `${Math.round((completedProjects / totalProjects) * 100)}%`,
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

  const getPhaseLabel = (phase: string) => {
    const labels: Record<string, string> = {
      inception: 'Inception',
      definition: 'Definition',
      built: 'Built',
      deploy: 'Deploy',
      close: 'Close'
    };
    return labels[phase] || phase;
  };

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

      <div className="grid gap-6 md:grid-cols-2">
        {/* Projects by Phase */}
        <Card className="border-card-border">
          <CardHeader>
            <CardTitle className="text-foreground flex items-center">
              <BarChart3 className="mr-2 h-5 w-5" />
              Projetos por Fase
            </CardTitle>
            <CardDescription className="text-text-secondary">
              Distribuição dos projetos nas diferentes fases
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Object.entries(projectsByPhase).map(([phase, count]) => (
                <div key={phase} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 rounded-full bg-primary" />
                    <span className="text-sm font-medium text-foreground">
                      {getPhaseLabel(phase)}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Badge variant="outline">{count}</Badge>
                    <div className="w-24 bg-surface-secondary rounded-full h-2">
                      <div 
                        className="bg-primary h-2 rounded-full"
                        style={{ width: `${(count / totalProjects) * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Projects by Status */}
        <Card className="border-card-border">
          <CardHeader>
            <CardTitle className="text-foreground flex items-center">
              <Users className="mr-2 h-5 w-5" />
              Projetos por Status
            </CardTitle>
            <CardDescription className="text-text-secondary">
              Status atual dos projetos
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Object.entries(projectsByStatus).map(([status, count]) => {
                const getStatusColor = (status: string) => {
                  switch (status) {
                    case 'active': return 'bg-success';
                    case 'hold': return 'bg-warning';
                    case 'completed': return 'bg-primary';
                    case 'cancelled': return 'bg-danger';
                    default: return 'bg-muted';
                  }
                };

                return (
                  <div key={status} className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <div className={`w-3 h-3 rounded-full ${getStatusColor(status)}`} />
                      <span className="text-sm font-medium text-foreground">
                        {getStatusLabel(status)}
                      </span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline">{count}</Badge>
                      <div className="w-24 bg-surface-secondary rounded-full h-2">
                        <div 
                          className={`${getStatusColor(status)} h-2 rounded-full`}
                          style={{ width: `${(count / totalProjects) * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Project Management Performance */}
      <Card className="border-card-border">
        <CardHeader>
          <CardTitle className="text-foreground">Performance de Gestão</CardTitle>
          <CardDescription className="text-text-secondary">
            Métricas de desempenho e qualidade
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="text-center p-4 border border-card-border rounded-lg">
              <div className="text-2xl font-bold text-success mb-2">
                {Math.round((completedProjects / totalProjects) * 100)}%
              </div>
              <p className="text-sm text-text-secondary">Taxa de Entrega</p>
            </div>
            <div className="text-center p-4 border border-card-border rounded-lg">
              <div className="text-2xl font-bold text-warning mb-2">
                {Math.round((projectsOnHold / totalProjects) * 100)}%
              </div>
              <p className="text-sm text-text-secondary">Projetos em Espera</p>
            </div>
            <div className="text-center p-4 border border-card-border rounded-lg">
              <div className="text-2xl font-bold text-danger mb-2">
                {Math.round((overdueProjects / activeProjects || 0) * 100)}%
              </div>
              <p className="text-sm text-text-secondary">Taxa de Atraso</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Analytics;