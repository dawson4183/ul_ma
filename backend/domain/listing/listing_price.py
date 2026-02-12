"""
Value Object: ListingPrice
Encapsule la logique de validation du prix d'une annonce.
Un Value Object est immuable et n'a pas d'identité propre.
"""


class ListingPrice:
    """
    Value Object représentant le prix d'une annonce.
    
    Règles métier:
    - Le prix doit être un nombre positif
    - Le prix doit être > 0 (pas d'annonces gratuites pour ce projet)
    - Le prix peut avoir jusqu'à 2 décimales
    """
    
    def __init__(self, amount: float):
        """
        Crée un ListingPrice.
        
        Args:
            amount: Le montant du prix en dollars canadiens
            
        Raises:
            ValueError: Si le prix est invalide
        """
        if not isinstance(amount, (int, float)):
            raise ValueError("Le prix doit être un nombre")
        
        if amount <= 0:
            raise ValueError("Le prix doit être supérieur à 0$")
        
        if amount > 999999:
            raise ValueError("Le prix ne peut pas dépasser 999,999$")
        
        # Arrondir à 2 décimales
        self._amount = round(float(amount), 2)
    
    @property
    def amount(self) -> float:
        """Retourne le montant du prix"""
        return self._amount
    
    def __str__(self) -> str:
        """Représentation en string"""
        return f"{self._amount:.2f}$"
    
    def __eq__(self, other) -> bool:
        """Égalité basée sur la valeur, pas sur l'identité"""
        if not isinstance(other, ListingPrice):
            return False
        return self._amount == other._amount
    
    def __hash__(self) -> int:
        """Hash pour utilisation dans sets/dicts"""
        return hash(self._amount)
    
    def __repr__(self) -> str:
        return f"ListingPrice({self._amount})"
