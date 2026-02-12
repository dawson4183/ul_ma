"""
Exception métier: SessionExpiredException
Levée quand une session est expirée.
"""
from typing import Optional

from domain.auth.exceptions.authentication_exception import AuthenticationException


class SessionExpiredException(AuthenticationException):
    """
    Exception levée quand une session a expiré.
    
    Cette exception est utilisée lors de la validation d'un token
    pour indiquer que la session associée n'est plus valide.
    """
    
    def __init__(self, token: Optional[str] = None):
        """
        Crée l'exception.
        
        Args:
            token: Token de la session expirée (optionnel)
        """
        self.token = token
        
        if token:
            # On tronque le token pour ne pas l'exposer en entier dans les logs
            masked_token = token[:10] + "..." if len(token) > 10 else token
            message = f"Session expirée pour le token: {masked_token}"
        else:
            message = "Session expirée"
        
        super().__init__(message)
