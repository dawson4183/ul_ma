"""
Interface (Port) : UserRepository
Définit le contrat pour la persistance des utilisateurs.
Le Domaine définit l'interface, l'Infrastructure l'implémente.
"""
from abc import ABC, abstractmethod
from typing import Optional
from domain.user.user import User


class UserRepository(ABC):
    """
    Interface définissant les opérations de persistance pour les utilisateurs.
    
    Cette interface est un PORT dans l'architecture hexagonale.
    Elle est définie dans le Domaine mais implémentée dans l'Infrastructure.
    
    Principe de l'inversion de dépendances (DIP) :
    - Le Domaine ne dépend PAS de l'Infrastructure
    - L'Infrastructure dépend du Domaine (implémente cette interface)
    """
    
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        """
        Trouve un utilisateur par son ID.
        
        Args:
            user_id: ID de l'utilisateur (UUID)
            
        Returns:
            L'utilisateur si trouvé, None sinon
        """
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """
        Trouve un utilisateur par son email.
        
        Args:
            email: Adresse email de l'utilisateur
            
        Returns:
            L'utilisateur si trouvé, None sinon
        """
        pass
    
    @abstractmethod
    def find_by_idul(self, idul: str) -> Optional[User]:
        """
        Trouve un utilisateur par son IDUL.
        
        Args:
            idul: IDUL de l'utilisateur (7 caractères)
            
        Returns:
            L'utilisateur si trouvé, None sinon
        """
        pass
    
    @abstractmethod
    def save(self, user: User) -> None:
        """
        Sauvegarde un utilisateur (création ou mise à jour).
        
        Args:
            user: L'utilisateur à sauvegarder
            
        Raises:
            RuntimeError: Si la sauvegarde échoue
        """
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """
        Vérifie si un utilisateur existe avec cet email.
        
        Args:
            email: Adresse email à vérifier
            
        Returns:
            True si un utilisateur existe avec cet email, False sinon
        """
        pass
