import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { StatusBadge, PhaseBadge } from "@/components/ui/status-badge";
import { mockProjects } from "@/data/mockData";
import { Button } from "@/components/ui/button";
import { Plus, TrendingUp, Clock, Users, AlertTriangle } from "lucide-react";
import { Link } from "react-router-dom";

const Dashboard = () => {
  // Calculate dashboard metrics
  const totalProjects = mockProjects.length;
  const activeProjects = mockProjects.filter(p => p.status === 'active').length;
  const projectsOnHold = mockProjects.filter(p => p.status === 'hold').length;
  const completedProjects = mockProjects.filter(p => p.status === 'completed').length;

  // Get recent projects (last 5)
  const recentProjects = mockProjects
    .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
    .slice(0, 5);

  const stats = [
    {
      title: "Total de Projetos",
      value: totalProjects,
      description: "Projetos no sistema",
      icon: TrendingUp,
      color: "text-primary"
    },
    {
      title: "Projetos Ativos",
      value: activeProjects,
      description: "Em andamento",
      icon: Clock,
      color: "text-success"
    },
    {
      title: "Em Espera",
      value: projectsOnHold,
      description: "Aguardando resolução",
      icon: AlertTriangle,
      color: "text-warning"
    },
    {
      title: "Finalizados",
      value: completedProjects,
      description: "Projetos entregues",
      icon: Users,
      color: "text-primary"
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
          <p className="text-text-secondary mt-2">
            Visão geral dos seus projetos e atividades
          </p>
        </div>
        <Link to="/projects/new">
          <Button className="bg-gradient-to-r from-primary to-primary-light hover:from-primary-dark hover:to-primary">
            <Plus className="mr-2 h-4 w-4" />
            Novo Projeto
          </Button>
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card key={index} className="border-card-border">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-text-secondary">
                  {stat.title}
                </CardTitle>
                <Icon className={`h-4 w-4 ${stat.color}`} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-foreground">{stat.value}</div>
                <p className="text-xs text-text-tertiary">
                  {stat.description}
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Recent Projects */}
      <Card className="border-card-border">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-foreground">Projetos Recentes</CardTitle>
              <CardDescription className="text-text-secondary">
                Últimos projetos atualizados
              </CardDescription>
            </div>
            <Link to="/projects">
              <Button variant="outline" size="sm">
                Ver Todos
              </Button>
            </Link>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentProjects.map((project) => (
              <div key={project.id} className="flex items-center justify-between p-4 border border-card-border rounded-lg bg-surface hover:bg-surface-secondary transition-colors">
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    <h3 className="font-semibold text-foreground">{project.name}</h3>
                    <StatusBadge status={project.status} />
                    <PhaseBadge phase={project.phase} />
                  </div>
                  <div className="flex items-center space-x-4 mt-2 text-sm text-text-secondary">
                    <span>{project.client}</span>
                    <span>•</span>
                    <span>GP: {project.projectManager}</span>
                    <span>•</span>
                    <span>Previsão: {new Date(project.estimatedEndDate).toLocaleDateString('pt-BR')}</span>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Link to={`/projects/${project.id}`}>
                    <Button variant="outline" size="sm">
                      Visualizar
                    </Button>
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;