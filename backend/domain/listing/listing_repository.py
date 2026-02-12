"""
Interface (Port) : ListingRepository
Définit le contrat pour la persistance des annonces.
Le Domaine définit l'interface, l'Infrastructure l'implémente.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.listing.listing import Listing


class ListingRepository(ABC):
    """
    Interface définissant les opérations de persistance pour les annonces.
    
    Cette interface est un PORT dans l'architecture hexagonale.
    Elle est définie dans le Domaine mais implémentée dans l'Infrastructure.
    
    Principe de l'inversion de dépendances (DIP) :
    - Le Domaine ne dépend PAS de l'Infrastructure
    - L'Infrastructure dépend du Domaine (implémente cette interface)
    """
    
    @abstractmethod
    def find_by_id(self, listing_id: str) -> Optional[Listing]:
        """
        Trouve une annonce par son ID.
        
        Args:
            listing_id: ID de l'annonce
            
        Returns:
            L'annonce si trouvée, None sinon
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[Listing]:
        """
        Retourne toutes les annonces.
        
        Returns:
            Liste de toutes les annonces
        """
        pass
    
    @abstractmethod
    def find_by_seller_id(self, seller_id: str) -> List[Listing]:
        """
        Trouve toutes les annonces d'un vendeur.
        
        Args:
            seller_id: ID du vendeur
            
        Returns:
            Liste des annonces du vendeur
        """
        pass
    
    @abstractmethod
    def find_by_category(self, category: str) -> List[Listing]:
        """
        Trouve toutes les annonces d'une catégorie.
        
        Args:
            category: Catégorie recherchée
            
        Returns:
            Liste des annonces de cette catégorie
        """
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[Listing]:
        """
        Recherche des annonces par mots-clés.
        
        Args:
            query: Terme de recherche
            
        Returns:
            Liste des annonces correspondantes
        """
        pass
    
    @abstractmethod
    def save(self, listing: Listing) -> None:
        """
        Sauvegarde une annonce (création ou mise à jour).
        
        Args:
            listing: L'annonce à sauvegarder
            
        Raises:
            RuntimeError: Si la sauvegarde échoue
        """
        pass
    
    @abstractmethod
    def delete(self, listing: Listing) -> None:
        """
        Supprime une annonce.
        
        Args:
            listing: L'annonce à supprimer
            
        Raises:
            RuntimeError: Si la suppression échoue
        """
        pass
    
    @abstractmethod
    def exists(self, listing_id: str) -> bool:
        """
        Vérifie si une annonce existe.
        
        Args:
            listing_id: ID de l'annonce
            
        Returns:
            True si l'annonce existe, False sinon
        """
        pass
