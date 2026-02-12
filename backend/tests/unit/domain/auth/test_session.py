"""
Tests pour l'entité Session.
"""
from datetime import datetime, timedelta
import pytest
from domain.auth.session import Session


class TestSession:
    """Tests pour la classe Session"""
    
    @pytest.fixture
    def valid_session_data(self):
        """Fixture fournissant des données de session valides"""
        return {
            "session_id": "123e4567-e89b-12d3-a456-426614174000",
            "user_id": "987e6543-e21b-45d3-c456-426614174999",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
            "token_type": Session.TOKEN_TYPE_AUTH,
            "expires_at": datetime.now() + timedelta(hours=24),
            "used_at": None
        }
    
    @pytest.fixture
    def valid_session(self, valid_session_data):
        """Fixture fournissant une session valide"""
        return Session(**valid_session_data)
    
    def test_create_session_success(self, valid_session_data):
        """Vérifie qu'on peut créer une session avec des données valides"""
        session = Session(**valid_session_data)
        
        assert session.session_id == valid_session_data["session_id"]
        assert session.user_id == valid_session_data["user_id"]
        assert session.token == valid_session_data["token"]
        assert session.token_type == valid_session_data["token_type"]
        assert session.expires_at == valid_session_data["expires_at"]
        assert session.used_at is None
    
    def test_create_session_with_auth_token_type(self, valid_session_data):
        """Vérifie qu'on peut créer une session avec le type 'auth'"""
        data = valid_session_data.copy()
        data["token_type"] = Session.TOKEN_TYPE_AUTH
        session = Session(**data)
        
        assert session.token_type == Session.TOKEN_TYPE_AUTH
    
    def test_create_session_with_email_verification_token_type(self, valid_session_data):
        """Vérifie qu'on peut créer une session avec le type 'email_verification'"""
        data = valid_session_data.copy()
        data["token_type"] = Session.TOKEN_TYPE_EMAIL_VERIFICATION
        session = Session(**data)
        
        assert session.token_type == Session.TOKEN_TYPE_EMAIL_VERIFICATION
    
    def test_create_session_with_password_reset_token_type(self, valid_session_data):
        """Vérifie qu'on peut créer une session avec le type 'password_reset'"""
        data = valid_session_data.copy()
        data["token_type"] = Session.TOKEN_TYPE_PASSWORD_RESET
        session = Session(**data)
        
        assert session.token_type == Session.TOKEN_TYPE_PASSWORD_RESET
    
    def test_create_session_with_used_at(self, valid_session_data):
        """Vérifie qu'on peut créer une session avec used_at défini"""
        data = valid_session_data.copy()
        data["used_at"] = datetime.now()
        session = Session(**data)
        
        assert session.used_at is not None
    
    def test_empty_session_id_raises_error(self, valid_session_data):
        """Vérifie qu'un session_id vide lève une erreur"""
        data = valid_session_data.copy()
        data["session_id"] = ""
        
        with pytest.raises(ValueError, match="L'ID de session est requis"):
            Session(**data)
    
    def test_whitespace_session_id_raises_error(self, valid_session_data):
        """Vérifie qu'un session_id avec espaces lève une erreur"""
        data = valid_session_data.copy()
        data["session_id"] = "   "
        
        with pytest.raises(ValueError, match="L'ID de session est requis"):
            Session(**data)
    
    def test_empty_user_id_raises_error(self, valid_session_data):
        """Vérifie qu'un user_id vide lève une erreur"""
        data = valid_session_data.copy()
        data["user_id"] = ""
        
        with pytest.raises(ValueError, match="L'ID utilisateur est requis"):
            Session(**data)
    
    def test_whitespace_user_id_raises_error(self, valid_session_data):
        """Vérifie qu'un user_id avec espaces lève une erreur"""
        data = valid_session_data.copy()
        data["user_id"] = "   "
        
        with pytest.raises(ValueError, match="L'ID utilisateur est requis"):
            Session(**data)
    
    def test_empty_token_raises_error(self, valid_session_data):
        """Vérifie qu'un token vide lève une erreur"""
        data = valid_session_data.copy()
        data["token"] = ""
        
        with pytest.raises(ValueError, match="Le token est requis"):
            Session(**data)
    
    def test_whitespace_token_raises_error(self, valid_session_data):
        """Vérifie qu'un token avec espaces lève une erreur"""
        data = valid_session_data.copy()
        data["token"] = "   "
        
        with pytest.raises(ValueError, match="Le token est requis"):
            Session(**data)
    
    def test_invalid_token_type_raises_error(self, valid_session_data):
        """Vérifie qu'un type de token invalide lève une erreur"""
        data = valid_session_data.copy()
        data["token_type"] = "invalid_type"
        
        with pytest.raises(ValueError, match="Le type de token doit être l'un de"):
            Session(**data)
    
    def test_empty_token_type_raises_error(self, valid_session_data):
        """Vérifie qu'un type de token vide lève une erreur"""
        data = valid_session_data.copy()
        data["token_type"] = ""
        
        with pytest.raises(ValueError, match="Le type de token doit être l'un de"):
            Session(**data)
    
    def test_non_datetime_expires_at_raises_error(self, valid_session_data):
        """Vérifie qu'une date d'expiration non-datetime lève une erreur"""
        data = valid_session_data.copy()
        data["expires_at"] = "not-a-datetime"
        
        with pytest.raises(ValueError, match="La date d'expiration doit être un datetime"):
            Session(**data)
    
    def test_non_datetime_used_at_raises_error(self, valid_session_data):
        """Vérifie qu'une date d'utilisation non-datetime lève une erreur"""
        data = valid_session_data.copy()
        data["used_at"] = "not-a-datetime"
        
        with pytest.raises(ValueError, match="La date d'utilisation doit être un datetime ou None"):
            Session(**data)
    
    def test_is_expired_when_future(self, valid_session_data):
        """Vérifie qu'une session avec date future n'est pas expirée"""
        data = valid_session_data.copy()
        data["expires_at"] = datetime.now() + timedelta(hours=1)
        session = Session(**data)
        
        assert session.is_expired() is False
    
    def test_is_expired_when_past(self, valid_session_data):
        """Vérifie qu'une session avec date passée est expirée"""
        data = valid_session_data.copy()
        data["expires_at"] = datetime.now() - timedelta(hours=1)
        session = Session(**data)
        
        assert session.is_expired() is True
    
    def test_is_used_when_used_at_is_none(self, valid_session_data):
        """Vérifie qu'une session sans used_at n'est pas marquée comme utilisée"""
        data = valid_session_data.copy()
        data["used_at"] = None
        session = Session(**data)
        
        assert session.is_used() is False
    
    def test_is_used_when_used_at_is_set(self, valid_session_data):
        """Vérifie qu'une session avec used_at est marquée comme utilisée"""
        data = valid_session_data.copy()
        data["used_at"] = datetime.now()
        session = Session(**data)
        
        assert session.is_used() is True
    
    def test_mark_as_used_updates_used_at(self, valid_session_data):
        """Vérifie que mark_as_used() met à jour used_at"""
        data = valid_session_data.copy()
        data["used_at"] = None
        session = Session(**data)
        
        assert session.used_at is None
        
        session.mark_as_used()
        
        assert session.used_at is not None
        assert session.is_used() is True
    
    def test_mark_as_used_sets_current_datetime(self, valid_session_data):
        """Vérifie que mark_as_used() définit la date/heure actuelle"""
        data = valid_session_data.copy()
        data["used_at"] = None
        session = Session(**data)
        
        before = datetime.now()
        session.mark_as_used()
        after = datetime.now()
        
        assert before <= session.used_at <= after
    
    def test_repr_output(self, valid_session):
        """Vérifie le format de __repr__"""
        repr_str = repr(valid_session)
        
        assert "Session" in repr_str
        assert valid_session.session_id in repr_str
        assert valid_session.user_id in repr_str
        assert valid_session.token_type in repr_str