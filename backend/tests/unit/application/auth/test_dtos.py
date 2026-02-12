"""
Tests unitaires pour les DTOs d'authentification.
"""
import pytest
from application.auth.dtos import (
    RegisterRequestDto,
    LoginRequestDto,
    AuthResponseDto,
    UserResponseDto,
)


class TestRegisterRequestDto:
    """Tests pour RegisterRequestDto"""
    
    def test_register_request_dto_creation(self):
        """Test de création d'un RegisterRequestDto"""
        dto = RegisterRequestDto(
            email="test@ulaval.ca",
            password="password123",
            idul="1234567"
        )
        
        assert dto.email == "test@ulaval.ca"
        assert dto.password == "password123"
        assert dto.idul == "1234567"
    
    def test_register_request_dto_different_values(self):
        """Test avec différentes valeurs"""
        dto = RegisterRequestDto(
            email="etudiant@ulaval.ca",
            password="monmotdepasse",
            idul="7654321"
        )
        
        assert dto.email == "etudiant@ulaval.ca"
        assert dto.password == "monmotdepasse"
        assert dto.idul == "7654321"


class TestLoginRequestDto:
    """Tests pour LoginRequestDto"""
    
    def test_login_request_dto_creation(self):
        """Test de création d'un LoginRequestDto"""
        dto = LoginRequestDto(
            email="test@ulaval.ca",
            password="password123"
        )
        
        assert dto.email == "test@ulaval.ca"
        assert dto.password == "password123"
    
    def test_login_request_dto_different_values(self):
        """Test avec différentes valeurs"""
        dto = LoginRequestDto(
            email="etudiant@ulaval.ca",
            password="monmotdepasse"
        )
        
        assert dto.email == "etudiant@ulaval.ca"
        assert dto.password == "monmotdepasse"


class TestAuthResponseDto:
    """Tests pour AuthResponseDto"""
    
    def test_auth_response_dto_creation(self):
        """Test de création d'un AuthResponseDto"""
        dto = AuthResponseDto(
            token="jwt_token_123",
            expires_at="2024-12-31T23:59:59",
            user_id=1,
            email="test@ulaval.ca"
        )
        
        assert dto.token == "jwt_token_123"
        assert dto.expires_at == "2024-12-31T23:59:59"
        assert dto.user_id == 1
        assert dto.email == "test@ulaval.ca"
    
    def test_auth_response_dto_to_dict(self):
        """Test de la méthode to_dict"""
        dto = AuthResponseDto(
            token="jwt_token_123",
            expires_at="2024-12-31T23:59:59",
            user_id=42,
            email="user@ulaval.ca"
        )
        
        result = dto.to_dict()
        
        expected = {
            'token': "jwt_token_123",
            'expires_at': "2024-12-31T23:59:59",
            'user_id': 42,
            'email': "user@ulaval.ca"
        }
        assert result == expected
    
    def test_auth_response_dto_to_dict_returns_dict(self):
        """Test que to_dict retourne bien un dict"""
        dto = AuthResponseDto(
            token="token",
            expires_at="2024-01-01T00:00:00",
            user_id=1,
            email="test@ulaval.ca"
        )
        
        result = dto.to_dict()
        
        assert isinstance(result, dict)
        assert 'token' in result
        assert 'expires_at' in result
        assert 'user_id' in result
        assert 'email' in result


class TestUserResponseDto:
    """Tests pour UserResponseDto"""
    
    def test_user_response_dto_creation(self):
        """Test de création d'un UserResponseDto"""
        dto = UserResponseDto(
            user_id=1,
            idul="1234567",
            email="test@ulaval.ca",
            is_verified=True,
            is_active=True
        )
        
        assert dto.user_id == 1
        assert dto.idul == "1234567"
        assert dto.email == "test@ulaval.ca"
        assert dto.is_verified is True
        assert dto.is_active is True
    
    def test_user_response_dto_creation_unverified_inactive(self):
        """Test de création avec is_verified et is_active à False"""
        dto = UserResponseDto(
            user_id=2,
            idul="7654321",
            email="nouveau@ulaval.ca",
            is_verified=False,
            is_active=False
        )
        
        assert dto.user_id == 2
        assert dto.idul == "7654321"
        assert dto.email == "nouveau@ulaval.ca"
        assert dto.is_verified is False
        assert dto.is_active is False
    
    def test_user_response_dto_to_dict(self):
        """Test de la méthode to_dict"""
        dto = UserResponseDto(
            user_id=42,
            idul="1234567",
            email="user@ulaval.ca",
            is_verified=True,
            is_active=True
        )
        
        result = dto.to_dict()
        
        expected = {
            'user_id': 42,
            'idul': "1234567",
            'email': "user@ulaval.ca",
            'is_verified': True,
            'is_active': True
        }
        assert result == expected
    
    def test_user_response_dto_to_dict_returns_dict(self):
        """Test que to_dict retourne bien un dict"""
        dto = UserResponseDto(
            user_id=1,
            idul="1234567",
            email="test@ulaval.ca",
            is_verified=False,
            is_active=True
        )
        
        result = dto.to_dict()
        
        assert isinstance(result, dict)
        assert 'user_id' in result
        assert 'idul' in result
        assert 'email' in result
        assert 'is_verified' in result
        assert 'is_active' in result
