import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { StatusBadge, PhaseBadge } from "@/components/ui/status-badge";
import { Button } from "@/components/ui/button";
import { Plus, TrendingUp, Clock, Users, AlertTriangle } from "lucide-react";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import { projectsAPI, Project } from "@/lib/apiClient";

const Dashboard = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        setLoading(true);
        const response = await projectsAPI.getProjects(1, 10);
        setProjects(response.items);
      } catch (err) {
        console.error('Erro ao carregar projetos:', err);
        setError('Erro ao carregar projetos');
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
          <p className="text-text-secondary">Buscando dados do dashboard</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-foreground mb-2">Erro</h2>
          <p className="text-text-secondary">{error}</p>
        </div>
      </div>
    );
  }

  // Calculate dashboard metrics
  const totalProjects = projects.length;
  const activeProjects = projects.filter(p => p.status === 'active').length;
  const projectsOnHold = projects.filter(p => p.status === 'hold').length;
  const completedProjects = projects.filter(p => p.status === 'completed').length;

  // Get recent projects (last 5)
  const recentProjects = projects
    .sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
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
                    <StatusBadge status={project.status as any} />
                  </div>
                  <div className="flex items-center space-x-4 mt-2 text-sm text-text-secondary">
                    <span>Prioridade: {project.priority}</span>
                    <span>•</span>
                    <span>Gerente: {project.manager?.full_name || 'Não atribuído'}</span>
                    <span>•</span>
                    <span>Fim: {new Date(project.end_date).toLocaleDateString('pt-BR')}</span>
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