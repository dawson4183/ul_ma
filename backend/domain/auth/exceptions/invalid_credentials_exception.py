"""
Exception métier: InvalidCredentialsException
Levée quand les identifiants sont invalides.
"""
from typing import Optional

from domain.auth.exceptions.authentication_exception import AuthenticationException


class InvalidCredentialsException(AuthenticationException):
    """
    Exception levée quand les identifiants (email/password) sont invalides.
    
    Cette exception est utilisée lors de la vérification des credentials
    pour indiquer que le mot de passe ou l'email ne correspondent pas.
    """
    
    def __init__(self, message: Optional[str] = None):
        """
        Crée l'exception.
        
        Args:
            message: Message personnalisé (optionnel)
        """
        super().__init__(message if message else "Identifiants invalides")
