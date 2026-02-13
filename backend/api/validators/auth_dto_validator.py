"""
Validator: AuthDtoValidator
Valide les données entrantes pour l'API d'authentification.
"""
from typing import List, Dict, Any


class AuthDtoValidator:
    """
    Validateur pour les DTOs d'authentification.
    
    Valide les données côté serveur AVANT de les passer au service d'authentification.
    Double protection avec la validation côté client.
    """
    
    @staticmethod
    def validate_register(data: Dict[str, Any]) -> List[str]:
        """
        Valide les données d'inscription.
        
        Args:
            data: Dictionnaire contenant email, password, idul
            
        Returns:
            Liste d'erreurs (vide si aucune erreur)
            
        Raises:
            ValueError: Si la validation échoue, avec message descriptif
        """
        errors: List[str] = []
        
        # Validation email
        email = data.get('email', '')
        if not email:
            errors.append("L'email est requis")
        elif '@' not in email:
            errors.append("L'email doit contenir un '@'")
        
        # Validation password
        password = data.get('password', '')
        if not password:
            errors.append("Le mot de passe est requis")
        elif len(password) < 8:
            errors.append("Le mot de passe doit avoir au moins 8 caractères")
        
        # Validation idul
        idul = data.get('idul', '')
        if not idul:
            errors.append("L'idul est requis")
        elif len(idul) != 7:
            errors.append("L'idul doit avoir exactement 7 caractères")
        
        if errors:
            raise ValueError("; ".join(errors))
        
        return errors
    
    @staticmethod
    def validate_login(data: Dict[str, Any]) -> List[str]:
        """
        Valide les données de connexion.
        
        Args:
            data: Dictionnaire contenant email et password
            
        Returns:
            Liste d'erreurs (vide si aucune erreur)
            
        Raises:
            ValueError: Si la validation échoue, avec message descriptif
        """
        errors: List[str] = []
        
        # Validation email
        email = data.get('email', '')
        if not email:
            errors.append("L'email est requis")
        
        # Validation password
        password = data.get('password', '')
        if not password:
            errors.append("Le mot de passe est requis")
        
        if errors:
            raise ValueError("; ".join(errors))
        
        return errors
