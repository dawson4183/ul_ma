"""
Exception Mapper: Convertit les exceptions d'authentification en réponses HTTP
"""
from typing import Any, Tuple
from flask import Flask, jsonify
from domain.auth.exceptions.user_not_found_exception import UserNotFoundException
from domain.auth.exceptions.invalid_credentials_exception import InvalidCredentialsException
from domain.auth.exceptions.session_expired_exception import SessionExpiredException
from domain.auth.exceptions.token_invalid_exception import TokenInvalidException
from api.exceptions.error_response import ErrorResponse


def register_auth_exception_handlers(app: Flask) -> None:
    """
    Enregistre les gestionnaires d'exceptions pour l'authentification.
    
    Cette fonction doit être appelée dans main.py pour activer
    la conversion automatique des exceptions en réponses HTTP.
    
    Args:
        app: Instance Flask
    """
    
    @app.errorhandler(UserNotFoundException)
    def handle_user_not_found(error: UserNotFoundException) -> Tuple[Any, int]:
        """
        Convertit UserNotFoundException en réponse HTTP 404.
        
        Args:
            error: L'exception levée
            
        Returns:
            Réponse JSON avec status 404
        """
        response = ErrorResponse(
            error='USER_NOT_FOUND',
            description=str(error)
        )
        return jsonify(response.to_dict()), 404
    
    @app.errorhandler(InvalidCredentialsException)
    def handle_invalid_credentials(error: InvalidCredentialsException) -> Tuple[Any, int]:
        """
        Convertit InvalidCredentialsException en réponse HTTP 401.
        
        Args:
            error: L'exception levée
            
        Returns:
            Réponse JSON avec status 401
        """
        response = ErrorResponse(
            error='INVALID_CREDENTIALS',
            description=str(error)
        )
        return jsonify(response.to_dict()), 401
    
    @app.errorhandler(SessionExpiredException)
    def handle_session_expired(error: SessionExpiredException) -> Tuple[Any, int]:
        """
        Convertit SessionExpiredException en réponse HTTP 401.
        
        Args:
            error: L'exception levée
            
        Returns:
            Réponse JSON avec status 401
        """
        response = ErrorResponse(
            error='SESSION_EXPIRED',
            description=str(error)
        )
        return jsonify(response.to_dict()), 401
    
    @app.errorhandler(TokenInvalidException)
    def handle_token_invalid(error: TokenInvalidException) -> Tuple[Any, int]:
        """
        Convertit TokenInvalidException en réponse HTTP 401.
        
        Args:
            error: L'exception levée
            
        Returns:
            Réponse JSON avec status 401
        """
        response = ErrorResponse(
            error='TOKEN_INVALID',
            description=str(error)
        )
        return jsonify(response.to_dict()), 401
