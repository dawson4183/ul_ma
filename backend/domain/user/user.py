"""
Entité: User
Représente un utilisateur dans le système.
Une entité a une identité propre (user_id) et peut changer d'état.
"""
from typing import Optional


class User:
    """
    Entité représentant un utilisateur.
    
    Un utilisateur contient:
    - Des informations d'identification (user_id, idul, email)
    - Des informations de sécurité (password_hash)
    - Un état (vérifié ou non, actif ou non)
    """
    
    def __init__(
        self,
        user_id: str,
        idul: str,
        email: str,
        password_hash: str,
        is_verified: bool = False,
        is_active: bool = True
    ):
        """
        Crée un utilisateur.
        
        Args:
            user_id: Identifiant unique de l'utilisateur (UUID)
            idul: IDUL de l'utilisateur (7 caractères)
            email: Adresse email de l'utilisateur
            password_hash: Hash du mot de passe
            is_verified: Si l'email a été vérifié
            is_active: Si le compte est actif
        
        Raises:
            ValueError: Si les données sont invalides
        """
        # Validation de l'IDUL (doit avoir exactement 7 caractères)
        if not idul or len(idul) != 7:
            raise ValueError("L'IDUL doit avoir exactement 7 caractères")
        
        # Validation de l'email (doit contenir '@')
        if not email or '@' not in email:
            raise ValueError("L'email doit être valide et contenir '@'")
        
        # Validation des champs obligatoires
        if not user_id or not user_id.strip():
            raise ValueError("L'ID utilisateur est requis")
        
        if not password_hash or not password_hash.strip():
            raise ValueError("Le hash du mot de passe est requis")
        
        # Assignation des attributs
        self._user_id = user_id
        self._idul = idul
        self._email = email.lower().strip()
        self._password_hash = password_hash
        self._is_verified = is_verified
        self._is_active = is_active
    
    # ===== Properties (Getters) =====
    
    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def idul(self) -> str:
        return self._idul
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def password_hash(self) -> str:
        return self._password_hash
    
    @property
    def is_verified(self) -> bool:
        return self._is_verified
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    # ===== Méthodes Métier =====
    
    def can_authenticate(self) -> bool:
        """
        Vérifie si l'utilisateur peut s'authentifier.
        
        Règle métier: Un utilisateur peut s'authentifier s'il est
        à la fois actif ET vérifié.
        
        Returns:
            True si l'utilisateur peut s'authentifier, False sinon
        """
        return self._is_active and self._is_verified
    
    def verify(self) -> None:
        """
        Marque l'utilisateur comme vérifié.
        
        Cette méthode est appelée après confirmation de l'email
        ou validation par un administrateur.
        """
        self._is_verified = True
    
    def deactivate(self) -> None:
        """
        Désactive le compte utilisateur.
        
        Un utilisateur désactivé ne peut plus s'authentifier.
        """
        self._is_active = False
    
    def activate(self) -> None:
        """
        Active le compte utilisateur.
        
        Réactive un compte précédemment désactivé.
        """
        self._is_active = True
    
    def __repr__(self) -> str:
        return (
            f"User(user_id={self._user_id}, "
            f"idul='{self._idul}', "
            f"email='{self._email}', "
            f"is_verified={self._is_verified}, "
            f"is_active={self._is_active})"
        )
