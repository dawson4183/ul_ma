"""
Exception métier: AuthenticationException
Classe de base pour toutes les exceptions d'authentification.
"""
from typing import Optional


class AuthenticationException(RuntimeError):
    """
    Exception de base pour les erreurs d'authentification.
    
    Cette exception est la classe parent de toutes les exceptions
    liées à l'authentification (login, token, session, etc.).
    Elle hérite de RuntimeError pour être compatible avec les
    autres exceptions du domaine.
    """
    
    def __init__(self, message: Optional[str] = None):
        """
        Crée l'exception.
        
        Args:
            message: Message décrivant l'erreur d'authentification
        """
        if message is None:
            message = "Erreur d'authentification"
        
        super().__init__(message)
