"""
Entité: Listing
Représente une annonce de produit dans le système.
Une entité a une identité propre (ID) et peut changer d'état.
"""
from datetime import datetime
from typing import List, Optional
from domain.listing.listing_price import ListingPrice
from domain.listing.listing_condition import ListingCondition


class Listing:
    """
    Entité représentant une annonce de produit.
    
    Une annonce contient:
    - Des informations sur le produit (titre, description, prix)
    - Des métadonnées (catégorie, condition, localisation)
    - Des relations (vendeur, images)
    - Un état (vendue ou non)
    """
    
    def __init__(
        self,
        listing_id: str,
        seller_id: str,
        title: str,
        description: str,
        price: ListingPrice,
        category: str,
        condition: ListingCondition,
        location: str,
        course_code: Optional[str] = None,
        images: Optional[List[str]] = None,
        is_sold: bool = False,
        created_at: Optional[datetime] = None
    ):
        """
        Crée une annonce.
        
        Args:
            listing_id: Identifiant unique de l'annonce
            seller_id: ID du vendeur
            title: Titre de l'annonce
            description: Description détaillée
            price: Prix (Value Object)
            category: Catégorie (books, electronics, etc.)
            condition: État du produit (Value Object)
            location: Lieu de remise sur le campus
            course_code: Code de cours (optionnel, ex: GLO-2005)
            images: Liste des URLs des images
            is_sold: Statut de vente
            created_at: Date de création
        
        Raises:
            ValueError: Si les données sont invalides
        """
        # Validation des champs obligatoires
        if not listing_id or not listing_id.strip():
            raise ValueError("L'ID de l'annonce est requis")
        
        if not seller_id or not seller_id.strip():
            raise ValueError("L'ID du vendeur est requis")
        
        if not title or not title.strip():
            raise ValueError("Le titre est requis")
        
        if len(title) < 5:
            raise ValueError("Le titre doit contenir au moins 5 caractères")
        
        if len(title) > 200:
            raise ValueError("Le titre ne peut pas dépasser 200 caractères")
        
        if not description or not description.strip():
            raise ValueError("La description est requise")
        
        if len(description) < 10:
            raise ValueError("La description doit contenir au moins 10 caractères")
        
        if not category or not category.strip():
            raise ValueError("La catégorie est requise")
        
        if not location or not location.strip():
            raise ValueError("Le lieu de remise est requis")
        
        # Assignation des attributs
        self._listing_id = listing_id
        self._seller_id = seller_id
        self._title = title.strip()
        self._description = description.strip()
        self._price = price
        self._category = category.strip()
        self._condition = condition
        self._location = location.strip()
        self._course_code = course_code.strip() if course_code else None
        self._images = images if images else []
        self._is_sold = is_sold
        self._created_at = created_at if created_at else datetime.now()
    
    # ===== Properties (Getters) =====
    
    @property
    def listing_id(self) -> str:
        return self._listing_id
    
    @property
    def seller_id(self) -> str:
        return self._seller_id
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def price(self) -> ListingPrice:
        return self._price
    
    @property
    def category(self) -> str:
        return self._category
    
    @property
    def condition(self) -> ListingCondition:
        return self._condition
    
    @property
    def location(self) -> str:
        return self._location
    
    @property
    def course_code(self) -> Optional[str]:
        return self._course_code
    
    @property
    def images(self) -> List[str]:
        return self._images.copy()  # Retourner une copie pour immutabilité
    
    @property
    def is_sold(self) -> bool:
        return self._is_sold
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    # ===== Méthodes Métier =====
    
    def mark_as_sold(self) -> None:
        """
        Marque l'annonce comme vendue.
        Règle métier: Une annonce vendue ne peut plus être modifiée.
        """
        if self._is_sold:
            raise ValueError("L'annonce est déjà marquée comme vendue")
        
        self._is_sold = True
    
    def add_image(self, image_url: str) -> None:
        """
        Ajoute une image à l'annonce.
        
        Args:
            image_url: URL de l'image
            
        Raises:
            ValueError: Si l'annonce a déjà 5 images (maximum)
        """
        if len(self._images) >= 5:
            raise ValueError("Maximum 5 images autorisées par annonce")
        
        if not image_url or not image_url.strip():
            raise ValueError("L'URL de l'image ne peut pas être vide")
        
        self._images.append(image_url.strip())
    
    def can_be_edited_by(self, user_id: str) -> bool:
        """
        Vérifie si un utilisateur peut éditer cette annonce.
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            True si l'utilisateur est le vendeur et l'annonce n'est pas vendue
        """
        return self._seller_id == user_id and not self._is_sold
    
    def __repr__(self) -> str:
        return (
            f"Listing(id={self._listing_id}, "
            f"title='{self._title}', "
            f"price={self._price}, "
            f"is_sold={self._is_sold})"
        )
