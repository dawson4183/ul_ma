"""
Tests pour l'interface UserRepository.

Ces tests vérifient que l'interface est correctement définie
et que les méthodes sont bien abstraites.
"""
from typing import Optional
import pytest
from domain.user.user import User
from domain.user.user_repository import UserRepository


class ConcreteUserRepository(UserRepository):
    """Implémentation concrète pour tester l'interface."""
    
    def __init__(self):
        self._users = {}
        self._idul_index = {}
        self._email_index = {}
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
    
    def find_by_email(self, email: str) -> Optional[User]:
        return self._email_index.get(email.lower())
    
    def find_by_idul(self, idul: str) -> Optional[User]:
        return self._idul_index.get(idul)
    
    def save(self, user: User) -> None:
        self._users[user.user_id] = user
        self._idul_index[user.idul] = user
        self._email_index[user.email.lower()] = user
    
    def exists_by_email(self, email: str) -> bool:
        return email.lower() in self._email_index


class TestUserRepositoryInterface:
    """Tests pour l'interface UserRepository."""
    
    def test_user_repository_is_abstract(self):
        """Vérifie que UserRepository est une classe abstraite."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            UserRepository()
    
    def test_find_by_id_is_abstract(self):
        """Vérifie que find_by_id est une méthode abstraite."""
        class IncompleteRepository(UserRepository):
            def find_by_email(self, email: str) -> Optional[User]:
                pass
            def find_by_idul(self, idul: str) -> Optional[User]:
                pass
            def save(self, user: User) -> None:
                pass
            def exists_by_email(self, email: str) -> bool:
                pass
        
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteRepository()
    
    def test_find_by_email_is_abstract(self):
        """Vérifie que find_by_email est une méthode abstraite."""
        class IncompleteRepository(UserRepository):
            def find_by_id(self, user_id: str) -> Optional[User]:
                pass
            def find_by_idul(self, idul: str) -> Optional[User]:
                pass
            def save(self, user: User) -> None:
                pass
            def exists_by_email(self, email: str) -> bool:
                pass
        
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteRepository()
    
    def test_find_by_idul_is_abstract(self):
        """Vérifie que find_by_idul est une méthode abstraite."""
        class IncompleteRepository(UserRepository):
            def find_by_id(self, user_id: str) -> Optional[User]:
                pass
            def find_by_email(self, email: str) -> Optional[User]:
                pass
            def save(self, user: User) -> None:
                pass
            def exists_by_email(self, email: str) -> bool:
                pass
        
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteRepository()
    
    def test_save_is_abstract(self):
        """Vérifie que save est une méthode abstraite."""
        class IncompleteRepository(UserRepository):
            def find_by_id(self, user_id: str) -> Optional[User]:
                pass
            def find_by_email(self, email: str) -> Optional[User]:
                pass
            def find_by_idul(self, idul: str) -> Optional[User]:
                pass
            def exists_by_email(self, email: str) -> bool:
                pass
        
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteRepository()
    
    def test_exists_by_email_is_abstract(self):
        """Vérifie que exists_by_email est une méthode abstraite."""
        class IncompleteRepository(UserRepository):
            def find_by_id(self, user_id: str) -> Optional[User]:
                pass
            def find_by_email(self, email: str) -> Optional[User]:
                pass
            def find_by_idul(self, idul: str) -> Optional[User]:
                pass
            def save(self, user: User) -> None:
                pass
        
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteRepository()


class TestConcreteUserRepository:
    """Tests avec une implémentation concrète."""
    
    @pytest.fixture
    def repository(self):
        """Fixture pour le repository concret."""
        return ConcreteUserRepository()
    
    @pytest.fixture
    def sample_user(self):
        """Fixture pour un utilisateur de test."""
        return User(
            user_id="user-123",
            idul="ABC1234",
            email="test@ulaval.ca",
            password_hash="hashed_password",
            is_verified=False,
            is_active=True
        )
    
    def test_save_and_find_by_id(self, repository, sample_user):
        """Test save et find_by_id."""
        repository.save(sample_user)
        
        found = repository.find_by_id(sample_user.user_id)
        
        assert found is not None
        assert found.user_id == sample_user.user_id
        assert found.email == sample_user.email
        assert found.idul == sample_user.idul
    
    def test_find_by_id_returns_none_if_not_found(self, repository):
        """Test find_by_id retourne None si utilisateur non trouvé."""
        found = repository.find_by_id("non-existent-id")
        
        assert found is None
    
    def test_find_by_email(self, repository, sample_user):
        """Test find_by_email."""
        repository.save(sample_user)
        
        found = repository.find_by_email("test@ulaval.ca")
        
        assert found is not None
        assert found.user_id == sample_user.user_id
    
    def test_find_by_email_case_insensitive(self, repository, sample_user):
        """Test find_by_email est insensible à la casse."""
        repository.save(sample_user)
        
        found = repository.find_by_email("TEST@ULAVAL.CA")
        
        assert found is not None
        assert found.user_id == sample_user.user_id
    
    def test_find_by_email_returns_none_if_not_found(self, repository):
        """Test find_by_email retourne None si utilisateur non trouvé."""
        found = repository.find_by_email("notfound@ulaval.ca")
        
        assert found is None
    
    def test_find_by_idul(self, repository, sample_user):
        """Test find_by_idul."""
        repository.save(sample_user)
        
        found = repository.find_by_idul("ABC1234")
        
        assert found is not None
        assert found.user_id == sample_user.user_id
    
    def test_find_by_idul_returns_none_if_not_found(self, repository):
        """Test find_by_idul retourne None si utilisateur non trouvé."""
        found = repository.find_by_idul("XYZ9999")
        
        assert found is None
    
    def test_exists_by_email_returns_true_when_exists(self, repository, sample_user):
        """Test exists_by_email retourne True si l'email existe."""
        repository.save(sample_user)
        
        exists = repository.exists_by_email("test@ulaval.ca")
        
        assert exists is True
    
    def test_exists_by_email_case_insensitive(self, repository, sample_user):
        """Test exists_by_email est insensible à la casse."""
        repository.save(sample_user)
        
        exists = repository.exists_by_email("TEST@ULAVAL.CA")
        
        assert exists is True
    
    def test_exists_by_email_returns_false_when_not_exists(self, repository):
        """Test exists_by_email retourne False si l'email n'existe pas."""
        exists = repository.exists_by_email("notfound@ulaval.ca")
        
        assert exists is False
    
    def test_save_updates_existing_user(self, repository, sample_user):
        """Test save met à jour un utilisateur existant."""
        repository.save(sample_user)
        
        # Mise à jour de l'utilisateur
        sample_user.verify()
        repository.save(sample_user)
        
        found = repository.find_by_id(sample_user.user_id)
        assert found.is_verified is True
    
    def test_save_multiple_users(self, repository):
        """Test save avec plusieurs utilisateurs."""
        user1 = User(
            user_id="user-1",
            idul="ABC1234",
            email="user1@ulaval.ca",
            password_hash="hash1"
        )
        user2 = User(
            user_id="user-2",
            idul="DEF5678",
            email="user2@ulaval.ca",
            password_hash="hash2"
        )
        
        repository.save(user1)
        repository.save(user2)
        
        assert repository.find_by_id("user-1") is not None
        assert repository.find_by_id("user-2") is not None
        assert repository.find_by_email("user1@ulaval.ca") is not None
        assert repository.find_by_email("user2@ulaval.ca") is not None
