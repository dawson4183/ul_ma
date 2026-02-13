"""
Implémentation MySQL du UserRepository.
Fournit une persistance des utilisateurs dans MySQL.
"""
from typing import Optional, Dict, Any

from infrastructure.persistence.mysql.base_repository import BaseMySQLRepository
from domain.user.user_repository import UserRepository
from domain.user.user import User


class MySQLUserRepository(BaseMySQLRepository, UserRepository):
    """
    Repository MySQL pour les utilisateurs.
    
    Implémente l'interface UserRepository (Port) en utilisant
    MySQL comme système de stockage.
    
    Attributes:
        _connection: Instance de DatabaseConnection injectée
    """
    
    def _get_table_name(self) -> str:
        """
        Retourne le nom de la table des utilisateurs.
        
        Returns:
            Nom de la table: 'users'
        """
        return "users"
    
    def _map_to_entity(self, data: Dict[str, Any]) -> User:
        """
        Convertit un dictionnaire de données en entité User.
        
        Args:
            data: Dictionnaire contenant les colonnes de la table users
            
        Returns:
            Instance de User avec les données
        """
        return User(
            user_id=data["user_id"],
            idul=data["idul"],
            email=data["email"],
            password_hash=data["password_hash"],
            is_verified=bool(data["is_verified"]),
            is_active=bool(data["is_active"])
        )
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        """
        Trouve un utilisateur par son ID.
        
        Args:
            user_id: ID de l'utilisateur (UUID)
            
        Returns:
            L'utilisateur si trouvé, None sinon
        """
        query = f"SELECT * FROM {self._get_table_name()} WHERE user_id = %s"
        row = self._fetch_one(query, (user_id,))
        
        if row is None:
            return None
        
        return self._map_to_entity(row)
    
    def find_by_email(self, email: str) -> Optional[User]:
        """
        Trouve un utilisateur par son email.
        
        La recherche est insensible à la casse.
        
        Args:
            email: Adresse email de l'utilisateur
            
        Returns:
            L'utilisateur si trouvé, None sinon
        """
        query = f"SELECT * FROM {self._get_table_name()} WHERE email = %s"
        row = self._fetch_one(query, (email.lower(),))
        
        if row is None:
            return None
        
        return self._map_to_entity(row)
    
    def find_by_idul(self, idul: str) -> Optional[User]:
        """
        Trouve un utilisateur par son IDUL.
        
        Args:
            idul: IDUL de l'utilisateur (7 caractères)
            
        Returns:
            L'utilisateur si trouvé, None sinon
        """
        query = f"SELECT * FROM {self._get_table_name()} WHERE idul = %s"
        row = self._fetch_one(query, (idul,))
        
        if row is None:
            return None
        
        return self._map_to_entity(row)
    
    def save(self, user: User) -> None:
        """
        Sauvegarde un utilisateur (création ou mise à jour).
        
        Si l'utilisateur existe déjà (user_id existe), fait un UPDATE.
        Sinon, fait un INSERT.
        
        Args:
            user: L'utilisateur à sauvegarder
            
        Raises:
            DatabaseException: Si la sauvegarde échoue
        """
        # Vérifie si l'utilisateur existe déjà
        existing = self.find_by_id(user.user_id)
        
        cursor = None
        try:
            cursor = self._connection.get_cursor()
            
            if existing is None:
                # INSERT - nouvel utilisateur
                query = f"""
                    INSERT INTO {self._get_table_name()} 
                    (user_id, idul, email, password_hash, is_verified, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                params: tuple = (
                    user.user_id,
                    user.idul,
                    user.email,
                    user.password_hash,
                    user.is_verified,
                    user.is_active
                )
            else:
                # UPDATE - utilisateur existant
                query = f"""
                    UPDATE {self._get_table_name()}
                    SET idul = %s, email = %s, password_hash = %s, 
                        is_verified = %s, is_active = %s
                    WHERE user_id = %s
                """
                params = (
                    user.idul,
                    user.email,
                    user.password_hash,
                    user.is_verified,
                    user.is_active,
                    user.user_id
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
    
    def exists_by_email(self, email: str) -> bool:
        """
        Vérifie si un utilisateur existe avec cet email.
        
        La vérification est insensible à la casse.
        
        Args:
            email: Adresse email à vérifier
            
        Returns:
            True si un utilisateur existe avec cet email, False sinon
        """
        query = f"SELECT 1 FROM {self._get_table_name()} WHERE email = %s LIMIT 1"
        row = self._fetch_one(query, (email.lower(),))
        
        return row is not None
