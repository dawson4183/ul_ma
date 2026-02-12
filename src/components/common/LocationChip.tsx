import { MapPin } from 'lucide-react';
import { cn } from '@/lib/utils';

interface LocationChipProps {
  location: string;
  className?: string;
  compact?: boolean;
}

const LocationChip = ({ location, className, compact = false }: LocationChipProps) => {
  // Shorten long location names for compact display
  const shortName = compact
    ? location
        .replace('Pavillon ', '')
        .replace('Bibliothèque', 'Biblio')
    : location;

  return (
    <span className={cn('location-chip', className)}>
      <MapPin className="w-3 h-3" />
      <span className="truncate">{shortName}</span>
    </span>
  );
};

export default LocationChip;
