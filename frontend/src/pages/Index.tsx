// Sistema de Gestão de Projetos - Página Principal
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

const Index = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Redirect to dashboard automatically
    navigate("/");
  }, [navigate]);

  return null;
};

export default Index;
