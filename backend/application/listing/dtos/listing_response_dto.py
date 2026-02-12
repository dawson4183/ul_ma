"""
DTO: ListingResponseDto
Data Transfer Object pour retourner une annonce via l'API.
"""
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ListingResponseDto:
    """
    DTO pour retourner les informations d'une annonce au client.
    
    Ce DTO est ce qui sera sérialisé en JSON et envoyé au frontend.
    Il peut contenir plus ou moins de champs que l'entité selon les besoins.
    """
    
    listing_id: str
    seller_id: str
    title: str
    description: str
    price: float
    category: str
    condition: str
    location: str
    course_code: Optional[str]
    images: List[str]
    is_sold: bool
    created_at: str  # ISO format string
    
    def to_dict(self) -> dict:
        """
        Convertit le DTO en dictionnaire pour sérialisation JSON.
        
        Returns:
            Dictionnaire représentant l'annonce
        """
        return {
            'listing_id': self.listing_id,
            'seller_id': self.seller_id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'condition': self.condition,
            'location': self.location,
            'course_code': self.course_code,
            'images': self.images,
            'is_sold': self.is_sold,
            'created_at': self.created_at
        }
