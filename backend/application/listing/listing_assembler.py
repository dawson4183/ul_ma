"""
Assembler: ListingAssembler
Convertit entre DTOs (Application) et Entités (Domaine).
Responsable de la transformation des données entre les couches.
"""
import uuid
from datetime import datetime
from domain.listing.listing import Listing
from domain.listing.listing_price import ListingPrice
from domain.listing.listing_condition import ListingCondition
from application.listing.dtos.listing_creation_dto import ListingCreationDto
from application.listing.dtos.listing_response_dto import ListingResponseDto


class ListingAssembler:
    """
    Assembler pour convertir entre DTOs et Entité Listing.
    
    Un Assembler est un pattern qui sépare la logique de conversion
    des DTOs et des Entités. Il appartient à la couche Application.
    """
    
    @staticmethod
    def to_listing(dto: ListingCreationDto) -> Listing:
        """
        Convertit un ListingCreationDto en entité Listing.
        
        Cette méthode est utilisée lors de la création d'une annonce:
        API → DTO → Assembler → Entité Domaine
        
        Args:
            dto: DTO contenant les données de création
            
        Returns:
            Une nouvelle entité Listing
            
        Raises:
            ValueError: Si les données du DTO sont invalides
        """
        # Générer un nouvel ID unique (UUID)
        listing_id = str(uuid.uuid4())
        
        # Créer les Value Objects
        price = ListingPrice(dto.price)
        condition = ListingCondition.from_string(dto.condition)
        
        # Créer l'entité Listing
        listing = Listing(
            listing_id=listing_id,
            seller_id=dto.seller_id,
            title=dto.title,
            description=dto.description,
            price=price,
            category=dto.category,
            condition=condition,
            location=dto.location,
            course_code=dto.course_code,
            images=dto.images if dto.images else [],
            is_sold=False,
            created_at=datetime.now()
        )
        
        return listing
    
    @staticmethod
    def to_response_dto(listing: Listing) -> ListingResponseDto:
        """
        Convertit une entité Listing en ListingResponseDto.
        
        Cette méthode est utilisée pour retourner des données au client:
        Entité Domaine → Assembler → DTO → API → JSON
        
        Args:
            listing: L'entité Listing
            
        Returns:
            DTO pour la réponse API
        """
        return ListingResponseDto(
            listing_id=listing.listing_id,
            seller_id=listing.seller_id,
            title=listing.title,
            description=listing.description,
            price=listing.price.amount,  # Extraire la valeur du Value Object
            category=listing.category,
            condition=str(listing.condition),  # Convertir l'enum en string
            location=listing.location,
            course_code=listing.course_code,
            images=listing.images,
            is_sold=listing.is_sold,
            created_at=listing.created_at.isoformat()  # Format ISO 8601
        )
    
    @staticmethod
    def to_response_dto_list(listings: list[Listing]) -> list[ListingResponseDto]:
        """
        Convertit une liste d'entités Listing en liste de DTOs.
        
        Args:
            listings: Liste d'entités Listing
            
        Returns:
            Liste de DTOs pour la réponse API
        """
        return [
            ListingAssembler.to_response_dto(listing)
            for listing in listings
        ]
