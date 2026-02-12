"""
Interface (Port) : SessionRepository
Définit le contrat pour la persistance des sessions.
Le Domaine définit l'interface, l'Infrastructure l'implémente.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.auth.session import Session


class SessionRepository(ABC):
    """
    Interface définissant les opérations de persistance pour les sessions.
    
    Cette interface est un PORT dans l'architecture hexagonale.
    Elle est définie dans le Domaine mais implémentée dans l'Infrastructure.
    
    Principe de l'inversion de dépendances (DIP) :
    - Le Domaine ne dépend PAS de l'Infrastructure
    - L'Infrastructure dépend du Domaine (implémente cette interface)
    """
    
    @abstractmethod
    def find_by_token(self, token: str) -> Optional[Session]:
        """
        Trouve une session par son token.
        
        Args:
            token: Token JWT de la session
            
        Returns:
            La session si trouvée, None sinon
        """
        pass
    
    @abstractmethod
    def find_by_user_id(self, user_id: str) -> List[Session]:
        """
        Trouve toutes les sessions d'un utilisateur.
        
        Args:
            user_id: ID de l'utilisateur (UUID)
            
        Returns:
            Liste des sessions de l'utilisateur
        """
        pass
    
    @abstractmethod
    def save(self, session: Session) -> None:
        """
        Sauvegarde une session (création ou mise à jour).
        
        Args:
            session: La session à sauvegarder
            
        Raises:
            RuntimeError: Si la sauvegarde échoue
        """
        pass
    
    @abstractmethod
    def delete(self, session_id: str) -> None:
        """
        Supprime une session par son ID.
        
        Args:
            session_id: ID de la session à supprimer (UUID)
            
        Raises:
            RuntimeError: Si la suppression échoue
        """
        pass
    
    @abstractmethod
    def mark_as_used(self, session_id: str) -> None:
        """
        Marque une session comme utilisée.
        
        Cette méthode met à jour la date d'utilisation de la session.
        Elle est appelée lors de la consommation du token.
        
        Args:
            session_id: ID de la session à marquer (UUID)
            
        Raises:
            RuntimeError: Si la mise à jour échoue
        """
        pass
