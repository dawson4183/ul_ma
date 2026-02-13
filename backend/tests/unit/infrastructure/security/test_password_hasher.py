"""
Tests pour le service PasswordHasher.
"""
import pytest
from unittest.mock import patch, MagicMock

from infrastructure.security.password_hasher import PasswordHasher


class TestPasswordHasher:
    """Tests pour la classe PasswordHasher"""

    @pytest.fixture
    def password_hasher(self):
        """Fixture fournissant une instance de PasswordHasher"""
        return PasswordHasher()

    def test_hash_password_returns_string(self, password_hasher):
        """Vérifie que hash_password retourne une chaîne de caractères"""
        password = "mon_mot_de_passe"
        hashed = password_hasher.hash_password(password)

        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hash_password_returns_bcrypt_hash(self, password_hasher):
        """Vérifie que hash_password retourne un hash bcrypt valide"""
        password = "mon_mot_de_passe"
        hashed = password_hasher.hash_password(password)

        # Un hash bcrypt commence par $2b$ (ou $2a$, $2y$ selon la version)
        assert hashed.startswith('$2')

    def test_hash_password_uses_salt(self, password_hasher):
        """Vérifie que hash_password utilise un salt automatique"""
        password = "mon_mot_de_passe"
        hash1 = password_hasher.hash_password(password)
        hash2 = password_hasher.hash_password(password)

        # Les deux hashs doivent être différents (salt aléatoire)
        assert hash1 != hash2

    def test_hash_password_empty_password_raises_error(self, password_hasher):
        """Vérifie que hash_password lève une erreur pour un mot de passe vide"""
        with pytest.raises(ValueError, match="ne peut pas être vide"):
            password_hasher.hash_password("")

    def test_hash_password_none_password_raises_error(self, password_hasher):
        """Vérifie que hash_password lève une erreur pour un mot de passe None"""
        with pytest.raises(ValueError, match="ne peut pas être vide"):
            password_hasher.hash_password(None)  # type: ignore

    def test_verify_password_returns_true_for_match(self, password_hasher):
        """Vérifie que verify_password retourne True si le mot de passe correspond"""
        password = "mon_mot_de_passe"
        hashed = password_hasher.hash_password(password)

        result = password_hasher.verify_password(password, hashed)

        assert result is True

    def test_verify_password_returns_false_for_mismatch(self, password_hasher):
        """Vérifie que verify_password retourne False si le hash ne correspond pas"""
        password = "mon_mot_de_passe"
        wrong_password = "autre_mot_de_passe"
        hashed = password_hasher.hash_password(password)

        result = password_hasher.verify_password(wrong_password, hashed)

        assert result is False

    def test_verify_password_empty_password_raises_error(self, password_hasher):
        """Vérifie que verify_password lève une erreur pour un mot de passe vide"""
        with pytest.raises(ValueError, match="ne peut pas être vide"):
            password_hasher.verify_password("", "some_hash")

    def test_verify_password_empty_hash_raises_error(self, password_hasher):
        """Vérifie que verify_password lève une erreur pour un hash vide"""
        with pytest.raises(ValueError, match="ne peut pas être vide"):
            password_hasher.verify_password("password", "")

    def test_verify_password_none_password_raises_error(self, password_hasher):
        """Vérifie que verify_password lève une erreur pour un mot de passe None"""
        with pytest.raises(ValueError, match="ne peut pas être vide"):
            password_hasher.verify_password(None, "some_hash")  # type: ignore

    def test_verify_password_none_hash_raises_error(self, password_hasher):
        """Vérifie que verify_password lève une erreur pour un hash None"""
        with pytest.raises(ValueError, match="ne peut pas être vide"):
            password_hasher.verify_password("password", None)  # type: ignore

    def test_verify_password_returns_false_for_invalid_hash(self, password_hasher):
        """Vérifie que verify_password retourne False pour un hash invalide"""
        password = "mon_mot_de_passe"
        invalid_hash = "hash_invalide"

        result = password_hasher.verify_password(password, invalid_hash)

        assert result is False

    def test_hash_and_verify_integration(self, password_hasher):
        """Test d'intégration: hasher puis vérifier avec différents mots de passe"""
        passwords = [
            "password123",
            "MotDePasseComplexe!@#",
            "1234567890",
            "!@#$%^&*()",
            "àéèùôî",
        ]

        for password in passwords:
            hashed = password_hasher.hash_password(password)
            assert password_hasher.verify_password(password, hashed) is True

            # Vérifier qu'un mot de passe différent ne matche pas
            assert password_hasher.verify_password(password + "x", hashed) is False

    @patch('bcrypt.hashpw')
    def test_hash_password_handles_bcrypt_error(self, mock_hashpw, password_hasher):
        """Vérifie que hash_password gère les erreurs de bcrypt"""
        mock_hashpw.side_effect = Exception("bcrypt error")

        with pytest.raises(RuntimeError, match="Erreur lors du hashage"):
            password_hasher.hash_password("password")
