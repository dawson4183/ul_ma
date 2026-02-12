"""
Point d'entrée principal de l'application Flask
"""
import os
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def create_app():
    """Factory pour créer l'application Flask"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('FLASK_ENV') == 'development'
    
    # CORS - Permettre les requêtes du frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": os.getenv('FRONTEND_URL', 'http://localhost:5173'),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Route de santé (health check)
    @app.route('/health', methods=['GET'])
    def health_check():
        return {
            'status': 'healthy',
            'service': 'ULavalMarket API',
            'version': '1.0.0'
        }, 200
    
    # Route racine
    @app.route('/', methods=['GET'])
    def index():
        return {
            'message': 'Bienvenue sur l\'API ULavalMarket',
            'documentation': '/api/docs',
            'health': '/health'
        }, 200
    
    logger.info("Application Flask initialisée avec succès")
    
    # Enregistrer les blueprints (resources)
    from api.listing_resource import listing_bp
    app.register_blueprint(listing_bp, url_prefix='/api')
    logger.info("Blueprint 'listings' enregistré")
    
    # Enregistrer les exception handlers
    from api.exceptions.mappers.listing_exception_mapper import register_listing_exception_handlers
    register_listing_exception_handlers(app)
    logger.info("Exception handlers enregistrés")
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    # Récupérer le port depuis les variables d'environnement
    port = int(os.getenv('PORT', 5000))
    
    logger.info(f"Démarrage du serveur sur le port {port}...")
    logger.info(f"Frontend autorisé: {os.getenv('FRONTEND_URL', 'http://localhost:5173')}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG']
    )
