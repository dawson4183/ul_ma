"""
DTO: UserResponseDto
Data Transfer Object pour retourner les informations utilisateur.
"""
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class UserResponseDto:
    """
    DTO contenant les informations utilisateur à retourner.
    
    Attributs:
        user_id: Identifiant de l'utilisateur
        idul: Identifiant UL à 7 caractères
        email: Adresse email de l'utilisateur
        is_verified: Indique si l'email est vérifié
        is_active: Indique si le compte est actif
    """
    
    user_id: int
    idul: str
    email: str
    is_verified: bool
    is_active: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit le DTO en dictionnaire pour sérialisation JSON.
        
        Returns:
            Dictionnaire représentant l'utilisateur
        """
        return {
            'user_id': self.user_id,
            'idul': self.idul,
            'email': self.email,
            'is_verified': self.is_verified,
            'is_active': self.is_active
        }
