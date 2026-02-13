"""
Resource: AuthResource
Définit les endpoints REST pour l'authentification (Couche API).
"""
from flask import Blueprint, request, jsonify, Response
from werkzeug.exceptions import UnsupportedMediaType
from typing import Tuple, Any, Union
import logging

from application.auth.auth_service import AuthService
from application.auth.dtos.register_request_dto import RegisterRequestDto
from application.auth.dtos.login_request_dto import LoginRequestDto
from infrastructure.persistence.mysql.mysql_user_repository import MySQLUserRepository
from infrastructure.persistence.mysql.mysql_session_repository import MySQLSessionRepository
from infrastructure.security.password_hasher import PasswordHasher
from infrastructure.security.jwt_service import JwtService
from infrastructure.database.connection import DatabaseConnection
from api.validators.auth_dto_validator import AuthDtoValidator
from api.exceptions.error_response import ErrorResponse
from domain.auth.exceptions.invalid_credentials_exception import InvalidCredentialsException
from domain.auth.exceptions.token_invalid_exception import TokenInvalidException
from domain.auth.exceptions.session_expired_exception import SessionExpiredException

logger = logging.getLogger(__name__)

# Créer le Blueprint Flask
auth_bp = Blueprint('auth', __name__)

# ===== Initialisation des dépendances =====
# Pour cet exemple, on crée les instances directement
# En production, utilisez l'injection de dépendances
_db_connection = DatabaseConnection()
_user_repository = MySQLUserRepository(_db_connection)
_session_repository = MySQLSessionRepository(_db_connection)
_password_hasher = PasswordHasher()
_jwt_service = JwtService(secret_key='votre-cle-super-secrete-pour-dev')
_auth_service = AuthService(
    _user_repository,
    _session_repository,
    _password_hasher,
    _jwt_service
)
_auth_validator = AuthDtoValidator()


@auth_bp.route('/auth/register', methods=['POST'])
def register() -> Tuple[Any, int]:
    """
    Endpoint: POST /api/auth/register
    Inscrit un nouvel utilisateur.
    
    Request Body (JSON):
    {
        "email": "user@example.com",
        "password": "password123",
        "idul": "ABCD123"
    }
    
    Response (201):
    {
        "token": "jwt-token",
        "expires_at": "2024-02-14T10:30:00",
        "user_id": 12345,
        "email": "user@example.com"
    }
    
    Errors:
    - 400: Données invalides
    - 409: Email déjà existant
    - 500: Erreur serveur
    """
    try:
        # 1. Extraire les données JSON
        try:
            data = request.get_json()
        except UnsupportedMediaType:
            data = None
        
        if not data:
            error = ErrorResponse(
                error='INVALID_REQUEST',
                description='Le corps de la requête doit être au format JSON valide'
            )
            return jsonify(error.to_dict()), 400
        
        logger.info(f"Requête d'inscription reçue: {data.get('email', 'N/A')}")
        
        # 2. Valider les données
        _auth_validator.validate_register(data)
        
        # 3. Créer le DTO
        register_dto = RegisterRequestDto(
            email=data['email'],
            password=data['password'],
            idul=data['idul']
        )
        
        # 4. Appeler le service
        response_dto = _auth_service.register(register_dto)
        
        # 5. Retourner la réponse
        return jsonify(response_dto.to_dict()), 201
        
    except ValueError as e:
        # Erreurs de validation ou email déjà existant
        logger.warning(f"Validation échouée: {str(e)}")
        # Déterminer si c'est une erreur de validation ou de conflit
        error_msg = str(e)
        if "existe déjà" in error_msg:
            error = ErrorResponse(
                error='EMAIL_ALREADY_EXISTS',
                description=error_msg
            )
            return jsonify(error.to_dict()), 409
        else:
            error = ErrorResponse(
                error='VALIDATION_ERROR',
                description=error_msg
            )
            return jsonify(error.to_dict()), 400
        
    except Exception as e:
        # Erreurs inattendues
        logger.error(f"Erreur lors de l'inscription: {str(e)}", exc_info=True)
        error = ErrorResponse(
            error='INTERNAL_SERVER_ERROR',
            description='Une erreur inattendue est survenue'
        )
        return jsonify(error.to_dict()), 500


