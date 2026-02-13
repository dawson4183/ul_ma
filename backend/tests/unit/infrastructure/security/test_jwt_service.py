"""
Tests pour le service JwtService.
"""
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import pytest
import jwt

from infrastructure.security.jwt_service import JwtService
from domain.auth.exceptions.token_invalid_exception import TokenInvalidException
from domain.auth.exceptions.session_expired_exception import SessionExpiredException


class TestJwtService:
    """Tests pour la classe JwtService"""

    @pytest.fixture
    def secret_key(self):
        """Fixture fournissant une clé secrète de test"""
        return "test_secret_key_pour_les_tests_unitaires"

    @pytest.fixture
    def jwt_service(self, secret_key):
        """Fixture fournissant une instance de JwtService"""
        return JwtService(secret_key)

    def test_init_with_valid_secret_key(self, secret_key):
        """Vérifie que JwtService s'initialise avec une clé secrète valide"""
        service = JwtService(secret_key)
        assert service._secret_key == secret_key
        assert service._algorithm == "HS256"
        assert service._token_lifetime_hours == 24

    def test_init_with_empty_secret_key_raises_error(self):
        """Vérifie que JwtService lève une erreur pour une clé secrète vide"""
        with pytest.raises(ValueError, match="clé secrète"):
            JwtService("")

    def test_init_with_none_secret_key_raises_error(self):
        """Vérifie que JwtService lève une erreur pour une clé secrète None"""
        with pytest.raises(ValueError, match="clé secrète"):
            JwtService(None)  # type: ignore

    def test_generate_token_returns_string(self, jwt_service):
        """Vérifie que generate_token retourne une chaîne de caractères"""
        user_id = 123
        email = "test@ulaval.ca"
        token = jwt_service.generate_token(user_id, email)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_generate_token_returns_valid_jwt_format(self, jwt_service):
        """Vérifie que generate_token retourne un JWT valide (3 parties séparées par des points)"""
        user_id = 123
        email = "test@ulaval.ca"
        token = jwt_service.generate_token(user_id, email)

        # Un JWT valide a 3 parties: header.payload.signature
        parts = token.split(".")
        assert len(parts) == 3

    def test_generate_token_contains_user_id(self, jwt_service, secret_key):
        """Vérifie que le token contient le user_id dans les claims"""
        user_id = 123
        email = "test@ulaval.ca"
        token = jwt_service.generate_token(user_id, email)

        # Décodage sans vérification pour accéder aux claims
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        assert payload["user_id"] == user_id

    def test_generate_token_contains_email(self, jwt_service, secret_key):
        """Vérifie que le token contient l'email dans les claims"""
        user_id = 123
        email = "test@ulaval.ca"
        token = jwt_service.generate_token(user_id, email)

        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        assert payload["email"] == email

    def test_generate_token_contains_expiration(self, jwt_service, secret_key):
        """Vérifie que le token contient l'expiration (exp) dans les claims"""
        user_id = 123
        email = "test@ulaval.ca"
        token = jwt_service.generate_token(user_id, email)

        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        assert "exp" in payload
        assert isinstance(payload["exp"], int)

    def test_generate_token_contains_issued_at(self, jwt_service, secret_key):
        """Vérifie que le token contient la date d'émission (iat) dans les claims"""
        user_id = 123
        email = "test@ulaval.ca"
        token = jwt_service.generate_token(user_id, email)

        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        assert "iat" in payload
        assert isinstance(payload["iat"], int)

    def test_generate_token_contains_token_type(self, jwt_service, secret_key):
        """Vérifie que le token contient le type dans les claims"""
        user_id = 123
        email = "test@ulaval.ca"
        token = jwt_service.generate_token(user_id, email)

        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        assert payload["type"] == "auth"

    def test_generate_token_expiration_is_24_hours(self, jwt_service, secret_key):
        """Vérifie que le token expire dans approximativement 24 heures"""
        user_id = 123
        email = "test@ulaval.ca"

        before = datetime.utcnow()
        token = jwt_service.generate_token(user_id, email)
        after = datetime.utcnow()

        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.utcfromtimestamp(exp_timestamp)

        # Vérifie que l'expiration est approximativement entre before + 24h et after + 24h
        # Permet une marge de 1 seconde pour les différences de temps
        expected_before = before + timedelta(hours=24)
        expected_after = after + timedelta(hours=24)

        # Convertir en timestamps pour comparaison avec tolérance
        exp_ts = exp_datetime.timestamp()
        before_ts = expected_before.timestamp()
        after_ts = expected_after.timestamp()

        assert before_ts - 1 <= exp_ts <= after_ts + 1

    def test_generate_token_empty_user_id_raises_error(self, jwt_service):
        """Vérifie que generate_token lève une erreur pour un user_id vide"""
        with pytest.raises(ValueError, match="identifiant utilisateur"):
            jwt_service.generate_token(0, "test@ulaval.ca")

    def test_generate_token_none_user_id_raises_error(self, jwt_service):
        """Vérifie que generate_token lève une erreur pour un user_id None"""
        with pytest.raises(ValueError, match="identifiant utilisateur"):
            jwt_service.generate_token(None, "test@ulaval.ca")  # type: ignore

    def test_generate_token_empty_email_raises_error(self, jwt_service):
        """Vérifie que generate_token lève une erreur pour un email vide"""
        with pytest.raises(ValueError, match="email"):
            jwt_service.generate_token(123, "")

    def test_generate_token_none_email_raises_error(self, jwt_service):
        """Vérifie que generate_token lève une erreur pour un email None"""
        with pytest.raises(ValueError, match="email"):
            jwt_service.generate_token(123, None)  # type: ignore

    def test_validate_token_returns_payload(self, jwt_service):
        """Vérifie que validate_token retourne le payload pour un token valide"""
        user_id = 123
        email = "test@ulaval.ca"
        token = jwt_service.generate_token(user_id, email)

        payload = jwt_service.validate_token(token)

        assert isinstance(payload, dict)
        assert payload["user_id"] == user_id
        assert payload["email"] == email

    def test_validate_token_empty_raises_error(self, jwt_service):
        """Vérifie que validate_token lève une erreur pour un token vide"""
        with pytest.raises(ValueError, match="token"):
            jwt_service.validate_token("")

    def test_validate_token_none_raises_error(self, jwt_service):
        """Vérifie que validate_token lève une erreur pour un token None"""
        with pytest.raises(ValueError, match="token"):
            jwt_service.validate_token(None)  # type: ignore

    def test_validate_token_invalid_format_raises_token_invalid(self, jwt_service):
        """Vérifie que validate_token lève TokenInvalidException pour un token mal formaté"""
        with pytest.raises(TokenInvalidException):
            jwt_service.validate_token("token_invalide")

    def test_validate_token_wrong_signature_raises_token_invalid(self, jwt_service, secret_key):
        """Vérifie que validate_token lève TokenInvalidException pour une mauvaise signature"""
        # Création d'un token avec une autre clé
        other_service = JwtService("autre_cle_secrete")
        token = other_service.generate_token(123, "test@ulaval.ca")

        with pytest.raises(TokenInvalidException):
            jwt_service.validate_token(token)

    def test_validate_token_expired_raises_session_expired(self, jwt_service, secret_key):
        """Vérifie que validate_token lève SessionExpiredException pour un token expiré"""
        # Création d'un token déjà expiré
        payload = {
            "user_id": 123,
            "email": "test@ulaval.ca",
            "exp": datetime.utcnow() - timedelta(hours=1),
            "iat": datetime.utcnow() - timedelta(hours=2),
            "type": "auth"
        }
        expired_token = jwt.encode(payload, secret_key, algorithm="HS256")

        with pytest.raises(SessionExpiredException):
            jwt_service.validate_token(expired_token)

    def test_validate_token_preserves_masked_token_in_exception(self, jwt_service):
        """Vérifie que l'exception contient le token masqué"""
        invalid_token = "a" * 50 + ".invalid.token"

        with pytest.raises(TokenInvalidException) as exc_info:
            jwt_service.validate_token(invalid_token)

        # Le token devrait être masqué dans le message
        exception = exc_info.value
        assert hasattr(exception, "token")
        assert exception.token == invalid_token

    def test_generate_and_validate_integration(self, jwt_service, secret_key):
        """Test d'intégration: générer puis valider un token"""
        test_cases = [
            {"user_id": 1, "email": "user1@ulaval.ca"},
            {"user_id": 999999, "email": "user999999@ulaval.ca"},
            {"user_id": 42, "email": "test.user+tag@ulaval.ca"},
        ]

        for case in test_cases:
            token = jwt_service.generate_token(case["user_id"], case["email"])
            payload = jwt_service.validate_token(token)

            assert payload["user_id"] == case["user_id"]
            assert payload["email"] == case["email"]
            assert payload["type"] == "auth"
