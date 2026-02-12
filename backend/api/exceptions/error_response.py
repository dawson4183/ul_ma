"""
ErrorResponse: Format standardisé des erreurs API
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ErrorResponse:
    """
    Réponse d'erreur standardisée pour l'API.
    
    Format conforme aux bonnes pratiques REST:
    {
        "error": "ERROR_CODE_UPPERCASE",
        "description": "Message descriptif pour l'utilisateur",
        "field": "nom_du_champ"  # Optionnel
    }
    """
    
    error: str  # Code d'erreur en UPPERCASE
    description: str  # Message descriptif
    field: Optional[str] = None  # Champ en erreur (pour validation)
    
    def to_dict(self) -> dict:
        """
        Convertit en dictionnaire pour sérialisation JSON.
        
        Returns:
            Dictionnaire représentant l'erreur
        """
        response = {
            'error': self.error,
            'description': self.description
        }
        
        if self.field:
            response['field'] = self.field
        
        return response
