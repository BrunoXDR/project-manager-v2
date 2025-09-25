import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Alert, AlertDescription } from '../components/ui/alert';
import { Loader2 } from 'lucide-react';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('🔍 Login: Iniciando processo de login');
    console.log('📧 Email:', email);
    console.log('🔒 Password length:', password.length);
    
    setError('');
    setIsSubmitting(true);

    try {
      console.log('🚀 Login: Chamando função login do contexto');
      const result = await login({ username: email, password });
      console.log('✅ Login: Sucesso na autenticação', result);
      console.log('🔄 Login: Redirecionando para dashboard');
      navigate('/dashboard');
    } catch (err: any) {
      console.error('❌ Erro no login:', err);
      console.error('📊 Detalhes do erro:', {
        message: err.message,
        response: err.response,
        status: err.response?.status,
        data: err.response?.data
      });
      
      if (err.response?.status === 401) {
        setError('Credenciais inválidas. Verifique seu email e senha.');
      } else if (err.response?.status === 422) {
        setError('Dados inválidos. Verifique os campos preenchidos.');
      } else {
        setError('Erro ao conectar com o servidor. Tente novamente.');
      }
    } finally {
      console.log('🏁 Login: Finalizando processo');
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Sistema de Gestão de Projetos
          </h1>
          <p className="text-gray-600">
            Faça login para acessar o sistema
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Login</CardTitle>
            <CardDescription>
              Entre com suas credenciais para acessar o sistema
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Digite seu email"
                  required
                  disabled={isSubmitting}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Senha</Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Digite sua senha"
                  required
                  disabled={isSubmitting}
                />
              </div>

              <Button 
                type="submit" 
                className="w-full" 
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Entrando...
                  </>
                ) : (
                  'Entrar'
                )}
              </Button>
            </form>

            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <h3 className="text-sm font-medium text-blue-800 mb-2">
                Credenciais de Teste:
              </h3>
              <div className="text-sm text-blue-700 space-y-1">
                <p><strong>Admin:</strong> admin@planomaster.com / admin123</p>
                <p><strong>Gerente:</strong> gerente@planomaster.com / gerente123</p>
                <p><strong>Membro:</strong> membro@planomaster.com / membro123</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Login;