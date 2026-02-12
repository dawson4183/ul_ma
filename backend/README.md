# Backend - ULavalMarket

API REST Python/Flask avec architecture hexagonale

## 🏗️ Architecture Hexagonale (Ports & Adapters)

```
backend/
├── api/              🔷 Couche PRÉSENTATION
│   ├── *_resource.py         # Endpoints REST (routes Flask)
│   ├── validators/           # Validation des DTOs entrants
│   └── exceptions/           # Mappers d'exceptions HTTP
│
├── application/      🔷 Couche APPLICATION
│   ├── */
│   │   ├── *_service.py      # Orchestration logique métier
│   │   ├── *_assembler.py    # Conversion DTO ↔ Entité
│   │   └── dtos/             # Data Transfer Objects
│
├── domain/           🔷 Couche DOMAINE
│   ├── */
│   │   ├── *.py              # Entités métier
│   │   ├── *_repository.py   # Interfaces (ports)
│   │   └── exceptions/       # Exceptions métier
│
└── infrastructure/   🔷 Couche INFRASTRUCTURE
    ├── persistence/
    │   ├── mysql/            # Implémentation MySQL
    │   └── in_memory/        # Implémentation pour tests
    ├── security/             # Chiffrement, sécurité
    └── config/               # Configuration
```

## 🚀 Installation

### 1. Créer l'environnement virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement

```bash
copy .env.example .env
# Éditer .env avec vos credentials
```

### 4. Lancer le serveur

```bash
python main.py
```

Le serveur démarre sur `http://localhost:5000`

## 📡 API Endpoints

### Utilisateurs

- `POST /api/users/register` - Inscription
- `POST /api/users/login` - Connexion
- `GET /api/users/{id}` - Profil utilisateur
- `PUT /api/users/{id}` - Modifier profil
- `DELETE /api/users/{id}` - Supprimer compte

### Annonces

- `GET /api/listings` - Liste des annonces
- `GET /api/listings/{id}` - Détail annonce
- `POST /api/listings` - Créer annonce
- `PUT /api/listings/{id}` - Modifier annonce
- `DELETE /api/listings/{id}` - Supprimer annonce
- `GET /api/listings/search` - Rechercher

### Messages

- `GET /api/conversations/{userId}` - Liste conversations
- `POST /api/messages` - Envoyer message
- `GET /api/messages/{conversationId}` - Messages d'une conversation

## 🧪 Tests

### Lancer tous les tests

```bash
pytest tests/ -v
```

### Tests avec couverture

```bash
pytest tests/ --cov=. --cov-report=html
```

### Tests par couche

```bash
# Tests unitaires du domaine
pytest tests/unit/domain/ -v

# Tests des services
pytest tests/unit/application/ -v

# Tests d'intégration API
pytest tests/integration/ -v
```

## 🔒 Sécurité

### Chiffrement des mots de passe

```python
from infrastructure.security.password_hasher import PasswordHasher

# Hacher un mot de passe
hashed = PasswordHasher.hash_password("password123")

# Vérifier un mot de passe
is_valid = PasswordHasher.verify_password("password123", hashed)
```

### Protection SQL Injection

✅ **Toutes les requêtes utilisent des requêtes préparées**

```python
# ✅ BON - Requête préparée
cursor.execute(
    "SELECT * FROM users WHERE email = %s",
    (email,)
)

# ❌ MAUVAIS - Vulnérable à SQL injection
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

## 📝 Conventions de Code

### Nommage

- **Fichiers** : `snake_case.py`
- **Classes** : `PascalCase`
- **Fonctions** : `snake_case`
- **Constantes** : `UPPER_SNAKE_CASE`

### Structure d'une entité

```python
class User:
    """Entité représentant un utilisateur."""

    def __init__(self, user_id: str, email: Email, username: Username):
        self._user_id = user_id
        self._email = email
        self._username = username

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def email(self) -> Email:
        return self._email
```

### Structure d'un service

```python
class UserService:
    """Service gérant les opérations sur les utilisateurs."""

    def __init__(
        self,
        user_repository: UserRepository,
        user_assembler: UserAssembler,
        password_hasher: PasswordHasher
    ):
        self._user_repository = user_repository
        self._user_assembler = user_assembler
        self._password_hasher = password_hasher

    def register_user(self, user_dto: UserCreationDto) -> UserResponseDto:
        """Inscrit un nouvel utilisateur."""
        # Logique d'inscription
        pass
```

## 🐛 Debugging

### Logs

Les logs sont configurés dans `main.py`. Niveau par défaut : `INFO`

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Message d'information")
logger.error("Message d'erreur")
```

### Variables d'environnement

```env
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## 📚 Ressources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Architecture Hexagonale](https://alistair.cockburn.us/hexagonal-architecture/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
