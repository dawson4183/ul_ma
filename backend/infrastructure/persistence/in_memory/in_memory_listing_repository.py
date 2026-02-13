"""
Repository: InMemoryListingRepository
Implémentation en mémoire du ListingRepository pour les tests et le développement.
"""
from typing import List, Optional, Dict
from domain.listing.listing import Listing
from domain.listing.listing_repository import ListingRepository


class InMemoryListingRepository(ListingRepository):
    """
    Implémentation en mémoire du repository des annonces.
    
    Utilisé pour:
    - Les tests unitaires (pas de dépendance à une vraie BDD)
    - Le développement local (pas besoin de configurer MySQL)
    - Les démos rapides
    
    Stockage: dictionnaire Python en mémoire (ne persiste pas après redémarrage)
    """
    
    def __init__(self):
        """Initialise le repository avec un stockage vide."""
        # Stockage en mémoire: clé = listing_id, valeur = Listing
        self._listings: Dict[str, Listing] = {}
    
    def find_by_id(self, listing_id: str) -> Optional[Listing]:
        """
        Trouve une annonce par son ID.
        
        Args:
            listing_id: ID de l'annonce
            
        Returns:
            L'annonce si trouvée, None sinon
        """
        return self._listings.get(listing_id)
    
    def find_all(self) -> List[Listing]:
        """
        Retourne toutes les annonces.
        
        Returns:
            Liste de toutes les annonces
        """
        return list(self._listings.values())
    
    def find_by_seller_id(self, seller_id: str) -> List[Listing]:
        """
        Trouve toutes les annonces d'un vendeur.
        
        Args:
            seller_id: ID du vendeur
            
        Returns:
            Liste des annonces du vendeur
        """
        return [
            listing for listing in self._listings.values()
            if listing.seller_id == seller_id
        ]
    
    def find_by_category(self, category: str) -> List[Listing]:
        """
        Trouve toutes les annonces d'une catégorie.
        
        Args:
            category: Catégorie recherchée
            
        Returns:
            Liste des annonces de cette catégorie
        """
        return [
            listing for listing in self._listings.values()
            if listing.category.lower() == category.lower()
        ]
    
    def search(self, query: str) -> List[Listing]:
        """
        Recherche des annonces par mots-clés.
        
        Args:
            query: Terme de recherche
            
        Returns:
            Liste des annonces correspondantes
        """
        query_lower = query.lower()
        return [
            listing for listing in self._listings.values()
            if (query_lower in listing.title.lower() or
                query_lower in listing.description.lower())
        ]
    
    def save(self, listing: Listing) -> None:
        """
        Sauvegarde une annonce (création ou mise à jour).
        
        Args:
            listing: L'annonce à sauvegarder
            
        Raises:
            RuntimeError: Si la sauvegarde échoue
        """
        if listing is None:
            raise RuntimeError("L'annonce ne peut pas être None")
        
        self._listings[listing.listing_id] = listing
    
    def delete(self, listing: Listing) -> None:
        """
        Supprime une annonce.
        
        Args:
            listing: L'annonce à supprimer
            
        Raises:
            RuntimeError: Si la suppression échoue
        """
        if listing is None:
            raise RuntimeError("L'annonce ne peut pas être None")
        
        if listing.listing_id in self._listings:
            del self._listings[listing.listing_id]
    
    def exists(self, listing_id: str) -> bool:
        """
        Vérifie si une annonce existe.
        
        Args:
            listing_id: ID de l'annonce
            
        Returns:
            True si l'annonce existe, False sinon
        """
        return listing_id in self._listings
    
    def count(self) -> int:
        """
        Retourne le nombre d'annonces stockées.
        
        Returns:
            Nombre d'annonces
        """
        return len(self._listings)
    
    def clear(self) -> None:
        """
        Vide le stockage (utile pour les tests).
        """
        self._listings.clear()
