"""
Tests pour AuthResource.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from flask import Flask

from api.auth_resource import auth_bp
from application.auth.dtos.auth_response_dto import AuthResponseDto
from application.auth.dtos.user_response_dto import UserResponseDto
from domain.auth.exceptions.invalid_credentials_exception import InvalidCredentialsException
from domain.auth.exceptions.token_invalid_exception import TokenInvalidException
from domain.auth.exceptions.session_expired_exception import SessionExpiredException


@pytest.fixture
def app():
    """Crée une application Flask de test."""
    app = Flask(__name__)
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.testing = True
    return app


@pytest.fixture
def client(app):
    """Crée un client de test."""
    return app.test_client()


class TestRegisterEndpoint:
    """Tests pour POST /api/auth/register."""
    
    @patch('api.auth_resource._auth_service')
    def test_register_success_201(self, mock_service, client):
        """Test inscription réussie retourne 201 avec AuthResponseDto."""
        # Arrange
        mock_response = AuthResponseDto(
            token='test-token-123',
            expires_at='2024-02-14T10:30:00',
            user_id=12345,
            email='test@ulaval.ca'
        )
        mock_service.register.return_value = mock_response
        
        data = {
            'email': 'test@ulaval.ca',
            'password': 'password123',
            'idul': 'abc1234'
        }
        
        # Act
        response = client.post('/api/auth/register', json=data)
        
        # Assert
        assert response.status_code == 201
        assert response.json['token'] == 'test-token-123'
        assert response.json['email'] == 'test@ulaval.ca'
        assert response.json['user_id'] == 12345
        mock_service.register.assert_called_once()
    
    def test_register_missing_body_400(self, client):
        """Test avec corps de requête manquant retourne 400."""
        response = client.post('/api/auth/register')
        
        assert response.status_code == 400
        assert response.json['error'] == 'INVALID_REQUEST'
    
    def test_register_empty_json_400(self, client):
        """Test avec JSON vide retourne 400."""
        response = client.post('/api/auth/register', json={})
        
        # Un dict vide est falsy, donc retourne INVALID_REQUEST
        assert response.status_code == 400
        assert response.json['error'] == 'INVALID_REQUEST'
    
    def test_register_missing_email_400(self, client):
        """Test avec email manquant retourne 400."""
        data = {
            'password': 'password123',
            'idul': 'abc1234'
        }
        
        response = client.post('/api/auth/register', json=data)
        
        assert response.status_code == 400
        assert 'email' in response.json['description'].lower() or 'L\'email' in response.json['description']
    
    def test_register_invalid_email_400(self, client):
        """Test avec email invalide retourne 400."""
        data = {
            'email': 'invalid-email',
            'password': 'password123',
            'idul': 'abc1234'
        }
        
        response = client.post('/api/auth/register', json=data)
        
        assert response.status_code == 400
        assert '@' in response.json['description'] or 'email' in response.json['description'].lower()
    
    def test_register_password_too_short_400(self, client):
        """Test avec mot de passe trop court retourne 400."""
        data = {
            'email': 'test@ulaval.ca',
            'password': 'short',
            'idul': 'abc1234'
        }
        
        response = client.post('/api/auth/register', json=data)
        
        assert response.status_code == 400
        assert '8' in response.json['description'] or 'caractères' in response.json['description']
    
    def test_register_idul_wrong_length_400(self, client):
        """Test avec idul de mauvaise longueur retourne 400."""
        data = {
            'email': 'test@ulaval.ca',
            'password': 'password123',
            'idul': 'abc12'  # Trop court
        }
        
        response = client.post('/api/auth/register', json=data)
        
        assert response.status_code == 400
        assert '7' in response.json['description'] or 'caractères' in response.json['description']
    
    @patch('api.auth_resource._auth_service')
    def test_register_email_already_exists_409(self, mock_service, client):
        """Test avec email déjà existant retourne 409."""
        mock_service.register.side_effect = ValueError("Un utilisateur existe déjà avec l'email: test@ulaval.ca")
        
        data = {
            'email': 'test@ulaval.ca',
            'password': 'password123',
            'idul': 'abc1234'
        }
        
        response = client.post('/api/auth/register', json=data)
        
        assert response.status_code == 409
        assert response.json['error'] == 'EMAIL_ALREADY_EXISTS'


class TestLoginEndpoint:
    """Tests pour POST /api/auth/login."""
    
    @patch('api.auth_resource._auth_service')
    def test_login_success_200(self, mock_service, client):
        """Test connexion réussie retourne 200 avec AuthResponseDto."""
        # Arrange
        mock_response = AuthResponseDto(
            token='test-token-456',
            expires_at='2024-02-14T10:30:00',
            user_id=12345,
            email='test@ulaval.ca'
        )
        mock_service.login.return_value = mock_response
        
        data = {
            'email': 'test@ulaval.ca',
            'password': 'password123'
        }
        
        # Act
        response = client.post('/api/auth/login', json=data)
        
        # Assert
        assert response.status_code == 200
        assert response.json['token'] == 'test-token-456'
        assert response.json['email'] == 'test@ulaval.ca'
        mock_service.login.assert_called_once()
    
    def test_login_missing_body_400(self, client):
        """Test avec corps de requête manquant retourne 400."""
        response = client.post('/api/auth/login')
        
        assert response.status_code == 400
        assert response.json['error'] == 'INVALID_REQUEST'
    
    def test_login_missing_email_400(self, client):
        """Test avec email manquant retourne 400."""
        data = {
            'password': 'password123'
        }
        
        response = client.post('/api/auth/login', json=data)
        
        assert response.status_code == 400
        assert response.json['error'] == 'VALIDATION_ERROR'
    
    def test_login_missing_password_400(self, client):
        """Test avec password manquant retourne 400."""
        data = {
            'email': 'test@ulaval.ca'
        }
        
        response = client.post('/api/auth/login', json=data)
        
        assert response.status_code == 400
        assert response.json['error'] == 'VALIDATION_ERROR'
    
    @patch('api.auth_resource._auth_service')
    def test_login_invalid_credentials_401(self, mock_service, client):
        """Test avec identifiants invalides lève InvalidCredentialsException."""
        mock_service.login.side_effect = InvalidCredentialsException("Email ou mot de passe invalide")
        
        data = {
            'email': 'test@ulaval.ca',
            'password': 'wrongpassword'
        }
        
        # L'exception est propagée pour être gérée par l'exception mapper
        with pytest.raises(InvalidCredentialsException):
            client.post('/api/auth/login', json=data)


class TestMeEndpoint:
    """Tests pour GET /api/auth/me."""
    
    @patch('api.auth_resource._auth_service')
    def test_me_success_200(self, mock_service, client):
        """Test récupération utilisateur courant retourne 200 avec UserResponseDto."""
        # Arrange
        mock_response = UserResponseDto(
            user_id=12345,
            idul='abc1234',
            email='test@ulaval.ca',
            is_verified=True,
            is_active=True
        )
        mock_service.get_current_user.return_value = mock_response
        
        # Act
        response = client.get('/api/auth/me', headers={'Authorization': 'Bearer valid-token'})
        
        # Assert
        assert response.status_code == 200
        assert response.json['user_id'] == 12345
        assert response.json['idul'] == 'abc1234'
        assert response.json['email'] == 'test@ulaval.ca'
        assert response.json['is_verified'] == True
        assert response.json['is_active'] == True
        mock_service.get_current_user.assert_called_once_with('valid-token')
    
    def test_me_missing_auth_header_401(self, client):
        """Test sans header Authorization retourne 401."""
        response = client.get('/api/auth/me')
        
        assert response.status_code == 401
        assert response.json['error'] == 'TOKEN_MISSING'
    
    def test_me_invalid_auth_format_401(self, client):
        """Test avec format de token invalide retourne 401."""
        response = client.get('/api/auth/me', headers={'Authorization': 'invalid-format'})
        
        assert response.status_code == 401
        assert response.json['error'] == 'TOKEN_INVALID_FORMAT'
    
    @patch('api.auth_resource._auth_service')
    def test_me_invalid_token_401(self, mock_service, client):
        """Test avec token invalide propage TokenInvalidException."""
        mock_service.get_current_user.side_effect = TokenInvalidException('invalid-token')
        
        with pytest.raises(TokenInvalidException):
            client.get('/api/auth/me', headers={'Authorization': 'Bearer invalid-token'})
    
    @patch('api.auth_resource._auth_service')
    def test_me_expired_token_401(self, mock_service, client):
        """Test avec token expiré propage SessionExpiredException."""
        mock_service.get_current_user.side_effect = SessionExpiredException('expired-token')
        
        with pytest.raises(SessionExpiredException):
            client.get('/api/auth/me', headers={'Authorization': 'Bearer expired-token'})
    
    def test_me_case_insensitive_bearer(self, client):
        """Test que 'bearer' est insensible à la casse."""
        mock_response = UserResponseDto(
            user_id=12345,
            idul='abc1234',
            email='test@ulaval.ca',
            is_verified=True,
            is_active=True
        )
        
        with patch('api.auth_resource._auth_service') as mock_service:
            mock_service.get_current_user.return_value = mock_response
            
            response = client.get('/api/auth/me', headers={'Authorization': 'bearer valid-token'})
            
            assert response.status_code == 200
            mock_service.get_current_user.assert_called_once_with('valid-token')


class TestLogoutEndpoint:
    """Tests pour POST /api/auth/logout."""
    
    @patch('api.auth_resource._auth_service')
    def test_logout_success_204(self, mock_service, client):
        """Test déconnexion réussie retourne 204."""
        mock_service.logout.return_value = None
        
        response = client.post('/api/auth/logout', headers={'Authorization': 'Bearer valid-token'})
        
        assert response.status_code == 204
        assert response.data == b''
        mock_service.logout.assert_called_once_with('valid-token')
    
    def test_logout_missing_auth_header_401(self, client):
        """Test sans header Authorization retourne 401."""
        response = client.post('/api/auth/logout')
        
        assert response.status_code == 401
        assert response.json['error'] == 'TOKEN_MISSING'
    
    def test_logout_invalid_auth_format_401(self, client):
        """Test avec format de token invalide retourne 401."""
        response = client.post('/api/auth/logout', headers={'Authorization': 'invalid-format'})
        
        assert response.status_code == 401
        assert response.json['error'] == 'TOKEN_INVALID_FORMAT'
    
    @patch('api.auth_resource._auth_service')
    def test_logout_invalid_token_401(self, mock_service, client):
        """Test avec token invalide propage TokenInvalidException."""
        mock_service.logout.side_effect = TokenInvalidException('invalid-token')
        
        with pytest.raises(TokenInvalidException):
            client.post('/api/auth/logout', headers={'Authorization': 'Bearer invalid-token'})


class TestHealthEndpoint:
    """Tests pour GET /api/auth/health."""
    
    def test_health_200(self, client):
        """Test endpoint de santé retourne 200 avec info du module."""
        response = client.get('/api/auth/health')
        
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'
        assert response.json['module'] == 'auth'
        assert 'endpoints' in response.json
        assert len(response.json['endpoints']) == 4


class TestAuthBlueprint:
    """Tests pour le Blueprint auth."""
    
    def test_blueprint_name(self):
        """Test que le Blueprint a le bon nom."""
        from api.auth_resource import auth_bp
        
        assert auth_bp.name == 'auth'
    
    def test_routes_registered(self, app):
        """Test que toutes les routes sont enregistrées."""
        # Récupérer toutes les URLs enregistrées
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        
        assert '/api/auth/register' in routes
        assert '/api/auth/login' in routes
        assert '/api/auth/me' in routes
        assert '/api/auth/logout' in routes
        assert '/api/auth/health' in routes
