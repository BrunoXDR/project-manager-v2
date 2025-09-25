import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog";
import { StatusBadge } from "@/components/ui/status-badge";
import { projectsAPI, UpdateProjectRequest } from "@/lib/apiClient";
import { ArrowLeft, Edit, Trash2, Calendar, User, Target } from "lucide-react";
import { ProjectStatus } from "@/types/project";
import { useAuth } from "@/contexts/AuthContext";
import { toast } from "sonner";
import ProjectForm from "@/components/ProjectForm";
import type { Project } from "@/lib/apiClient";

const ProjectDetails = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  // Check if user can manage projects (ADMIN or MANAGER)
  const canManageProjects = user?.role === 'ADMIN' || user?.role === 'MANAGER';

  // Fetch project details
  const fetchProject = async () => {
    if (!id) return;
    
    try {
      setLoading(true);
      setError(null);
      const response = await projectsAPI.getProject(id);
      setProject(response);
    } catch (err) {
      setError("Erro ao carregar detalhes do projeto. Tente novamente.");
      console.error("Error fetching project:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProject();
  }, [id]);

  // Handle project update
  const handleUpdateProject = async (projectData: UpdateProjectRequest) => {
    if (!id || !project) return;

    try {
      setIsEditing(true);
      const updatedProject = await projectsAPI.updateProject(id, projectData);
      setProject(updatedProject);
      toast.success("Projeto atualizado com sucesso!");
      setIsEditModalOpen(false);
    } catch (error) {
      console.error("Error updating project:", error);
      toast.error("Erro ao atualizar projeto. Tente novamente.");
    } finally {
      setIsEditing(false);
    }
  };

  // Handle project deletion
  const handleDeleteProject = async () => {
    if (!id) return;

    try {
      setIsDeleting(true);
      await projectsAPI.deleteProject(id);
      toast.success("Projeto excluído com sucesso!");
      navigate("/projects");
    } catch (error) {
      console.error("Error deleting project:", error);
      toast.error("Erro ao excluir projeto. Tente novamente.");
    } finally {
      setIsDeleting(false);
    }
  };

  // Format date for display
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <Card className="border-card-border">
          <CardContent className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
            <h3 className="text-lg font-semibold text-foreground mb-2">Carregando projeto...</h3>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="space-y-6">
        <Card className="border-card-border">
          <CardContent className="text-center py-12">
            <Target className="mx-auto h-12 w-12 text-red-500 mb-4" />
            <h3 className="text-lg font-semibold text-foreground mb-2">Erro ao carregar projeto</h3>
            <p className="text-text-secondary mb-4">{error || "Projeto não encontrado"}</p>
            <div className="space-x-2">
              <Button onClick={fetchProject} variant="outline">
                Tentar novamente
              </Button>
              <Link to="/projects">
                <Button variant="ghost">
                  Voltar para projetos
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link to="/projects">
            <Button variant="ghost" size="sm">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Voltar
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-foreground">{project.name}</h1>
            <p className="text-text-secondary mt-2">
              Detalhes e informações do projeto
            </p>
          </div>
        </div>
        {canManageProjects && (
          <div className="flex space-x-2">
            <Dialog open={isEditModalOpen} onOpenChange={setIsEditModalOpen}>
              <DialogTrigger asChild>
                <Button variant="outline">
                  <Edit className="mr-2 h-4 w-4" />
                  Editar
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl">
                <DialogHeader>
                  <DialogTitle>Editar Projeto</DialogTitle>
                </DialogHeader>
                <ProjectForm
                  project={project}
                  onSubmit={handleUpdateProject}
                  onCancel={() => setIsEditModalOpen(false)}
                  isLoading={isEditing}
                  submitLabel="Salvar Alterações"
                />
              </DialogContent>
            </Dialog>
            
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button variant="destructive">
                  <Trash2 className="mr-2 h-4 w-4" />
                  Excluir
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Confirmar Exclusão</AlertDialogTitle>
                  <AlertDialogDescription>
                    Tem certeza que deseja excluir o projeto "{project.name}"? 
                    Esta ação não pode ser desfeita.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancelar</AlertDialogCancel>
                  <AlertDialogAction
                    onClick={handleDeleteProject}
                    disabled={isDeleting}
                    className="bg-red-600 hover:bg-red-700"
                  >
                    {isDeleting ? "Excluindo..." : "Excluir"}
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </div>
        )}
      </div>

      {/* Project Details */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Main Information */}
        <Card className="border-card-border">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Target className="h-5 w-5" />
              <span>Informações Gerais</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium text-text-secondary">Status</label>
              <div className="mt-1">
                <StatusBadge status={project.status as ProjectStatus} />
              </div>
            </div>
            <div>
              <label className="text-sm font-medium text-text-secondary">Descrição</label>
              <p className="mt-1 text-foreground">{project.description}</p>
            </div>
          </CardContent>
        </Card>

        {/* Dates and People */}
        <Card className="border-card-border">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Calendar className="h-5 w-5" />
              <span>Datas e Responsáveis</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium text-text-secondary">Data de Início</label>
              <p className="mt-1 text-foreground">{formatDate(project.start_date)}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-text-secondary">Data de Término</label>
              <p className="mt-1 text-foreground">{formatDate(project.end_date)}</p>
            </div>
            {project.manager && (
              <div>
                <label className="text-sm font-medium text-text-secondary">Gerente</label>
                <div className="mt-1 flex items-center space-x-2">
                  <User className="h-4 w-4 text-blue-600" />
                  <span className="text-foreground">{project.manager.full_name}</span>
                </div>
              </div>
            )}
            <div>
              <label className="text-sm font-medium text-text-secondary">Criado em</label>
              <p className="mt-1 text-foreground">{formatDate(project.created_at)}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-text-secondary">Última atualização</label>
              <p className="mt-1 text-foreground">{formatDate(project.updated_at)}</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ProjectDetails;