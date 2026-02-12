"""
Module de configuration pour la connexion MySQL.
Gère les paramètres de connexion à la base de données.
"""
import os
from typing import Dict, Any


class DatabaseConfig:
    """
    Configuration centralisée pour la connexion MySQL.
    Gère les paramètres de connexion avec support des variables d'environnement.
    """
    
    def __init__(
        self,
        host: str = None,
        port: int = None,
        user: str = None,
        password: str = None,
        database: str = None,
        charset: str = None,
        autocommit: bool = None
    ):
        """
        Initialise la configuration de la base de données.
        
        Les valeurs peuvent être passées directement ou via variables d'environnement.
        Valeurs par défaut: localhost, 3306, root, @Lskdj1220Kevin, ulaval_market
        """
        # Paramètres de connexion avec valeurs par défaut
        self.host: str = host or os.getenv('DB_HOST', 'localhost')
        self.port: int = port or int(os.getenv('DB_PORT', '3306'))
        self.user: str = user or os.getenv('DB_USER', 'root')
        self.password: str = password or os.getenv('DB_PASSWORD', '@Lskdj1220Kevin')
        self.database: str = database or os.getenv('DB_NAME', 'ulaval_market')
        self.charset: str = charset or os.getenv('DB_CHARSET', 'utf8mb4')
        self.autocommit: bool = autocommit if autocommit is not None else os.getenv('DB_AUTOCOMMIT', 'False').lower() == 'true'
    
    def get_connection_params(self) -> Dict[str, Any]:
        """
        Retourne un dictionnaire avec tous les paramètres de connexion MySQL.
        
        Returns:
            Dict contenant host, port, user, password, database, charset et autocommit
        """
        return {
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.password,
            'database': self.database,
            'charset': self.charset,
            'autocommit': self.autocommit
        }
