"""
Tests unitaires pour DatabaseConfig.
Vérifie que la configuration de base de données fonctionne correctement.
"""
import os
import pytest
from unittest.mock import patch

from infrastructure.database.config import DatabaseConfig


class TestDatabaseConfig:
    """Tests pour la classe DatabaseConfig"""

    def test_init_with_default_values(self):
        """Vérifie que les valeurs par défaut sont utilisées"""
        config = DatabaseConfig()
        
        assert config.host == 'localhost'
        assert config.port == 3306
        assert config.user == 'root'
        assert config.password == '@Lskdj1220Kevin'
        assert config.database == 'ulaval_market'
        assert config.charset == 'utf8mb4'
        assert config.autocommit is False

    def test_init_with_custom_values(self):
        """Vérifie que les valeurs personnalisées sont utilisées"""
        config = DatabaseConfig(
            host='custom-host',
            port=3307,
            user='admin',
            password='secret123',
            database='mydb',
            charset='utf8',
            autocommit=True
        )
        
        assert config.host == 'custom-host'
        assert config.port == 3307
        assert config.user == 'admin'
        assert config.password == 'secret123'
        assert config.database == 'mydb'
        assert config.charset == 'utf8'
        assert config.autocommit is True

    def test_init_with_partial_values(self):
        """Vérifie que les valeurs manquantes utilisent les défauts"""
        config = DatabaseConfig(host='custom-host', port=3307)
        
        assert config.host == 'custom-host'
        assert config.port == 3307
        assert config.user == 'root'  # défaut
        assert config.password == '@Lskdj1220Kevin'  # défaut

    def test_init_from_environment_variables(self):
        """Vérifie que les variables d'environnement sont utilisées"""
        env_vars = {
            'DB_HOST': 'env-host',
            'DB_PORT': '3308',
            'DB_USER': 'env-user',
            'DB_PASSWORD': 'env-pass',
            'DB_NAME': 'env-db',
            'DB_CHARSET': 'latin1',
            'DB_AUTOCOMMIT': 'true'
        }
        
        with patch.dict(os.environ, env_vars, clear=False):
            config = DatabaseConfig()
            
            assert config.host == 'env-host'
            assert config.port == 3308
            assert config.user == 'env-user'
            assert config.password == 'env-pass'
            assert config.database == 'env-db'
            assert config.charset == 'latin1'
            assert config.autocommit is True

    def test_init_from_environment_partial(self):
        """Vérifie que les variables d'environnement partielles fonctionnent"""
        with patch.dict(os.environ, {'DB_HOST': 'partial-host'}, clear=False):
            config = DatabaseConfig()
            
            assert config.host == 'partial-host'
            assert config.port == 3306  # défaut
            assert config.user == 'root'  # défaut

    def test_init_explicit_overrides_environment(self):
        """Vérifie que les valeurs explicites priorisent les variables d'env"""
        with patch.dict(os.environ, {'DB_HOST': 'env-host', 'DB_PORT': '3308'}, clear=False):
            config = DatabaseConfig(host='explicit-host')
            
            assert config.host == 'explicit-host'  # valeur explicite prioritaire
            assert config.port == 3308  # variable d'env utilisée

    def test_get_connection_params(self):
        """Vérifie que get_connection_params retourne un dictionnaire complet"""
        config = DatabaseConfig(
            host='test-host',
            port=3309,
            user='testuser',
            password='testpass',
            database='testdb',
            charset='utf8',
            autocommit=True
        )
        
        params = config.get_connection_params()
        
        expected = {
            'host': 'test-host',
            'port': 3309,
            'user': 'testuser',
            'password': 'testpass',
            'database': 'testdb',
            'charset': 'utf8',
            'autocommit': True
        }
        assert params == expected

    def test_get_connection_params_with_defaults(self):
        """Vérifie que get_connection_params fonctionne avec les valeurs par défaut"""
        config = DatabaseConfig()
        
        params = config.get_connection_params()
        
        assert params['host'] == 'localhost'
        assert params['port'] == 3306
        assert params['user'] == 'root'
        assert params['password'] == '@Lskdj1220Kevin'
        assert params['database'] == 'ulaval_market'
        assert params['charset'] == 'utf8mb4'
        assert params['autocommit'] is False

    def test_port_conversion_from_string_env(self):
        """Vérifie que le port est correctement converti depuis une chaîne env"""
        with patch.dict(os.environ, {'DB_PORT': '3307'}, clear=False):
            config = DatabaseConfig()
            assert config.port == 3307
            assert isinstance(config.port, int)

    def test_autocommit_conversion_from_string_env_true(self):
        """Vérifie que autocommit 'true' est converti en booléen"""
        with patch.dict(os.environ, {'DB_AUTOCOMMIT': 'true'}, clear=False):
            config = DatabaseConfig()
            assert config.autocommit is True

    def test_autocommit_conversion_from_string_env_false(self):
        """Vérifie que autocommit 'false' est converti en booléen"""
        with patch.dict(os.environ, {'DB_AUTOCOMMIT': 'false'}, clear=False):
            config = DatabaseConfig()
            assert config.autocommit is False

    def test_autocommit_conversion_from_string_env_uppercase(self):
        """Vérifie que autocommit est insensible à la casse"""
        with patch.dict(os.environ, {'DB_AUTOCOMMIT': 'TRUE'}, clear=False):
            config = DatabaseConfig()
            assert config.autocommit is True

    def test_autocommit_explicit_false_not_overridden(self):
        """Vérifie que autocommit=False explicite n'est pas écrasé"""
        with patch.dict(os.environ, {'DB_AUTOCOMMIT': 'true'}, clear=False):
            config = DatabaseConfig(autocommit=False)
            assert config.autocommit is False