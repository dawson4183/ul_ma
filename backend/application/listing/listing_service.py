"""
Service: ListingService
Orchestre les opérations métier liées aux annonces.
Coordonne le Domaine et l'Infrastructure.
"""
import logging
from typing import List
from domain.listing.listing_repository import ListingRepository
from domain.listing.exceptions.listing_not_found_exception import ListingNotFoundException
from application.listing.listing_assembler import ListingAssembler
from application.listing.dtos.listing_creation_dto import ListingCreationDto
from application.listing.dtos.listing_response_dto import ListingResponseDto

logger = logging.getLogger(__name__)


class ListingService:
    """
    Service gérant les opérations sur les annonces.
    
    Le Service fait partie de la couche Application.
    Il orchestre les opérations entre le Domaine et l'Infrastructure.
    
    Responsabilités:
    - Coordonner les appels au repository
    - Convertir entre DTOs et Entités (via Assembler)
    - Gérer les transactions
    - Logger les opérations importantes
    """
    
    def __init__(
        self,
        listing_repository: ListingRepository,
        listing_assembler: ListingAssembler
    ):
        """
        Initialise le service avec ses dépendances.
        
        Args:
            listing_repository: Repository pour la persistance
            listing_assembler: Assembler pour les conversions
            
        Note: Les dépendances sont injectées (Dependency Injection)
        """
        self._listing_repository = listing_repository
        self._listing_assembler = listing_assembler
    
    def create_listing(self, dto: ListingCreationDto) -> ListingResponseDto:
        """
        Crée une nouvelle annonce.
        
        Flux:
        1. Convertir DTO → Entité (via Assembler)
        2. Valider l'entité (logique dans le constructeur)
        3. Sauvegarder dans le repository
        4. Convertir Entité → DTO de réponse
        5. Retourner le DTO
        
        Args:
            dto: Données de création de l'annonce
            
        Returns:
            DTO contenant l'annonce créée
            
        Raises:
            ValueError: Si les données sont invalides
        """
        logger.info(f"Création d'une annonce: '{dto.title}' par vendeur {dto.seller_id}")
        
        try:
            # 1. Convertir DTO → Entité Domaine
            listing = self._listing_assembler.to_listing(dto)
            
            # 2. Sauvegarder (la validation est faite dans le constructeur de Listing)
            self._listing_repository.save(listing)
            
            logger.info(f"Annonce créée avec succès: {listing.listing_id}")
            
            # 3. Convertir Entité → DTO de réponse
            response_dto = self._listing_assembler.to_response_dto(listing)
            
            return response_dto
            
        except ValueError as e:
            logger.error(f"Erreur lors de la création de l'annonce: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la création: {str(e)}", exc_info=True)
            raise RuntimeError(f"Erreur lors de la création de l'annonce: {str(e)}")
    
    def get_listing_by_id(self, listing_id: str) -> ListingResponseDto:
        """
        Récupère une annonce par son ID.
        
        Args:
            listing_id: ID de l'annonce
            
        Returns:
            DTO contenant l'annonce
            
        Raises:
            ListingNotFoundException: Si l'annonce n'existe pas
        """
        logger.info(f"Récupération de l'annonce: {listing_id}")
        
        listing = self._listing_repository.find_by_id(listing_id)
        
        if not listing:
            logger.warning(f"Annonce non trouvée: {listing_id}")
            raise ListingNotFoundException(listing_id)
        
        return self._listing_assembler.to_response_dto(listing)
    
    def get_all_listings(self) -> List[ListingResponseDto]:
        """
        Récupère toutes les annonces.
        
        Returns:
            Liste de DTOs des annonces
        """
        logger.info("Récupération de toutes les annonces")
        
        listings = self._listing_repository.find_all()
        
        return self._listing_assembler.to_response_dto_list(listings)
    
    def get_listings_by_seller(self, seller_id: str) -> List[ListingResponseDto]:
        """
        Récupère toutes les annonces d'un vendeur.
        
        Args:
            seller_id: ID du vendeur
            
        Returns:
            Liste de DTOs des annonces du vendeur
        """
        logger.info(f"Récupération des annonces du vendeur: {seller_id}")
        
        listings = self._listing_repository.find_by_seller_id(seller_id)
        
        return self._listing_assembler.to_response_dto_list(listings)
    
    def search_listings(self, query: str) -> List[ListingResponseDto]:
        """
        Recherche des annonces par mots-clés.
        
        Args:
            query: Terme de recherche
            
        Returns:
            Liste de DTOs des annonces correspondantes
        """
        logger.info(f"Recherche d'annonces: '{query}'")
        
        listings = self._listing_repository.search(query)
        
        return self._listing_assembler.to_response_dto_list(listings)
    
    def delete_listing(self, listing_id: str, user_id: str) -> None:
        """
        Supprime une annonce.
        
        Règles métier:
        - Seul le vendeur peut supprimer son annonce
        - Une annonce vendue ne peut pas être supprimée
        
        Args:
            listing_id: ID de l'annonce
            user_id: ID de l'utilisateur demandant la suppression
            
        Raises:
            ListingNotFoundException: Si l'annonce n'existe pas
            PermissionError: Si l'utilisateur n'est pas autorisé
        """
        logger.info(f"Suppression de l'annonce {listing_id} par utilisateur {user_id}")
        
        # Récupérer l'annonce
        listing = self._listing_repository.find_by_id(listing_id)
        
        if not listing:
            raise ListingNotFoundException(listing_id)
        
        # Vérifier les permissions (règle métier)
        if not listing.can_be_edited_by(user_id):
            logger.warning(
                f"Tentative non autorisée de suppression: "
                f"listing={listing_id}, user={user_id}"
            )
            raise PermissionError("Vous n'êtes pas autorisé à supprimer cette annonce")
        
        # Supprimer
        self._listing_repository.delete(listing)
        
        logger.info(f"Annonce supprimée: {listing_id}")
