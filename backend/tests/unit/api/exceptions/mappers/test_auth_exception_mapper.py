"""
Tests pour le mapper des exceptions d'authentification
"""
import pytest
from flask import Flask
from domain.auth.exceptions.user_not_found_exception import UserNotFoundException
from domain.auth.exceptions.invalid_credentials_exception import InvalidCredentialsException
from domain.auth.exceptions.session_expired_exception import SessionExpiredException
from domain.auth.exceptions.token_invalid_exception import TokenInvalidException
from api.exceptions.mappers.auth_exception_mapper import register_auth_exception_handlers


class TestAuthExceptionMapper:
    """Tests pour le mapper des exceptions d'authentification"""
    
    @pytest.fixture
    def app(self):
        """Fixture: Crée une application Flask de test"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Routes de test pour déclencher les exceptions
        @app.route('/test/user-not-found')
        def user_not_found():
            raise UserNotFoundException("123")
        
        @app.route('/test/user-not-found-no-id')
        def user_not_found_no_id():
            raise UserNotFoundException()
        
        @app.route('/test/invalid-credentials')
        def invalid_credentials():
            raise InvalidCredentialsException()
        
        @app.route('/test/invalid-credentials-custom')
        def invalid_credentials_custom():
            raise InvalidCredentialsException("Email ou mot de passe incorrect")
        
        @app.route('/test/session-expired')
        def session_expired():
            raise SessionExpiredException("some.token.here")
        
        @app.route('/test/session-expired-no-token')
        def session_expired_no_token():
            raise SessionExpiredException()
        
        @app.route('/test/token-invalid')
        def token_invalid():
            raise TokenInvalidException("invalid.token.here")
        
        @app.route('/test/token-invalid-no-token')
        def token_invalid_no_token():
            raise TokenInvalidException()
        
        # Enregistrer les handlers
        register_auth_exception_handlers(app)
        
        return app
    
    @pytest.fixture
    def client(self, app):
        """Fixture: Crée un client de test Flask"""
        return app.test_client()
    
    def test_register_auth_exception_handlers_exists(self, app):
        """Vérifie que la fonction register_auth_exception_handlers existe"""
        assert callable(register_auth_exception_handlers)
    
    def test_user_not_found_returns_404(self, client):
        """UserNotFoundException doit retourner HTTP 404 avec message"""
        response = client.get('/test/user-not-found')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'USER_NOT_FOUND'
        assert 'Utilisateur non trouvé' in data['description']
        assert '123' in data['description']
    
    def test_user_not_found_no_id_returns_404(self, client):
        """UserNotFoundException sans ID doit retourner HTTP 404 avec message générique"""
        response = client.get('/test/user-not-found-no-id')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'USER_NOT_FOUND'
        assert data['description'] == 'Utilisateur non trouvé'
    
    def test_invalid_credentials_returns_401(self, client):
        """InvalidCredentialsException doit retourner HTTP 401 avec message par défaut"""
        response = client.get('/test/invalid-credentials')
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'INVALID_CREDENTIALS'
        assert data['description'] == 'Identifiants invalides'
    
    def test_invalid_credentials_custom_returns_401(self, client):
        """InvalidCredentialsException avec message custom doit retourner HTTP 401"""
        response = client.get('/test/invalid-credentials-custom')
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'INVALID_CREDENTIALS'
        assert data['description'] == 'Email ou mot de passe incorrect'
    
    def test_session_expired_returns_401(self, client):
        """SessionExpiredException doit retourner HTTP 401 avec message"""
        response = client.get('/test/session-expired')
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'SESSION_EXPIRED'
        assert 'Session expirée' in data['description']
    
    def test_session_expired_no_token_returns_401(self, client):
        """SessionExpiredException sans token doit retourner HTTP 401 avec message générique"""
        response = client.get('/test/session-expired-no-token')
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'SESSION_EXPIRED'
        assert data['description'] == 'Session expirée'
    
    def test_token_invalid_returns_401(self, client):
        """TokenInvalidException doit retourner HTTP 401 avec message"""
        response = client.get('/test/token-invalid')
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'TOKEN_INVALID'
        assert 'Token invalide' in data['description']
    
    def test_token_invalid_no_token_returns_401(self, client):
        """TokenInvalidException sans token doit retourner HTTP 401 avec message générique"""
        response = client.get('/test/token-invalid-no-token')
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'TOKEN_INVALID'
        assert data['description'] == 'Token invalide'
    
    def test_error_response_format(self, client):
        """Vérifie que la réponse d'erreur suit le format standard"""
        response = client.get('/test/user-not-found')
        
        data = response.get_json()
        # Vérifie la structure de ErrorResponse
        assert 'error' in data
        assert 'description' in data
        assert isinstance(data['error'], str)
        assert isinstance(data['description'], str)
        assert data['error'].isupper()  # Les codes d'erreur sont en majuscules
