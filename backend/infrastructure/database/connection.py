"""
Module de gestion des connexions MySQL.
Fournit une classe DatabaseConnection pour gérer les connexions de manière centralisée.
"""
from typing import Optional, Any
import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from infrastructure.database.config import DatabaseConfig
from domain.exceptions.database_exception import DatabaseException


class DatabaseConnection:
    """
    Gestionnaire de connexion MySQL utilisant mysql-connector-python.
    
    Cette classe encapsule la connexion à la base de données et fournit
    des méthodes pour gérer les transactions et les curseurs.
    Elle supporte le context manager (with statement) pour une gestion
    automatique des ressources.
    """
    
    def __init__(self, config: DatabaseConfig = None):
        """
        Initialise le gestionnaire de connexion.
        
        Args:
            config: Configuration de la base de données. Si None, utilise DatabaseConfig par défaut.
        """
        self._config = config or DatabaseConfig()
        self._connection: Optional[MySQLConnection] = None
        self._cursor: Optional[MySQLCursor] = None
    
    def connect(self) -> None:
        """
        Établit la connexion à la base de données.
        
        Raises:
            DatabaseException: Si la connexion échoue.
        """
        try:
            params = self._config.get_connection_params()
            self._connection = mysql.connector.connect(**params)
        except mysql.connector.Error as e:
            raise DatabaseException(
                f"Échec de connexion à la base de données: {str(e)}",
                original_error=e
            )
    
    def disconnect(self) -> None:
        """
        Ferme la connexion à la base de données et libère les ressources.
        
        Cette méthode est sûre à appeler même si la connexion n'est pas établie.
        """
        if self._cursor is not None:
            try:
                self._cursor.close()
            except Exception:
                pass  # Ignorer les erreurs lors de la fermeture du curseur
            self._cursor = None
        
        if self._connection is not None:
            try:
                self._connection.close()
            except Exception:
                pass  # Ignorer les erreurs lors de la fermeture de la connexion
            self._connection = None
    
    def is_connected(self) -> bool:
        """
        Vérifie si la connexion est établie et active.
        
        Returns:
            True si la connexion est active, False sinon.
        """
        if self._connection is None:
            return False
        try:
            return self._connection.is_connected()
        except Exception:
            return False
    
    def get_cursor(self) -> MySQLCursor:
        """
        Retourne un curseur pour exécuter des requêtes.
        
        La connexion doit être établie avant d'appeler cette méthode.
        
        Returns:
            Un curseur MySQLCursor.
            
        Raises:
            DatabaseException: Si la connexion n'est pas établie.
        """
        if not self.is_connected():
            raise DatabaseException("La connexion n'est pas établie. Appelez connect() d'abord.")
        
        try:
            self._cursor = self._connection.cursor()
            return self._cursor
        except mysql.connector.Error as e:
            raise DatabaseException(
                f"Impossible de créer le curseur: {str(e)}",
                original_error=e
            )
    
    def commit(self) -> None:
        """
        Valide les transactions en cours.
        
        Raises:
            DatabaseException: Si la validation échoue ou si pas de connexion.
        """
        if not self.is_connected():
            raise DatabaseException("Impossible de commit: connexion non établie")
        
        try:
            self._connection.commit()
        except mysql.connector.Error as e:
            raise DatabaseException(
                f"Échec du commit: {str(e)}",
                original_error=e
            )
    
    def rollback(self) -> None:
        """
        Annule les transactions en cours.
        
        Raises:
            DatabaseException: Si l'annulation échoue ou si pas de connexion.
        """
        if not self.is_connected():
            raise DatabaseException("Impossible de rollback: connexion non établie")
        
        try:
            self._connection.rollback()
        except mysql.connector.Error as e:
            raise DatabaseException(
                f"Échec du rollback: {str(e)}",
                original_error=e
            )
    
    def __enter__(self) -> 'DatabaseConnection':
        """
        Entrée du context manager - établit la connexion.
        
        Returns:
            L'instance elle-même pour utilisation dans le bloc with.
        """
        self.connect()
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Sortie du context manager - ferme la connexion proprement.
        
        Si une exception a eu lieu dans le bloc with, un rollback est effectué.
        Sinon, un commit est effectué.
        
        Args:
            exc_type: Type de l'exception si une erreur est survenue, None sinon.
            exc_val: Valeur de l'exception.
            exc_tb: Traceback de l'exception.
        """
        if self.is_connected():
            if exc_type is not None:
                # Une exception s'est produite, on annule les changements
                try:
                    self._connection.rollback()
                except Exception:
                    pass  # Ignorer les erreurs de rollback
            else:
                # Pas d'exception, on valide les changements
                try:
                    self._connection.commit()
                except Exception:
                    pass  # Ignorer les erreurs de commit
        
        # Toujours fermer la connexion
        self.disconnect()
