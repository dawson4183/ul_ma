"""
Tests pour AuthDtoValidator.
"""
import pytest
from api.validators.auth_dto_validator import AuthDtoValidator


class TestAuthDtoValidator:
    """Tests pour le validateur d'authentification."""
    
    class TestValidateRegister:
        """Tests pour validate_register."""
        
        def test_valide_tous_les_champs(self):
            """Test avec données valides complètes."""
            data = {
                'email': 'test@ulaval.ca',
                'password': 'password123',
                'idul': 'abc1234'
            }
            
            errors = AuthDtoValidator.validate_register(data)
            
            assert errors == []
        
        def test_email_manquant(self):
            """Test avec email manquant."""
            data = {
                'password': 'password123',
                'idul': 'abc1234'
            }
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_register(data)
            
            assert "L'email est requis" in str(exc_info.value)
        
        def test_email_vide(self):
            """Test avec email vide."""
            data = {
                'email': '',
                'password': 'password123',
                'idul': 'abc1234'
            }
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_register(data)
            
            assert "L'email est requis" in str(exc_info.value)
        
        def test_email_sans_arobase(self):
            """Test avec email sans @."""
            data = {
                'email': 'testulaval.ca',
                'password': 'password123',
                'idul': 'abc1234'
            }
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_register(data)
            
            assert "L'email doit contenir un '@'" in str(exc_info.value)
        
        def test_password_manquant(self):
            """Test avec password manquant."""
            data = {
                'email': 'test@ulaval.ca',
                'idul': 'abc1234'
            }
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_register(data)
            
            assert "Le mot de passe est requis" in str(exc_info.value)
        
        def test_password_vide(self):
            """Test avec password vide."""
            data = {
                'email': 'test@ulaval.ca',
                'password': '',
                'idul': 'abc1234'
            }
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_register(data)
            
            assert "Le mot de passe est requis" in str(exc_info.value)
        
        def test_password_trop_court(self):
            """Test avec password de 7 caractères (min 8 requis)."""
            data = {
                'email': 'test@ulaval.ca',
                'password': 'short12',
                'idul': 'abc1234'
            }
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_register(data)
            
            assert "au moins 8 caractères" in str(exc_info.value)
        
        def test_password_exactement_8_caracteres(self):
            """Test avec password de exactement 8 caractères."""
            data = {
                'email': 'test@ulaval.ca',
                'password': 'exactly8',
                'idul': 'abc1234'
            }
            
            errors = AuthDtoValidator.validate_register(data)
            
            assert errors == []
        
        def test_idul_manquant(self):
            """Test avec idul manquant."""
            data = {
                'email': 'test@ulaval.ca',
                'password': 'password123'
            }
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_register(data)
            
            assert "L'idul est requis" in str(exc_info.value)
        
        def test_idul_vide(self):
            """Test avec idul vide."""
            data = {
                'email': 'test@ulaval.ca',
                'password': 'password123',
                'idul': ''
            }
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_register(data)
            
            assert "L'idul est requis" in str(exc_info.value)
        
        def test_idul_trop_court(self):
            """Test avec idul de 6 caractères (exactement 7 requis)."""
            data = {
                'email': 'test@ulaval.ca',
                'password': 'password123',
                'idul': 'abc123'
            }
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_register(data)
            
            assert "exactement 7 caractères" in str(exc_info.value)
        
        def test_idul_trop_long(self):
            """Test avec idul de 8 caractères (exactement 7 requis)."""
            data = {
                'email': 'test@ulaval.ca',
                'password': 'password123',
                'idul': 'abc12345'
            }
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_register(data)
            
            assert "exactement 7 caractères" in str(exc_info.value)
        
        def test_idul_exactement_7_caracteres(self):
            """Test avec idul de exactement 7 caractères."""
            data = {
                'email': 'test@ulaval.ca',
                'password': 'password123',
                'idul': 'abcdefg'
            }
            
            errors = AuthDtoValidator.validate_register(data)
            
            assert errors == []
        
        def test_plusieurs_erreurs(self):
            """Test avec plusieurs erreurs de validation."""
            data = {
                'email': 'invalid',
                'password': 'short',
                'idul': 'ab'
            }
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_register(data)
            
            error_msg = str(exc_info.value)
            assert "L'email doit contenir un '@'" in error_msg
            assert "au moins 8 caractères" in error_msg
            assert "exactement 7 caractères" in error_msg
    
    class TestValidateLogin:
        """Tests pour validate_login."""
        
        def test_valide_tous_les_champs(self):
            """Test avec données valides complètes."""
            data = {
                'email': 'test@ulaval.ca',
                'password': 'password123'
            }
            
            errors = AuthDtoValidator.validate_login(data)
            
            assert errors == []
        
        def test_email_manquant(self):
            """Test avec email manquant."""
            data = {
                'password': 'password123'
            }
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_login(data)
            
            assert "L'email est requis" in str(exc_info.value)
        
        def test_email_vide(self):
            """Test avec email vide."""
            data = {
                'email': '',
                'password': 'password123'
            }
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_login(data)
            
            assert "L'email est requis" in str(exc_info.value)
        
        def test_password_manquant(self):
            """Test avec password manquant."""
            data = {
                'email': 'test@ulaval.ca'
            }
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_login(data)
            
            assert "Le mot de passe est requis" in str(exc_info.value)
        
        def test_password_vide(self):
            """Test avec password vide."""
            data = {
                'email': 'test@ulaval.ca',
                'password': ''
            }
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_login(data)
            
            assert "Le mot de passe est requis" in str(exc_info.value)
        
        def test_les_deux_champs_manquants(self):
            """Test avec email et password manquants."""
            data = {}
            
            with pytest.raises(ValueError) as exc_info:
                AuthDtoValidator.validate_login(data)
            
            error_msg = str(exc_info.value)
            assert "L'email est requis" in error_msg
            assert "Le mot de passe est requis" in error_msg
