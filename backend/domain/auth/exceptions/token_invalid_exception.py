"""
Exception métier: TokenInvalidException
Levée quand un token est invalide.
"""
from typing import Optional

from domain.auth.exceptions.authentication_exception import AuthenticationException


class TokenInvalidException(AuthenticationException):
    """
    Exception levée quand un token JWT est invalide.
    
    Cette exception est utilisée lors de la validation d'un token
    pour indiquer que le format ou la signature est incorrecte.
    """
    
    def __init__(self, token: Optional[str] = None):
        """
        Crée l'exception.
        
        Args:
            token: Token invalide (optionnel)
        """
        self.token = token
        
        if token:
            # On tronque le token pour ne pas l'exposer en entier dans les logs
            masked_token = token[:10] + "..." if len(token) > 10 else token
            message = f"Token invalide: {masked_token}"
        else:
            message = "Token invalide"
        
        super().__init__(message)
