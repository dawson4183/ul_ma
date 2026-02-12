"""
Tests pour le module de gestion des connexions MySQL.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import mysql.connector

from infrastructure.database.connection import DatabaseConnection
from infrastructure.database.config import DatabaseConfig
from domain.exceptions.database_exception import DatabaseException


class TestDatabaseConnection:
    """Tests pour la classe DatabaseConnection"""
    
    def test_init_with_default_config(self):
        """Vérifie que l'initialisation avec config par défaut fonctionne"""
        db_conn = DatabaseConnection()
        
        assert db_conn._config is not None
        assert db_conn._connection is None
        assert db_conn._cursor is None
    
    def test_init_with_custom_config(self):
        """Vérifie que l'initialisation avec config personnalisée fonctionne"""
        custom_config = DatabaseConfig(host='custom_host', port=3307)
        db_conn = DatabaseConnection(config=custom_config)
        
        assert db_conn._config == custom_config
    
    @patch('infrastructure.database.connection.mysql.connector.connect')
    def test_connect_success(self, mock_connect):
        """Vérifie que connect() établit la connexion avec succès"""
        mock_connection = Mock()
        mock_connect.return_value = mock_connection
        
        db_conn = DatabaseConnection()
        db_conn.connect()
        
        mock_connect.assert_called_once()
        assert db_conn._connection == mock_connection
    
    @patch('infrastructure.database.connection.mysql.connector.connect')
    def test_connect_failure_raises_database_exception(self, mock_connect):
        """Vérifie que connect() lève DatabaseException en cas d'erreur"""
        mock_connect.side_effect = mysql.connector.Error("Connection refused")
        
        db_conn = DatabaseConnection()
        
        with pytest.raises(DatabaseException) as exc_info:
            db_conn.connect()
        
        assert "Échec de connexion" in str(exc_info.value)
        assert exc_info.value.original_error is not None
    
    def test_disconnect_closes_connection_and_cursor(self):
        """Vérifie que disconnect() ferme proprement la connexion et le curseur"""
        db_conn = DatabaseConnection()
        mock_connection = Mock()
        mock_cursor = Mock()
        db_conn._connection = mock_connection
        db_conn._cursor = mock_cursor
        
        db_conn.disconnect()
        
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
        assert db_conn._cursor is None
        assert db_conn._connection is None
    
    def test_disconnect_safe_when_not_connected(self):
        """Vérifie que disconnect() est sûr quand pas de connexion"""
        db_conn = DatabaseConnection()
        
        # Ne doit pas lever d'exception
        db_conn.disconnect()
        
        assert db_conn._connection is None
        assert db_conn._cursor is None
    
    def test_is_connected_returns_true_when_connected(self):
        """Vérifie que is_connected() retourne True quand connecté"""
        db_conn = DatabaseConnection()
        db_conn._connection = Mock()
        db_conn._connection.is_connected.return_value = True
        
        assert db_conn.is_connected() is True
    
    def test_is_connected_returns_false_when_not_connected(self):
        """Vérifie que is_connected() retourne False quand pas connecté"""
        db_conn = DatabaseConnection()
        
        assert db_conn.is_connected() is False
    
    def test_is_connected_returns_false_when_connection_none(self):
        """Vérifie que is_connected() retourne False quand _connection est None"""
        db_conn = DatabaseConnection()
        
        assert db_conn.is_connected() is False
    
    def test_get_cursor_raises_when_not_connected(self):
        """Vérifie que get_cursor() lève DatabaseException si pas connecté"""
        db_conn = DatabaseConnection()
        
        with pytest.raises(DatabaseException) as exc_info:
            db_conn.get_cursor()
        
        assert "connexion n'est pas établie" in str(exc_info.value)
    
    def test_get_cursor_returns_cursor_when_connected(self):
        """Vérifie que get_cursor() retourne un curseur quand connecté"""
        db_conn = DatabaseConnection()
        mock_cursor = Mock()
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        db_conn._connection = mock_connection
        
        cursor = db_conn.get_cursor()
        
        assert cursor == mock_cursor
        mock_connection.cursor.assert_called_once()
    
    def test_commit_raises_when_not_connected(self):
        """Vérifie que commit() lève DatabaseException si pas connecté"""
        db_conn = DatabaseConnection()
        
        with pytest.raises(DatabaseException) as exc_info:
            db_conn.commit()
        
        assert "connexion non établie" in str(exc_info.value)
    
    def test_commit_calls_connection_commit(self):
        """Vérifie que commit() appelle commit() sur la connexion"""
        db_conn = DatabaseConnection()
        mock_connection = Mock()
        mock_connection.is_connected.return_value = True
        db_conn._connection = mock_connection
        
        db_conn.commit()
        
        mock_connection.commit.assert_called_once()
    
    def test_commit_raises_on_mysql_error(self):
        """Vérifie que commit() lève DatabaseException en cas d'erreur MySQL"""
        db_conn = DatabaseConnection()
        mock_connection = Mock()
        mock_connection.is_connected.return_value = True
        mock_connection.commit.side_effect = mysql.connector.Error("Commit failed")
        db_conn._connection = mock_connection
        
        with pytest.raises(DatabaseException) as exc_info:
            db_conn.commit()
        
        assert "Échec du commit" in str(exc_info.value)
    
    def test_rollback_raises_when_not_connected(self):
        """Vérifie que rollback() lève DatabaseException si pas connecté"""
        db_conn = DatabaseConnection()
        
        with pytest.raises(DatabaseException) as exc_info:
            db_conn.rollback()
        
        assert "connexion non établie" in str(exc_info.value)
    
    def test_rollback_calls_connection_rollback(self):
        """Vérifie que rollback() appelle rollback() sur la connexion"""
        db_conn = DatabaseConnection()
        mock_connection = Mock()
        mock_connection.is_connected.return_value = True
        db_conn._connection = mock_connection
        
        db_conn.rollback()
        
        mock_connection.rollback.assert_called_once()
    
    def test_rollback_raises_on_mysql_error(self):
        """Vérifie que rollback() lève DatabaseException en cas d'erreur MySQL"""
        db_conn = DatabaseConnection()
        mock_connection = Mock()
        mock_connection.is_connected.return_value = True
        mock_connection.rollback.side_effect = mysql.connector.Error("Rollback failed")
        db_conn._connection = mock_connection
        
        with pytest.raises(DatabaseException) as exc_info:
            db_conn.rollback()
        
        assert "Échec du rollback" in str(exc_info.value)


