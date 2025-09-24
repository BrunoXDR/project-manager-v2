import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  Settings, 
  Users, 
  Shield, 
  Database, 
  FileText, 
  Activity,
  Trash2,
  Download
} from "lucide-react";

const Admin = () => {
  const adminSections = [
    {
      title: "Gestão de Usuários",
      description: "Gerencie contas de usuário e permissões",
      icon: Users,
      actions: ["Criar usuário", "Editar permissões", "Desativar conta"],
      status: "active"
    },
    {
      title: "Configurações do Sistema",
      description: "Configure parâmetros globais do sistema",
      icon: Settings,
      actions: ["Status de projetos", "Templates de tarefas", "Tipos de documento"],
      status: "active"
    },
    {
      title: "Logs de Auditoria",
      description: "Visualize o histórico de alterações",
      icon: Activity,
      actions: ["Ver logs", "Exportar relatório", "Filtrar por usuário"],
      status: "active"
    },
    {
      title: "Backup e Recuperação",
      description: "Gerencie backups dos dados",
      icon: Database,
      actions: ["Criar backup", "Restaurar dados", "Agendar backup"],
      status: "active"
    },
    {
      title: "Relatórios Customizados",
      description: "Configure relatórios automatizados",
      icon: FileText,
      actions: ["Criar relatório", "Agendar envio", "Gerenciar templates"],
      status: "coming-soon"
    },
    {
      title: "Lixeira",
      description: "Recupere projetos excluídos",
      icon: Trash2,
      actions: ["Ver itens excluídos", "Restaurar projeto", "Exclusão permanente"],
      status: "active"
    }
  ];

  const recentActivities = [
    {
      action: "Usuário criado",
      user: "Admin",
      details: "Pedro Costa adicionado ao sistema",
      timestamp: "2024-02-20T10:30:00Z"
    },
    {
      action: "Projeto restaurado",
      user: "João Silva",
      details: "Projeto 'Migração Office 365' restaurado da lixeira",
      timestamp: "2024-02-19T15:45:00Z"
    },
    {
      action: "Configuração alterada",
      user: "Admin",
      details: "Template de tarefas atualizado para fase Built",
      timestamp: "2024-02-19T09:20:00Z"
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Administração</h1>
          <p className="text-text-secondary mt-2">
            Gerencie configurações e usuários do sistema
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline">
            <Download className="mr-2 h-4 w-4" />
            Exportar Dados
          </Button>
          <Button>
            <Shield className="mr-2 h-4 w-4" />
            Backup Agora
          </Button>
        </div>
      </div>

      {/* Admin Sections Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {adminSections.map((section, index) => {
          const Icon = section.icon;
          return (
            <Card key={index} className="border-card-border hover:shadow-md transition-shadow">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Icon className="h-5 w-5 text-primary" />
                    <CardTitle className="text-lg text-foreground">{section.title}</CardTitle>
                  </div>
                  <Badge 
                    variant={section.status === 'active' ? 'default' : 'outline'}
                    className={section.status === 'active' ? 'bg-success text-success-foreground' : ''}
                  >
                    {section.status === 'active' ? 'Ativo' : 'Em Breve'}
                  </Badge>
                </div>
                <CardDescription className="text-text-secondary">
                  {section.description}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {section.actions.map((action, actionIndex) => (
                    <Button 
                      key={actionIndex} 
                      variant="outline" 
                      size="sm" 
                      className="w-full justify-start"
                      disabled={section.status !== 'active'}
                    >
                      {action}
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Recent Activities */}
      <Card className="border-card-border">
        <CardHeader>
          <CardTitle className="text-foreground flex items-center">
            <Activity className="mr-2 h-5 w-5" />
            Atividades Recentes
          </CardTitle>
          <CardDescription className="text-text-secondary">
            Últimas ações administrativas no sistema
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentActivities.map((activity, index) => (
              <div key={index} className="flex items-center justify-between p-4 border border-card-border rounded-lg">
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <h4 className="font-medium text-foreground">{activity.action}</h4>
                    <Badge variant="outline" className="text-xs">
                      {activity.user}
                    </Badge>
                  </div>
                  <p className="text-sm text-text-secondary">{activity.details}</p>
                </div>
                <div className="text-xs text-text-tertiary">
                  {new Date(activity.timestamp).toLocaleDateString('pt-BR', {
                    day: '2-digit',
                    month: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* System Health */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card className="border-card-border">
          <CardHeader>
            <CardTitle className="text-foreground">Status do Sistema</CardTitle>
            <CardDescription className="text-text-secondary">
              Monitoramento em tempo real
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-text-secondary">API</span>
                <Badge className="bg-success text-success-foreground">Online</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-text-secondary">Database</span>
                <Badge className="bg-success text-success-foreground">Online</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-text-secondary">Backup</span>
                <Badge className="bg-success text-success-foreground">OK</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-text-secondary">Último Backup</span>
                <span className="text-sm text-foreground">Ontem às 02:00</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-card-border">
          <CardHeader>
            <CardTitle className="text-foreground">Uso do Sistema</CardTitle>
            <CardDescription className="text-text-secondary">
              Estatísticas de utilização
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-text-secondary">Usuários Ativos</span>
                <span className="text-sm font-medium text-foreground">12</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-text-secondary">Projetos Ativos</span>
                <span className="text-sm font-medium text-foreground">8</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-text-secondary">Armazenamento</span>
                <span className="text-sm font-medium text-foreground">2.1 GB / 10 GB</span>
              </div>
              <div className="w-full bg-surface-secondary rounded-full h-2">
                <div className="bg-primary h-2 rounded-full" style={{ width: '21%' }} />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Admin;