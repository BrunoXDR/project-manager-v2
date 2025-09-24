import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { ProjectStatus, ProjectPhase } from "@/types/project";

interface StatusBadgeProps {
  status: ProjectStatus;
  className?: string;
}

interface PhaseBadgeProps {
  phase: ProjectPhase;
  className?: string;
}

export const StatusBadge = ({ status, className }: StatusBadgeProps) => {
  const getStatusStyles = (status: ProjectStatus) => {
    switch (status) {
      case 'active':
        return "bg-success text-success-foreground hover:bg-success/80";
      case 'hold':
        return "bg-warning text-warning-foreground hover:bg-warning/80";
      case 'completed':
        return "bg-primary text-primary-foreground hover:bg-primary/80";
      case 'cancelled':
        return "bg-danger text-danger-foreground hover:bg-danger/80";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  const getStatusLabel = (status: ProjectStatus) => {
    switch (status) {
      case 'active':
        return 'Ativo';
      case 'hold':
        return 'Em Espera';
      case 'completed':
        return 'Finalizado';
      case 'cancelled':
        return 'Cancelado';
      default:
        return status;
    }
  };

  return (
    <Badge className={cn(getStatusStyles(status), className)}>
      {getStatusLabel(status)}
    </Badge>
  );
};

export const PhaseBadge = ({ phase, className }: PhaseBadgeProps) => {
  const getPhaseStyles = (phase: ProjectPhase) => {
    switch (phase) {
      case 'inception':
        return "bg-phase-inception text-primary hover:bg-phase-inception/80";
      case 'definition':
        return "bg-phase-definition text-primary hover:bg-phase-definition/80";
      case 'built':
        return "bg-phase-built text-primary hover:bg-phase-built/80";
      case 'deploy':
        return "bg-phase-deploy text-primary hover:bg-phase-deploy/80";
      case 'close':
        return "bg-phase-close text-primary hover:bg-phase-close/80";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  const getPhaseLabel = (phase: ProjectPhase) => {
    switch (phase) {
      case 'inception':
        return 'Inception';
      case 'definition':
        return 'Definition';
      case 'built':
        return 'Built';
      case 'deploy':
        return 'Deploy';
      case 'close':
        return 'Close';
      default:
        return phase;
    }
  };

  return (
    <Badge variant="outline" className={cn(getPhaseStyles(phase), className)}>
      {getPhaseLabel(phase)}
    </Badge>
  );
};