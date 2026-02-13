"""
Tests pour MySQLSessionRepository.

Ces tests vérifient que l'implémentation MySQL du SessionRepository
fonctionne correctement avec une base de données MySQL.
"""
from datetime import datetime, timedelta
from typing import Dict, Any
import pytest
from unittest.mock import Mock, MagicMock

from infrastructure.persistence.mysql.mysql_session_repository import MySQLSessionRepository
from domain.auth.session import Session
from domain.exceptions.database_exception import DatabaseException


class TestMySQLSessionRepository:
    """Tests pour MySQLSessionRepository."""
    
    @pytest.fixture
    def mock_connection(self):
        """Fixture pour une connexion mockée."""
        return Mock()
    
    @pytest.fixture
    def repository(self, mock_connection):
        """Fixture pour le repository avec connexion mockée."""
        return MySQLSessionRepository(mock_connection)
    
    @pytest.fixture
    def sample_session_data(self) -> Dict[str, Any]:
        """Fixture pour les données brutes d'une session."""
        return {
            "session_id": "sess-123",
            "user_id": "user-456",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": Session.TOKEN_TYPE_AUTH,
            "expires_at": datetime.now() + timedelta(hours=24),
            "used_at": None
        }
    
    @pytest.fixture
    def sample_session(self) -> Session:
        """Fixture pour une session de test."""
        return Session(
            session_id="sess-123",
            user_id="user-456",
            token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            token_type=Session.TOKEN_TYPE_AUTH,
            expires_at=datetime.now() + timedelta(hours=24),
            used_at=None
        )
    
    @pytest.fixture
    def used_session(self) -> Session:
        """Fixture pour une session utilisée de test."""
        return Session(
            session_id="sess-789",
            user_id="user-456",
            token="used_token...",
            token_type=Session.TOKEN_TYPE_AUTH,
            expires_at=datetime.now() + timedelta(hours=24),
            used_at=datetime.now()
        )
    
    def test_get_table_name_returns_sessions(self, repository):
        """Test que _get_table_name retourne 'sessions'."""
        assert repository._get_table_name() == "sessions"
    
    def test_map_to_entity_creates_session(self, repository, sample_session_data):
        """Test que _map_to_entity crée correctement une Session."""
        session = repository._map_to_entity(sample_session_data)
        
        assert isinstance(session, Session)
        assert session.session_id == "sess-123"
        assert session.user_id == "user-456"
        assert session.token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        assert session.token_type == Session.TOKEN_TYPE_AUTH
        assert session.used_at is None
    
    def test_map_to_entity_handles_used_at_datetime(self, repository):
        """Test que _map_to_entity gère used_at comme datetime."""
        data = {
            "session_id": "sess-789",
            "user_id": "user-456",
            "token": "used_token...",
            "token_type": Session.TOKEN_TYPE_AUTH,
            "expires_at": datetime.now() + timedelta(hours=24),
            "used_at": datetime.now()
        }
        
        session = repository._map_to_entity(data)
        
        assert session.used_at is not None
        assert isinstance(session.used_at, datetime)
    
    def test_map_to_entity_handles_used_at_none(self, repository, sample_session_data):
        """Test que _map_to_entity gère used_at à None."""
        sample_session_data["used_at"] = None
        
        session = repository._map_to_entity(sample_session_data)
        
        assert session.used_at is None
    
    def test_find_by_token_returns_session(self, repository, mock_connection, sample_session_data):
        """Test find_by_token retourne une session quand trouvée."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (
            "sess-123", "user-456", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "auth", sample_session_data["expires_at"], None
        )
        mock_cursor.description = [
            ("session_id",), ("user_id",), ("token",),
            ("token_type",), ("expires_at",), ("used_at",)
        ]
        mock_connection.get_cursor.return_value = mock_cursor
        
        session = repository.find_by_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        
        assert session is not None
        assert session.session_id == "sess-123"
        assert session.token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert "WHERE token = %s" in args[0]
    
    def test_find_by_token_returns_none_when_not_found(self, repository, mock_connection):
        """Test find_by_token retourne None quand session non trouvée."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connection.get_cursor.return_value = mock_cursor
        
        session = repository.find_by_token("non-existent-token")
        
        assert session is None
    
    def test_find_by_user_id_returns_list_of_sessions(self, repository, mock_connection, sample_session_data):
        """Test find_by_user_id retourne une liste de sessions."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ("sess-123", "user-456", "token1...", "auth", sample_session_data["expires_at"], None),
            ("sess-124", "user-456", "token2...", "auth", sample_session_data["expires_at"], None)
        ]
        mock_cursor.description = [
            ("session_id",), ("user_id",), ("token",),
            ("token_type",), ("expires_at",), ("used_at",)
        ]
        mock_connection.get_cursor.return_value = mock_cursor
        
        sessions = repository.find_by_user_id("user-456")
        
        assert len(sessions) == 2
        assert all(isinstance(s, Session) for s in sessions)
        assert sessions[0].user_id == "user-456"
        assert sessions[1].user_id == "user-456"
    
    def test_find_by_user_id_returns_empty_list_when_none(self, repository, mock_connection):
        """Test find_by_user_id retourne une liste vide quand aucune session."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_connection.get_cursor.return_value = mock_cursor
        
        sessions = repository.find_by_user_id("user-with-no-sessions")
        
        assert sessions == []
    
    def test_save_inserts_new_session(self, repository, mock_connection, sample_session):
        """Test save fait un INSERT pour une nouvelle session."""
        mock_cursor = MagicMock()
        mock_connection.get_cursor.return_value = mock_cursor
        
        repository.save(sample_session)
        
        mock_connection.commit.assert_called_once()
        
        # Vérifie que c'était bien un INSERT
        args = mock_cursor.execute.call_args[0]
        assert "INSERT" in args[0]
        assert "sessions" in args[0]
        assert args[1] == (
            sample_session.session_id,
            sample_session.user_id,
            sample_session.token,
            sample_session.token_type,
            sample_session.expires_at,
            sample_session.used_at
        )
    
    def test_save_rollback_on_error(self, repository, mock_connection, sample_session):
        """Test save fait un rollback en cas d'erreur."""
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("DB Error")
        mock_connection.get_cursor.return_value = mock_cursor
        
        with pytest.raises(Exception):
            repository.save(sample_session)
        
        mock_connection.rollback.assert_called_once()
    
    def test_save_closes_cursor_on_error(self, repository, mock_connection, sample_session):
        """Test save ferme le curseur même en cas d'erreur."""
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("DB Error")
        mock_connection.get_cursor.return_value = mock_cursor
        
        with pytest.raises(Exception):
            repository.save(sample_session)
        
        mock_cursor.close.assert_called_once()
    
    def test_mark_as_used_updates_used_at(self, repository, mock_connection):
        """Test mark_as_used met à jour used_at avec CURRENT_TIMESTAMP."""
        mock_cursor = MagicMock()
        mock_connection.get_cursor.return_value = mock_cursor
        
        repository.mark_as_used("sess-123")
        
        mock_connection.commit.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert "UPDATE" in args[0]
        assert "sessions" in args[0]
        assert "used_at = CURRENT_TIMESTAMP" in args[0]
        assert args[1] == ("sess-123",)
    
    def test_mark_as_used_rollback_on_error(self, repository, mock_connection):
        """Test mark_as_used fait un rollback en cas d'erreur."""
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("DB Error")
        mock_connection.get_cursor.return_value = mock_cursor
        
        with pytest.raises(Exception):
            repository.mark_as_used("sess-123")
        
        mock_connection.rollback.assert_called_once()
    
    def test_mark_as_used_closes_cursor_on_error(self, repository, mock_connection):
        """Test mark_as_used ferme le curseur même en cas d'erreur."""
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("DB Error")
        mock_connection.get_cursor.return_value = mock_cursor
        
        with pytest.raises(Exception):
            repository.mark_as_used("sess-123")
        
        mock_cursor.close.assert_called_once()
    
    def test_delete_removes_session(self, repository, mock_connection):
        """Test delete supprime la session par son ID."""
        mock_cursor = MagicMock()
        mock_connection.get_cursor.return_value = mock_cursor
        
        repository.delete("sess-123")
        
        mock_connection.commit.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert "DELETE" in args[0]
        assert "sessions" in args[0]
        assert "WHERE session_id = %s" in args[0]
        assert args[1] == ("sess-123",)
    
    def test_delete_rollback_on_error(self, repository, mock_connection):
        """Test delete fait un rollback en cas d'erreur."""
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("DB Error")
        mock_connection.get_cursor.return_value = mock_cursor
        
        with pytest.raises(Exception):
            repository.delete("sess-123")
        
        mock_connection.rollback.assert_called_once()
    
    def test_delete_closes_cursor_on_error(self, repository, mock_connection):
        """Test delete ferme le curseur même en cas d'erreur."""
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("DB Error")
        mock_connection.get_cursor.return_value = mock_cursor
        
        with pytest.raises(Exception):
            repository.delete("sess-123")
        
        mock_cursor.close.assert_called_once()
    
    def test_inherits_from_base_repository(self, repository):
        """Test que MySQLSessionRepository hérite de BaseMySQLRepository."""
        from infrastructure.persistence.mysql.base_repository import BaseMySQLRepository
        assert isinstance(repository, BaseMySQLRepository)
    
    def test_implements_session_repository(self, repository):
        """Test que MySQLSessionRepository implémente SessionRepository."""
        from domain.auth.session_repository import SessionRepository
        assert isinstance(repository, SessionRepository)
