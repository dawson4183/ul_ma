import Layout from '@/components/layout/Layout';
import HeroSection from '@/components/home/HeroSection';
import FeaturedListings from '@/components/home/FeaturedListings';
import CategoriesSection from '@/components/home/CategoriesSection';
import TrustSection from '@/components/home/TrustSection';

const Index = () => {
  return (
    <Layout>
      <HeroSection />
      <CategoriesSection />
      <FeaturedListings />
      <TrustSection />
      
      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-br from-primary to-laval-red-dark">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-2xl md:text-3xl font-bold text-primary-foreground mb-4">
            Prêt à vendre tes affaires ?
          </h2>
          <p className="text-primary-foreground/80 mb-8 max-w-md mx-auto">
            Dépose ta première annonce gratuitement et rejoins la communauté ULavalMarket
          </p>
          <a
            href="/vendre"
            className="inline-flex items-center justify-center gap-2 h-14 px-10 rounded-xl bg-gold text-accent-foreground font-bold text-lg shadow-gold hover:bg-gold/90 transition-all hover:scale-105"
          >
            Publier une annonce
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 bg-card border-t border-border">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
                <span className="text-primary-foreground font-bold">U</span>
              </div>
              <span className="font-semibold text-foreground">ULavalMarket</span>
            </div>
            <p className="text-sm text-muted-foreground">
              © 2024 ULavalMarket. Fait avec ❤️ pour les étudiants ULaval.
            </p>
          </div>
        </div>
      </footer>
    </Layout>
  );
};

export default Index;
