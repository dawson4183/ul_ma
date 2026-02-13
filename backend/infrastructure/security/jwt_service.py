"""Service JWT pour la génération et validation des tokens."""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import jwt

from domain.auth.exceptions.token_invalid_exception import TokenInvalidException
from domain.auth.exceptions.session_expired_exception import SessionExpiredException


class JwtService:
    """Service pour générer et valider les tokens JWT."""

    def __init__(self, secret_key: str):
        """
        Initialise le service JWT avec une clé secrète.

        Args:
            secret_key: La clé secrète pour signer les tokens

        Raises:
            ValueError: Si la clé secrète est vide ou None
        """
        if not secret_key:
            raise ValueError("La clé secrète ne peut pas être vide")
        self._secret_key = secret_key
        self._algorithm = "HS256"
        self._token_lifetime_hours = 24

    def generate_token(self, user_id: int, email: str) -> str:
        """
        Génère un token JWT pour un utilisateur.

        Args:
            user_id: L'identifiant de l'utilisateur
            email: L'email de l'utilisateur

        Returns:
            Un token JWT signé valide pour 24 heures

        Raises:
            ValueError: Si user_id ou email est vide/None
        """
        if not user_id:
            raise ValueError("L'identifiant utilisateur ne peut pas être vide")
        if not email:
            raise ValueError("L'email ne peut pas être vide")

        # Calcul de l'expiration (24 heures à partir de maintenant)
        expires_at = datetime.utcnow() + timedelta(hours=self._token_lifetime_hours)

        # Payload du token avec claims standard et personnalisés
        payload: Dict[str, Any] = {
            "user_id": user_id,
            "email": email,
            "exp": expires_at,
            "iat": datetime.utcnow(),  # issued at
            "type": "auth"  # type de token
        }

        # Génération du token JWT
        token = jwt.encode(payload, self._secret_key, algorithm=self._algorithm)
        return token

    def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Valide un token JWT et retourne son payload.

        Args:
            token: Le token JWT à valider

        Returns:
            Le payload décodé du token si valide

        Raises:
            TokenInvalidException: Si le token est invalide (format, signature)
            SessionExpiredException: Si le token est expiré
            ValueError: Si le token est vide ou None
        """
        if not token:
            raise ValueError("Le token ne peut pas être vide")

        try:
            # Décodage et validation du token
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            # Le token est expiré
            raise SessionExpiredException(token)
        except jwt.InvalidTokenError as e:
            # Le token est invalide (signature, format, etc.)
            raise TokenInvalidException(token)
