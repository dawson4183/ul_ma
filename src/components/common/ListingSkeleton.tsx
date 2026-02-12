const ListingSkeleton = () => {
  return (
    <div className="listing-card animate-pulse">
      {/* Image skeleton */}
      <div className="aspect-[4/3] skeleton-shimmer" />
      
      {/* Content skeleton */}
      <div className="p-4 space-y-3">
        {/* Title */}
        <div className="h-5 skeleton-shimmer rounded-md w-3/4" />
        
        {/* Price */}
        <div className="h-6 skeleton-shimmer rounded-md w-1/3" />
        
        {/* Location chip */}
        <div className="h-6 skeleton-shimmer rounded-full w-1/2" />
      </div>
    </div>
  );
};

export default ListingSkeleton;
