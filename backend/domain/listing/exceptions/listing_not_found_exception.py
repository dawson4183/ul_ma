"""
Exception métier: ListingNotFoundException
Levée quand une annonce n'est pas trouvée.
"""


class ListingNotFoundException(RuntimeError):
    """
    Exception levée quand une annonce demandée n'existe pas.
    
    Cette exception fait partie de la couche Domaine et représente
    une règle métier: on ne peut pas opérer sur une annonce inexistante.
    """
    
    def __init__(self, listing_id: str = None):
        """
        Crée l'exception.
        
        Args:
            listing_id: ID de l'annonce non trouvée (optionnel)
        """
        if listing_id:
            message = f"Annonce non trouvée: {listing_id}"
        else:
            message = "Annonce non trouvée"
        
        super().__init__(message)
        self.listing_id = listing_id
