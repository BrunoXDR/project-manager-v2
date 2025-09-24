import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { StatusBadge, PhaseBadge } from "@/components/ui/status-badge";
import { mockProjects } from "@/data/mockData";
import { Plus, Search, Filter, Eye } from "lucide-react";
import { Link } from "react-router-dom";
import { ProjectStatus, ProjectPhase } from "@/types/project";

const Projects = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [phaseFilter, setPhaseFilter] = useState<string>("all");

  // Filter projects based on search and filters
  const filteredProjects = mockProjects.filter((project) => {
    const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         project.client.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         project.projectManager?.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === "all" || project.status === statusFilter;
    const matchesPhase = phaseFilter === "all" || project.phase === phaseFilter;

    return matchesSearch && matchesStatus && matchesPhase;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Projetos</h1>
          <p className="text-text-secondary mt-2">
            Gerencie todos os seus projetos em um só lugar
          </p>
        </div>
        <Link to="/projects/new">
          <Button className="bg-gradient-to-r from-primary to-primary-light hover:from-primary-dark hover:to-primary">
            <Plus className="mr-2 h-4 w-4" />
            Novo Projeto
          </Button>
        </Link>
      </div>

      {/* Filters */}
      <Card className="border-card-border">
        <CardHeader>
          <CardTitle className="text-lg">Filtros</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-text-tertiary" />
                <Input
                  placeholder="Buscar por nome, cliente ou gerente..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <div className="w-full md:w-48">
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger>
                  <SelectValue placeholder="Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos os Status</SelectItem>
                  <SelectItem value="active">Ativo</SelectItem>
                  <SelectItem value="hold">Em Espera</SelectItem>
                  <SelectItem value="completed">Finalizado</SelectItem>
                  <SelectItem value="cancelled">Cancelado</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="w-full md:w-48">
              <Select value={phaseFilter} onValueChange={setPhaseFilter}>
                <SelectTrigger>
                  <SelectValue placeholder="Fase" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todas as Fases</SelectItem>
                  <SelectItem value="inception">Inception</SelectItem>
                  <SelectItem value="definition">Definition</SelectItem>
                  <SelectItem value="built">Built</SelectItem>
                  <SelectItem value="deploy">Deploy</SelectItem>
                  <SelectItem value="close">Close</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Projects List */}
      <div className="grid gap-4">
        {filteredProjects.length === 0 ? (
          <Card className="border-card-border">
            <CardContent className="text-center py-12">
              <Filter className="mx-auto h-12 w-12 text-text-tertiary mb-4" />
              <h3 className="text-lg font-semibold text-foreground mb-2">Nenhum projeto encontrado</h3>
              <p className="text-text-secondary">
                Tente ajustar os filtros ou criar um novo projeto.
              </p>
            </CardContent>
          </Card>
        ) : (
          filteredProjects.map((project) => (
            <Card key={project.id} className="border-card-border hover:shadow-md transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-3">
                      <h3 className="text-xl font-semibold text-foreground">{project.name}</h3>
                      <StatusBadge status={project.status} />
                      <PhaseBadge phase={project.phase} />
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-text-secondary">Cliente:</span>
                        <p className="font-medium text-foreground">{project.client}</p>
                      </div>
                      <div>
                        <span className="text-text-secondary">Valor OV:</span>
                        <p className="font-medium text-foreground">{project.orderValue}</p>
                      </div>
                      <div>
                        <span className="text-text-secondary">GP:</span>
                        <p className="font-medium text-foreground">{project.projectManager}</p>
                      </div>
                      <div>
                        <span className="text-text-secondary">Previsão:</span>
                        <p className="font-medium text-foreground">
                          {new Date(project.estimatedEndDate).toLocaleDateString('pt-BR')}
                        </p>
                      </div>
                    </div>

                    <div className="mt-4">
                      <p className="text-text-secondary text-sm line-clamp-2">
                        {project.description}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2 ml-4">
                    <Link to={`/projects/${project.id}`}>
                      <Button variant="outline" size="sm">
                        <Eye className="mr-2 h-4 w-4" />
                        Visualizar
                      </Button>
                    </Link>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      {/* Results count */}
      {filteredProjects.length > 0 && (
        <div className="text-center text-text-secondary text-sm">
          Mostrando {filteredProjects.length} de {mockProjects.length} projetos
        </div>
      )}
    </div>
  );
};

export default Projects;