import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";
import { 
  LayoutDashboard, 
  FolderKanban, 
  BarChart3, 
  Settings, 
  Bell,
  User
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

const Navigation = () => {
  const location = useLocation();
  
  const navigationItems = [
    {
      name: "Dashboard",
      href: "/",
      icon: LayoutDashboard,
      active: location.pathname === "/"
    },
    {
      name: "Projetos",
      href: "/projects",
      icon: FolderKanban,
      active: location.pathname.startsWith("/projects")
    },
    {
      name: "Analytics",
      href: "/analytics",
      icon: BarChart3,
      active: location.pathname === "/analytics"
    },
    {
      name: "Administração",
      href: "/admin",
      icon: Settings,
      active: location.pathname.startsWith("/admin")
    }
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center space-x-8">
          <Link to="/" className="flex items-center space-x-2">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-primary to-primary-light flex items-center justify-center">
              <FolderKanban className="h-5 w-5 text-primary-foreground" />
            </div>
            <span className="font-bold text-lg text-foreground">Sistema de Projetos</span>
          </Link>
          
          <nav className="flex items-center space-x-6">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    "flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                    item.active
                      ? "bg-primary text-primary-foreground"
                      : "text-text-secondary hover:text-text-primary hover:bg-surface-secondary"
                  )}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="flex items-center space-x-4">
          <Button variant="outline" size="sm" className="relative">
            <Bell className="h-4 w-4" />
            <Badge className="absolute -top-2 -right-2 h-5 w-5 rounded-full bg-danger text-danger-foreground text-xs p-0 flex items-center justify-center">
              3
            </Badge>
          </Button>
          
          <Button variant="outline" size="sm">
            <User className="h-4 w-4" />
            <span className="ml-2">Perfil</span>
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Navigation;