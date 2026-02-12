import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { mockListings, Listing } from '@/data/mockData';

interface ListingsContextType {
  listings: Listing[];
  deletedListingIds: Set<string>;
  deleteListing: (id: string) => void;
  isListingDeleted: (id: string) => boolean;
  getListingById: (id: string) => Listing | undefined;
}

const ListingsContext = createContext<ListingsContextType | undefined>(undefined);

export const ListingsProvider = ({ children }: { children: ReactNode }) => {
  const [listings, setListings] = useState<Listing[]>(mockListings);
  const [deletedListingIds, setDeletedListingIds] = useState<Set<string>>(new Set());

  const deleteListing = useCallback((id: string) => {
    setListings((prev) => prev.filter((listing) => listing.id !== id));
    setDeletedListingIds((prev) => new Set([...prev, id]));
  }, []);

  const isListingDeleted = useCallback((id: string) => {
    return deletedListingIds.has(id);
  }, [deletedListingIds]);

  const getListingById = useCallback((id: string): Listing | undefined => {
    return listings.find((listing) => listing.id === id);
  }, [listings]);

  return (
    <ListingsContext.Provider
      value={{
        listings,
        deletedListingIds,
        deleteListing,
        isListingDeleted,
        getListingById,
      }}
    >
      {children}
    </ListingsContext.Provider>
  );
};

export const useListings = () => {
  const context = useContext(ListingsContext);
  if (!context) {
    throw new Error('useListings must be used within a ListingsProvider');
  }
  return context;
};
