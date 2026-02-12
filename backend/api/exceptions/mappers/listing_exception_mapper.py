"""
Exception Mapper: Convertit les exceptions métier en réponses HTTP
"""
from flask import jsonify
from domain.listing.exceptions.listing_not_found_exception import ListingNotFoundException
from api.exceptions.error_response import ErrorResponse


def register_listing_exception_handlers(app):
    """
    Enregistre les gestionnaires d'exceptions pour les annonces.
    
    Cette fonction doit être appelée dans main.py pour activer
    la conversion automatique des exceptions en réponses HTTP.
    
    Args:
        app: Instance Flask
    """
    
    @app.errorhandler(ListingNotFoundException)
    def handle_listing_not_found(error):
        """
        Convertit ListingNotFoundException en réponse HTTP 404.
        
        Args:
            error: L'exception levée
            
        Returns:
            Réponse JSON avec status 404
        """
        response = ErrorResponse(
            error='LISTING_NOT_FOUND',
            description=str(error)
        )
        return jsonify(response.to_dict()), 404
    
    @app.errorhandler(PermissionError)
    def handle_permission_error(error):
        """
        Convertit PermissionError en réponse HTTP 403.
        
        Args:
            error: L'exception levée
            
        Returns:
            Réponse JSON avec status 403
        """
        response = ErrorResponse(
            error='PERMISSION_DENIED',
            description=str(error)
        )
        return jsonify(response.to_dict()), 403
    
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        """
        Convertit ValueError en réponse HTTP 400.
        Gère les erreurs de validation.
        
        Args:
            error: L'exception levée
            
        Returns:
            Réponse JSON avec status 400
        """
        # Si l'erreur contient déjà un ErrorResponse (du validator)
        error_message = str(error)
        
        # Essayer de parser comme dict (venant du validator)
        try:
            import ast
            error_dict = ast.literal_eval(error_message)
            if isinstance(error_dict, dict) and 'error' in error_dict:
                return jsonify(error_dict), 400
        except:
            pass
        
        # Sinon, créer une ErrorResponse générique
        response = ErrorResponse(
            error='INVALID_INPUT',
            description=error_message
        )
        return jsonify(response.to_dict()), 400
