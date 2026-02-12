import { Shield, Users, MapPin, Clock } from 'lucide-react';

const features = [
  {
    icon: Shield,
    title: 'Étudiants vérifiés',
    description: 'Chaque membre est vérifié avec son courriel @ulaval.ca',
  },
  {
    icon: MapPin,
    title: 'Rencontres sur campus',
    description: 'Échangez en toute sécurité dans les pavillons de l\'université',
  },
  {
    icon: Clock,
    title: 'Rapide et simple',
    description: 'Publiez une annonce en moins de 2 minutes',
  },
  {
    icon: Users,
    title: 'Communauté active',
    description: 'Des milliers d\'étudiants font confiance à LavalMarket',
  },
];

const TrustSection = () => {
  return (
    <section className="py-16 md:py-24">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-14">
          <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-3">
            Pourquoi choisir <span className="gradient-text">LavalMarket</span> ?
          </h2>
          <p className="text-muted-foreground max-w-lg mx-auto">
            La plateforme pensée par et pour les étudiants de l'Université Laval
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <div
              key={feature.title}
              className="relative p-6 rounded-2xl bg-card border border-border hover:border-primary/30 hover:shadow-card transition-all duration-300 opacity-0 animate-fade-in-up"
              style={{ animationDelay: `${index * 0.15}s` }}
            >
              {/* Icon */}
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4">
                <feature.icon className="w-6 h-6 text-primary" />
              </div>

              {/* Content */}
              <h3 className="font-semibold text-foreground mb-2">
                {feature.title}
              </h3>
              <p className="text-sm text-muted-foreground">
                {feature.description}
              </p>

              {/* Decorative accent */}
              <div className="absolute top-0 right-0 w-20 h-20 rounded-tr-2xl overflow-hidden">
                <div className="absolute -top-10 -right-10 w-20 h-20 bg-gold/5 rounded-full" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TrustSection;
