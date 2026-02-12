"""
Resource: ListingResource
Définit les endpoints REST pour les annonces (Couche API).
"""
from flask import Blueprint, request, jsonify
import logging
from application.listing.listing_service import ListingService
from application.listing.listing_assembler import ListingAssembler
from application.listing.dtos.listing_creation_dto import ListingCreationDto
from infrastructure.persistence.in_memory.in_memory_listing_repository import InMemoryListingRepository
from api.validators.listing_dto_validator import ListingDtoValidator
from api.exceptions.error_response import ErrorResponse

logger = logging.getLogger(__name__)

# Créer le Blueprint Flask
listing_bp = Blueprint('listings', __name__)

# ===== Initialisation des dépendances =====
# Pour cet exemple, on crée les instances directement
# En production, utilisez l'injection de dépendances (voir configuration.py)
_listing_repository = InMemoryListingRepository()
_listing_assembler = ListingAssembler()
_listing_service = ListingService(_listing_repository, _listing_assembler)
_listing_validator = ListingDtoValidator()


@listing_bp.route('/listings', methods=['POST'])
def create_listing():
    """
    Endpoint: POST /api/listings
    Crée une nouvelle annonce.
    
    Request Body (JSON):
    {
        "seller_id": "user-123",
        "title": "Calculatrice TI-84",
        "description": "En excellent état",
        "price": 85.00,
        "category": "electronics",
        "condition": "Comme neuf",
        "location": "Pavillon Adrien-Pouliot",
        "course_code": "MAT-1900",  # Optionnel
        "images": ["url1.jpg", "url2.jpg"]  # Optionnel
    }
    
    Response (201):
    {
        "listing_id": "uuid-generated",
        "seller_id": "user-123",
        "title": "Calculatrice TI-84",
        ...
    }
    
    Errors:
    - 400: Données invalides
    - 500: Erreur serveur
    """
    try:
        # 1. Extraire les données JSON
        data = request.get_json()
        
        if not data:
            error = ErrorResponse(
                error='INVALID_REQUEST',
                description='Le corps de la requête doit être au format JSON'
            )
            return jsonify(error.to_dict()), 400
        
        logger.info(f"Requête de création d'annonce reçue: {data.get('title', 'N/A')}")
        
        # 2. Valider les données
        _listing_validator.validate(data)
        
        # 3. Créer le DTO
        listing_dto = ListingCreationDto(**data)
        
        # 4. Appeler le service
        response_dto = _listing_service.create_listing(listing_dto)
        
        # 5. Retourner la réponse
        return jsonify(response_dto.to_dict()), 201
        
    except ValueError as e:
        # Erreurs de validation
        logger.warning(f"Validation échouée: {str(e)}")
        return jsonify(e.args[0] if e.args else {'error': 'VALIDATION_ERROR'}), 400
        
    except Exception as e:
        # Erreurs inattendues
        logger.error(f"Erreur lors de la création d'annonce: {str(e)}", exc_info=True)
        error = ErrorResponse(
            error='INTERNAL_SERVER_ERROR',
            description='Une erreur inattendue est survenue'
        )
        return jsonify(error.to_dict()), 500


@listing_bp.route('/listings/<listing_id>', methods=['GET'])
def get_listing(listing_id: str):
    """
    Endpoint: GET /api/listings/{id}
    Récupère une annonce par son ID.
    
    Response (200):
    {
        "listing_id": "...",
        "title": "...",
        ...
    }
    
    Errors:
    - 404: Annonce non trouvée
    """
    try:
        logger.info(f"Requête GET pour annonce: {listing_id}")
        
        response_dto = _listing_service.get_listing_by_id(listing_id)
        
        return jsonify(response_dto.to_dict()), 200
        
    except Exception as e:
        # Les exceptions sont gérées par les exception mappers
        raise


@listing_bp.route('/listings', methods=['GET'])
def get_all_listings():
    """
    Endpoint: GET /api/listings
    Récupère toutes les annonces.
    
    Query Parameters:
    - seller_id: Filtrer par vendeur
    - search: Recherche par mots-clés
    
    Response (200):
    [
        {"listing_id": "...", "title": "..."},
        ...
    ]
    """
    try:
        # Récupérer les query parameters
        seller_id = request.args.get('seller_id')
        search_query = request.args.get('search')
        
        # Appliquer les filtres
        if seller_id:
            logger.info(f"Filtrage par vendeur: {seller_id}")
            listings = _listing_service.get_listings_by_seller(seller_id)
        elif search_query:
            logger.info(f"Recherche: {search_query}")
            listings = _listing_service.search_listings(search_query)
        else:
            logger.info("Récupération de toutes les annonces")
            listings = _listing_service.get_all_listings()
        
        # Convertir en liste de dicts
        listings_data = [listing.to_dict() for listing in listings]
        
        return jsonify(listings_data), 200
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des annonces: {str(e)}", exc_info=True)
        error = ErrorResponse(
            error='INTERNAL_SERVER_ERROR',
            description='Erreur lors de la récupération des annonces'
        )
        return jsonify(error.to_dict()), 500


@listing_bp.route('/listings/<listing_id>', methods=['DELETE'])
def delete_listing(listing_id: str):
    """
    Endpoint: DELETE /api/listings/{id}
    Supprime une annonce.
    
    Headers:
    - X-User-Id: ID de l'utilisateur (simplifié pour l'exemple)
    
    Response (204): Pas de contenu
    
    Errors:
    - 401: Non authentifié
    - 403: Non autorisé
    - 404: Annonce non trouvée
    """
    try:
        # Pour cet exemple, on récupère l'user_id depuis un header
        # En production, utiliser un token JWT
        user_id = request.headers.get('X-User-Id')
        
        if not user_id:
            error = ErrorResponse(
                error='UNAUTHORIZED',
                description='Authentification requise'
            )
            return jsonify(error.to_dict()), 401
        
        logger.info(f"Suppression annonce {listing_id} par user {user_id}")
        
        _listing_service.delete_listing(listing_id, user_id)
        
        return '', 204  # No Content
        
    except Exception as e:
        # Les exceptions sont gérées par les exception mappers
        raise


# Route de test pour vérifier que le module est chargé
@listing_bp.route('/listings/health', methods=['GET'])
def health():
    """Endpoint de santé pour vérifier que le module fonctionne"""
    return jsonify({
        'status': 'healthy',
        'module': 'listings',
        'repository_type': type(_listing_repository).__name__,
        'listings_count': _listing_repository.count()
    }), 200
