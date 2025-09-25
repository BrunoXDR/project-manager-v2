import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI, LoginRequest, LoginResponse } from '../lib/apiClient';

// Tipos para o contexto de autenticação
interface User {
  id: string;
  username: string;
  email: string;
  role: string;
  full_name: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => void;
}

// Criar o contexto
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider do contexto
interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Verificar se há token salvo no localStorage ao inicializar
  useEffect(() => {
    const savedToken = localStorage.getItem('authToken');
    const savedUser = localStorage.getItem('user');

    if (savedToken && savedUser && savedUser !== 'undefined') {
      try {
        setToken(savedToken);
        setUser(JSON.parse(savedUser));
      } catch (error) {
        console.error('Erro ao recuperar dados de autenticação:', error);
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
      }
    }
    
    setIsLoading(false);
  }, []);

  // Função de login
  const login = async (credentials: LoginRequest): Promise<void> => {
    try {
      console.log('🔐 AuthContext: Iniciando login');
      console.log('📝 Credenciais:', { username: credentials.username, passwordLength: credentials.password.length });
      
      setIsLoading(true);
      console.log('📡 AuthContext: Fazendo requisição para API');
      
      const response: LoginResponse = await authAPI.login(credentials);
      console.log('📨 AuthContext: Resposta recebida da API:', response);
      
      // Salvar token
      const { access_token } = response;
      console.log('🎫 AuthContext: Token recebido:', access_token ? 'Presente' : 'Ausente');
      
      setToken(access_token);
      localStorage.setItem('authToken', access_token);
      
      // Buscar dados do usuário usando o token
      console.log('👤 AuthContext: Buscando dados do usuário');
      const userData = await authAPI.getCurrentUser();
      console.log('📋 AuthContext: Dados do usuário recebidos:', userData);
      
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      console.log('💾 AuthContext: Dados salvos no localStorage');
      
    } catch (error) {
      console.error('❌ AuthContext: Erro no login:', error);
      throw error;
    } finally {
      console.log('🏁 AuthContext: Finalizando login');
      setIsLoading(false);
    }
  };

  // Função de logout
  const logout = (): void => {
    setUser(null);
    setToken(null);
    
    // Remover do localStorage
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    
    // Redirecionar para a página de login
    window.location.href = '/';
  };

  // Valor do contexto
  const contextValue: AuthContextType = {
    user,
    token,
    isAuthenticated: !!user && !!token,
    isLoading,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook personalizado para usar o contexto
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  
  return context;
};

export default AuthContext;