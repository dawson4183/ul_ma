"""
DTO: AuthResponseDto
Data Transfer Object pour la réponse d'authentification.
"""
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class AuthResponseDto:
    """
    DTO contenant les données de réponse après authentification.
    
    Attributs:
        token: Le token JWT
        expires_at: Date d'expiration au format ISO
        user_id: Identifiant de l'utilisateur
        email: Adresse email de l'utilisateur
    """
    
    token: str
    expires_at: str
    user_id: int
    email: str
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit le DTO en dictionnaire pour sérialisation JSON.
        
        Returns:
            Dictionnaire représentant la réponse d'authentification
        """
        return {
            'token': self.token,
            'expires_at': self.expires_at,
            'user_id': self.user_id,
            'email': self.email
        }
