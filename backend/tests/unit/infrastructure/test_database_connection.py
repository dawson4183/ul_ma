"""
Tests unitaires pour DatabaseConnection.
Vérifie que la gestion des connexions MySQL fonctionne correctement.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from infrastructure.database.connection import DatabaseConnection
from infrastructure.database.config import DatabaseConfig
from domain.exceptions.database_exception import DatabaseException


class TestDatabaseConnection:
    """Tests pour la classe DatabaseConnection"""

    @pytest.fixture
    def mock_config(self):
        """Fixture fournissant une configuration mockée"""
        config = Mock(spec=DatabaseConfig)
        config.get_connection_params.return_value = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'password',
            'database': 'testdb',
            'charset': 'utf8mb4',
            'autocommit': False
        }
        return config

    @pytest.fixture
    def mock_mysql_connection(self):
        """Fixture fournissant une connexion MySQL mockée"""
        conn = Mock(spec=MySQLConnection)
        conn.is_connected.return_value = True
        return conn

    @pytest.fixture
    def mock_mysql_cursor(self):
        """Fixture fournissant un curseur MySQL mocké"""
        cursor = Mock(spec=MySQLCursor)
        return cursor

    def test_init_with_default_config(self):
        """Vérifie que l'initialisation sans config crée une DatabaseConfig"""
        with patch('infrastructure.database.connection.DatabaseConfig') as mock_config_class:
            mock_config_instance = Mock()
            mock_config_class.return_value = mock_config_instance
            
            conn = DatabaseConnection()
            
            assert conn._config == mock_config_instance
            assert conn._connection is None
            assert conn._cursor is None

    def test_init_with_custom_config(self, mock_config):
        """Vérifie que l'initialisation accepte une config personnalisée"""
        conn = DatabaseConnection(mock_config)
        
        assert conn._config == mock_config
        assert conn._connection is None
        assert conn._cursor is None

    @patch('infrastructure.database.connection.mysql.connector.connect')
    def test_connect_success(self, mock_connect, mock_config, mock_mysql_connection):
        """Vérifie que connect() établit la connexion avec succès"""
        mock_connect.return_value = mock_mysql_connection
        
        conn = DatabaseConnection(mock_config)
        conn.connect()
        
        mock_connect.assert_called_once_with(
            host='localhost',
            port=3306,
            user='root',
            password='password',
            database='testdb',
            charset='utf8mb4',
            autocommit=False
        )
        assert conn._connection == mock_mysql_connection

    @patch('infrastructure.database.connection.mysql.connector.connect')
    def test_connect_raises_database_exception(self, mock_connect, mock_config):
        """Vérifie que connect() convertit les erreurs mysql en DatabaseException"""
        mock_connect.side_effect = mysql.connector.Error("Connection failed")
        
        conn = DatabaseConnection(mock_config)
        
        with pytest.raises(DatabaseException) as exc_info:
            conn.connect()
        
        assert "Échec de connexion à la base de données" in str(exc_info.value)
        assert exc_info.value.original_error is not None

    def test_disconnect_closes_cursor_and_connection(self, mock_config, mock_mysql_connection):
        """Vérifie que disconnect() ferme le curseur et la connexion"""
        conn = DatabaseConnection(mock_config)
        conn._connection = mock_mysql_connection
        mock_cursor = Mock()
        conn._cursor = mock_cursor
        
        conn.disconnect()
        
        mock_cursor.close.assert_called_once()
        mock_mysql_connection.close.assert_called_once()
        assert conn._cursor is None
        assert conn._connection is None

    def test_disconnect_safe_when_not_connected(self, mock_config):
        """Vérifie que disconnect() est sûr quand pas de connexion"""
        conn = DatabaseConnection(mock_config)
        
        # Ne doit pas lever d'exception
        conn.disconnect()
        
        assert conn._connection is None
        assert conn._cursor is None

    def test_disconnect_ignores_cursor_close_errors(self, mock_config, mock_mysql_connection):
        """Vérifie que disconnect() ignore les erreurs de fermeture du curseur"""
        conn = DatabaseConnection(mock_config)
        conn._connection = mock_mysql_connection
        conn._cursor = Mock()
        conn._cursor.close.side_effect = Exception("Cursor close failed")
        
        # Ne doit pas lever d'exception
        conn.disconnect()
        
        assert conn._cursor is None
        assert conn._connection is None

    def test_disconnect_ignores_connection_close_errors(self, mock_config, mock_mysql_connection):
        """Vérifie que disconnect() ignore les erreurs de fermeture de la connexion"""
        mock_mysql_connection.close.side_effect = Exception("Connection close failed")
        conn = DatabaseConnection(mock_config)
        conn._connection = mock_mysql_connection
        
        # Ne doit pas lever d'exception
        conn.disconnect()
        
        assert conn._connection is None

    def test_is_connected_returns_false_when_none(self, mock_config):
        """Vérifie que is_connected() retourne False quand connexion est None"""
        conn = DatabaseConnection(mock_config)
        
        assert conn.is_connected() is False

    def test_is_connected_returns_true_when_active(self, mock_config, mock_mysql_connection):
        """Vérifie que is_connected() retourne True quand connexion active"""
        mock_mysql_connection.is_connected.return_value = True
        conn = DatabaseConnection(mock_config)
        conn._connection = mock_mysql_connection
        
        assert conn.is_connected() is True

    def test_is_connected_returns_false_when_inactive(self, mock_config, mock_mysql_connection):
        """Vérifie que is_connected() retourne False quand connexion inactive"""
        mock_mysql_connection.is_connected.return_value = False
        conn = DatabaseConnection(mock_config)
        conn._connection = mock_mysql_connection
        
        assert conn.is_connected() is False

    def test_is_connected_returns_false_on_exception(self, mock_config, mock_mysql_connection):
        """Vérifie que is_connected() retourne False en cas d'exception"""
        mock_mysql_connection.is_connected.side_effect = Exception("Check failed")
        conn = DatabaseConnection(mock_config)
        conn._connection = mock_mysql_connection
        
        assert conn.is_connected() is False

    def test_get_cursor_raises_when_not_connected(self, mock_config):
        """Vérifie que get_cursor() lève une exception si pas connecté"""
        conn = DatabaseConnection(mock_config)
        
        with pytest.raises(DatabaseException) as exc_info:
            conn.get_cursor()
        
        assert "connexion n'est pas établie" in str(exc_info.value)

    def test_get_cursor_returns_cursor_when_connected(self, mock_config, mock_mysql_connection, mock_mysql_cursor):
        """Vérifie que get_cursor() retourne un curseur quand connecté"""
        mock_mysql_connection.cursor.return_value = mock_mysql_cursor
        conn = DatabaseConnection(mock_config)
        conn._connection = mock_mysql_connection
        
        cursor = conn.get_cursor()
        
        assert cursor == mock_mysql_cursor
        mock_mysql_connection.cursor.assert_called_once()

    def test_get_cursor_raises_on_cursor_error(self, mock_config, mock_mysql_connection):
        """Vérifie que get_cursor() convertit les erreurs en DatabaseException"""
        mock_mysql_connection.cursor.side_effect = mysql.connector.Error("Cursor creation failed")
        conn = DatabaseConnection(mock_config)
        conn._connection = mock_mysql_connection
        
        with pytest.raises(DatabaseException) as exc_info:
            conn.get_cursor()
        
        assert "Impossible de créer le curseur" in str(exc_info.value)

    def test_commit_raises_when_not_connected(self, mock_config):
        """Vérifie que commit() lève une exception si pas connecté"""
        conn = DatabaseConnection(mock_config)
        
        with pytest.raises(DatabaseException) as exc_info:
            conn.commit()
        
        assert "Impossible de commit" in str(exc_info.value)

    def test_commit_success(self, mock_config, mock_mysql_connection):
        """Vérifie que commit() appelle connection.commit()"""
        conn = DatabaseConnection(mock_config)
        conn._connection = mock_mysql_connection
        
        conn.commit()
        
        mock_mysql_connection.commit.assert_called_once()

    def test_commit_raises_on_error(self, mock_config, mock_mysql_connection):
        """Vérifie que commit() convertit les erreurs en DatabaseException"""
        mock_mysql_connection.commit.side_effect = mysql.connector.Error("Commit failed")
        conn = DatabaseConnection(mock_config)
        conn._connection = mock_mysql_connection
        
        with pytest.raises(DatabaseException) as exc_info:
            conn.commit()
        
        assert "Échec du commit" in str(exc_info.value)

    def test_rollback_raises_when_not_connected(self, mock_config):
        """Vérifie que rollback() lève une exception si pas connecté"""
        conn = DatabaseConnection(mock_config)
        
        with pytest.raises(DatabaseException) as exc_info:
            conn.rollback()
        
        assert "Impossible de rollback" in str(exc_info.value)

    def test_rollback_success(self, mock_config, mock_mysql_connection):
        """Vérifie que rollback() appelle connection.rollback()"""
        conn = DatabaseConnection(mock_config)
        conn._connection = mock_mysql_connection
        
        conn.rollback()
        
        mock_mysql_connection.rollback.assert_called_once()

    def test_rollback_raises_on_error(self, mock_config, mock_mysql_connection):
        """Vérifie que rollback() convertit les erreurs en DatabaseException"""
        mock_mysql_connection.rollback.side_effect = mysql.connector.Error("Rollback failed")
        conn = DatabaseConnection(mock_config)
        conn._connection = mock_mysql_connection
        
        with pytest.raises(DatabaseException) as exc_info:
            conn.rollback()
        
        assert "Échec du rollback" in str(exc_info.value)

    @patch('infrastructure.database.connection.mysql.connector.connect')
    def test_context_manager_enters_with_connect(self, mock_connect, mock_config, mock_mysql_connection):
        """Vérifie que le context manager établit la connexion"""
        mock_connect.return_value = mock_mysql_connection
        
        with DatabaseConnection(mock_config) as conn:
            assert conn.is_connected() is True
        
        mock_connect.assert_called_once()

    @patch('infrastructure.database.connection.mysql.connector.connect')
    def test_context_manager_exits_with_disconnect(self, mock_connect, mock_config, mock_mysql_connection):
        """Vérifie que le context manager ferme la connexion à la sortie"""
        mock_connect.return_value = mock_mysql_connection
        
        with DatabaseConnection(mock_config) as conn:
            pass
        
        mock_mysql_connection.close.assert_called_once()

    @patch('infrastructure.database.connection.mysql.connector.connect')
    def test_context_manager_rollback_on_exception(self, mock_connect, mock_config, mock_mysql_connection):
        """Vérifie que le context manager fait un rollback en cas d'exception"""
        mock_connect.return_value = mock_mysql_connection
        
        try:
            with DatabaseConnection(mock_config) as conn:
                raise ValueError("Test exception")
        except ValueError:
            pass
        
        mock_mysql_connection.rollback.assert_called_once()

    @patch('infrastructure.database.connection.mysql.connector.connect')
    def test_context_manager_commit_on_success(self, mock_connect, mock_config, mock_mysql_connection):
        """Vérifie que le context manager fait un commit en cas de succès"""
        mock_connect.return_value = mock_mysql_connection
        
        with DatabaseConnection(mock_config) as conn:
            pass
        
        mock_mysql_connection.commit.assert_called_once()

    @patch('infrastructure.database.connection.mysql.connector.connect')
    def test_context_manager_ignores_rollback_errors(self, mock_connect, mock_config, mock_mysql_connection):
        """Vérifie que le context manager ignore les erreurs de rollback"""
        mock_connect.return_value = mock_mysql_connection
        mock_mysql_connection.rollback.side_effect = Exception("Rollback failed")
        
        try:
            with DatabaseConnection(mock_config) as conn:
                raise ValueError("Test exception")
        except ValueError:
            pass
        
        # Ne doit pas propager l'exception de rollback
        mock_mysql_connection.close.assert_called_once()

    @patch('infrastructure.database.connection.mysql.connector.connect')
    def test_context_manager_ignores_commit_errors(self, mock_connect, mock_config, mock_mysql_connection):
        """Vérifie que le context manager ignore les erreurs de commit"""
        mock_connect.return_value = mock_mysql_connection
        mock_mysql_connection.commit.side_effect = Exception("Commit failed")
        
        with DatabaseConnection(mock_config) as conn:
            pass
        
        # Ne doit pas propager l'exception de commit
        mock_mysql_connection.close.assert_called_once()