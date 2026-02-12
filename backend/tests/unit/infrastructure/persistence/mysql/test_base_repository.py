"""
Tests pour le pattern Repository de base MySQL.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import mysql.connector
from mysql.connector.cursor import MySQLCursor

from infrastructure.persistence.mysql.base_repository import BaseMySQLRepository
from infrastructure.database.connection import DatabaseConnection
from domain.exceptions.database_exception import DatabaseException


class ConcreteRepository(BaseMySQLRepository):
    """Repository concret de test implémentant les méthodes abstraites"""
    
    def _get_table_name(self) -> str:
        return "test_table"
    
    def _map_to_entity(self, data):
        return data


class TestBaseMySQLRepository:
    """Tests pour la classe BaseMySQLRepository"""
    
    @pytest.fixture
    def mock_connection(self):
        """Fixture fournissant une connexion mockée"""
        return Mock(spec=DatabaseConnection)
    
    @pytest.fixture
    def repository(self, mock_connection):
        """Fixture fournissant un repository de test"""
        return ConcreteRepository(mock_connection)
    
    @pytest.fixture
    def mock_cursor(self):
        """Fixture fournissant un curseur mocké"""
        cursor = Mock(spec=MySQLCursor)
        cursor.description = [["id"], ["name"], ["email"]]
        return cursor
    
    def test_init_with_database_connection(self, mock_connection):
        """Vérifie que le constructeur accepte une DatabaseConnection"""
        repo = ConcreteRepository(mock_connection)
        assert repo._connection == mock_connection
    
    def test_is_abstract_class(self):
        """Vérifie que BaseMySQLRepository est abstraite"""
        with pytest.raises(TypeError):
            BaseMySQLRepository(Mock())
    
    def test_execute_query_success(self, repository, mock_connection, mock_cursor):
        """Vérifie que _execute_query fonctionne correctement"""
        mock_connection.get_cursor.return_value = mock_cursor
        
        result = repository._execute_query("SELECT * FROM users WHERE id = %s", (1,))
        
        mock_connection.get_cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE id = %s", (1,))
        assert result == mock_cursor
    
    def test_execute_query_without_params(self, repository, mock_connection, mock_cursor):
        """Vérifie que _execute_query fonctionne sans paramètres"""
        mock_connection.get_cursor.return_value = mock_cursor
        
        result = repository._execute_query("SELECT * FROM users")
        
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users", None)
        assert result == mock_cursor
    
    def test_execute_query_raises_database_exception(self, repository, mock_connection):
        """Vérifie que _execute_query convertit les erreurs SQL"""
        mock_connection.get_cursor.side_effect = mysql.connector.Error("Query failed")
        
        with pytest.raises(DatabaseException) as exc_info:
            repository._execute_query("SELECT * FROM users")
        
        assert "Échec de l'exécution de la requête" in str(exc_info.value)
        assert exc_info.value.original_error is not None
    
    def test_execute_many_success(self, repository, mock_connection, mock_cursor):
        """Vérifie que _execute_many fonctionne correctement avec commit"""
        mock_connection.get_cursor.return_value = mock_cursor
        mock_cursor.rowcount = 3
        
        params_list = [("name1",), ("name2",), ("name3",)]
        result = repository._execute_many("INSERT INTO users (name) VALUES (%s)", params_list)
        
        mock_connection.get_cursor.assert_called_once()
        mock_cursor.executemany.assert_called_once()
        mock_connection.commit.assert_called_once()
        assert result == 3
    
    def test_execute_many_rollback_on_error(self, repository, mock_connection):
        """Vérifie que _execute_many fait un rollback en cas d'erreur"""
        mock_connection.get_cursor.side_effect = mysql.connector.Error("Batch failed")
        
        with pytest.raises(DatabaseException) as exc_info:
            repository._execute_many("INSERT INTO users VALUES (%s)", [("data",)])
        
        mock_connection.rollback.assert_called_once()
        assert "Échec de l'exécution batch" in str(exc_info.value)
    
    def test_execute_many_closes_cursor(self, repository, mock_connection, mock_cursor):
        """Vérifie que _execute_many ferme le curseur même en cas d'erreur"""
        mock_connection.get_cursor.return_value = mock_cursor
        mock_cursor.executemany.side_effect = mysql.connector.Error("Batch failed")
        
        with pytest.raises(DatabaseException):
            repository._execute_many("INSERT INTO users VALUES (%s)", [("data",)])
        
        mock_cursor.close.assert_called_once()
    
    def test_fetch_one_success(self, repository, mock_connection, mock_cursor):
        """Vérifie que _fetch_one retourne un dictionnaire"""
        mock_connection.get_cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, "John", "john@example.com")
        
        result = repository._fetch_one("SELECT * FROM users WHERE id = %s", (1,))
        
        assert result == {"id": 1, "name": "John", "email": "john@example.com"}
        mock_cursor.close.assert_called_once()
    
    def test_fetch_one_no_result(self, repository, mock_connection, mock_cursor):
        """Vérifie que _fetch_one retourne None quand pas de résultat"""
        mock_connection.get_cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        
        result = repository._fetch_one("SELECT * FROM users WHERE id = %s", (999,))
        
        assert result is None
        mock_cursor.close.assert_called_once()
    
    def test_fetch_one_closes_cursor_on_error(self, repository, mock_connection, mock_cursor):
        """Vérifie que _fetch_one ferme le curseur même en cas d'erreur"""
        mock_connection.get_cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = mysql.connector.Error("Fetch failed")
        
        with pytest.raises(DatabaseException):
            repository._fetch_one("SELECT * FROM users")
        
        mock_cursor.close.assert_called_once()
    
    def test_fetch_one_raises_database_exception(self, repository, mock_connection):
        """Vérifie que _fetch_one convertit les erreurs SQL"""
        mock_connection.get_cursor.side_effect = mysql.connector.Error("Fetch failed")
        
        with pytest.raises(DatabaseException) as exc_info:
            repository._fetch_one("SELECT * FROM users")
        
        assert "Échec de la récupération d'un enregistrement" in str(exc_info.value)
    
    def test_fetch_all_success(self, repository, mock_connection, mock_cursor):
        """Vérifie que _fetch_all retourne une liste de dictionnaires"""
        mock_connection.get_cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "John", "john@example.com"),
            (2, "Jane", "jane@example.com")
        ]
        
        result = repository._fetch_all("SELECT * FROM users")
        
        expected = [
            {"id": 1, "name": "John", "email": "john@example.com"},
            {"id": 2, "name": "Jane", "email": "jane@example.com"}
        ]
        assert result == expected
        mock_cursor.close.assert_called_once()
    
    def test_fetch_all_empty_result(self, repository, mock_connection, mock_cursor):
        """Vérifie que _fetch_all retourne une liste vide"""
        mock_connection.get_cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        result = repository._fetch_all("SELECT * FROM users WHERE 1=0")
        
        assert result == []
        mock_cursor.close.assert_called_once()
    
    def test_fetch_all_with_params(self, repository, mock_connection, mock_cursor):
        """Vérifie que _fetch_all gère les paramètres"""
        mock_connection.get_cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        repository._fetch_all("SELECT * FROM users WHERE active = %s", (True,))
        
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM users WHERE active = %s", 
            (True,)
        )
    
    def test_fetch_all_closes_cursor_on_error(self, repository, mock_connection, mock_cursor):
        """Vérifie que _fetch_all ferme le curseur même en cas d'erreur"""
        mock_connection.get_cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = mysql.connector.Error("Fetch failed")
        
        with pytest.raises(DatabaseException):
            repository._fetch_all("SELECT * FROM users")
        
        mock_cursor.close.assert_called_once()
    
    def test_fetch_all_raises_database_exception(self, repository, mock_connection):
        """Vérifie que _fetch_all convertit les erreurs SQL"""
        mock_connection.get_cursor.side_effect = mysql.connector.Error("Fetch failed")
        
        with pytest.raises(DatabaseException) as exc_info:
            repository._fetch_all("SELECT * FROM users")
        
        assert "Échec de la récupération des enregistrements" in str(exc_info.value)
    
    def test_abstract_methods_must_be_implemented(self):
        """Vérifie que les méthodes abstraites doivent être implémentées"""
        class IncompleteRepository(BaseMySQLRepository):
            pass
        
        with pytest.raises(TypeError):
            IncompleteRepository(Mock())
