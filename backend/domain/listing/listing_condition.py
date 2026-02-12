"""
Value Object / Enum: ListingCondition
Représente l'état d'un article mis en vente.
"""
from enum import Enum


class ListingCondition(str, Enum):
    """
    Énumération des conditions possibles pour un article.
    Hérite de str pour faciliter la sérialisation JSON.
    """
    
    NEUF = "Neuf"
    COMME_NEUF = "Comme neuf"
    BON_ETAT = "Bon état"
    USAGE = "Usagé"
    
    @classmethod
    def from_string(cls, condition_str: str) -> 'ListingCondition':
        """
        Crée un ListingCondition depuis une string.
        
        Args:
            condition_str: La condition en string
            
        Returns:
            L'énumération correspondante
            
        Raises:
            ValueError: Si la condition est invalide
        """
        try:
            return cls(condition_str)
        except ValueError:
            valid_conditions = [c.value for c in cls]
            raise ValueError(
                f"Condition invalide: '{condition_str}'. "
                f"Valeurs acceptées: {', '.join(valid_conditions)}"
            )
    
    def __str__(self) -> str:
        return self.value
