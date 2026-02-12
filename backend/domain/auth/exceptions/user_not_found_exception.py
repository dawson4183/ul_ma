"""
Exception métier: UserNotFoundException
Levée quand un utilisateur n'est pas trouvé.
"""
from typing import Optional

from domain.auth.exceptions.authentication_exception import AuthenticationException


class UserNotFoundException(AuthenticationException):
    """
    Exception levée quand un utilisateur n'existe pas dans le système.
    
    Cette exception est utilisée lorsqu'on tente d'authentifier
    un utilisateur avec un identifiant ou un email qui n'existe pas.
    """
    
    def __init__(self, user_id: Optional[str] = None):
        """
        Crée l'exception.
        
        Args:
            user_id: Identifiant de l'utilisateur recherché (optionnel)
        """
        self.user_id = user_id
        
        if user_id:
            message = f"Utilisateur non trouvé: {user_id}"
        else:
            message = "Utilisateur non trouvé"
        
        super().__init__(message)
