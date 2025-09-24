import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Task, TaskStatus } from "@/types/project";
import { Plus, Calendar, AlertCircle, User } from "lucide-react";
import { cn } from "@/lib/utils";

interface KanbanBoardProps {
  tasks: Task[];
  onTaskUpdate?: (taskId: string, updates: Partial<Task>) => void;
  onAddTask?: (status: TaskStatus) => void;
}

const KanbanBoard = ({ tasks, onTaskUpdate, onAddTask }: KanbanBoardProps) => {
  const columns: { status: TaskStatus; title: string; color: string }[] = [
    { status: 'todo', title: 'To Do', color: 'bg-surface-secondary' },
    { status: 'in-progress', title: 'Em Progresso', color: 'bg-info' },
    { status: 'done', title: 'Concluído', color: 'bg-success/10' },
    { status: 'hold', title: 'Em Espera', color: 'bg-warning/10' }
  ];

  const getTasksByStatus = (status: TaskStatus) => {
    return tasks.filter(task => task.status === status);
  };

  const getPriorityColor = (priority: Task['priority']) => {
    switch (priority) {
      case 'critical':
        return 'bg-danger text-danger-foreground';
      case 'high':
        return 'bg-warning text-warning-foreground';
      case 'medium':
        return 'bg-info text-info-foreground';
      case 'low':
        return 'bg-muted text-muted-foreground';
      default:
        return 'bg-muted text-muted-foreground';
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return null;
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const getInitials = (name?: string) => {
    if (!name) return 'UN';
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {columns.map((column) => {
        const columnTasks = getTasksByStatus(column.status);
        
        return (
          <div key={column.status} className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className={cn("w-3 h-3 rounded-full", column.color)} />
                <h3 className="font-semibold text-foreground">{column.title}</h3>
                <Badge variant="outline" className="text-xs">
                  {columnTasks.length}
                </Badge>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onAddTask?.(column.status)}
                className="h-6 w-6 p-0"
              >
                <Plus className="h-4 w-4" />
              </Button>
            </div>

            <div className="space-y-3">
              {columnTasks.map((task) => (
                <Card key={task.id} className="border-card-border hover:shadow-md transition-shadow cursor-pointer">
                  <CardContent className="p-4">
                    <div className="space-y-3">
                      <div className="flex items-start justify-between">
                        <h4 className="font-medium text-sm text-foreground line-clamp-2">
                          {task.title}
                        </h4>
                        <Badge className={cn("text-xs", getPriorityColor(task.priority))}>
                          {task.priority}
                        </Badge>
                      </div>

                      {task.description && (
                        <p className="text-xs text-text-secondary line-clamp-2">
                          {task.description}
                        </p>
                      )}

                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          {task.assignedTo && (
                            <div className="flex items-center space-x-1">
                              <Avatar className="h-5 w-5">
                                <AvatarFallback className="text-xs">
                                  {getInitials(task.assignedTo)}
                                </AvatarFallback>
                              </Avatar>
                            </div>
                          )}
                          
                          {task.dueDate && (
                            <div className="flex items-center space-x-1 text-xs text-text-secondary">
                              <Calendar className="h-3 w-3" />
                              <span>{formatDate(task.dueDate)}</span>
                            </div>
                          )}
                        </div>

                        {task.dependencies && task.dependencies.length > 0 && (
                          <div className="flex items-center space-x-1">
                            <AlertCircle className="h-3 w-3 text-warning" />
                            <span className="text-xs text-text-secondary">
                              {task.dependencies.length}
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}

              {columnTasks.length === 0 && (
                <div className="text-center py-8 text-text-tertiary">
                  <div className="w-8 h-8 mx-auto mb-2 rounded-full bg-surface-secondary flex items-center justify-center">
                    <Plus className="h-4 w-4" />
                  </div>
                  <p className="text-sm">Nenhuma tarefa</p>
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default KanbanBoard;