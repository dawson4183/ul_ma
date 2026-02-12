"""
Configuration et Injection de Dépendances (Dependency Injection Container)
Utilise le pattern Dependency Injector pour gérer les dépendances
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()


class DatabaseConfig:
    """Configuration de la base de données MySQL"""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.database = os.getenv('DB_NAME', 'ulavalmarket')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
    
    def get_connection_params(self):
        """Retourne les paramètres de connexion MySQL"""
        return {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'user': self.user,
            'password': self.password,
            'charset': 'utf8mb4',
            'autocommit': False
        }


class AppConfig:
    """Configuration générale de l'application"""
    
    def __init__(self):
        self.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')
        self.frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.flask_env = os.getenv('FLASK_ENV', 'development')
    
    @property
    def is_development(self):
        return self.flask_env == 'development'
    
    @property
    def is_production(self):
        return self.flask_env == 'production'



