import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { StatusBadge, PhaseBadge } from "@/components/ui/status-badge";
import { projectsAPI } from "@/lib/apiClient";
import { Plus, Search, Filter, Eye, ChevronLeft, ChevronRight } from "lucide-react";
import { Link } from "react-router-dom";
import { ProjectStatus, ProjectPhase } from "@/types/project";
import type { Project, ProjectsResponse } from "@/lib/apiClient";

const Projects = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [phaseFilter, setPhaseFilter] = useState<string>("all");
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalProjects, setTotalProjects] = useState(0);

  // Fetch projects from API
  const fetchProjects = async (page: number = 1) => {
    try {
      setLoading(true);
      setError(null);
      const response = await projectsAPI.getProjects(page);
      setProjects(response.items);
      setCurrentPage(response.page);
      setTotalPages(response.pages);
      setTotalProjects(response.total);
    } catch (err) {
      setError("Erro ao carregar projetos. Tente novamente.");
      console.error("Error fetching projects:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects(currentPage);
  }, [currentPage]);

  // Filter projects based on search and filters (client-side filtering)
  const filteredProjects = projects.filter((project) => {
    const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         project.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         project.manager?.full_name?.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === "all" || project.status === statusFilter;
    // Note: API project doesn't have phase, so we'll skip phase filtering for now
    const matchesPhase = phaseFilter === "all"; // Always true since API doesn't have phase

    return matchesSearch && matchesStatus && matchesPhase;
  });

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

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
        {loading ? (
          <Card className="border-card-border">
            <CardContent className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
              <h3 className="text-lg font-semibold text-foreground mb-2">Carregando projetos...</h3>
            </CardContent>
          </Card>
        ) : error ? (
          <Card className="border-card-border">
            <CardContent className="text-center py-12">
              <Filter className="mx-auto h-12 w-12 text-red-500 mb-4" />
              <h3 className="text-lg font-semibold text-foreground mb-2">Erro ao carregar projetos</h3>
              <p className="text-text-secondary mb-4">{error}</p>
              <Button onClick={() => fetchProjects(currentPage)} variant="outline">
                Tentar novamente
              </Button>
            </CardContent>
          </Card>
        ) : filteredProjects.length === 0 ? (
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
                      <StatusBadge status={project.status as ProjectStatus} />
                      {/* Phase badge removed since API doesn't have phase */}
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-text-secondary">Status:</span>
                        <p className="font-medium text-foreground">{project.status}</p>
                      </div>
                      <div>
                        <span className="text-text-secondary">Prioridade:</span>
                        <p className="font-medium text-foreground">{project.priority}</p>
                      </div>
                      <div>
                        <span className="text-text-secondary">Gerente:</span>
                        <p className="font-medium text-foreground">{project.manager?.full_name || 'Não atribuído'}</p>
                      </div>
                      <div>
                        <span className="text-text-secondary">Data Final:</span>
                        <p className="font-medium text-foreground">
                          {project.end_date ? new Date(project.end_date).toLocaleDateString('pt-BR') : 'Não definida'}
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

      {/* Pagination */}
      {!loading && !error && totalPages > 1 && (
        <div className="flex items-center justify-center space-x-4">
          <Button
            variant="outline"
            size="sm"
            onClick={handlePreviousPage}
            disabled={currentPage === 1}
          >
            <ChevronLeft className="mr-2 h-4 w-4" />
            Anterior
          </Button>
          
          <span className="text-sm text-text-secondary">
            Página {currentPage} de {totalPages}
          </span>
          
          <Button
            variant="outline"
            size="sm"
            onClick={handleNextPage}
            disabled={currentPage === totalPages}
          >
            Próxima
            <ChevronRight className="ml-2 h-4 w-4" />
          </Button>
        </div>
      )}

      {/* Results count */}
      {!loading && !error && filteredProjects.length > 0 && (
        <div className="text-center text-text-secondary text-sm">
          Mostrando {filteredProjects.length} de {totalProjects} projetos
        </div>
      )}
    </div>
  );
};

export default Projects;