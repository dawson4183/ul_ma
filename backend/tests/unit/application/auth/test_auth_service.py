"""
Tests pour AuthService.

Ces tests vérifient que le service d'authentification orchestre
correctement les repositories et services de sécurité.
"""
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock, patch
import pytest

from application.auth.auth_service import AuthService
from application.auth.dtos.register_request_dto import RegisterRequestDto
from application.auth.dtos.login_request_dto import LoginRequestDto
from domain.user.user import User
from domain.auth.session import Session
from domain.auth.exceptions.invalid_credentials_exception import InvalidCredentialsException
from domain.auth.exceptions.token_invalid_exception import TokenInvalidException
from domain.auth.exceptions.session_expired_exception import SessionExpiredException


class TestAuthService:
    """Tests pour AuthService."""
    
    @pytest.fixture
    def mock_user_repository(self):
        """Fixture pour le UserRepository mocké."""
        return Mock()
    
    @pytest.fixture
    def mock_session_repository(self):
        """Fixture pour le SessionRepository mocké."""
        return Mock()
    
    @pytest.fixture
    def mock_password_hasher(self):
        """Fixture pour le PasswordHasher mocké."""
        hasher = Mock()
        hasher.hash_password.return_value = "hashed_password_123"
        hasher.verify_password.return_value = True
        return hasher
    
    @pytest.fixture
    def mock_jwt_service(self):
        """Fixture pour le JwtService mocké."""
        jwt = Mock()
        jwt.generate_token.return_value = "jwt_token_123"
        jwt.validate_token.return_value = {
            "user_id": 123,
            "email": "test@ulaval.ca",
            "exp": datetime.utcnow() + timedelta(hours=24),
            "type": "auth"
        }
        return jwt
    
    @pytest.fixture
    def auth_service(self, mock_user_repository, mock_session_repository, 
                     mock_password_hasher, mock_jwt_service):
        """Fixture pour le AuthService avec dépendances mockées."""
        return AuthService(
            user_repository=mock_user_repository,
            session_repository=mock_session_repository,
            password_hasher=mock_password_hasher,
            jwt_service=mock_jwt_service
        )
    
    @pytest.fixture
    def sample_user(self):
        """Fixture pour un utilisateur de test."""
        return User(
            user_id="user-123",
            idul="ABC1234",
            email="test@ulaval.ca",
            password_hash="hashed_password_123",
            is_verified=True,
            is_active=True
        )
    
    # ===== Tests pour register() =====
    
    def test_register_creates_new_user(self, auth_service, mock_user_repository, 
                                       mock_password_hasher, mock_jwt_service):
        """Test que register() crée un nouvel utilisateur."""
        # Arrange
        mock_user_repository.exists_by_email.return_value = False
        mock_user_repository.find_by_email.return_value = None
        
        dto = RegisterRequestDto(
            email="test@ulaval.ca",
            password="password123",
            idul="ABC1234"
        )
        
        # Act
        response = auth_service.register(dto)
        
        # Assert
        assert response is not None
        assert response.token == "jwt_token_123"
        assert response.email == "test@ulaval.ca"
        mock_user_repository.exists_by_email.assert_called_once_with("test@ulaval.ca")
        mock_password_hasher.hash_password.assert_called_once_with("password123")
        mock_user_repository.save.assert_called_once()
        mock_jwt_service.generate_token.assert_called_once()
    
    def test_register_raises_when_email_exists(self, auth_service, mock_user_repository):
        """Test que register() lève une exception si l'email existe déjà."""
        # Arrange
        mock_user_repository.exists_by_email.return_value = True
        
        dto = RegisterRequestDto(
            email="test@ulaval.ca",
            password="password123",
            idul="ABC1234"
        )
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            auth_service.register(dto)
        
        assert "existe déjà" in str(exc_info.value)
        mock_user_repository.exists_by_email.assert_called_once_with("test@ulaval.ca")
        mock_user_repository.save.assert_not_called()
    
    def test_register_creates_session(self, auth_service, mock_user_repository, 
                                      mock_session_repository, mock_jwt_service):
        """Test que register() crée une session après l'inscription."""
        # Arrange
        mock_user_repository.exists_by_email.return_value = False
        dto = RegisterRequestDto(
            email="test@ulaval.ca",
            password="password123",
            idul="ABC1234"
        )
        
        # Act
        response = auth_service.register(dto)
        
        # Assert
        mock_session_repository.save.assert_called_once()
        call_args = mock_session_repository.save.call_args[0][0]
        assert isinstance(call_args, Session)
        assert call_args.token_type == Session.TOKEN_TYPE_AUTH
    
    def test_register_returns_auth_response_dto(self, auth_service, mock_user_repository):
        """Test que register() retourne un AuthResponseDto valide."""
        # Arrange
        mock_user_repository.exists_by_email.return_value = False
        dto = RegisterRequestDto(
            email="test@ulaval.ca",
            password="password123",
            idul="ABC1234"
        )
        
        # Act
        response = auth_service.register(dto)
        
        # Assert
        from application.auth.dtos.auth_response_dto import AuthResponseDto
        assert isinstance(response, AuthResponseDto)
        assert response.token is not None
        assert response.expires_at is not None
        assert response.email == "test@ulaval.ca"
    
    # ===== Tests pour login() =====
    
    def test_login_successful(self, auth_service, mock_user_repository, 
                              mock_password_hasher, mock_jwt_service, sample_user):
        """Test que login() réussit avec des credentials valides."""
        # Arrange
        mock_user_repository.find_by_email.return_value = sample_user
        mock_password_hasher.verify_password.return_value = True
        
        dto = LoginRequestDto(
            email="test@ulaval.ca",
            password="password123"
        )
        
        # Act
        response = auth_service.login(dto)
        
        # Assert
        assert response is not None
        assert response.token == "jwt_token_123"
        assert response.email == "test@ulaval.ca"
        mock_user_repository.find_by_email.assert_called_once_with("test@ulaval.ca")
        mock_password_hasher.verify_password.assert_called_once_with(
            "password123", "hashed_password_123"
        )
        mock_jwt_service.generate_token.assert_called_once()
    
    def test_login_raises_when_user_not_found(self, auth_service, mock_user_repository):
        """Test que login() lève InvalidCredentialsException si utilisateur non trouvé."""
        # Arrange
        mock_user_repository.find_by_email.return_value = None
        
        dto = LoginRequestDto(
            email="notfound@ulaval.ca",
            password="password123"
        )
        
        # Act & Assert
        with pytest.raises(InvalidCredentialsException) as exc_info:
            auth_service.login(dto)
        
        assert "Email ou mot de passe invalide" in str(exc_info.value)
    
    def test_login_raises_when_password_invalid(self, auth_service, mock_user_repository,
                                                mock_password_hasher, sample_user):
        """Test que login() lève InvalidCredentialsException si mot de passe invalide."""
        # Arrange
        mock_user_repository.find_by_email.return_value = sample_user
        mock_password_hasher.verify_password.return_value = False
        
        dto = LoginRequestDto(
            email="test@ulaval.ca",
            password="wrong_password"
        )
        
        # Act & Assert
        with pytest.raises(InvalidCredentialsException) as exc_info:
            auth_service.login(dto)
        
        assert "Email ou mot de passe invalide" in str(exc_info.value)
    
    def test_login_raises_when_user_not_verified(self, auth_service, mock_user_repository,
                                                 mock_password_hasher):
        """Test que login() lève InvalidCredentialsException si email non vérifié."""
        # Arrange
        unverified_user = User(
            user_id="user-123",
            idul="ABC1234",
            email="test@ulaval.ca",
            password_hash="hashed_password_123",
            is_verified=False,
            is_active=True
        )
        mock_user_repository.find_by_email.return_value = unverified_user
        mock_password_hasher.verify_password.return_value = True
        
        dto = LoginRequestDto(
            email="test@ulaval.ca",
            password="password123"
        )
        
        # Act & Assert
        with pytest.raises(InvalidCredentialsException) as exc_info:
            auth_service.login(dto)
        
        assert "non vérifié" in str(exc_info.value)
    
    def test_login_raises_when_user_inactive(self, auth_service, mock_user_repository,
                                             mock_password_hasher):
        """Test que login() lève InvalidCredentialsException si compte désactivé."""
        # Arrange
        inactive_user = User(
            user_id="user-123",
            idul="ABC1234",
            email="test@ulaval.ca",
            password_hash="hashed_password_123",
            is_verified=True,
            is_active=False
        )
        mock_user_repository.find_by_email.return_value = inactive_user
        mock_password_hasher.verify_password.return_value = True
        
        dto = LoginRequestDto(
            email="test@ulaval.ca",
            password="password123"
        )
        
        # Act & Assert
        with pytest.raises(InvalidCredentialsException) as exc_info:
            auth_service.login(dto)
        
        assert "désactivé" in str(exc_info.value)
    
    def test_login_creates_session(self, auth_service, mock_user_repository,
                                   mock_session_repository, mock_password_hasher, sample_user):
        """Test que login() crée une session après connexion réussie."""
        # Arrange
        mock_user_repository.find_by_email.return_value = sample_user
        mock_password_hasher.verify_password.return_value = True
        
        dto = LoginRequestDto(
            email="test@ulaval.ca",
            password="password123"
        )
        
        # Act
        auth_service.login(dto)
        
        # Assert
        mock_session_repository.save.assert_called_once()
        call_args = mock_session_repository.save.call_args[0][0]
        assert isinstance(call_args, Session)
        assert call_args.token_type == Session.TOKEN_TYPE_AUTH
    
    # ===== Tests pour get_current_user() =====
    
    def test_get_current_user_successful(self, auth_service, mock_jwt_service,
                                          mock_user_repository, sample_user):
        """Test que get_current_user() retourne UserResponseDto avec token valide."""
        # Arrange
        mock_jwt_service.validate_token.return_value = {
            "user_id": 123,
            "email": "test@ulaval.ca",
            "exp": datetime.utcnow() + timedelta(hours=24),
            "type": "auth"
        }
        mock_user_repository.find_by_email.return_value = sample_user
        
        token = "valid_token"
        
        # Act
        response = auth_service.get_current_user(token)
        
        # Assert
        assert response is not None
        assert response.email == "test@ulaval.ca"
        assert response.idul == "ABC1234"
        assert response.is_verified is True
        assert response.is_active is True
        mock_jwt_service.validate_token.assert_called_once_with(token)
        mock_user_repository.find_by_email.assert_called_once_with("test@ulaval.ca")
    
    def test_get_current_user_raises_when_token_invalid(self, auth_service, mock_jwt_service):
        """Test que get_current_user() lève TokenInvalidException si token invalide."""
        # Arrange
        mock_jwt_service.validate_token.side_effect = TokenInvalidException("invalid_token")
        
        # Act & Assert
        with pytest.raises(TokenInvalidException):
            auth_service.get_current_user("invalid_token")
    
    def test_get_current_user_raises_when_token_expired(self, auth_service, mock_jwt_service):
        """Test que get_current_user() lève SessionExpiredException si token expiré."""
        # Arrange
        mock_jwt_service.validate_token.side_effect = SessionExpiredException("expired_token")
        
        # Act & Assert
        with pytest.raises(SessionExpiredException):
            auth_service.get_current_user("expired_token")
    
    def test_get_current_user_raises_when_user_not_found(self, auth_service, mock_jwt_service,
                                                         mock_user_repository):
        """Test que get_current_user() lève InvalidCredentialsException si utilisateur non trouvé."""
        # Arrange
        mock_jwt_service.validate_token.return_value = {
            "user_id": 123,
            "email": "deleted@ulaval.ca",
            "exp": datetime.utcnow() + timedelta(hours=24),
            "type": "auth"
        }
        mock_user_repository.find_by_email.return_value = None
        
        # Act & Assert
        with pytest.raises(InvalidCredentialsException) as exc_info:
            auth_service.get_current_user("valid_token")
        
        assert "Utilisateur non trouvé" in str(exc_info.value)
    
    def test_get_current_user_raises_when_email_missing_in_token(self, auth_service, mock_jwt_service):
        """Test que get_current_user() lève TokenInvalidException si email manquant dans payload."""
        # Arrange
        mock_jwt_service.validate_token.return_value = {
            "user_id": 123,
            "exp": datetime.utcnow() + timedelta(hours=24),
            "type": "auth"
        }
        
        # Act & Assert
        with pytest.raises(TokenInvalidException):
            auth_service.get_current_user("valid_token_but_no_email")
    
    # ===== Tests pour logout() =====
    
    def test_logout_marks_session_as_used(self, auth_service, mock_session_repository):
        """Test que logout() marque la session comme utilisée."""
        # Arrange
        session = Session(
            session_id="session-123",
            user_id="user-123",
            token="token_to_invalidate",
            token_type=Session.TOKEN_TYPE_AUTH,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        mock_session_repository.find_by_token.return_value = session
        
        # Act
        auth_service.logout("token_to_invalidate")
        
        # Assert
        mock_session_repository.find_by_token.assert_called_once_with("token_to_invalidate")
        mock_session_repository.mark_as_used.assert_called_once_with("session-123")
    
    def test_logout_succeeds_when_session_not_found(self, auth_service, mock_session_repository):
        """Test que logout() réussit même si la session n'existe pas."""
        # Arrange
        mock_session_repository.find_by_token.return_value = None
        
        # Act - should not raise
        auth_service.logout("unknown_token")
        
        # Assert
        mock_session_repository.find_by_token.assert_called_once_with("unknown_token")
        mock_session_repository.mark_as_used.assert_not_called()
    
    # ===== Tests d'intégration des services =====
    
    def test_injection_de_dependances(self, auth_service, mock_user_repository,
                                      mock_session_repository, mock_password_hasher,
                                      mock_jwt_service):
        """Test que le service utilise les dépendances injectées."""
        # Vérifie que les dépendances sont bien stockées
        assert auth_service._user_repository is mock_user_repository
        assert auth_service._session_repository is mock_session_repository
        assert auth_service._password_hasher is mock_password_hasher
        assert auth_service._jwt_service is mock_jwt_service
    
    def test_register_and_login_flow(self, auth_service, mock_user_repository,
                                     mock_session_repository, mock_password_hasher,
                                     mock_jwt_service):
        """Test d'intégration: register puis login avec les mêmes credentials."""
        # Arrange - Register
        mock_user_repository.exists_by_email.return_value = False
        mock_user_repository.find_by_email.return_value = None
        
        register_dto = RegisterRequestDto(
            email="newuser@ulaval.ca",
            password="secure_password",
            idul="NEW1234"
        )
        
        # Act - Register
        register_response = auth_service.register(register_dto)
        
        # Arrange - Login (simuler que l'utilisateur a été créé et est vérifié)
        created_user = User(
            user_id="user-456",
            idul="NEW1234",
            email="newuser@ulaval.ca",
            password_hash="hashed_secure_password",
            is_verified=True,
            is_active=True
        )
        mock_user_repository.find_by_email.return_value = created_user
        mock_password_hasher.verify_password.return_value = True
        
        login_dto = LoginRequestDto(
            email="newuser@ulaval.ca",
            password="secure_password"
        )
        
        # Act - Login
        login_response = auth_service.login(login_dto)
        
        # Assert
        assert register_response.token is not None
        assert login_response.token is not None
        assert register_response.email == login_response.email
    
    def test_full_auth_lifecycle(self, auth_service, mock_user_repository,
                                  mock_session_repository, mock_password_hasher,
                                  mock_jwt_service, sample_user):
        """Test du cycle complet: login, get_current_user, logout."""
        # Arrange - Login
        mock_user_repository.find_by_email.return_value = sample_user
        mock_password_hasher.verify_password.return_value = True
        
        # Créer une session simulée pour le logout
        session = Session(
            session_id="session-789",
            user_id=sample_user.user_id,
            token="jwt_token_123",
            token_type=Session.TOKEN_TYPE_AUTH,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        mock_session_repository.find_by_token.return_value = session
        
        # Act - Login
        login_response = auth_service.login(
            LoginRequestDto(email="test@ulaval.ca", password="password123")
        )
        
        # Act - Get current user
        user_response = auth_service.get_current_user(login_response.token)
        
        # Act - Logout
        auth_service.logout(login_response.token)
        
        # Assert
        assert login_response.email == user_response.email
        mock_session_repository.mark_as_used.assert_called_once_with("session-789")