@auth_bp.route('/auth/login', methods=['POST'])
def login() -> Tuple[Any, int]:
    """
    Endpoint: POST /api/auth/login
    Authentifie un utilisateur existant.
    
    Request Body (JSON):
    {
        "email": "user@example.com",
        "password": "password123"
    }
    
    Response (200):
    {
        "token": "jwt-token",
        "expires_at": "2024-02-14T10:30:00",
        "user_id": 12345,
        "email": "user@example.com"
    }
    
    Errors:
    - 400: Données invalides
    - 401: Identifiants invalides ou compte non vérifié
    - 500: Erreur serveur
    """
    try:
        # 1. Extraire les données JSON
        try:
            data = request.get_json()
        except UnsupportedMediaType:
            data = None
        
        if not data:
            error = ErrorResponse(
                error='INVALID_REQUEST',
                description='Le corps de la requête doit être au format JSON valide'
            )
            return jsonify(error.to_dict()), 400
        
        logger.info(f"Requête de connexion reçue: {data.get('email', 'N/A')}")
        
        # 2. Valider les données
        _auth_validator.validate_login(data)
        
        # 3. Créer le DTO
        login_dto = LoginRequestDto(
            email=data['email'],
            password=data['password']
        )
        
        # 4. Appeler le service
        response_dto = _auth_service.login(login_dto)
        
        # 5. Retourner la réponse
        return jsonify(response_dto.to_dict()), 200
        
    except ValueError as e:
        # Erreurs de validation
        logger.warning(f"Validation échouée: {str(e)}")
        error = ErrorResponse(
            error='VALIDATION_ERROR',
            description=str(e)
        )
        return jsonify(error.to_dict()), 400
        
    except InvalidCredentialsException as e:
        # Identifiants invalides
        logger.warning(f"Authentification échouée: {str(e)}")
        # Propager l'exception pour qu'elle soit gérée par l'exception mapper
        raise
        
    except Exception as e:
        # Erreurs inattendues
        logger.error(f"Erreur lors de la connexion: {str(e)}", exc_info=True)
        error = ErrorResponse(
            error='INTERNAL_SERVER_ERROR',
            description='Une erreur inattendue est survenue'
        )
        return jsonify(error.to_dict()), 500


@auth_bp.route('/auth/me', methods=['GET'])
def get_current_user() -> Tuple[Any, int]:
    """
    Endpoint: GET /api/auth/me
    Récupère les informations de l'utilisateur courant.
    
    Headers:
    - Authorization: Bearer <token>
    
    Response (200):
    {
        "user_id": 12345,
        "idul": "ABCD123",
        "email": "user@example.com",
        "is_verified": true,
        "is_active": true
    }
    
    Errors:
    - 401: Token manquant ou invalide
    - 500: Erreur serveur
    """
    try:
        # 1. Extraire le token du header Authorization
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            logger.warning("Tentative d'accès sans token")
            error = ErrorResponse(
                error='TOKEN_MISSING',
                description='Le header Authorization est requis'
            )
            return jsonify(error.to_dict()), 401
        
        # Vérifier le format Bearer
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            logger.warning(f"Format de token invalide: {auth_header}")
            error = ErrorResponse(
                error='TOKEN_INVALID_FORMAT',
                description='Le header doit être: Bearer <token>'
            )
            return jsonify(error.to_dict()), 401
        
        token = parts[1]
        logger.info("Requête GET /me reçue avec token")
        
        # 2. Appeler le service
        user_dto = _auth_service.get_current_user(token)
        
        # 3. Retourner la réponse
        return jsonify(user_dto.to_dict()), 200
        
    except (TokenInvalidException, SessionExpiredException):
        # Propager l'exception pour qu'elle soit gérée par l'exception mapper
        raise
        
    except Exception as e:
        # Erreurs inattendues
        logger.error(f"Erreur lors de la récupération de l'utilisateur: {str(e)}", exc_info=True)
        error = ErrorResponse(
            error='INTERNAL_SERVER_ERROR',
            description='Une erreur inattendue est survenue'
        )
        return jsonify(error.to_dict()), 500


@auth_bp.route('/auth/logout', methods=['POST'])
def logout() -> Tuple[Any, int]:
    """
    Endpoint: POST /api/auth/logout
    Déconnecte l'utilisateur courant.
    
    Headers:
    - Authorization: Bearer <token>
    
    Response (204): Pas de contenu
    
    Errors:
    - 401: Token manquant ou invalide
    - 500: Erreur serveur
    """
    try:
        # 1. Extraire le token du header Authorization
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            logger.warning("Tentative de déconnexion sans token")
            error = ErrorResponse(
                error='TOKEN_MISSING',
                description='Le header Authorization est requis'
            )
            return jsonify(error.to_dict()), 401
        
        # Vérifier le format Bearer
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            logger.warning(f"Format de token invalide: {auth_header}")
            error = ErrorResponse(
                error='TOKEN_INVALID_FORMAT',
                description='Le header doit être: Bearer <token>'
            )
            return jsonify(error.to_dict()), 401
        
        token = parts[1]
        logger.info("Requête de déconnexion reçue")
        
        # 2. Appeler le service
        _auth_service.logout(token)
        
        # 3. Retourner 204 No Content
        return ('', 204)
        
    except (TokenInvalidException, SessionExpiredException):
        # Propager l'exception pour qu'elle soit gérée par l'exception mapper
        raise
        
    except Exception as e:
        # Erreurs inattendues
        logger.error(f"Erreur lors de la déconnexion: {str(e)}", exc_info=True)
        error = ErrorResponse(
            error='INTERNAL_SERVER_ERROR',
            description='Une erreur inattendue est survenue'
        )
        return jsonify(error.to_dict()), 500


# Route de test pour vérifier que le module est chargé
@auth_bp.route('/auth/health', methods=['GET'])
def health() -> Tuple[Any, int]:
    """Endpoint de santé pour vérifier que le module fonctionne"""
    return jsonify({
        'status': 'healthy',
        'module': 'auth',
        'endpoints': [
            'POST /api/auth/register',
            'POST /api/auth/login',
            'GET /api/auth/me',
            'POST /api/auth/logout'
        ]
    }), 200
