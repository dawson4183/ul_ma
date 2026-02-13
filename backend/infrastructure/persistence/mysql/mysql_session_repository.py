"""
Implémentation MySQL du SessionRepository.
Fournit une persistance des sessions dans MySQL.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime

from infrastructure.persistence.mysql.base_repository import BaseMySQLRepository
from domain.auth.session_repository import SessionRepository
from domain.auth.session import Session


class MySQLSessionRepository(BaseMySQLRepository, SessionRepository):
    """
    Repository MySQL pour les sessions.
    
    Implémente l'interface SessionRepository (Port) en utilisant
    MySQL comme système de stockage.
    
    Attributes:
        _connection: Instance de DatabaseConnection injectée
    """
    
    def _get_table_name(self) -> str:
        """
        Retourne le nom de la table des sessions.
        
        Returns:
            Nom de la table: 'sessions'
        """
        return "sessions"
    
    def _map_to_entity(self, data: Dict[str, Any]) -> Session:
        """
        Convertit un dictionnaire de données en entité Session.
        
        Args:
            data: Dictionnaire contenant les colonnes de la table sessions
            
        Returns:
            Instance de Session avec les données
        """
        used_at = None
        if data.get("used_at") is not None:
            if isinstance(data["used_at"], datetime):
                used_at = data["used_at"]
            else:
                # MySQL peut retourner des formats variés
                used_at = data["used_at"]
        
        expires_at = data["expires_at"]
        if not isinstance(expires_at, datetime):
            expires_at = datetime.fromisoformat(str(expires_at))
        
        return Session(
            session_id=data["session_id"],
            user_id=data["user_id"],
            token=data["token"],
            token_type=data["token_type"],
            expires_at=expires_at,
            used_at=used_at
        )
    
    def find_by_token(self, token: str) -> Optional[Session]:
        """
        Trouve une session par son token.
        
        Args:
            token: Token JWT de la session
            
        Returns:
            La session si trouvée, None sinon
        """
        query = f"SELECT * FROM {self._get_table_name()} WHERE token = %s"
        row = self._fetch_one(query, (token,))
        
        if row is None:
            return None
        
        return self._map_to_entity(row)
    
    def find_by_user_id(self, user_id: str) -> List[Session]:
        """
        Trouve toutes les sessions d'un utilisateur.
        
        Args:
            user_id: ID de l'utilisateur (UUID)
            
        Returns:
            Liste des sessions de l'utilisateur
        """
        query = f"SELECT * FROM {self._get_table_name()} WHERE user_id = %s"
        rows = self._fetch_all(query, (user_id,))
        
        return [self._map_to_entity(row) for row in rows]
    
    def save(self, session: Session) -> None:
        """
        Sauvegarde une session (création seule, pas de mise à jour).
        
        Pour les sessions, on fait toujours un INSERT car elles sont
        immuables - on ne modifie jamais une session existante.
        
        Args:
            session: La session à sauvegarder
            
        Raises:
            DatabaseException: Si la sauvegarde échoue
        """
        cursor = None
        try:
            cursor = self._connection.get_cursor()
            
            query = f"""
                INSERT INTO {self._get_table_name()} 
                (session_id, user_id, token, token_type, expires_at, used_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params: tuple = (
                session.session_id,
                session.user_id,
                session.token,
                session.token_type,
                session.expires_at,
                session.used_at
            )
            
            cursor.execute(query, params)
            self._connection.commit()
        except Exception:
            self._connection.rollback()
            raise
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass
    
    def mark_as_used(self, session_id: str) -> None:
        """
        Marque une session comme utilisée.
        
        Cette méthode met à jour la date d'utilisation de la session
        avec CURRENT_TIMESTAMP.
        
        Args:
            session_id: ID de la session à marquer (UUID)
            
        Raises:
            DatabaseException: Si la mise à jour échoue
        """
        cursor = None
        try:
            cursor = self._connection.get_cursor()
            
            query = f"""
                UPDATE {self._get_table_name()}
                SET used_at = CURRENT_TIMESTAMP
                WHERE session_id = %s
            """
            
            cursor.execute(query, (session_id,))
            self._connection.commit()
        except Exception:
            self._connection.rollback()
            raise
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass
    
    def delete(self, session_id: str) -> None:
        """
        Supprime une session par son ID.
        
        Args:
            session_id: ID de la session à supprimer (UUID)
            
        Raises:
            DatabaseException: Si la suppression échoue
        """
        cursor = None
        try:
            cursor = self._connection.get_cursor()
            
            query = f"DELETE FROM {self._get_table_name()} WHERE session_id = %s"
            
            cursor.execute(query, (session_id,))
            self._connection.commit()
        except Exception:
            self._connection.rollback()
            raise
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass
