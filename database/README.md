# Database - ULavalMarket

Scripts SQL pour MySQL 8.0

## 📁 Structure

```
database/
├── ddl/              # Data Definition Language
│   ├── 01_create_database.sql
│   ├── 02_create_tables.sql
│   ├── 03_create_indexes.sql
│   └── 04_constraints.sql
│
├── dml/              # Data Manipulation Language
│   ├── 01_insert_categories.sql
│   ├── 02_insert_users.sql      # 100+ tuples
│   ├── 03_insert_listings.sql   # 100+ tuples
│   └── 04_insert_messages.sql
│
├── routines/         # Triggers, Procédures, Fonctions
│   ├── triggers.sql
│   ├── procedures.sql
│   └── functions.sql
│
└── scripts/          # Scripts utilitaires
    ├── reset_database.sql
    └── generate_test_data.py
```

## 🗄️ Schéma de Base de Données

### Tables Principales

#### 1. **users** - Comptes étudiants

```sql
CREATE TABLE users (
    user_id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    program VARCHAR(100),
    is_verified BOOLEAN DEFAULT FALSE,
    rating DECIMAL(3,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### 2. **listings** - Annonces

```sql
CREATE TABLE listings (
    listing_id VARCHAR(36) PRIMARY KEY,
    seller_id VARCHAR(36) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category_id VARCHAR(36) NOT NULL,
    condition ENUM('Neuf', 'Comme neuf', 'Bon état', 'Usagé'),
    location VARCHAR(100),
    is_sold BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
```

#### 3. **categories** - Catégories d'annonces

```sql
CREATE TABLE categories (
    category_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    icon VARCHAR(10),
    description TEXT
);
```

#### 4. **messages** - Messages entre utilisateurs

```sql
CREATE TABLE messages (
    message_id VARCHAR(36) PRIMARY KEY,
    conversation_id VARCHAR(36) NOT NULL,
    sender_id VARCHAR(36) NOT NULL,
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

#### 5. **conversations** - Fils de discussion

```sql
CREATE TABLE conversations (
    conversation_id VARCHAR(36) PRIMARY KEY,
    listing_id VARCHAR(36) NOT NULL,
    buyer_id VARCHAR(36) NOT NULL,
    seller_id VARCHAR(36) NOT NULL,
    last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (listing_id) REFERENCES listings(listing_id) ON DELETE CASCADE,
    FOREIGN KEY (buyer_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (seller_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

#### 6. **transactions** - Historique des ventes

```sql
CREATE TABLE transactions (
    transaction_id VARCHAR(36) PRIMARY KEY,
    listing_id VARCHAR(36) NOT NULL,
    buyer_id VARCHAR(36) NOT NULL,
    seller_id VARCHAR(36) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
    completed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (listing_id) REFERENCES listings(listing_id),
    FOREIGN KEY (buyer_id) REFERENCES users(user_id),
    FOREIGN KEY (seller_id) REFERENCES users(user_id)
);
```

## 📈 Index (Optimisation)

### Index définis basés sur la charge de travail

```sql
-- Recherche par catégorie (très fréquent)
CREATE INDEX idx_listings_category ON listings(category_id);

-- Annonces actives (recherche principale)
CREATE INDEX idx_listings_active ON listings(is_sold, created_at DESC);

-- Annonces par vendeur
CREATE INDEX idx_listings_seller ON listings(seller_id);

-- Recherche textuelle
CREATE FULLTEXT INDEX idx_listings_search ON listings(title, description);

-- Authentification
CREATE INDEX idx_users_email ON users(email);

-- Messages d'une conversation
CREATE INDEX idx_messages_conversation ON messages(conversation_id, created_at DESC);
```

## ⚙️ Routines SQL

### Triggers

#### Mise à jour automatique du dernier message

```sql
DELIMITER //
CREATE TRIGGER trg_update_conversation_time
AFTER INSERT ON messages
FOR EACH ROW
BEGIN
    UPDATE conversations
    SET last_message_at = NEW.created_at
    WHERE conversation_id = NEW.conversation_id;
END//
DELIMITER ;
```

#### Validation avant insertion d'annonce

```sql
DELIMITER //
CREATE TRIGGER trg_validate_listing_price
BEFORE INSERT ON listings
FOR EACH ROW
BEGIN
    IF NEW.price <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Le prix doit être supérieur à 0';
    END IF;
END//
DELIMITER ;
```

### Procédures Stockées

#### Créer une transaction complète

```sql
DELIMITER //
CREATE PROCEDURE sp_complete_transaction(
    IN p_listing_id VARCHAR(36),
    IN p_buyer_id VARCHAR(36),
    IN p_seller_id VARCHAR(36)
)
BEGIN
    DECLARE v_price DECIMAL(10,2);

    START TRANSACTION;

    -- Récupérer le prix
    SELECT price INTO v_price
    FROM listings
    WHERE listing_id = p_listing_id AND is_sold = FALSE;

    IF v_price IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Annonce non disponible';
    END IF;

    -- Marquer l'annonce comme vendue
    UPDATE listings
    SET is_sold = TRUE
    WHERE listing_id = p_listing_id;

    -- Créer la transaction
    INSERT INTO transactions (transaction_id, listing_id, buyer_id, seller_id, amount, status, completed_at)
    VALUES (UUID(), p_listing_id, p_buyer_id, p_seller_id, v_price, 'completed', NOW());

    COMMIT;
END//
DELIMITER ;
```

### Fonctions

#### Calculer le rating d'un utilisateur

```sql
DELIMITER //
CREATE FUNCTION fn_calculate_user_rating(p_user_id VARCHAR(36))
RETURNS DECIMAL(3,2)
DETERMINISTIC
BEGIN
    DECLARE v_rating DECIMAL(3,2);

    SELECT AVG(rating) INTO v_rating
    FROM reviews
    WHERE user_id = p_user_id;

    RETURN COALESCE(v_rating, 0);
END//
DELIMITER ;
```

## 🚀 Installation

### 1. Créer la base de données

```bash
mysql -u root -p < ddl/01_create_database.sql
```

### 2. Créer les tables

```bash
mysql -u root -p ulavalmarket < ddl/02_create_tables.sql
```

### 3. Créer les index

```bash
mysql -u root -p ulavalmarket < ddl/03_create_indexes.sql
```

### 4. Peupler avec des données de test

```bash
mysql -u root -p ulavalmarket < dml/01_insert_categories.sql
mysql -u root -p ulavalmarket < dml/02_insert_users.sql
mysql -u root -p ulavalmarket < dml/03_insert_listings.sql
```

### 5. Créer les routines

```bash
mysql -u root -p ulavalmarket < routines/triggers.sql
mysql -u root -p ulavalmarket < routines/procedures.sql
mysql -u root -p ulavalmarket < routines/functions.sql
```

## 🔄 Reset de la base de données

```bash
mysql -u root -p < scripts/reset_database.sql
```

## 📊 Normalisation

Toutes les tables sont en **Forme Normale de Boyce-Codd (FNBC)** :

- ✅ Pas d'attributs multivalués
- ✅ Pas de dépendances partielles
- ✅ Pas de dépendances transitives
- ✅ Chaque déterminant est une clé candidate

## 🔒 Contraintes d'Intégrité

### Clés primaires

- Toutes les tables ont une clé primaire (UUID)

### Clés étrangères

- Toutes les références sont protégées par des FK
- `ON DELETE CASCADE` pour les dépendances fortes
- `ON DELETE RESTRICT` pour les dépendances faibles

### Contraintes CHECK

- Prix > 0
- Email valide
- Rating entre 0 et 5

## 📝 Conventions SQL

- **Tables** : `snake_case` au pluriel (ex: `users`, `listings`)
- **Colonnes** : `snake_case` (ex: `user_id`, `created_at`)
- **Procédures** : Préfixe `sp_` (ex: `sp_complete_transaction`)
- **Fonctions** : Préfixe `fn_` (ex: `fn_calculate_rating`)
- **Triggers** : Préfixe `trg_` (ex: `trg_update_time`)
- **Index** : Préfixe `idx_` (ex: `idx_users_email`)
