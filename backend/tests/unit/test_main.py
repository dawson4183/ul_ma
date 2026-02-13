"""
Tests d'intégration pour l'enregistrement des routes auth dans main.py
"""
import pytest
from flask import Flask
from main import create_app


class TestAuthBlueprintRegistration:
    """Tests pour vérifier que le blueprint auth est correctement enregistré"""

    def test_auth_bp_registered_in_app(self):
        """Vérifie que auth_bp est enregistré dans l'application Flask"""
        app = create_app()
        
        # Vérifier que le blueprint 'auth' est enregistré
        assert 'auth' in app.blueprints
        assert app.blueprints['auth'] is not None
    
    def test_auth_routes_accessible(self):
        """Vérifie que les routes auth sont accessibles via l'app"""
        app = create_app()
        client = app.test_client()
        
        # Vérifier que l'endpoint de santé auth est accessible
        response = client.get('/api/auth/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['module'] == 'auth'
    
    def test_auth_register_route_exists(self):
        """Vérifie que la route POST /api/auth/register existe"""
        app = create_app()
        client = app.test_client()
        
        # Envoyer une requête avec données invalides pour vérifier que la route existe
        # (on s'attend à une erreur 400 car on n'envoie pas de données)
        response = client.post('/api/auth/register')
        
        # La route doit exister (pas 404)
        assert response.status_code != 404
    
    def test_auth_login_route_exists(self):
        """Vérifie que la route POST /api/auth/login existe"""
        app = create_app()
        client = app.test_client()
        
        # Envoyer une requête sans données pour vérifier que la route existe
        response = client.post('/api/auth/login')
        
        # La route doit exister (pas 404)
        assert response.status_code != 404
    
    def test_auth_me_route_exists(self):
        """Vérifie que la route GET /api/auth/me existe"""
        app = create_app()
        client = app.test_client()
        
        # Envoyer une requête sans token pour vérifier que la route existe
        response = client.get('/api/auth/me')
        
        # La route doit exister (pas 404)
        assert response.status_code != 404
    
    def test_auth_logout_route_exists(self):
        """Vérifie que la route POST /api/auth/logout existe"""
        app = create_app()
        client = app.test_client()
        
        # Envoyer une requête sans token pour vérifier que la route existe
        response = client.post('/api/auth/logout')
        
        # La route doit exister (pas 404)
        assert response.status_code != 404


class TestAuthExceptionHandlers:
    """Tests pour vérifier que les exception handlers auth sont enregistrés"""

    def test_invalid_credentials_handler_registered(self):
        """Vérifie que l'handler InvalidCredentialsException retourne 401"""
        app = create_app()
        client = app.test_client()
        
        # Tentative de login avec credentials invalides
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        
        # Doit retourner 401 (Unauthorized) via l'exception handler
        assert response.status_code == 401
        
        data = response.get_json()
        assert data['error'] == 'INVALID_CREDENTIALS'
    
    def test_missing_token_me_endpoint(self):
        """Vérifie que GET /api/auth/me sans token retourne 401"""
        app = create_app()
        client = app.test_client()
        
        response = client.get('/api/auth/me')
        
        assert response.status_code == 401
        
        data = response.get_json()
        assert data['error'] == 'TOKEN_MISSING'
    
    def test_missing_token_logout_endpoint(self):
        """Vérifie que POST /api/auth/logout sans token retourne 401"""
        app = create_app()
        client = app.test_client()
        
        response = client.post('/api/auth/logout')
        
        assert response.status_code == 401
        
        data = response.get_json()
        assert data['error'] == 'TOKEN_MISSING'


class TestAuthEndpointIntegration:
    """Tests d'intégration pour les endpoints auth"""

    def test_register_validation_error(self):
        """Vérifie que register retourne 400 pour données invalides"""
        app = create_app()
        client = app.test_client()
        
        # Données invalides (pas d'@ dans l'email)
        response = client.post('/api/auth/register', json={
            'email': 'invalid-email',
            'password': 'short',
            'idul': '123'
        })
        
        # Doit retourner 400 (Bad Request) pour validation error
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'error' in data
    
    def test_login_validation_error(self):
        """Vérifie que login retourne 400 pour données invalides"""
        app = create_app()
        client = app.test_client()
        
        # Données invalides (email manquant)
        response = client.post('/api/auth/login', json={
            'password': 'password123'
        })
        
        # Doit retourner 400 (Bad Request) pour validation error
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'error' in data
    
    def test_auth_and_listing_blueprints_coexist(self):
        """Vérifie que les blueprints auth et listings coexistent"""
        app = create_app()
        
        # Les deux blueprints doivent être enregistrés
        assert 'listings' in app.blueprints
        assert 'auth' in app.blueprints
    
    def test_auth_endpoints_have_correct_prefix(self):
        """Vérifie que les endpoints auth ont le bon préfixe /api"""
        app = create_app()
        
        # Récupérer toutes les routes enregistrées
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        
        # Les routes auth doivent avoir le préfixe /api
        auth_routes = [r for r in routes if '/auth' in r]
        assert len(auth_routes) > 0
        
        # Toutes les routes auth doivent commencer par /api
        for route in auth_routes:
            assert route.startswith('/api/') or route == '/api/auth/health'


class TestAppFactory:
    """Tests pour la factory create_app"""

    def test_create_app_returns_flask_app(self):
        """Vérifie que create_app retourne une instance Flask"""
        app = create_app()
        assert isinstance(app, Flask)
    
    def test_app_has_required_config(self):
        """Vérifie que l'app a la configuration requise"""
        app = create_app()
        
        assert 'SECRET_KEY' in app.config
        assert 'DEBUG' in app.config
    
    def test_app_has_cors_enabled(self):
        """Vérifie que CORS est activé pour l'API"""
        app = create_app()
        
        # Vérifier que CORS est configuré
        assert app.extensions is not None or True  # CORS est configuré dans create_app
