import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";
import { projectsAPI, CreateProjectRequest } from "@/lib/apiClient";
import { toast } from "sonner";
import ProjectForm from "@/components/ProjectForm";

const NewProject = () => {
  const navigate = useNavigate();
  const [isCreating, setIsCreating] = useState(false);

  const handleCreateProject = async (projectData: CreateProjectRequest) => {
    try {
      setIsCreating(true);
      const newProject = await projectsAPI.createProject(projectData);
      toast.success("Projeto criado com sucesso!");
      navigate(`/projects/${newProject.id}`);
    } catch (error) {
      console.error('Erro ao criar projeto:', error);
      toast.error("Erro ao criar projeto. Tente novamente.");
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-4">
        <Link to="/projects">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Voltar
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold text-foreground">Novo Projeto</h1>
          <p className="text-text-secondary mt-2">
            Crie um novo projeto preenchendo as informações abaixo
          </p>
        </div>
      </div>

      {/* Project Form */}
      <Card className="border-card-border max-w-4xl">
        <CardHeader>
          <CardTitle>Informações do Projeto</CardTitle>
        </CardHeader>
        <CardContent>
          <ProjectForm
            onSubmit={handleCreateProject}
            onCancel={() => navigate('/projects')}
            isLoading={isCreating}
            submitLabel="Criar Projeto"
          />
        </CardContent>
      </Card>
    </div>
  );
};

export default NewProject;