"""
Exception métier: InvalidPriceException
Levée quand le prix d'une annonce est invalide.
"""


class InvalidPriceException(ValueError):
    """
    Exception levée quand le prix d'une annonce ne respecte pas les règles métier.
    
    Exemples:
    - Prix négatif ou zéro
    - Prix trop élevé
    - Format invalide
    """
    
    def __init__(self, price_value, reason: str = "Prix invalide"):
        """
        Crée l'exception.
        
        Args:
            price_value: La valeur du prix invalide
            reason: Raison de l'invalidité
        """
        message = f"{reason}: {price_value}"
        super().__init__(message)
        self.price_value = price_value
        self.reason = reason
