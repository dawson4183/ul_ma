"""
Tests pour le module de configuration de base de données.
"""
import os
import pytest
from infrastructure.database.config import DatabaseConfig


class TestDatabaseConfig:
    """Tests pour la classe DatabaseConfig"""
    
    def test_default_values(self):
        """Vérifie que les valeurs par défaut sont correctement initialisées"""
        config = DatabaseConfig()
        
        assert config.host == 'localhost'
        assert config.port == 3306
        assert config.user == 'root'
        assert config.password == '@Lskdj1220Kevin'
        assert config.database == 'ulaval_market'
        assert config.charset == 'utf8mb4'
        assert config.autocommit is False
    
    def test_custom_values(self):
        """Vérifie que les valeurs personnalisées sont correctement utilisées"""
        config = DatabaseConfig(
            host='custom_host',
            port=3307,
            user='custom_user',
            password='custom_pass',
            database='custom_db',
            charset='latin1',
            autocommit=True
        )
        
        assert config.host == 'custom_host'
        assert config.port == 3307
        assert config.user == 'custom_user'
        assert config.password == 'custom_pass'
        assert config.database == 'custom_db'
        assert config.charset == 'latin1'
        assert config.autocommit is True
    
    def test_get_connection_params(self):
        """Vérifie que get_connection_params retourne un dict avec tous les paramètres"""
        config = DatabaseConfig(
            host='test_host',
            port=3308,
            user='test_user',
            password='test_pass',
            database='test_db',
            charset='utf8',
            autocommit=True
        )
        
        params = config.get_connection_params()
        
        assert isinstance(params, dict)
        assert params['host'] == 'test_host'
        assert params['port'] == 3308
        assert params['user'] == 'test_user'
        assert params['password'] == 'test_pass'
        assert params['database'] == 'test_db'
        assert params['charset'] == 'utf8'
        assert params['autocommit'] is True
    
    def test_get_connection_params_has_all_keys(self):
        """Vérifie que le dict retourné contient toutes les clés requises"""
        config = DatabaseConfig()
        params = config.get_connection_params()
        
        required_keys = ['host', 'port', 'user', 'password', 'database', 'charset', 'autocommit']
        for key in required_keys:
            assert key in params, f"La clé '{key}' est manquante dans les paramètres de connexion"
    
    def test_environment_variables_override_defaults(self, monkeypatch):
        """Vérifie que les variables d'environnement remplacent les valeurs par défaut"""
        monkeypatch.setenv('DB_HOST', 'env_host')
        monkeypatch.setenv('DB_PORT', '3309')
        monkeypatch.setenv('DB_USER', 'env_user')
        monkeypatch.setenv('DB_PASSWORD', 'env_pass')
        monkeypatch.setenv('DB_NAME', 'env_db')
        monkeypatch.setenv('DB_CHARSET', 'env_charset')
        monkeypatch.setenv('DB_AUTOCOMMIT', 'True')
        
        config = DatabaseConfig()
        
        assert config.host == 'env_host'
        assert config.port == 3309
        assert config.user == 'env_user'
        assert config.password == 'env_pass'
        assert config.database == 'env_db'
        assert config.charset == 'env_charset'
        assert config.autocommit is True
    
    def test_explicit_values_override_environment_variables(self, monkeypatch):
        """Vérifie que les valeurs explicites ont priorité sur les variables d'environnement"""
        monkeypatch.setenv('DB_HOST', 'env_host')
        
        config = DatabaseConfig(host='explicit_host')
        
        assert config.host == 'explicit_host'
    
    def test_partial_custom_values(self):
        """Vérifie que les valeurs partielles personnalisées fonctionnent avec les défauts pour le reste"""
        config = DatabaseConfig(host='custom_only')
        
        assert config.host == 'custom_only'
        assert config.port == 3306  # valeur par défaut
        assert config.user == 'root'  # valeur par défaut
