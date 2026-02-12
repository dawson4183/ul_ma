import { CheckCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface VerifiedBadgeProps {
  className?: string;
  showText?: boolean;
}

const VerifiedBadge = ({ className, showText = true }: VerifiedBadgeProps) => {
  return (
    <span className={cn('verified-badge', className)}>
      <CheckCircle className="w-3.5 h-3.5 text-gold" />
      {showText && <span>Vérifié</span>}
    </span>
  );
};

export default VerifiedBadge;
