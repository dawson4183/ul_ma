"""
Entité: Session
Représente une session d'authentification JWT dans le système.
Une entité a une identité propre (session_id) et peut changer d'état.
"""
from datetime import datetime
from typing import Optional


class Session:
    """
    Entité représentant une session d'authentification.
    
    Une session contient:
    - Un identifiant unique (session_id)
    - Une référence à l'utilisateur (user_id)
    - Un token JWT (token)
    - Un type de token (token_type)
    - Une date d'expiration (expires_at)
    - Une date d'utilisation (used_at)
    """
    
    # Types de token valides
    TOKEN_TYPE_AUTH = 'auth'
    TOKEN_TYPE_EMAIL_VERIFICATION = 'email_verification'
    TOKEN_TYPE_PASSWORD_RESET = 'password_reset'
    
    VALID_TOKEN_TYPES = [
        TOKEN_TYPE_AUTH,
        TOKEN_TYPE_EMAIL_VERIFICATION,
        TOKEN_TYPE_PASSWORD_RESET
    ]
    
    def __init__(
        self,
        session_id: str,
        user_id: str,
        token: str,
        token_type: str,
        expires_at: datetime,
        used_at: Optional[datetime] = None
    ):
        """
        Crée une session d'authentification.
        
        Args:
            session_id: Identifiant unique de la session (UUID)
            user_id: Identifiant de l'utilisateur associé (UUID)
            token: Token JWT
            token_type: Type de token ('auth', 'email_verification', 'password_reset')
            expires_at: Date d'expiration de la session
            used_at: Date d'utilisation du token (None si non utilisé)
        
        Raises:
            ValueError: Si les données sont invalides
        """
        # Validation des champs obligatoires
        if not session_id or not session_id.strip():
            raise ValueError("L'ID de session est requis")
        
        if not user_id or not user_id.strip():
            raise ValueError("L'ID utilisateur est requis")
        
        if not token or not token.strip():
            raise ValueError("Le token est requis")
        
        if not token_type or token_type not in self.VALID_TOKEN_TYPES:
            raise ValueError(
                f"Le type de token doit être l'un de: {', '.join(self.VALID_TOKEN_TYPES)}"
            )
        
        if not isinstance(expires_at, datetime):
            raise ValueError("La date d'expiration doit être un datetime")
        
        if used_at is not None and not isinstance(used_at, datetime):
            raise ValueError("La date d'utilisation doit être un datetime ou None")
        
        # Assignation des attributs
        self._session_id = session_id
        self._user_id = user_id
        self._token = token
        self._token_type = token_type
        self._expires_at = expires_at
        self._used_at = used_at
    
    # ===== Properties (Getters) =====
    
    @property
    def session_id(self) -> str:
        return self._session_id
    
    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def token(self) -> str:
        return self._token
    
    @property
    def token_type(self) -> str:
        return self._token_type
    
    @property
    def expires_at(self) -> datetime:
        return self._expires_at
    
    @property
    def used_at(self) -> Optional[datetime]:
        return self._used_at
    
    # ===== Méthodes Métier =====
    
    def is_expired(self) -> bool:
        """
        Vérifie si la session est expirée.
        
        Compare la date d'expiration avec la date/heure actuelle.
        
        Returns:
            True si la session est expirée, False sinon
        """
        return datetime.now() > self._expires_at
    
    def is_used(self) -> bool:
        """
        Vérifie si le token a été utilisé.
        
        Returns:
            True si used_at est défini (non None), False sinon
        """
        return self._used_at is not None
    
    def mark_as_used(self) -> None:
        """
        Marque le token comme utilisé.
        
        Définit la date/heure actuelle comme date d'utilisation.
        Cette méthode est appelée lors de la consommation du token.
        """
        self._used_at = datetime.now()
    
    def __repr__(self) -> str:
        return (
            f"Session(session_id={self._session_id}, "
            f"user_id={self._user_id}, "
            f"token_type='{self._token_type}', "
            f"expires_at={self._expires_at}, "
            f"is_used={self.is_used()})"
        )
