import { Link } from 'react-router-dom';
import { Listing, getUserById } from '@/data/mockData';
import LocationChip from '@/components/common/LocationChip';
import VerifiedBadge from '@/components/common/VerifiedBadge';
import { cn } from '@/lib/utils';

interface ListingCardProps {
  listing: Listing;
  className?: string;
  index?: number;
}

const ListingCard = ({ listing, className, index = 0 }: ListingCardProps) => {
  const seller = getUserById(listing.sellerId);

  return (
    <Link
      to={`/annonce/${listing.id}`}
      className={cn(
        'listing-card block opacity-0 animate-fade-in-up',
        className
      )}
      style={{ animationDelay: `${index * 0.1}s` }}
    >
      {/* Image */}
      <div className="relative aspect-[4/3] overflow-hidden bg-muted">
        <img
          src={listing.images[0]}
          alt={listing.title}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          loading="lazy"
        />
        
        {/* Condition Badge */}
        <span className="absolute top-3 left-3 px-2.5 py-1 rounded-full text-xs font-medium bg-card/90 backdrop-blur-sm text-card-foreground shadow-sm">
          {listing.condition}
        </span>
        
        {/* Course Code Badge */}
        {listing.courseCode && (
          <span className="absolute top-3 right-3 px-2.5 py-1 rounded-full text-xs font-bold bg-primary text-primary-foreground shadow-md">
            {listing.courseCode}
          </span>
        )}
        
        {listing.isSold && (
          <div className="absolute inset-0 bg-foreground/60 flex items-center justify-center">
            <span className="px-4 py-2 bg-card rounded-lg font-bold text-foreground">
              VENDU
            </span>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-4 space-y-3">
        {/* Title */}
        <h3 className="font-semibold text-card-foreground line-clamp-2 leading-tight">
          {listing.title}
        </h3>

        {/* Price */}
        <p className="text-xl font-bold text-primary">
          {listing.price}$
        </p>

        {/* Location & Seller */}
        <div className="flex items-center justify-between gap-2">
          <LocationChip location={listing.location} compact />
          
          {seller?.isVerified && (
            <VerifiedBadge showText={false} />
          )}
        </div>
      </div>
    </Link>
  );
};

export default ListingCard;