class TestDatabaseConnectionContextManager:
    """Tests pour le context manager de DatabaseConnection"""
    
    @patch('infrastructure.database.connection.mysql.connector.connect')
    def test_enter_establishes_connection(self, mock_connect):
        """Vérifie que __enter__ établit la connexion"""
        mock_connection = Mock()
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection
        
        with DatabaseConnection() as db_conn:
            mock_connect.assert_called_once()
            assert db_conn.is_connected() is True
    
    @patch('infrastructure.database.connection.mysql.connector.connect')
    def test_exit_closes_connection(self, mock_connect):
        """Vérifie que __exit__ ferme la connexion"""
        mock_connection = Mock()
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection
        
        with DatabaseConnection() as db_conn:
            pass
        
        mock_connection.close.assert_called_once()
    
    @patch('infrastructure.database.connection.mysql.connector.connect')
    def test_exit_commits_on_success(self, mock_connect):
        """Vérifie que __exit__ fait un commit quand pas d'exception"""
        mock_connection = Mock()
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection
        
        with DatabaseConnection() as db_conn:
            pass  # Pas d'exception
        
        mock_connection.commit.assert_called_once()
        mock_connection.rollback.assert_not_called()
    
    @patch('infrastructure.database.connection.mysql.connector.connect')
    def test_exit_rollback_on_exception(self, mock_connect):
        """Vérifie que __exit__ fait un rollback quand exception"""
        mock_connection = Mock()
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection
        
        try:
            with DatabaseConnection() as db_conn:
                raise ValueError("Test exception")
        except ValueError:
            pass
        
        mock_connection.rollback.assert_called_once()
        mock_connection.commit.assert_not_called()
    
    @patch('infrastructure.database.connection.mysql.connector.connect')
    def test_context_manager_returns_instance(self, mock_connect):
        """Vérifie que le context manager retourne l'instance"""
        mock_connection = Mock()
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection
        
        db_conn = None
        with DatabaseConnection() as conn:
            db_conn = conn
        
        assert isinstance(db_conn, DatabaseConnection)
