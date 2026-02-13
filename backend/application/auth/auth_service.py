"""
Service d'application: AuthService
Orchestre les opérations d'authentification.
Ce service coordonne les repositories et les services de sécurité.
"""
from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from domain.user.user import User
from domain.user.user_repository import UserRepository
from domain.auth.session import Session
from domain.auth.session_repository import SessionRepository
from domain.auth.exceptions.invalid_credentials_exception import InvalidCredentialsException
from domain.auth.exceptions.token_invalid_exception import TokenInvalidException
from domain.auth.exceptions.session_expired_exception import SessionExpiredException
from application.auth.dtos.register_request_dto import RegisterRequestDto
from application.auth.dtos.login_request_dto import LoginRequestDto
from application.auth.dtos.auth_response_dto import AuthResponseDto
from application.auth.dtos.user_response_dto import UserResponseDto
from infrastructure.security.password_hasher import PasswordHasher
from infrastructure.security.jwt_service import JwtService


class AuthService:
    """
    Service d'application pour l'authentification.
    
    Ce service orchestre les opérations d'authentification:
    - Inscription (register)
    - Connexion (login)
    - Récupération de l'utilisateur courant (get_current_user)
    - Déconnexion (logout)
    
    Il utilise l'injection de dépendances pour accéder aux repositories
    et aux services de sécurité.
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        session_repository: SessionRepository,
        password_hasher: PasswordHasher,
        jwt_service: JwtService
    ):
        """
        Initialise le service d'authentification.
        
        Args:
            user_repository: Repository pour les utilisateurs
            session_repository: Repository pour les sessions
            password_hasher: Service de hashage des mots de passe
            jwt_service: Service JWT pour générer/valider les tokens
        """
        self._user_repository = user_repository
        self._session_repository = session_repository
        self._password_hasher = password_hasher
        self._jwt_service = jwt_service
    
    def _user_id_to_int(self, user_id: str) -> int:
        """
        Convertit un user_id string en integer de manière déterministe.
        
        Cette méthode fonctionne avec n'importe quel format de string
        (UUID, format simple comme 'user-123', etc.)
        
        Args:
            user_id: L'identifiant utilisateur sous forme de string
            
        Returns:
            Un entier représentant l'user_id
        """
        # Utiliser hash() pour convertir n'importe quel string en entier
        # On limite à un entier 32-bit positif pour compatibilité
        return abs(hash(user_id)) % (2**31)
    
    def register(self, dto: RegisterRequestDto) -> AuthResponseDto:
        """
        Inscrit un nouvel utilisateur.
        
        Args:
            dto: Données d'inscription (email, password, idul)
            
        Returns:
            AuthResponseDto avec le token JWT et les infos utilisateur
            
        Raises:
            ValueError: Si l'email existe déjà
        """
        # Vérifier si l'email existe déjà
        if self._user_repository.exists_by_email(dto.email):
            raise ValueError(f"Un utilisateur existe déjà avec l'email: {dto.email}")
        
        # Hasher le mot de passe
        password_hash = self._password_hasher.hash_password(dto.password)
        
        # Créer l'utilisateur
        user_id = str(uuid4())
        user = User(
            user_id=user_id,
            idul=dto.idul,
            email=dto.email,
            password_hash=password_hash,
            is_verified=False,  # Par défaut, l'email n'est pas vérifié
            is_active=True
        )
        
        # Sauvegarder l'utilisateur
        self._user_repository.save(user)
        
        # Générer le token JWT
        token = self._jwt_service.generate_token(
            user_id=self._user_id_to_int(user.user_id),
            email=user.email
        )
        
        # Créer la session
        expires_at = datetime.now() + timedelta(hours=24)
        session_id = str(uuid4())
        session = Session(
            session_id=session_id,
            user_id=user_id,
            token=token,
            token_type=Session.TOKEN_TYPE_AUTH,
            expires_at=expires_at
        )
        self._session_repository.save(session)
        
        # Retourner la réponse
        return AuthResponseDto(
            token=token,
            expires_at=expires_at.isoformat(),
            user_id=self._user_id_to_int(user_id),
            email=user.email
        )
    
    def login(self, dto: LoginRequestDto) -> AuthResponseDto:
        """
        Authentifie un utilisateur existant.
        
        Args:
            dto: Données de connexion (email, password)
            
        Returns:
            AuthResponseDto avec le token JWT et les infos utilisateur
            
        Raises:
            InvalidCredentialsException: Si email ou mot de passe invalide
        """
        # Trouver l'utilisateur par email
        user = self._user_repository.find_by_email(dto.email)
        if user is None:
            raise InvalidCredentialsException("Email ou mot de passe invalide")
        
        # Vérifier le mot de passe
        if not self._password_hasher.verify_password(dto.password, user.password_hash):
            raise InvalidCredentialsException("Email ou mot de passe invalide")
        
        # Vérifier que l'utilisateur peut s'authentifier (actif et vérifié)
        if not user.can_authenticate():
            raise InvalidCredentialsException("Compte non vérifié ou désactivé")
        
        # Générer le token JWT
        token = self._jwt_service.generate_token(
            user_id=self._user_id_to_int(user.user_id),
            email=user.email
        )
        
        # Créer la session
        expires_at = datetime.now() + timedelta(hours=24)
        session_id = str(uuid4())
        session = Session(
            session_id=session_id,
            user_id=user.user_id,
            token=token,
            token_type=Session.TOKEN_TYPE_AUTH,
            expires_at=expires_at
        )
        self._session_repository.save(session)
        
        # Retourner la réponse
        return AuthResponseDto(
            token=token,
            expires_at=expires_at.isoformat(),
            user_id=self._user_id_to_int(user.user_id),
            email=user.email
        )
    
    def get_current_user(self, token: str) -> UserResponseDto:
        """
        Récupère l'utilisateur courant à partir d'un token JWT.
        
        Args:
            token: Le token JWT
            
        Returns:
            UserResponseDto avec les informations de l'utilisateur
            
        Raises:
            TokenInvalidException: Si le token est invalide
            SessionExpiredException: Si le token est expiré
            InvalidCredentialsException: Si l'utilisateur n'existe pas
        """
        # Valider le token JWT
        try:
            payload = self._jwt_service.validate_token(token)
        except (TokenInvalidException, SessionExpiredException):
            raise
        
        # Extraire l'email du payload
        email = payload.get('email')
        if not email:
            raise TokenInvalidException(token)
        
        # Trouver l'utilisateur par email
        user = self._user_repository.find_by_email(email)
        if user is None:
            raise InvalidCredentialsException("Utilisateur non trouvé")
        
        # Retourner les infos utilisateur
        return UserResponseDto(
            user_id=self._user_id_to_int(user.user_id),
            idul=user.idul,
            email=user.email,
            is_verified=user.is_verified,
            is_active=user.is_active
        )
    
    def logout(self, token: str) -> None:
        """
        Déconnecte un utilisateur en invalidant sa session.
        
        Args:
            token: Le token JWT à invalider
            
        Raises:
            TokenInvalidException: Si le token est invalide
        """
        # Trouver la session par token
        session = self._session_repository.find_by_token(token)
        if session is None:
            # Si pas de session trouvée, on considère que c'est déjà déconnecté
            return
        
        # Marquer la session comme utilisée (invalide le token)
        self._session_repository.mark_as_used(session.session_id)
