"""
DTO: ListingCreationDto
Data Transfer Object pour la création d'une annonce.
Utilisé pour transférer des données entre les couches (API → Application).
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ListingCreationDto:
    """
    DTO contenant les données nécessaires pour créer une annonce.
    
    Un DTO est un simple conteneur de données sans logique métier.
    Il sert à transporter des données entre les couches de l'application.
    
    Utilise @dataclass pour générer automatiquement __init__, __repr__, etc.
    """
    
    # Données obligatoires
    seller_id: str
    title: str
    description: str
    price: float
    category: str
    condition: str
    location: str
    
    # Données optionnelles
    course_code: Optional[str] = None
    images: Optional[List[str]] = None
    
    def __post_init__(self):
        """
        Validation de base après initialisation.
        Note: La validation complète se fait dans le validator de la couche API.
        """
        # S'assurer que images est une liste même si None
        if self.images is None:
            self.images = []
