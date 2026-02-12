import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Mail, Lock, ArrowLeft, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useToast } from '@/hooks/use-toast';
import { cn } from '@/lib/utils';

const Auth = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { toast } = useToast();

  const validateEmail = (email: string) => {
    if (!email.endsWith('@ulaval.ca')) {
      return 'Seuls les courriels @ulaval.ca sont acceptés';
    }
    if (!/^[^\s@]+@ulaval\.ca$/.test(email)) {
      return 'Courriel invalide';
    }
    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validate email
    const emailError = validateEmail(email);
    if (emailError) {
      setError(emailError);
      return;
    }

    // Validate password
    if (password.length < 6) {
      setError('Le mot de passe doit contenir au moins 6 caractères');
      return;
    }

    // Validate confirm password for signup
    if (!isLogin && password !== confirmPassword) {
      setError('Les mots de passe ne correspondent pas');
      return;
    }

    setIsLoading(true);

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500));

    toast({
      title: isLogin ? 'Connexion réussie!' : 'Compte créé!',
      description: isLogin
        ? 'Bienvenue sur ULavalMarket'
        : 'Vérifiez votre courriel @ulaval.ca pour confirmer votre compte',
    });

    setIsLoading(false);
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-background flex">
      {/* Left Panel - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary via-primary to-laval-red-dark p-12 flex-col justify-between relative overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute -top-40 -right-40 w-80 h-80 rounded-full bg-gold/10 blur-3xl" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 rounded-full bg-primary-foreground/5 blur-3xl" />

        <div className="relative">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-primary-foreground/20 backdrop-blur-sm flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-xl">U</span>
            </div>
            <div>
              <span className="font-bold text-2xl text-primary-foreground">ULaval</span>
              <span className="font-bold text-2xl text-gold">Market</span>
            </div>
          </Link>
        </div>

        <div className="relative space-y-6">
          <h1 className="text-4xl font-extrabold text-primary-foreground leading-tight">
            La marketplace
            <br />
            <span className="text-gold">des étudiants ULaval</span>
          </h1>
          <p className="text-primary-foreground/80 text-lg max-w-md">
            Achetez et vendez en toute confiance avec la communauté étudiante du Rouge et Or.
          </p>
        </div>

        <div className="relative">
          <p className="text-primary-foreground/60 text-sm">
            © 2024 ULavalMarket. Exclusif aux étudiants de l'Université Laval.
          </p>
        </div>
      </div>

      {/* Right Panel - Form */}
      <div className="flex-1 flex flex-col p-6 md:p-12">
        {/* Mobile back button */}
        <Link
          to="/"
          className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors mb-8 lg:mb-0"
        >
          <ArrowLeft className="w-4 h-4" />
          Retour
        </Link>

        <div className="flex-1 flex items-center justify-center">
          <div className="w-full max-w-md space-y-8">
            {/* Mobile Logo */}
            <div className="lg:hidden text-center">
              <Link to="/" className="inline-flex items-center gap-2">
                <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center">
                  <span className="text-primary-foreground font-bold text-lg">U</span>
                </div>
                <span className="font-bold text-xl text-foreground">ULavalMarket</span>
              </Link>
            </div>

            {/* Header */}
            <div className="text-center lg:text-left">
              <h2 className="text-2xl md:text-3xl font-bold text-foreground">
                {isLogin ? 'Connexion' : 'Créer un compte'}
              </h2>
              <p className="text-muted-foreground mt-2">
                {isLogin
                  ? 'Connectez-vous avec votre courriel @ulaval.ca'
                  : 'Inscrivez-vous avec votre courriel étudiant'}
              </p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Error Message */}
              {error && (
                <div className="flex items-center gap-2 p-3 rounded-lg bg-destructive/10 text-destructive text-sm">
                  <AlertCircle className="w-4 h-4 shrink-0" />
                  <span>{error}</span>
                </div>
              )}

              {/* Email */}
              <div className="space-y-2">
                <Label htmlFor="email">Courriel universitaire</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="prenom.nom@ulaval.ca"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="pl-10 h-12"
                    required
                  />
                </div>
                <p className="text-xs text-muted-foreground">
                  Seuls les courriels @ulaval.ca sont acceptés
                </p>
              </div>

              {/* Password */}
              <div className="space-y-2">
                <Label htmlFor="password">Mot de passe</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                  <Input
                    id="password"
                    type="password"
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="pl-10 h-12"
                    required
                  />
                </div>
              </div>

              {/* Confirm Password (Signup only) */}
              {!isLogin && (
                <div className="space-y-2">
                  <Label htmlFor="confirmPassword">Confirmer le mot de passe</Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                    <Input
                      id="confirmPassword"
                      type="password"
                      placeholder="••••••••"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      className="pl-10 h-12"
                      required
                    />
                  </div>
                </div>
              )}

              {/* Forgot Password (Login only) */}
              {isLogin && (
                <div className="text-right">
                  <button
                    type="button"
                    className="text-sm text-primary hover:underline"
                  >
                    Mot de passe oublié?
                  </button>
                </div>
              )}

              {/* Submit Button */}
              <Button
                type="submit"
                size="xl"
                className="w-full"
                disabled={isLoading}
              >
                {isLoading
                  ? 'Chargement...'
                  : isLogin
                  ? 'Se connecter'
                  : "S'inscrire"}
              </Button>
            </form>

            {/* Toggle Login/Signup */}
            <div className="text-center">
              <p className="text-muted-foreground">
                {isLogin ? "Pas encore de compte?" : 'Déjà un compte?'}{' '}
                <button
                  type="button"
                  onClick={() => {
                    setIsLogin(!isLogin);
                    setError('');
                  }}
                  className="text-primary font-semibold hover:underline"
                >
                  {isLogin ? "S'inscrire" : 'Se connecter'}
                </button>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Auth;
