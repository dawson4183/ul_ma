"""
Tests pour l'interface SessionRepository.

Ces tests vérifient que l'interface est correctement définie
et que les méthodes sont bien abstraites.
"""
from datetime import datetime, timedelta
from typing import List, Optional
import pytest
from domain.auth.session import Session
from domain.auth.session_repository import SessionRepository


class ConcreteSessionRepository(SessionRepository):
    """Implémentation concrète pour tester l'interface."""
    
    def __init__(self):
        self._sessions = {}  # session_id -> Session
        self._token_index = {}  # token -> session_id
        self._user_index = {}  # user_id -> List[session_id]
    
    def find_by_token(self, token: str) -> Optional[Session]:
        session_id = self._token_index.get(token)
        if session_id:
            return self._sessions.get(session_id)
        return None
    
    def find_by_user_id(self, user_id: str) -> List[Session]:
        session_ids = self._user_index.get(user_id, [])
        return [self._sessions[sid] for sid in session_ids if sid in self._sessions]
    
    def save(self, session: Session) -> None:
        # Supprimer l'ancien token de l'index si la session existe déjà
        if session.session_id in self._sessions:
            old_session = self._sessions[session.session_id]
            if old_session.token in self._token_index:
                del self._token_index[old_session.token]
        
        self._sessions[session.session_id] = session
        self._token_index[session.token] = session.session_id
        
        # Mise à jour de l'index utilisateur
        if session.user_id not in self._user_index:
            self._user_index[session.user_id] = []
        if session.session_id not in self._user_index[session.user_id]:
            self._user_index[session.user_id].append(session.session_id)
    
    def delete(self, session_id: str) -> None:
        session = self._sessions.get(session_id)
        if session:
            del self._sessions[session_id]
            del self._token_index[session.token]
            
            if session.user_id in self._user_index:
                self._user_index[session.user_id] = [
                    sid for sid in self._user_index[session.user_id]
                    if sid != session_id
                ]
    
    def mark_as_used(self, session_id: str) -> None:
        session = self._sessions.get(session_id)
        if session:
            session.mark_as_used()


