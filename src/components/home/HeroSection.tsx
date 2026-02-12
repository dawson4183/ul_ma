import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, BookOpen, Laptop, Home, FlaskConical } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { CATEGORIES } from '@/data/mockData';

const categoryIcons: Record<string, React.ReactNode> = {
  books: <BookOpen className="w-6 h-6" />,
  electronics: <Laptop className="w-6 h-6" />,
  housing: <Home className="w-6 h-6" />,
  lab: <FlaskConical className="w-6 h-6" />,
};

const HeroSection = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/catalogue?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  const quickCategories = CATEGORIES.slice(0, 4);

  return (
    <section className="relative overflow-hidden">
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary via-primary to-laval-red-dark" />
      
      {/* Decorative Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 rounded-full bg-primary-foreground/8 blur-3xl" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 rounded-full bg-gold/10 blur-3xl" />
      </div>

      <div className="relative container mx-auto px-4 py-16 md:py-24">
        <div className="max-w-3xl mx-auto text-center space-y-8">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-foreground/10 backdrop-blur-sm border border-primary-foreground/20 opacity-0 animate-fade-in-up">
            <span className="w-2 h-2 rounded-full bg-gold animate-pulse" />
            <span className="text-sm font-medium text-primary-foreground">
              Exclusif aux étudiants ULaval
            </span>
          </div>

          {/* Title */}
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold text-primary-foreground leading-tight opacity-0 animate-fade-in-up stagger-1">
            Achetez et vendez
            <br />
            <span className="text-gold">sur le campus</span>
          </h1>

          {/* Subtitle */}
          <p className="text-lg md:text-xl text-primary-foreground/80 max-w-xl mx-auto opacity-0 animate-fade-in-up stagger-2">
            La marketplace officielle des étudiants du Rouge et Or. 
            Livres, électronique, logement — tout ce dont tu as besoin.
          </p>

          {/* Search Bar */}
          <form
            onSubmit={handleSearch}
            className="relative max-w-xl mx-auto opacity-0 animate-fade-in-up stagger-3"
          >
            <div className="relative flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder="Ex: Calculatrice TI-84, Manuel GLO-2100..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-12 h-14 text-base bg-card border-0 shadow-lg focus:ring-2 focus:ring-gold"
                />
              </div>
              <Button type="submit" variant="gold" size="xl">
                Rechercher
              </Button>
            </div>
          </form>

          {/* Quick Categories */}
          <div className="opacity-0 animate-fade-in-up stagger-4">
            <p className="text-sm text-primary-foreground/60 mb-4">
              Catégories populaires
            </p>
            <div className="flex flex-wrap justify-center gap-3">
              {quickCategories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => navigate(`/catalogue?category=${category.id}`)}
                  className="flex items-center gap-2 px-4 py-2.5 rounded-full bg-primary-foreground/10 backdrop-blur-sm border border-primary-foreground/20 text-primary-foreground hover:bg-primary-foreground/20 transition-all duration-200 hover:scale-105"
                >
                  {categoryIcons[category.id] || <span className="text-lg">{category.icon}</span>}
                  <span className="font-medium">{category.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Wave Divider */}
      <div className="absolute bottom-0 left-0 right-0">
        <svg
          viewBox="0 0 1440 120"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="w-full h-auto"
          preserveAspectRatio="none"
        >
          <path
            d="M0 120L60 110C120 100 240 80 360 70C480 60 600 60 720 65C840 70 960 80 1080 85C1200 90 1320 90 1380 90L1440 90V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0Z"
            className="fill-background"
          />
        </svg>
      </div>
    </section>
  );
};

export default HeroSection;
