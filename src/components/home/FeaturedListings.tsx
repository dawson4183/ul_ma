import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import ListingCard from '@/components/listings/ListingCard';
import ListingSkeleton from '@/components/common/ListingSkeleton';
import { mockListings, Listing } from '@/data/mockData';

const FeaturedListings = () => {
  const [listings, setListings] = useState<Listing[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Simulate API call with loading state
  useEffect(() => {
    const timer = setTimeout(() => {
      setListings(mockListings.filter(l => !l.isSold).slice(0, 6));
      setIsLoading(false);
    }, 800);

    return () => clearTimeout(timer);
  }, []);

  return (
    <section className="py-16 md:py-24">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="flex items-end justify-between mb-10">
          <div>
            <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-2">
              Annonces récentes
            </h2>
            <p className="text-muted-foreground">
              Découvrez les dernières offres sur le campus
            </p>
          </div>
          <Link to="/catalogue" className="hidden sm:block">
            <Button variant="outline" className="gap-2">
              Voir tout
              <ArrowRight className="w-4 h-4" />
            </Button>
          </Link>
        </div>

        {/* Listings Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {isLoading
            ? Array.from({ length: 6 }).map((_, i) => (
                <ListingSkeleton key={i} />
              ))
            : listings.map((listing, index) => (
                <ListingCard
                  key={listing.id}
                  listing={listing}
                  index={index}
                />
              ))}
        </div>

        {/* Mobile CTA */}
        <div className="mt-8 text-center sm:hidden">
          <Link to="/catalogue">
            <Button variant="outline" className="gap-2">
              Voir toutes les annonces
              <ArrowRight className="w-4 h-4" />
            </Button>
          </Link>
        </div>
      </div>
    </section>
  );
};

export default FeaturedListings;
