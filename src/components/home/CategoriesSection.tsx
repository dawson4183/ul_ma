import { useNavigate } from 'react-router-dom';
import { BookOpen, Laptop, Home, FlaskConical, Dumbbell, Shirt, Package } from 'lucide-react';
import { CATEGORIES } from '@/data/mockData';

const categoryIcons: Record<string, React.ReactNode> = {
  books: <BookOpen className="w-8 h-8" />,
  electronics: <Laptop className="w-8 h-8" />,
  housing: <Home className="w-8 h-8" />,
  lab: <FlaskConical className="w-8 h-8" />,
  sports: <Dumbbell className="w-8 h-8" />,
  clothing: <Shirt className="w-8 h-8" />,
  other: <Package className="w-8 h-8" />,
};

const CategoriesSection = () => {
  const navigate = useNavigate();

  return (
    <section className="py-16 bg-card">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-12">
          <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-3">
            Parcourir par catégorie
          </h2>
          <p className="text-muted-foreground max-w-lg mx-auto">
            Trouvez exactement ce dont vous avez besoin pour votre session
          </p>
        </div>

        {/* Categories Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-7 gap-4">
          {CATEGORIES.map((category, index) => (
            <button
              key={category.id}
              onClick={() => navigate(`/catalogue?category=${category.id}`)}
              className="category-card opacity-0 animate-fade-in-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center text-primary transition-colors group-hover:bg-primary group-hover:text-primary-foreground">
                {categoryIcons[category.id]}
              </div>
              <span className="font-medium text-card-foreground text-sm text-center">
                {category.label}
              </span>
            </button>
          ))}
        </div>
      </div>
    </section>
  );
};

export default CategoriesSection;
