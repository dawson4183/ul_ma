"""
Tests pour MySQLUserRepository.

Ces tests vérifient que l'implémentation MySQL du UserRepository
fonctionne correctement avec une base de données MySQL.
"""
from typing import Optional, Dict, Any
import pytest
from unittest.mock import Mock, MagicMock, patch

from infrastructure.persistence.mysql.mysql_user_repository import MySQLUserRepository
from domain.user.user import User
from domain.exceptions.database_exception import DatabaseException


class TestMySQLUserRepository:
    """Tests pour MySQLUserRepository."""
    
    @pytest.fixture
    def mock_connection(self):
        """Fixture pour une connexion mockée."""
        return Mock()
    
    @pytest.fixture
    def repository(self, mock_connection):
        """Fixture pour le repository avec connexion mockée."""
        return MySQLUserRepository(mock_connection)
    
    @pytest.fixture
    def sample_user_data(self) -> Dict[str, Any]:
        """Fixture pour les données brutes d'un utilisateur."""
        return {
            "user_id": "user-123",
            "idul": "ABC1234",
            "email": "test@ulaval.ca",
            "password_hash": "hashed_password",
            "is_verified": True,
            "is_active": True
        }
    
    @pytest.fixture
    def sample_user(self) -> User:
        """Fixture pour un utilisateur de test."""
        return User(
            user_id="user-123",
            idul="ABC1234",
            email="test@ulaval.ca",
            password_hash="hashed_password",
            is_verified=True,
            is_active=True
        )
    
    def test_get_table_name_returns_users(self, repository):
        """Test que _get_table_name retourne 'users'."""
        assert repository._get_table_name() == "users"
    
    def test_map_to_entity_creates_user(self, repository, sample_user_data):
        """Test que _map_to_entity crée correctement un User."""
        user = repository._map_to_entity(sample_user_data)
        
        assert isinstance(user, User)
        assert user.user_id == "user-123"
        assert user.idul == "ABC1234"
        assert user.email == "test@ulaval.ca"
        assert user.password_hash == "hashed_password"
        assert user.is_verified is True
        assert user.is_active is True
    
    def test_map_to_entity_handles_int_booleans(self, repository):
        """Test que _map_to_entity gère les booléens comme entiers (MySQL)."""
        data = {
            "user_id": "user-456",
            "idul": "DEF5678",
            "email": "other@ulaval.ca",
            "password_hash": "hash",
            "is_verified": 0,  # MySQL retourne souvent 0/1
            "is_active": 1
        }
        
        user = repository._map_to_entity(data)
        
        assert user.is_verified is False
        assert user.is_active is True
    
    def test_find_by_id_returns_user(self, repository, mock_connection, sample_user_data):
        """Test find_by_id retourne un utilisateur quand trouvé."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (
            "user-123", "ABC1234", "test@ulaval.ca", "hashed_password", True, True
        )
        mock_cursor.description = [
            ("user_id",), ("idul",), ("email",), ("password_hash",), ("is_verified",), ("is_active",)
        ]
        mock_connection.get_cursor.return_value = mock_cursor
        
        user = repository.find_by_id("user-123")
        
        assert user is not None
        assert user.user_id == "user-123"
        assert user.email == "test@ulaval.ca"
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert "WHERE user_id = %s" in args[0]
    
    def test_find_by_id_returns_none_when_not_found(self, repository, mock_connection):
        """Test find_by_id retourne None quand utilisateur non trouvé."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connection.get_cursor.return_value = mock_cursor
        
        user = repository.find_by_id("non-existent")
        
        assert user is None
    
    def test_find_by_email_returns_user(self, repository, mock_connection, sample_user_data):
        """Test find_by_email retourne un utilisateur quand trouvé."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (
            "user-123", "ABC1234", "test@ulaval.ca", "hashed_password", True, True
        )
        mock_cursor.description = [
            ("user_id",), ("idul",), ("email",), ("password_hash",), ("is_verified",), ("is_active",)
        ]
        mock_connection.get_cursor.return_value = mock_cursor
        
        user = repository.find_by_email("test@ulaval.ca")
        
        assert user is not None
        assert user.user_id == "user-123"
        assert user.email == "test@ulaval.ca"
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert "WHERE email = %s" in args[0]
    
    def test_find_by_email_converts_to_lowercase(self, repository, mock_connection):
        """Test find_by_email convertit l'email en minuscules."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connection.get_cursor.return_value = mock_cursor
        
        repository.find_by_email("TEST@ULAVAL.CA")
        
        # Vérifie que l'email est passé en minuscules
        args = mock_cursor.execute.call_args[0]
        assert args[1] == ("test@ulaval.ca",)
    
    def test_find_by_email_returns_none_when_not_found(self, repository, mock_connection):
        """Test find_by_email retourne None quand utilisateur non trouvé."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connection.get_cursor.return_value = mock_cursor
        
        user = repository.find_by_email("notfound@ulaval.ca")
        
        assert user is None
    
    def test_find_by_idul_returns_user(self, repository, mock_connection, sample_user_data):
        """Test find_by_idul retourne un utilisateur quand trouvé."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (
            "user-123", "ABC1234", "test@ulaval.ca", "hashed_password", True, True
        )
        mock_cursor.description = [
            ("user_id",), ("idul",), ("email",), ("password_hash",), ("is_verified",), ("is_active",)
        ]
        mock_connection.get_cursor.return_value = mock_cursor
        
        user = repository.find_by_idul("ABC1234")
        
        assert user is not None
        assert user.user_id == "user-123"
        assert user.idul == "ABC1234"
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert "WHERE idul = %s" in args[0]
    
    def test_find_by_idul_returns_none_when_not_found(self, repository, mock_connection):
        """Test find_by_idul retourne None quand utilisateur non trouvé."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connection.get_cursor.return_value = mock_cursor
        
        user = repository.find_by_idul("XYZ9999")
        
        assert user is None
    
    def test_save_inserts_new_user(self, repository, mock_connection, sample_user):
        """Test save fait un INSERT pour un nouvel utilisateur."""
        # Mock pour find_by_id (vérifie existence) - retourne None
        mock_cursor_check = MagicMock()
        mock_cursor_check.fetchone.return_value = None
        
        # Mock pour l'INSERT
        mock_cursor_insert = MagicMock()
        
        def get_cursor_side_effect():
            if mock_connection.get_cursor.call_count == 1:
                return mock_cursor_check
            return mock_cursor_insert
        
        mock_connection.get_cursor.side_effect = get_cursor_side_effect
        
        repository.save(sample_user)
        
        # Vérifie que le commit est appelé
        mock_connection.commit.assert_called()
        
        # Vérifie que c'était bien un INSERT
        insert_call_found = False
        for call in mock_cursor_insert.execute.call_args_list:
            if call[0] and "INSERT" in call[0][0]:
                insert_call_found = True
                break
        assert insert_call_found, "Expected INSERT statement"
    
    def test_save_updates_existing_user(self, repository, mock_connection, sample_user):
        """Test save fait un UPDATE pour un utilisateur existant."""
        # Mock pour find_by_id - retourne une ligne (utilisateur existe)
        mock_cursor_check = MagicMock()
        mock_cursor_check.fetchone.return_value = (
            "user-123", "ABC1234", "test@ulaval.ca", "hashed_password", False, True
        )
        mock_cursor_check.description = [
            ("user_id",), ("idul",), ("email",), ("password_hash",), ("is_verified",), ("is_active",)
        ]
        
        # Mock pour l'UPDATE
        mock_cursor_update = MagicMock()
        
        def get_cursor_side_effect():
            if mock_connection.get_cursor.call_count == 1:
                return mock_cursor_check
            return mock_cursor_update
        
        mock_connection.get_cursor.side_effect = get_cursor_side_effect
        
        repository.save(sample_user)
        
        # Vérifie que le commit est appelé
        mock_connection.commit.assert_called()
        
        # Vérifie que c'était bien un UPDATE
        update_call_found = False
        for call in mock_cursor_update.execute.call_args_list:
            if call[0] and "UPDATE" in call[0][0]:
                update_call_found = True
                break
        assert update_call_found, "Expected UPDATE statement"
    
    def test_save_rollback_on_error(self, repository, mock_connection, sample_user):
        """Test save fait un rollback en cas d'erreur."""
        # First cursor for find_by_id check (returns None - new user)
        mock_cursor_check = MagicMock()
        mock_cursor_check.fetchone.return_value = None
        
        # Second cursor for INSERT that fails
        mock_cursor_insert = MagicMock()
        mock_cursor_insert.execute.side_effect = Exception("DB Error")
        
        call_count = [0]
        def get_cursor_side_effect():
            call_count[0] += 1
            if call_count[0] == 1:
                return mock_cursor_check
            return mock_cursor_insert
        
        mock_connection.get_cursor.side_effect = get_cursor_side_effect
        
        with pytest.raises(Exception):
            repository.save(sample_user)
        
        mock_connection.rollback.assert_called_once()
    
    def test_exists_by_email_returns_true_when_exists(self, repository, mock_connection):
        """Test exists_by_email retourne True si l'email existe."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)
        mock_connection.get_cursor.return_value = mock_cursor
        
        exists = repository.exists_by_email("test@ulaval.ca")
        
        assert exists is True
    
    def test_exists_by_email_converts_to_lowercase(self, repository, mock_connection):
        """Test exists_by_email convertit l'email en minuscules."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connection.get_cursor.return_value = mock_cursor
        
        repository.exists_by_email("TEST@ULAVAL.CA")
        
        args = mock_cursor.execute.call_args[0]
        assert args[1] == ("test@ulaval.ca",)
    
    def test_exists_by_email_returns_false_when_not_exists(self, repository, mock_connection):
        """Test exists_by_email retourne False si l'email n'existe pas."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connection.get_cursor.return_value = mock_cursor
        
        exists = repository.exists_by_email("notfound@ulaval.ca")
        
        assert exists is False
    
    def test_inherits_from_base_repository(self, repository):
        """Test que MySQLUserRepository hérite de BaseMySQLRepository."""
        from infrastructure.persistence.mysql.base_repository import BaseMySQLRepository
        assert isinstance(repository, BaseMySQLRepository)
    
    def test_implements_user_repository(self, repository):
        """Test que MySQLUserRepository implémente UserRepository."""
        from domain.user.user_repository import UserRepository
        assert isinstance(repository, UserRepository)
