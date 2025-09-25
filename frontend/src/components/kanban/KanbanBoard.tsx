import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Task } from "@/lib/apiClient";
import { Plus, Calendar, AlertCircle, User, Edit, Trash2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { useState } from "react";
import TaskModal from "./TaskModal";
import { DragDropContext, Droppable, Draggable, DropResult } from "react-beautiful-dnd";

type TaskStatus = 'todo' | 'in-progress' | 'done' | 'hold';

interface KanbanBoardProps {
  tasks: Task[];
  onTaskUpdate?: (taskId: string, updates: any) => void;
  onAddTask?: (taskData: any) => void;
  onDeleteTask?: (taskId: string) => void;
}

const KanbanBoard = ({ tasks, onTaskUpdate, onAddTask, onDeleteTask }: KanbanBoardProps) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [modalDefaultStatus, setModalDefaultStatus] = useState<TaskStatus | null>(null);

  const columns = [
    { status: 'todo' as TaskStatus, title: 'A Fazer', color: 'bg-gray-500' },
    { status: 'in-progress' as TaskStatus, title: 'Em Progresso', color: 'bg-blue-500' },
    { status: 'done' as TaskStatus, title: 'Concluído', color: 'bg-green-500' },
    { status: 'hold' as TaskStatus, title: 'Em Espera', color: 'bg-yellow-500' },
  ];

  const getTasksByStatus = (status: TaskStatus) => {
    return tasks.filter(task => task.status === status);
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const getInitials = (user: { full_name: string }) => {
    return user.full_name
      .split(' ')
      .map(name => name.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const handleAddTask = (status: TaskStatus) => {
    setSelectedTask(null);
    setModalDefaultStatus(status);
    setIsModalOpen(true);
  };

  const handleEditTask = (task: Task) => {
    setSelectedTask(task);
    setModalDefaultStatus(null);
    setIsModalOpen(true);
  };

  const handleSaveTask = async (taskData: any) => {
    try {
      if (selectedTask) {
        // Editando tarefa existente
        await onTaskUpdate?.(selectedTask.id, taskData);
      } else {
        // Criando nova tarefa
        const newTaskData = {
          ...taskData,
          status: modalDefaultStatus || 'todo'
        };
        await onAddTask?.(newTaskData);
      }
      setIsModalOpen(false);
      setSelectedTask(null);
      setModalDefaultStatus(null);
    } catch (error) {
      console.error('Erro ao salvar tarefa:', error);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (window.confirm('Tem certeza que deseja excluir esta tarefa?')) {
      await onDeleteTask?.(taskId);
    }
  };

  const handleDragEnd = (result: DropResult) => {
    const { destination, source, draggableId } = result;

    // Se não há destino, não faz nada
    if (!destination) {
      return;
    }

    // Se a posição não mudou, não faz nada
    if (
      destination.droppableId === source.droppableId &&
      destination.index === source.index
    ) {
      return;
    }

    // Encontra a tarefa que foi movida
    const task = tasks.find(t => t.id === draggableId);
    if (!task) return;

    // Atualiza o status da tarefa se mudou de coluna
    if (destination.droppableId !== source.droppableId) {
      const newStatus = destination.droppableId as TaskStatus;
      onTaskUpdate?.(task.id, { status: newStatus });
    }
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
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
                  onClick={() => handleAddTask(column.status)}
                  className="h-6 w-6 p-0"
                >
                  <Plus className="h-4 w-4" />
                </Button>
              </div>

              <Droppable droppableId={column.status}>
                {(provided) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.droppableProps}
                    className="space-y-3 min-h-[200px]"
                  >
                    {columnTasks.map((task, index) => (
                      <Draggable key={task.id} draggableId={task.id} index={index}>
                        {(provided, snapshot) => (
                          <Card
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className={cn(
                              "border-card-border hover:shadow-md transition-shadow cursor-pointer group",
                              snapshot.isDragging && "shadow-lg rotate-2"
                            )}
                          >
                            <CardContent className="p-4">
                              <div className="space-y-3">
                                <div className="flex items-start justify-between">
                                  <h4 className="font-medium text-sm text-foreground line-clamp-2">
                                    {task.title}
                                  </h4>
                                  <div className="flex items-center space-x-1">
                                    <Badge className={cn("text-xs", getPriorityColor(task.priority))}>
                                      {task.priority}
                                    </Badge>
                                    <div className="opacity-0 group-hover:opacity-100 transition-opacity flex space-x-1">
                                      <Button
                                        variant="ghost"
                                        size="sm"
                                        onClick={() => handleEditTask(task)}
                                        className="h-6 w-6 p-0"
                                      >
                                        <Edit className="h-3 w-3" />
                                      </Button>
                                      <Button
                                        variant="ghost"
                                        size="sm"
                                        onClick={() => handleDeleteTask(task.id)}
                                        className="h-6 w-6 p-0 text-danger hover:text-danger"
                                      >
                                        <Trash2 className="h-3 w-3" />
                                      </Button>
                                    </div>
                                  </div>
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
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}

                    {columnTasks.length === 0 && (
                      <div className="text-center py-8 text-text-tertiary">
                        <div className="w-8 h-8 mx-auto mb-2 rounded-full bg-surface-secondary flex items-center justify-center">
                          <Plus className="h-4 w-4" />
                        </div>
                        <p className="text-sm">Nenhuma tarefa</p>
                      </div>
                    )}
                  </div>
                )}
              </Droppable>
            </div>
          );
        })}
      </div>

      <TaskModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedTask(null);
          setModalDefaultStatus(null);
        }}
        onSave={handleSaveTask}
        task={selectedTask}
        defaultStatus={modalDefaultStatus}
      />
    </DragDropContext>
  );
};

export default KanbanBoard;