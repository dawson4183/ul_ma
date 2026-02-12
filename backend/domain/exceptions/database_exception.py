"""
Exception métier: DatabaseException
Levée quand une erreur de base de données survient.
"""


class DatabaseException(RuntimeError):
    """
    Exception levée quand une opération de base de données échoue.
    
    Cette exception fait partie de la couche Domaine et représente
    une erreur technique lors de l'accès à la base de données.
    Elle encapsule les erreurs techniques pour les rendre exploitables
    par la couche application.
    """
    
    def __init__(self, message: str = None, original_error: Exception = None):
        """
        Crée l'exception.
        
        Args:
            message: Message décrivant l'erreur
            original_error: Exception originale technique (optionnel)
        """
        if message is None:
            message = "Erreur de base de données"
        
        super().__init__(message)
        self.original_error = original_error