class TestSessionRepositoryInterface:
    """Tests pour l'interface SessionRepository."""
    
    def test_session_repository_is_abstract(self):
        """Vérifie que SessionRepository est une classe abstraite."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            SessionRepository()
    
    def test_find_by_token_is_abstract(self):
        """Vérifie que find_by_token est une méthode abstraite."""
        class IncompleteRepository(SessionRepository):
            def find_by_user_id(self, user_id: str) -> List[Session]:
                pass
            def save(self, session: Session) -> None:
                pass
            def delete(self, session_id: str) -> None:
                pass
            def mark_as_used(self, session_id: str) -> None:
                pass
        
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteRepository()
    
    def test_find_by_user_id_is_abstract(self):
        """Vérifie que find_by_user_id est une méthode abstraite."""
        class IncompleteRepository(SessionRepository):
            def find_by_token(self, token: str) -> Optional[Session]:
                pass
            def save(self, session: Session) -> None:
                pass
            def delete(self, session_id: str) -> None:
                pass
            def mark_as_used(self, session_id: str) -> None:
                pass
        
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteRepository()
    
    def test_save_is_abstract(self):
        """Vérifie que save est une méthode abstraite."""
        class IncompleteRepository(SessionRepository):
            def find_by_token(self, token: str) -> Optional[Session]:
                pass
            def find_by_user_id(self, user_id: str) -> List[Session]:
                pass
            def delete(self, session_id: str) -> None:
                pass
            def mark_as_used(self, session_id: str) -> None:
                pass
        
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteRepository()
    
    def test_delete_is_abstract(self):
        """Vérifie que delete est une méthode abstraite."""
        class IncompleteRepository(SessionRepository):
            def find_by_token(self, token: str) -> Optional[Session]:
                pass
            def find_by_user_id(self, user_id: str) -> List[Session]:
                pass
            def save(self, session: Session) -> None:
                pass
            def mark_as_used(self, session_id: str) -> None:
                pass
        
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteRepository()
    
    def test_mark_as_used_is_abstract(self):
        """Vérifie que mark_as_used est une méthode abstraite."""
        class IncompleteRepository(SessionRepository):
            def find_by_token(self, token: str) -> Optional[Session]:
                pass
            def find_by_user_id(self, user_id: str) -> List[Session]:
                pass
            def save(self, session: Session) -> None:
                pass
            def delete(self, session_id: str) -> None:
                pass
        
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteRepository()


class TestConcreteSessionRepository:
    """Tests avec une implémentation concrète."""
    
    @pytest.fixture
    def repository(self):
        """Fixture pour le repository concret."""
        return ConcreteSessionRepository()
    
    @pytest.fixture
    def sample_session(self):
        """Fixture pour une session de test."""
        return Session(
            session_id="session-123",
            user_id="user-456",
            token="jwt-token-abc",
            token_type=Session.TOKEN_TYPE_AUTH,
            expires_at=datetime.now() + timedelta(hours=24)
        )
    
    def test_save_and_find_by_token(self, repository, sample_session):
        """Test save et find_by_token."""
        repository.save(sample_session)
        
        found = repository.find_by_token("jwt-token-abc")
        
        assert found is not None
        assert found.session_id == sample_session.session_id
        assert found.token == "jwt-token-abc"
        assert found.user_id == sample_session.user_id
    
    def test_find_by_token_returns_none_if_not_found(self, repository):
        """Test find_by_token retourne None si session non trouvée."""
        found = repository.find_by_token("non-existent-token")
        
        assert found is None
    
    def test_find_by_user_id(self, repository):
        """Test find_by_user_id retourne les sessions d'un utilisateur."""
        session1 = Session(
            session_id="session-1",
            user_id="user-abc",
            token="token-1",
            token_type=Session.TOKEN_TYPE_AUTH,
            expires_at=datetime.now() + timedelta(hours=24)
        )
        session2 = Session(
            session_id="session-2",
            user_id="user-abc",
            token="token-2",
            token_type=Session.TOKEN_TYPE_AUTH,
            expires_at=datetime.now() + timedelta(hours=24)
        )
        
        repository.save(session1)
        repository.save(session2)
        
        found = repository.find_by_user_id("user-abc")
        
        assert len(found) == 2
        assert all(s.user_id == "user-abc" for s in found)
    
    def test_find_by_user_id_returns_empty_list_if_no_sessions(self, repository):
        """Test find_by_user_id retourne liste vide si pas de sessions."""
        found = repository.find_by_user_id("user-with-no-sessions")
        
        assert found == []
    
    def test_find_by_user_id_only_returns_user_sessions(self, repository):
        """Test find_by_user_id ne retourne que les sessions de l'utilisateur."""
        session1 = Session(
            session_id="session-1",
            user_id="user-a",
            token="token-a",
            token_type=Session.TOKEN_TYPE_AUTH,
            expires_at=datetime.now() + timedelta(hours=24)
        )
        session2 = Session(
            session_id="session-2",
            user_id="user-b",
            token="token-b",
            token_type=Session.TOKEN_TYPE_AUTH,
            expires_at=datetime.now() + timedelta(hours=24)
        )
        
        repository.save(session1)
        repository.save(session2)
        
        found = repository.find_by_user_id("user-a")
        
        assert len(found) == 1
        assert found[0].session_id == "session-1"
    
    def test_delete_removes_session(self, repository, sample_session):
        """Test delete supprime une session."""
        repository.save(sample_session)
        
        repository.delete(sample_session.session_id)
        
        assert repository.find_by_token(sample_session.token) is None
    
    def test_delete_does_nothing_if_session_not_exists(self, repository):
        """Test delete ne fait rien si session n'existe pas."""
        # Ne devrait pas lever d'exception
        repository.delete("non-existent-session-id")
    
    def test_delete_removes_from_user_index(self, repository):
        """Test delete met à jour l'index utilisateur."""
        session = Session(
            session_id="session-123",
            user_id="user-xyz",
            token="token-xyz",
            token_type=Session.TOKEN_TYPE_AUTH,
            expires_at=datetime.now() + timedelta(hours=24)
        )
        
        repository.save(session)
        repository.delete(session.session_id)
        
        assert repository.find_by_user_id("user-xyz") == []
    
    def test_mark_as_used_updates_session(self, repository, sample_session):
        """Test mark_as_used marque la session comme utilisée."""
        repository.save(sample_session)
        
        repository.mark_as_used(sample_session.session_id)
        
        found = repository.find_by_token(sample_session.token)
        assert found.is_used() is True
        assert found.used_at is not None
    
    def test_mark_as_used_does_nothing_if_session_not_exists(self, repository):
        """Test mark_as_used ne fait rien si session n'existe pas."""
        # Ne devrait pas lever d'exception
        repository.mark_as_used("non-existent-session-id")
    
    def test_save_updates_existing_session(self, repository, sample_session):
        """Test save met à jour une session existante."""
        repository.save(sample_session)
        
        # Créer une nouvelle session avec le même ID mais token différent
        updated_session = Session(
            session_id=sample_session.session_id,
            user_id=sample_session.user_id,
            token="new-token",
            token_type=Session.TOKEN_TYPE_AUTH,
            expires_at=sample_session.expires_at
        )
        repository.save(updated_session)
        
        # L'ancien token ne devrait plus fonctionner
        assert repository.find_by_token("jwt-token-abc") is None
        # Le nouveau token devrait fonctionner
        assert repository.find_by_token("new-token") is not None
    
    def test_save_multiple_sessions_same_user(self, repository):
        """Test save avec plusieurs sessions pour le même utilisateur."""
        session1 = Session(
            session_id="session-1",
            user_id="user-multi",
            token="token-1",
            token_type=Session.TOKEN_TYPE_AUTH,
            expires_at=datetime.now() + timedelta(hours=24)
        )
        session2 = Session(
            session_id="session-2",
            user_id="user-multi",
            token="token-2",
            token_type=Session.TOKEN_TYPE_EMAIL_VERIFICATION,
            expires_at=datetime.now() + timedelta(hours=1)
        )
        
        repository.save(session1)
        repository.save(session2)
        
        user_sessions = repository.find_by_user_id("user-multi")
        assert len(user_sessions) == 2
