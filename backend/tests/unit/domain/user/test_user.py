"""
Tests pour l'entité User.
"""
import pytest
from domain.user.user import User


class TestUser:
    """Tests pour la classe User"""
    
    @pytest.fixture
    def valid_user_data(self):
        """Fixture fournissant des données utilisateur valides"""
        return {
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "idul": "ABCDE12",
            "email": "test@ulaval.ca",
            "password_hash": "$2b$12$abcdefghijklmnopqrstuv",
            "is_verified": False,
            "is_active": True
        }
    
    @pytest.fixture
    def verified_user(self, valid_user_data):
        """Fixture fournissant un utilisateur vérifié"""
        data = valid_user_data.copy()
        data["is_verified"] = True
        return User(**data)
    
    def test_create_user_success(self, valid_user_data):
        """Vérifie qu'on peut créer un utilisateur avec des données valides"""
        user = User(**valid_user_data)
        
        assert user.user_id == valid_user_data["user_id"]
        assert user.idul == valid_user_data["idul"]
        assert user.email == "test@ulaval.ca"
        assert user.password_hash == valid_user_data["password_hash"]
        assert user.is_verified is False
        assert user.is_active is True
    
    def test_create_user_with_verified_email(self, valid_user_data):
        """Vérifie qu'on peut créer un utilisateur déjà vérifié"""
        data = valid_user_data.copy()
        data["is_verified"] = True
        user = User(**data)
        
        assert user.is_verified is True
        assert user.can_authenticate() is True
    
    def test_create_user_inactive(self, valid_user_data):
        """Vérifie qu'on peut créer un utilisateur inactif"""
        data = valid_user_data.copy()
        data["is_active"] = False
        user = User(**data)
        
        assert user.is_active is False
        assert user.can_authenticate() is False
    
    def test_idul_exactly_7_characters(self, valid_user_data):
        """Vérifie qu'un IDUL de exactement 7 caractères est accepté"""
        data = valid_user_data.copy()
        data["idul"] = "ABCDE12"
        user = User(**data)
        
        assert user.idul == "ABCDE12"
    
    def test_idul_less_than_7_characters_raises_error(self, valid_user_data):
        """Vérifie qu'un IDUL trop court lève une erreur"""
        data = valid_user_data.copy()
        data["idul"] = "ABC123"
        
        with pytest.raises(ValueError, match="L'IDUL doit avoir exactement 7 caractères"):
            User(**data)
    
    def test_idul_more_than_7_characters_raises_error(self, valid_user_data):
        """Vérifie qu'un IDUL trop long lève une erreur"""
        data = valid_user_data.copy()
        data["idul"] = "ABCDE123"
        
        with pytest.raises(ValueError, match="L'IDUL doit avoir exactement 7 caractères"):
            User(**data)
    
    def test_idul_empty_raises_error(self, valid_user_data):
        """Vérifie qu'un IDUL vide lève une erreur"""
        data = valid_user_data.copy()
        data["idul"] = ""
        
        with pytest.raises(ValueError, match="L'IDUL doit avoir exactement 7 caractères"):
            User(**data)
    
    def test_email_with_at_symbol(self, valid_user_data):
        """Vérifie qu'un email avec @ est accepté"""
        data = valid_user_data.copy()
        data["email"] = "user@example.com"
        user = User(**data)
        
        assert user.email == "user@example.com"
    
    def test_email_without_at_raises_error(self, valid_user_data):
        """Vérifie qu'un email sans @ lève une erreur"""
        data = valid_user_data.copy()
        data["email"] = "invalid-email"
        
        with pytest.raises(ValueError, match="L'email doit être valide et contenir '@'"):
            User(**data)
    
    def test_email_empty_raises_error(self, valid_user_data):
        """Vérifie qu'un email vide lève une erreur"""
        data = valid_user_data.copy()
        data["email"] = ""
        
        with pytest.raises(ValueError, match="L'email doit être valide et contenir '@'"):
            User(**data)
    
    def test_email_is_normalized_to_lowercase(self, valid_user_data):
        """Vérifie que l'email est normalisé en minuscules"""
        data = valid_user_data.copy()
        data["email"] = "Test.User@ULAVAL.CA"
        user = User(**data)
        
        assert user.email == "test.user@ulaval.ca"
    
    def test_empty_user_id_raises_error(self, valid_user_data):
        """Vérifie qu'un user_id vide lève une erreur"""
        data = valid_user_data.copy()
        data["user_id"] = ""
        
        with pytest.raises(ValueError, match="L'ID utilisateur est requis"):
            User(**data)
    
    def test_whitespace_user_id_raises_error(self, valid_user_data):
        """Vérifie qu'un user_id avec espaces lève une erreur"""
        data = valid_user_data.copy()
        data["user_id"] = "   "
        
        with pytest.raises(ValueError, match="L'ID utilisateur est requis"):
            User(**data)
    
    def test_empty_password_hash_raises_error(self, valid_user_data):
        """Vérifie qu'un password_hash vide lève une erreur"""
        data = valid_user_data.copy()
        data["password_hash"] = ""
        
        with pytest.raises(ValueError, match="Le hash du mot de passe est requis"):
            User(**data)
    
    def test_whitespace_password_hash_raises_error(self, valid_user_data):
        """Vérifie qu'un password_hash avec espaces lève une erreur"""
        data = valid_user_data.copy()
        data["password_hash"] = "   "
        
        with pytest.raises(ValueError, match="Le hash du mot de passe est requis"):
            User(**data)
    
    def test_can_authenticate_when_active_and_verified(self, verified_user):
        """Vérifie qu'un utilisateur actif et vérifié peut s'authentifier"""
        assert verified_user.is_active is True
        assert verified_user.is_verified is True
        assert verified_user.can_authenticate() is True
    
    def test_cannot_authenticate_when_not_verified(self, valid_user_data):
        """Vérifie qu'un utilisateur non vérifié ne peut pas s'authentifier"""
        data = valid_user_data.copy()
        data["is_verified"] = False
        data["is_active"] = True
        user = User(**data)
        
        assert user.can_authenticate() is False
    
    def test_cannot_authenticate_when_inactive(self, valid_user_data):
        """Vérifie qu'un utilisateur inactif ne peut pas s'authentifier"""
        data = valid_user_data.copy()
        data["is_verified"] = True
        data["is_active"] = False
        user = User(**data)
        
        assert user.can_authenticate() is False
    
    def test_cannot_authenticate_when_both_inactive_and_not_verified(self, valid_user_data):
        """Vérifie qu'un utilisateur inactif et non vérifié ne peut pas s'authentifier"""
        data = valid_user_data.copy()
        data["is_verified"] = False
        data["is_active"] = False
        user = User(**data)
        
        assert user.can_authenticate() is False
    
    def test_verify_updates_is_verified(self, valid_user_data):
        """Vérifie que verify() met à jour is_verified à True"""
        data = valid_user_data.copy()
        data["is_verified"] = False
        user = User(**data)
        
        user.verify()
        
        assert user.is_verified is True
    
    def test_verify_on_already_verified_user(self, verified_user):
        """Vérifie que verify() sur un utilisateur déjà vérifié reste True"""
        assert verified_user.is_verified is True
        
        verified_user.verify()
        
        assert verified_user.is_verified is True
    
    def test_deactivate_updates_is_active(self, verified_user):
        """Vérifie que deactivate() met à jour is_active à False"""
        assert verified_user.is_active is True
        
        verified_user.deactivate()
        
        assert verified_user.is_active is False
        assert verified_user.can_authenticate() is False
    
    def test_deactivate_on_already_inactive_user(self, valid_user_data):
        """Vérifie que deactivate() sur un utilisateur déjà inactif reste False"""
        data = valid_user_data.copy()
        data["is_active"] = False
        user = User(**data)
        
        user.deactivate()
        
        assert user.is_active is False
    
    def test_activate_updates_is_active(self, valid_user_data):
        """Vérifie que activate() met à jour is_active à True"""
        data = valid_user_data.copy()
        data["is_active"] = False
        user = User(**data)
        
        user.activate()
        
        assert user.is_active is True
    
    def test_activate_on_already_active_user(self, verified_user):
        """Vérifie que activate() sur un utilisateur déjà actif reste True"""
        assert verified_user.is_active is True
        
        verified_user.activate()
        
        assert verified_user.is_active is True
    
    def test_repr_output(self, verified_user):
        """Vérifie le format de __repr__"""
        repr_str = repr(verified_user)
        
        assert "User" in repr_str
        assert verified_user.user_id in repr_str
        assert verified_user.idul in repr_str
        assert verified_user.email in repr_str
