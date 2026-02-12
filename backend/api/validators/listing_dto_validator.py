"""
Validator: ListingDtoValidator
Valide les données entrantes pour la création d'une annonce.
"""
import re
from api.exceptions.error_response import ErrorResponse


class ListingDtoValidator:
    """
    Validateur pour les DTOs de création d'annonce.
    
    Valide les données côté serveur AVANT de les passer au service.
    Double protection avec la validation côté client JavaScript.
    """
    
    # Catégories valides (doit correspondre au frontend)
    VALID_CATEGORIES = [
        'books', 'electronics', 'housing', 'lab',
        'sports', 'clothing', 'other'
    ]
    
    # Conditions valides
    VALID_CONDITIONS = [
        'Neuf', 'Comme neuf', 'Bon état', 'Usagé'
    ]
    
    # Lieux campus valides
    VALID_LOCATIONS = [
        'Pavillon Adrien-Pouliot',
        'Pavillon Desjardins',
        'Pavillon Charles-De Koninck',
        'PEPS',
        'Bibliothèque',
        'Pavillon Alexandre-Vachon'
    ]
    
    @classmethod
    def validate(cls, data: dict) -> None:
        """
        Valide les données de création d'annonce.
        
        Args:
            data: Dictionnaire des données à valider
            
        Raises:
            ValueError: Si une donnée est invalide (avec ErrorResponse dans le message)
        """
        # Validation champs obligatoires
        cls._validate_required_field(data, 'seller_id')
        cls._validate_required_field(data, 'title')
        cls._validate_required_field(data, 'description')
        cls._validate_required_field(data, 'price')
        cls._validate_required_field(data, 'category')
        cls._validate_required_field(data, 'condition')
        cls._validate_required_field(data, 'location')
        
        # Validation titre
        title = data.get('title', '')
        if len(title) < 5:
            raise ValueError(
                ErrorResponse(
                    error='INVALID_TITLE',
                    description='Le titre doit contenir au moins 5 caractères',
                    field='title'
                ).to_dict()
            )
        
        if len(title) > 200:
            raise ValueError(
                ErrorResponse(
                    error='INVALID_TITLE',
                    description='Le titre ne peut pas dépasser 200 caractères',
                    field='title'
                ).to_dict()
            )
        
        # Validation description
        description = data.get('description', '')
        if len(description) < 10:
            raise ValueError(
                ErrorResponse(
                    error='INVALID_DESCRIPTION',
                    description='La description doit contenir au moins 10 caractères',
                    field='description'
                ).to_dict()
            )
        
        # Validation prix
        try:
            price = float(data.get('price', 0))
            if price <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError(
                ErrorResponse(
                    error='INVALID_PRICE',
                    description='Le prix doit être un nombre positif',
                    field='price'
                ).to_dict()
            )
        
        # Validation catégorie
        category = data.get('category', '')
        if category not in cls.VALID_CATEGORIES:
            raise ValueError(
                ErrorResponse(
                    error='INVALID_CATEGORY',
                    description=f'Catégorie invalide. Valeurs acceptées: {", ".join(cls.VALID_CATEGORIES)}',
                    field='category'
                ).to_dict()
            )
        
        # Validation condition
        condition = data.get('condition', '')
        if condition not in cls.VALID_CONDITIONS:
            raise ValueError(
                ErrorResponse(
                    error='INVALID_CONDITION',
                    description=f'Condition invalide. Valeurs acceptées: {", ".join(cls.VALID_CONDITIONS)}',
                    field='condition'
                ).to_dict()
            )
        
        # Validation location
        location = data.get('location', '')
        if location not in cls.VALID_LOCATIONS:
            raise ValueError(
                ErrorResponse(
                    error='INVALID_LOCATION',
                    description=f'Lieu invalide. Valeurs acceptées: {", ".join(cls.VALID_LOCATIONS)}',
                    field='location'
                ).to_dict()
            )
        
        # Validation course_code (optionnel mais format si présent)
        course_code = data.get('course_code')
        if course_code:
            if not cls._is_valid_course_code(course_code):
                raise ValueError(
                    ErrorResponse(
                        error='INVALID_COURSE_CODE',
                        description='Format invalide. Exemple: GLO-2005, MAT-1900',
                        field='course_code'
                    ).to_dict()
                )
        
        # Validation images (max 5)
        images = data.get('images', [])
        if images and len(images) > 5:
            raise ValueError(
                ErrorResponse(
                    error='TOO_MANY_IMAGES',
                    description='Maximum 5 images autorisées',
                    field='images'
                ).to_dict()
            )
    
    @staticmethod
    def _validate_required_field(data: dict, field_name: str) -> None:
        """
        Valide qu'un champ requis est présent et non vide.
        
        Args:
            data: Données à valider
            field_name: Nom du champ
            
        Raises:
            ValueError: Si le champ est manquant ou vide
        """
        if field_name not in data or not data[field_name]:
            raise ValueError(
                ErrorResponse(
                    error='MISSING_PARAMETER',
                    description=f'Le champ "{field_name}" est requis',
                    field=field_name
                ).to_dict()
            )
    
    @staticmethod
    def _is_valid_course_code(course_code: str) -> bool:
        """
        Valide le format d'un code de cours ULaval.
        Format: 3-4 lettres - 4 chiffres (ex: GLO-2005, MAT-1900)
        
        Args:
            course_code: Code de cours à valider
            
        Returns:
            True si valide, False sinon
        """
        pattern = r'^[A-Z]{3,4}-\d{4}$'
        return bool(re.match(pattern, course_code.upper()))
