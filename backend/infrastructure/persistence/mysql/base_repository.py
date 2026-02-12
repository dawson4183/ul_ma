"""
Module du pattern Repository de base pour MySQL.
Fournit une classe abstraite BaseMySQLRepository pour standardiser l'accès aux données.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Tuple
import mysql.connector
from mysql.connector.cursor import MySQLCursor

from infrastructure.database.connection import DatabaseConnection
from domain.exceptions.database_exception import DatabaseException


class BaseMySQLRepository(ABC):
    """
    Classe de base abstraite pour tous les repositories MySQL.
    
    Cette classe fournit des méthodes utilitaires pour exécuter des requêtes SQL
    et gérer les transactions. Elle suit le pattern Template Method pour
    standardiser les opérations CRUD.
    
    Attributes:
        _connection: Instance de DatabaseConnection injectée
    """
    
    def __init__(self, database_connection: DatabaseConnection):
        """
        Initialise le repository avec une connexion.
        
        Args:
            database_connection: Instance de DatabaseConnection pour accès aux données
        """
        self._connection = database_connection
    
    def _execute_query(
        self, 
        query: str, 
        params: Optional[Tuple] = None
    ) -> MySQLCursor:
        """
        Exécute une requête SQL simple.
        
        Cette méthode gère automatiquement la création du curseur,
        l'exécution de la requête et la gestion des erreurs.
        
        Args:
            query: Requête SQL à exécuter
            params: Paramètres pour la requête (optionnel)
            
        Returns:
            Le curseur contenant les résultats
            
        Raises:
            DatabaseException: Si une erreur SQL survient
        """
        cursor = None
        try:
            cursor = self._connection.get_cursor()
            cursor.execute(query, params)
            return cursor
        except mysql.connector.Error as e:
            raise DatabaseException(
                f"Échec de l'exécution de la requête: {str(e)}",
                original_error=e
            )
    
    def _execute_many(
        self, 
        query: str, 
        params_list: List[Tuple]
    ) -> int:
        """
        Exécute une requête SQL pour plusieurs ensembles de paramètres.
        
        Utile pour les insertions ou mises à jour en batch.
        Cette méthode gère les transactions (commit/rollback).
        
        Args:
            query: Requête SQL à exécuter
            params_list: Liste des tuples de paramètres
            
        Returns:
            Nombre de lignes affectées
            
        Raises:
            DatabaseException: Si une erreur SQL survient
        """
        cursor = None
        try:
            cursor = self._connection.get_cursor()
            cursor.executemany(query, params_list)
            self._connection.commit()
            return cursor.rowcount
        except mysql.connector.Error as e:
            self._connection.rollback()
            raise DatabaseException(
                f"Échec de l'exécution batch: {str(e)}",
                original_error=e
            )
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass
    
    def _fetch_one(
        self, 
        query: str, 
        params: Optional[Tuple] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Récupère un seul résultat de la requête.
        
        Gère automatiquement le curseur et retourne le résultat
        sous forme de dictionnaire.
        
        Args:
            query: Requête SQL SELECT
            params: Paramètres pour la requête (optionnel)
            
        Returns:
            Dictionnaire représentant l'enregistrement, ou None si pas trouvé
            
        Raises:
            DatabaseException: Si une erreur SQL survient
        """
        cursor = None
        try:
            cursor = self._connection.get_cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            
            if row is None:
                return None
            
            # Convertir en dictionnaire avec les noms de colonnes
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        except mysql.connector.Error as e:
            raise DatabaseException(
                f"Échec de la récupération d'un enregistrement: {str(e)}",
                original_error=e
            )
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass
    
    def _fetch_all(
        self, 
        query: str, 
        params: Optional[Tuple] = None
    ) -> List[Dict[str, Any]]:
        """
        Récupère tous les résultats de la requête.
        
        Gère automatiquement le curseur et retourne les résultats
        sous forme de liste de dictionnaires.
        
        Args:
            query: Requête SQL SELECT
            params: Paramètres pour la requête (optionnel)
            
        Returns:
            Liste de dictionnaires représentant les enregistrements
            
        Raises:
            DatabaseException: Si une erreur SQL survient
        """
        cursor = None
        try:
            cursor = self._connection.get_cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            if not rows:
                return []
            
            # Convertir en liste de dictionnaires avec les noms de colonnes
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except mysql.connector.Error as e:
            raise DatabaseException(
                f"Échec de la récupération des enregistrements: {str(e)}",
                original_error=e
            )
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass
    
    @abstractmethod
    def _get_table_name(self) -> str:
        """
        Retourne le nom de la table associée au repository.
        
        Méthode abstraite que les classes filles doivent implémenter.
        
        Returns:
            Nom de la table
        """
        pass
    
    @abstractmethod
    def _map_to_entity(self, data: Dict[str, Any]) -> Any:
        """
        Convertit un dictionnaire en entité métier.
        
        Méthode abstraite que les classes filles doivent implémenter.
        
        Args:
            data: Dictionnaire contenant les données
            
        Returns:
            Instance de l'entité métier
        """
        pass
