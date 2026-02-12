import { Link, useLocation } from 'react-router-dom';
import { Search, MessageCircle, PlusCircle, User, Menu, X, Package } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useState } from 'react';
import { cn } from '@/lib/utils';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { href: '/catalogue', label: 'Catalogue', icon: Search },
    { href: '/mes-annonces', label: 'Mes Annonces', icon: Package },
    { href: '/messages', label: 'Messages', icon: MessageCircle },
    { href: '/vendre', label: 'Vendre', icon: PlusCircle },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="sticky top-0 z-50 bg-card/95 backdrop-blur-md border-b border-border shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center shadow-md group-hover:shadow-lg transition-shadow">
              <span className="text-primary-foreground font-bold text-lg">U</span>
            </div>
            <div className="hidden sm:block">
              <span className="font-bold text-lg text-foreground">ULaval</span>
              <span className="font-bold text-lg text-primary">Market</span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-2">
            {navItems.map((item) => (
              <Link key={item.href} to={item.href}>
                <Button
                  variant={isActive(item.href) ? 'default' : 'ghost'}
                  className={cn(
                    'gap-2',
                    isActive(item.href) && 'shadow-md'
                  )}
                >
                  <item.icon className="w-4 h-4" />
                  {item.label}
                </Button>
              </Link>
            ))}
          </div>

          {/* User Menu */}
          <div className="flex items-center gap-2">
            <Link to="/auth" className="hidden md:block">
              <Button variant="outline" className="gap-2">
                <User className="w-4 h-4" />
                Connexion
              </Button>
            </Link>

            {/* Mobile Menu Toggle */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </Button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-border animate-fade-in">
            <div className="flex flex-col gap-2">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  to={item.href}
                  onClick={() => setIsMenuOpen(false)}
                >
                  <Button
                    variant={isActive(item.href) ? 'default' : 'ghost'}
                    className="w-full justify-start gap-3"
                  >
                    <item.icon className="w-5 h-5" />
                    {item.label}
                  </Button>
                </Link>
              ))}
              <Link to="/profil" onClick={() => setIsMenuOpen(false)}>
                <Button variant="ghost" className="w-full justify-start gap-3">
                  <User className="w-5 h-5" />
                  Mon Profil
                </Button>
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
