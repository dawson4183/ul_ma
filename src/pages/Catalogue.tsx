import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Filter, X, SlidersHorizontal } from 'lucide-react';
import Layout from '@/components/layout/Layout';
import ListingCard from '@/components/listings/ListingCard';
import ListingSkeleton from '@/components/common/ListingSkeleton';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import {
  mockListings,
  CATEGORIES,
  CAMPUS_LOCATIONS,
  searchListings,
  getListingsByCategory,
  Listing,
} from '@/data/mockData';
import { cn } from '@/lib/utils';

const CONDITIONS = ['Neuf', 'Comme neuf', 'Bon état', 'Usagé'] as const;

const Catalogue = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [listings, setListings] = useState<Listing[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showFilters, setShowFilters] = useState(false);

  // Filters state
  const [selectedCategory, setSelectedCategory] = useState<string>(
    searchParams.get('category') || ''
  );
  const [selectedLocations, setSelectedLocations] = useState<string[]>([]);
  const [selectedConditions, setSelectedConditions] = useState<string[]>([]);
  const [priceRange, setPriceRange] = useState({ min: '', max: '' });
  const [searchQuery, setSearchQuery] = useState(searchParams.get('q') || '');

  // Apply filters
  useEffect(() => {
    setIsLoading(true);

    const timer = setTimeout(() => {
      let filtered = [...mockListings].filter((l) => !l.isSold);

      // Search query
      if (searchQuery) {
        filtered = searchListings(searchQuery);
      }

      // Category filter
      if (selectedCategory) {
        filtered = filtered.filter((l) => l.category === selectedCategory);
      }

      // Location filter
      if (selectedLocations.length > 0) {
        filtered = filtered.filter((l) => selectedLocations.includes(l.location));
      }

      // Condition filter
      if (selectedConditions.length > 0) {
        filtered = filtered.filter((l) => selectedConditions.includes(l.condition));
      }

      // Price filter
      if (priceRange.min) {
        filtered = filtered.filter((l) => l.price >= Number(priceRange.min));
      }
      if (priceRange.max) {
        filtered = filtered.filter((l) => l.price <= Number(priceRange.max));
      }

      setListings(filtered);
      setIsLoading(false);
    }, 500);

    return () => clearTimeout(timer);
  }, [searchQuery, selectedCategory, selectedLocations, selectedConditions, priceRange]);

  const toggleLocation = (location: string) => {
    setSelectedLocations((prev) =>
      prev.includes(location)
        ? prev.filter((l) => l !== location)
        : [...prev, location]
    );
  };

  const toggleCondition = (condition: string) => {
    setSelectedConditions((prev) =>
      prev.includes(condition)
        ? prev.filter((c) => c !== condition)
        : [...prev, condition]
    );
  };

  const clearFilters = () => {
    setSelectedCategory('');
    setSelectedLocations([]);
    setSelectedConditions([]);
    setPriceRange({ min: '', max: '' });
    setSearchQuery('');
    setSearchParams({});
  };

  const hasActiveFilters =
    selectedCategory ||
    selectedLocations.length > 0 ||
    selectedConditions.length > 0 ||
    priceRange.min ||
    priceRange.max;

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-foreground">
              Catalogue
            </h1>
            <p className="text-muted-foreground mt-1">
              {isLoading ? 'Chargement...' : `${listings.length} annonces trouvées`}
            </p>
          </div>

          <div className="flex items-center gap-3">
            {/* Search Input */}
            <div className="relative flex-1 md:w-64">
              <Input
                type="text"
                placeholder="Rechercher..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pr-10"
              />
            </div>

            {/* Mobile Filter Toggle */}
            <Button
              variant="outline"
              className="md:hidden gap-2"
              onClick={() => setShowFilters(!showFilters)}
            >
              <SlidersHorizontal className="w-4 h-4" />
              Filtres
            </Button>
          </div>
        </div>

        <div className="flex gap-8">
          {/* Filters Sidebar */}
          <aside
            className={cn(
              'fixed inset-0 z-50 bg-background p-6 overflow-y-auto',
              'md:static md:block md:w-64 md:shrink-0 md:bg-transparent md:p-0 md:overflow-visible',
              showFilters ? 'block' : 'hidden md:block'
            )}
          >
            {/* Desktop Sticky Container */}
            <div className="md:sticky md:top-24">
              {/* Mobile close button */}
              <div className="flex items-center justify-between mb-6 md:hidden">
                <h2 className="font-semibold text-lg">Filtres</h2>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setShowFilters(false)}
                >
                  <X className="w-5 h-5" />
                </Button>
              </div>

            <div className="space-y-6">
              {/* Clear Filters */}
              {hasActiveFilters && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearFilters}
                  className="text-destructive hover:text-destructive"
                >
                  <X className="w-4 h-4 mr-1" />
                  Effacer les filtres
                </Button>
              )}

              {/* Categories */}
              <div>
                <h3 className="font-semibold text-foreground mb-3">Catégorie</h3>
                <div className="space-y-2">
                  {CATEGORIES.map((cat) => (
                    <button
                      key={cat.id}
                      onClick={() =>
                        setSelectedCategory(
                          selectedCategory === cat.id ? '' : cat.id
                        )
                      }
                      className={cn(
                        'w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors',
                        selectedCategory === cat.id
                          ? 'bg-primary text-primary-foreground'
                          : 'hover:bg-secondary text-foreground'
                      )}
                    >
                      <span>{cat.icon}</span>
                      <span>{cat.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Price Range */}
              <div>
                <h3 className="font-semibold text-foreground mb-3">Prix</h3>
                <div className="flex items-center gap-2">
                  <Input
                    type="number"
                    placeholder="Min"
                    value={priceRange.min}
                    onChange={(e) =>
                      setPriceRange({ ...priceRange, min: e.target.value })
                    }
                    className="w-full"
                  />
                  <span className="text-muted-foreground">-</span>
                  <Input
                    type="number"
                    placeholder="Max"
                    value={priceRange.max}
                    onChange={(e) =>
                      setPriceRange({ ...priceRange, max: e.target.value })
                    }
                    className="w-full"
                  />
                </div>
              </div>

              {/* Condition */}
              <div>
                <h3 className="font-semibold text-foreground mb-3">État</h3>
                <div className="space-y-2">
                  {CONDITIONS.map((condition) => (
                    <div key={condition} className="flex items-center gap-2">
                      <Checkbox
                        id={`condition-${condition}`}
                        checked={selectedConditions.includes(condition)}
                        onCheckedChange={() => toggleCondition(condition)}
                      />
                      <Label
                        htmlFor={`condition-${condition}`}
                        className="text-sm cursor-pointer"
                      >
                        {condition}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>

              {/* Location */}
              <div>
                <h3 className="font-semibold text-foreground mb-3">
                  Lieu de remise
                </h3>
                <div className="space-y-2">
                  {CAMPUS_LOCATIONS.map((location) => (
                    <div key={location} className="flex items-center gap-2">
                      <Checkbox
                        id={`location-${location}`}
                        checked={selectedLocations.includes(location)}
                        onCheckedChange={() => toggleLocation(location)}
                      />
                      <Label
                        htmlFor={`location-${location}`}
                        className="text-sm cursor-pointer"
                      >
                        {location.replace('Pavillon ', '')}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Mobile Apply Button */}
            <div className="mt-8 md:hidden">
              <Button
                className="w-full"
                onClick={() => setShowFilters(false)}
              >
                Voir {listings.length} résultats
              </Button>
            </div>
            </div>
          </aside>

          {/* Listings Grid */}
          <div className="flex-1">
            {isLoading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {Array.from({ length: 6 }).map((_, i) => (
                  <ListingSkeleton key={i} />
                ))}
              </div>
            ) : listings.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {listings.map((listing, index) => (
                  <ListingCard
                    key={listing.id}
                    listing={listing}
                    index={index}
                  />
                ))}
              </div>
            ) : (
              <div className="text-center py-16">
                <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center mx-auto mb-4">
                  <Filter className="w-8 h-8 text-muted-foreground" />
                </div>
                <h3 className="font-semibold text-foreground mb-2">
                  Aucune annonce trouvée
                </h3>
                <p className="text-muted-foreground mb-4">
                  Essayez de modifier vos critères de recherche
                </p>
                <Button variant="outline" onClick={clearFilters}>
                  Effacer les filtres
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Catalogue;
