# 🛒 ULavalMarket - Marketplace Étudiant

> Plateforme de petites annonces C2C (Consumer-to-Consumer) pour les étudiants de l'Université Laval

## 📋 Description

ULavalMarket est une application web complète permettant aux étudiants de l'Université Laval d'acheter et vendre des articles entre eux (livres, matériel scolaire, électronique, logements, etc.).

**Projet réalisé dans le cadre du cours GLO-2005 - Systèmes de gestion de bases de données**

## 🏗️ Architecture

### Architecture à 3 Niveaux

1. **Niveau Client (Frontend)**
   - React 18 + TypeScript + Vite
   - Tailwind CSS + shadcn/ui
   - Interface responsive et moderne

2. **Niveau Serveur (Backend)**
   - Python 3.11+ avec Flask
   - Architecture Hexagonale (Ports & Adapters)
   - Séparation stricte des responsabilités :
     - **Couche API** : Endpoints REST, validation DTOs
     - **Couche Application** : Services, orchestration
     - **Couche Domaine** : Logique métier, entités
     - **Couche Infrastructure** : Repositories, persistance

3. **Niveau Données (Database)**
   - MySQL 8.0
   - SQL pur (sans ORM)
   - Triggers, procédures stockées, fonctions
   - Index optimisés

## 🚀 Installation

### Prérequis

- **Python** 3.11 ou supérieur
- **Node.js** 18+ et npm
- **MySQL** 8.0+
- **Git**

### Installation Rapide

#### 1. Cloner le repository

```bash
git clone https://github.com/votre-equipe/laval-market-hub.git
cd laval-market-hub
```

#### 2. Configuration Backend

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Activer l'environnement (Linux/Mac)
# source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
copy .env.example .env
# Éditer .env avec vos credentials MySQL
```

#### 3. Configuration Base de Données

```bash
# Se connecter à MySQL
mysql -u root -p

# Exécuter les scripts DDL
source database/ddl/01_create_database.sql
source database/ddl/02_create_tables.sql
source database/ddl/03_create_indexes.sql

# Peupler la base avec des données de test
source database/dml/01_insert_users.sql
source database/dml/02_insert_listings.sql

# Créer les routines SQL
source database/routines/triggers.sql
source database/routines/procedures.sql
source database/routines/functions.sql
```

#### 4. Lancer le Backend

```bash
cd backend
python main.py
# Le serveur démarre sur http://localhost:5000
```

#### 5. Configuration Frontend

```bash
# Dans un nouveau terminal
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
# L'application démarre sur http://localhost:5173
```

## 📁 Structure du Projet

```
laval-market-hub/
├── backend/              # API Flask (Architecture Hexagonale)
│   ├── api/              # Couche Présentation
│   ├── application/      # Couche Application (Services)
│   ├── domain/           # Couche Domaine (Logique métier)
│   ├── infrastructure/   # Couche Infrastructure (BD, config)
│   └── tests/            # Tests unitaires & intégration
│
├── database/             # Scripts SQL
│   ├── ddl/              # Création tables, index
│   ├── dml/              # Données de test
│   └── routines/         # Triggers, procédures, fonctions
│
├── src/                  # Frontend React
│   ├── components/       # Composants réutilisables
│   ├── pages/            # Pages de l'application
│   ├── contexts/         # Context API
│   └── data/             # Mock data (à remplacer par API)
│
└── docs/                 # Documentation
    ├── rapport/          # Rapport technique
    └── api/              # Documentation API
```

## 🔧 Fonctionnalités

### Pour les utilisateurs

- ✅ Inscription et authentification sécurisée
- ✅ Création d'annonces avec photos
- ✅ Recherche et filtrage avancés
- ✅ Messagerie intégrée
- ✅ Système de favoris
- ✅ Évaluations et notes

### Fonctionnalités techniques

- ✅ Chiffrement des mots de passe (bcrypt)
- ✅ Protection contre SQL injection (requêtes préparées)
- ✅ Validation des données (frontend + backend)
- ✅ Gestion des erreurs robuste
- ✅ Tests unitaires et d'intégration
- ✅ API REST documentée

## 🧪 Tests

```bash
# Tests backend
cd backend
pytest tests/ -v --cov=.

# Tests frontend
cd frontend
npm run test
```

## 📊 Base de Données

### Relations principales

- **users** : Comptes étudiants
- **listings** : Annonces de produits
- **categories** : Catégories d'annonces
- **messages** : Messages entre utilisateurs
- **conversations** : Fils de discussion
- **transactions** : Historique des ventes

### Routines SQL

- **Triggers** : Mise à jour automatique des compteurs, validation
- **Procédures** : Opérations complexes (création annonce, transaction)
- **Fonctions** : Calculs (rating, statistiques)

Voir [database/README.md](database/README.md) pour plus de détails.

## 📖 Documentation

- [Rapport Technique](docs/rapport/rapport_technique.pdf)
- [Documentation API](docs/api/openapi.yaml)
- [Guide Backend](backend/README.md)
- [Guide Base de Données](database/README.md)

## 👥 Équipe

- **Membre 1** - Rôle
- **Membre 2** - Rôle
- **Membre 3** - Rôle

## 📝 Licence

Projet académique - GLO-2005 (Hiver 2026)  
Université Laval - Département d'informatique et de génie logiciel

---

**Note** : Ce projet a été développé dans le cadre du cours GLO-2005 et respecte toutes les contraintes académiques imposées (architecture 3 niveaux, SQL pur, routines SQL, sécurité, etc.)
