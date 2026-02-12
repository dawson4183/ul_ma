"""
Tests pour les exceptions métier d'authentification.
"""
import pytest

from domain.auth.exceptions.authentication_exception import AuthenticationException
from domain.auth.exceptions.user_not_found_exception import UserNotFoundException
from domain.auth.exceptions.invalid_credentials_exception import InvalidCredentialsException
from domain.auth.exceptions.session_expired_exception import SessionExpiredException
from domain.auth.exceptions.token_invalid_exception import TokenInvalidException


class TestAuthenticationException:
    """Tests pour AuthenticationException"""
    
    def test_default_message(self):
        """Vérifie que le message par défaut est utilisé"""
        exc = AuthenticationException()
        
        assert str(exc) == "Erreur d'authentification"
    
    def test_custom_message(self):
        """Vérifie qu'on peut définir un message personnalisé"""
        exc = AuthenticationException("Message personnalisé")
        
        assert str(exc) == "Message personnalisé"
    
    def test_inherits_from_runtime_error(self):
        """Vérifie que l'exception hérite de RuntimeError"""
        exc = AuthenticationException()
        
        assert isinstance(exc, RuntimeError)
    
    def test_can_be_caught_as_runtime_error(self):
        """Vérifie qu'on peut catcher comme RuntimeError"""
        with pytest.raises(RuntimeError):
            raise AuthenticationException("Test")


class TestUserNotFoundException:
    """Tests pour UserNotFoundException"""
    
    def test_default_message(self):
        """Vérifie que le message par défaut est utilisé sans user_id"""
        exc = UserNotFoundException()
        
        assert str(exc) == "Utilisateur non trouvé"
    
    def test_with_user_id(self):
        """Vérifie que le message inclut le user_id"""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        exc = UserNotFoundException(user_id=user_id)
        
        assert str(exc) == f"Utilisateur non trouvé: {user_id}"
        assert exc.user_id == user_id
    
    def test_inherits_from_authentication_exception(self):
        """Vérifie que l'exception hérite de AuthenticationException"""
        exc = UserNotFoundException()
        
        assert isinstance(exc, AuthenticationException)
    
    def test_inherits_from_runtime_error(self):
        """Vérifie que l'exception hérite de RuntimeError"""
        exc = UserNotFoundException()
        
        assert isinstance(exc, RuntimeError)
    
    def test_can_be_caught_as_authentication_exception(self):
        """Vérifie qu'on peut catcher comme AuthenticationException"""
        with pytest.raises(AuthenticationException):
            raise UserNotFoundException()


class TestInvalidCredentialsException:
    """Tests pour InvalidCredentialsException"""
    
    def test_default_message(self):
        """Vérifie que le message par défaut est utilisé"""
        exc = InvalidCredentialsException()
        
        assert str(exc) == "Identifiants invalides"
    
    def test_custom_message(self):
        """Vérifie qu'on peut définir un message personnalisé"""
        exc = InvalidCredentialsException("Email ou mot de passe incorrect")
        
        assert str(exc) == "Email ou mot de passe incorrect"
    
    def test_inherits_from_authentication_exception(self):
        """Vérifie que l'exception hérite de AuthenticationException"""
        exc = InvalidCredentialsException()
        
        assert isinstance(exc, AuthenticationException)
    
    def test_inherits_from_runtime_error(self):
        """Vérifie que l'exception hérite de RuntimeError"""
        exc = InvalidCredentialsException()
        
        assert isinstance(exc, RuntimeError)


class TestSessionExpiredException:
    """Tests pour SessionExpiredException"""
    
    def test_default_message(self):
        """Vérifie que le message par défaut est utilisé sans token"""
        exc = SessionExpiredException()
        
        assert str(exc) == "Session expirée"
    
    def test_with_token(self):
        """Vérifie que le message inclut le token masqué"""
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test"
        exc = SessionExpiredException(token=token)
        
        assert "Session expirée pour le token:" in str(exc)
        assert exc.token == token
    
    def test_token_is_masked(self):
        """Vérifie que le token est masqué dans le message"""
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        exc = SessionExpiredException(token=token)
        
        # Le token doit être tronqué à 10 caractères
        assert "eyJhbGciOi..." in str(exc)
        # Le token complet ne doit pas être dans le message
        assert token not in str(exc)
    
    def test_short_token_not_over_masked(self):
        """Vérifie qu'un token court n'est pas trop masqué"""
        token = "short"
        exc = SessionExpiredException(token=token)
        
        assert token in str(exc)
    
    def test_inherits_from_authentication_exception(self):
        """Vérifie que l'exception hérite de AuthenticationException"""
        exc = SessionExpiredException()
        
        assert isinstance(exc, AuthenticationException)


class TestTokenInvalidException:
    """Tests pour TokenInvalidException"""
    
    def test_default_message(self):
        """Vérifie que le message par défaut est utilisé sans token"""
        exc = TokenInvalidException()
        
        assert str(exc) == "Token invalide"
    
    def test_with_token(self):
        """Vérifie que le message inclut le token masqué"""
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test"
        exc = TokenInvalidException(token=token)
        
        assert "Token invalide:" in str(exc)
        assert exc.token == token
    
    def test_token_is_masked(self):
        """Vérifie que le token est masqué dans le message"""
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        exc = TokenInvalidException(token=token)
        
        # Le token doit être tronqué à 10 caractères
        assert "eyJhbGciOi..." in str(exc)
        # Le token complet ne doit pas être dans le message
        assert token not in str(exc)
    
    def test_inherits_from_authentication_exception(self):
        """Vérifie que l'exception hérite de AuthenticationException"""
        exc = TokenInvalidException()
        
        assert isinstance(exc, AuthenticationException)


class TestExceptionHierarchy:
    """Tests pour vérifier la hiérarchie des exceptions"""
    
    def test_all_exceptions_inherit_from_runtime_error(self):
        """Vérifie que toutes les exceptions héritent de RuntimeError"""
        exceptions = [
            AuthenticationException(),
            UserNotFoundException(),
            InvalidCredentialsException(),
            SessionExpiredException(),
            TokenInvalidException(),
        ]
        
        for exc in exceptions:
            assert isinstance(exc, RuntimeError), f"{type(exc).__name__} n'hérite pas de RuntimeError"
    
    def test_all_exceptions_inherit_from_authentication_exception(self):
        """Vérifie que toutes les exceptions spécifiques héritent de AuthenticationException"""
        exceptions = [
            UserNotFoundException(),
            InvalidCredentialsException(),
            SessionExpiredException(),
            TokenInvalidException(),
        ]
        
        for exc in exceptions:
            assert isinstance(exc, AuthenticationException), f"{type(exc).__name__} n'hérite pas de AuthenticationException"
