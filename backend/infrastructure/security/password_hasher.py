"""Service de hashage de mots de passe avec bcrypt."""

import bcrypt


class PasswordHasher:
    """Service pour hasher et vérifier les mots de passe avec bcrypt."""

    def hash_password(self, password: str) -> str:
        """
        Hashe un mot de passe avec bcrypt et un salt automatique.

        Args:
            password: Le mot de passe en clair à hasher

        Returns:
            Le hash bcrypt du mot de passe

        Raises:
            ValueError: Si le password est vide ou None
        """
        if not password:
            raise ValueError("Le mot de passe ne peut pas être vide")

        try:
            # Génère un salt automatique et hashe le mot de passe
            password_bytes = password.encode('utf-8')
            hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
            return hashed.decode('utf-8')
        except Exception as e:
            raise RuntimeError(f"Erreur lors du hashage du mot de passe: {str(e)}")

    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Vérifie si un mot de passe correspond à un hash bcrypt.

        Args:
            password: Le mot de passe en clair à vérifier
            password_hash: Le hash bcrypt stocké

        Returns:
            True si le mot de passe correspond, False sinon

        Raises:
            ValueError: Si le password ou le hash est vide/None
        """
        if not password:
            raise ValueError("Le mot de passe ne peut pas être vide")
        if not password_hash:
            raise ValueError("Le hash ne peut pas être vide")

        try:
            password_bytes = password.encode('utf-8')
            hash_bytes = password_hash.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hash_bytes)
        except Exception:
            # En cas d'erreur (hash invalide, etc.), retourne False
            return False
