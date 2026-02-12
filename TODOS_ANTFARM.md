# TODOs pour Antfarm - Projet ULavalMarket

## Conventions (À RESPECTER ABSOLUMENT)
- **Commits** : `fonctionnalite:`, `correctif:`, `correctif(securite):`
- **Branches** : `fonctionnalite/description`, `correctif/description`
- **Code** : Commentaires en FRANÇAIS, noms de variables en ANGLAIS
- **Database** : `~/.openclaw/workspace/UL/database/` est SACROSANCT, READ-ONLY (permissions 555), NE JAMAIS MODIFIER
- **Status protocol** : Retourner `STATUS: done` (pas "STATUT: terminé") pour completion
- **Structure** : Backend Flask avec architecture DDD existante

---

## TODO 1/13 : Configuration Connexion MySQL

Configure la connexion MySQL 8 dans le backend Flask en utilisant le pattern DDD existant. Ajoute la configuration dans infrastructure/database/ avec un fichier de config (config.py ou yaml). La base s'appelle `ulaval_market`. Respecte l'architecture: infrastructure pour la connexion, repository pattern pour les accès. Ajoute le code source seulement, comments en français.

**Credentials MySQL:**
- Host: localhost (127.0.0.1)
- Port: 3306
- User: root
- Password: @Lskdj1220Kevin
- Database: ulaval_market

STATUS: done quand terminé.

---

## TODO 2/13 : API Authentification JWT

Implémente l'API d'authentification avec JWT dans le backend Flask:
- POST /api/auth/register : Crée user avec idul (format: 5 lettres + 0-3 chiffres), password hashé bcrypt, email auto = idul@ulaval.ca
- POST /api/auth/login : Vérifie credentials, retourne JWT access_token (validité 24h), crée session en DB
- GET /api/auth/me : Retourne user courant depuis JWT
- Stockage sessions dans table `sessions` (token, expires_at)
Respecte DDD: domain/auth/, application/auth/, infrastructure/auth/, api/auth/
Comments français, variables anglais. NE TOUCHE PAS au dossier database/. STATUS: done quand terminé.

---

## TODO 3/13 : API Listings CRUD avec Upload Photos

Crée l'API REST pour la table `listings` avec upload de photos:
- GET /api/listings : Liste avec filtres (category_id, price_min/max, search text, pagination)
- GET /api/listings/:id : Détail avec photos depuis `listing_pictures`
- POST /api/listings : Création (protégé JWT), prendre title, description, price, category_id, item_condition, location, Program (string), + fichiers photos
- PUT /api/listings/:id : Update own listing (protégé, vérifier seller_id)
- DELETE /api/listings/:id : Soft delete (is_deleted = TRUE, protégé)
- GET /api/listings/mine : Listings du user courant (protégé)
Photos: stocker dans `backend/uploads/` avec nom unique (uuid + timestamp), servir en static, path enregistré dans `listing_pictures` avec is_cover pour la première photo.
Comments français. STATUS: done quand terminé.

---

## TODO 4/13 : Wire Backend→Frontend CORS & Config

Configure la communication entre frontend React et backend Flask:
- Vérifier CORS configuré dans Flask (déjà présent dans main.py, vérifier ça fonctionne)
- Créer fichier .env pour frontend: `VITE_API_URL=http://localhost:5000`
- Créer fichier .env pour backend: y mettre DATABASE_URL, SECRET_KEY, FRONTEND_URL
- Créer un client API de base avec axios (src/lib/api.ts) avec baseURL depuis env
- Tester un endpoint simple (/health) depuis le frontend pour valider la connexion
Comments français dans le code. STATUS: done quand terminé.

---

## TODO 5/13 : Auth Context & Protected Routes React

Implémente l'authentification côté frontend:
- AuthContext (src/contexts/AuthContext.tsx) avec: user, login(token), logout(), register(), loading
- Stockage JWT dans localStorage (key: 'ul_token')
- Hook useAuth() pour accéder au contexte
- Composant ProtectedRoute qui: vérifie JWT, si non connecté redirige vers /auth?returnUrl=xxx avec l'URL demandée encodée
- Axios interceptor pour ajouter header Authorization: Bearer <token>
- Gestion logout automatique si 401 reçu
Comments français, variables anglais. STATUS: done quand terminé.

---

## TODO 6/13 : Remove Mock Data & Create API Hooks

Supprime TOUTES les données mock et crée les hooks de connexion API:
- Supprimer mockListings et tout le dossier src/data/mockData.ts
- Garder ListingsContext mais le modifier pour fetcher depuis /api/listings
- Créer hooks React:
  - useListings(filters) → GET /api/listings
  - useListing(id) → GET /api/listings/:id
  - useCreateListing() → POST /api/listings avec FormData pour photos
  - useMyListings() → GET /api/listings/mine (protégé)
  - useDeleteListing(id) → DELETE /api/listings/:id
- Mettre à jour toutes les pages qui utilisaient mockListings (Catalogue, Listing, etc.)
Comments français. STATUS: done quand terminé.

---

## TODO 7/13 : Rename Pages & Update Routing

Renomme les routes et met à jour le routing:
- Renommer dossier/page: /vendre → /sell
- Renommer: /mes-annonces → /my-listings
- Renommer: /annonce/:id → /listing/:id
- Mettre à jour App.tsx avec les nouvelles routes
- Créer redirections ?redirect= pour compatibilité (optionnel)
- Protéger /sell, /my-listings, /messages avec ProtectedRoute
- Laisser /catalogue et /listing/:id publics (mais avec CTAs si pas auth - voir TODO 9)
Comments français dans le code des composants. STATUS: done quand terminé.

---

## TODO 8/13 : Page My-Listings Composant Partagé Favoris

Crée la page /my-listings avec bascule vers favoris:
- Composant MyListingsPage avec mode state: 'listings' | 'favorites'
- Mode 'listings': affiche annonces du user courant (useMyListings)
- Mode 'favorites': affiche favoris (placeholder pour le moment, sera rempli au TODO 11)
- Bouton toggle visuel: "Mes annonces | Mes favoris"
- Même layout de grille pour les deux modes
- Page protégée (redirect vers /auth si pas connecté)
- Gérer le cas "aucune annonce" / "aucun favori"
Comments français. STATUS: done quand terminé.

---

## TODO 9/13 : CTAs pour Utilisateurs Non-Authentifiés

Ajoute les appels à action pour visiteurs non connectés:
- Sur /listing/:id: Si pas auth, bouton "Connectez-vous pour contacter le vendeur" → redirect /auth?returnUrl=/listing/:id
- Sur /catalogue: Banner/button "Connectez-vous pour commencer à vendre" → redirect /auth?returnUrl=/sell
- Les CTAs ne doivent pas casser le layout, juste remplacer les fonctionnalités protégées
- Utiliser le AuthContext pour détecter l'état de connexion
- Style avec les composants shadcn existants (Button avec variant)
Comments français. STATUS: done quand terminé.

---

## TODO 10/13 : API Categories & Users Profile

Crée les endpoints API secondaires:
- GET /api/categories : Retourne toutes les catégories (table `categories`) avec name, icon, description
- GET /api/users/:id/profile : Profil public (username, program, rating depuis users_profiles)
- Ces endpoints sont publics (pas besoin de JWT)
- Intégrer dans le DDD existant: domain/, application/, api/
- Mettre à jour le frontend pour utiliser ces endpoints (dropdown catégories dans /sell, profil vendeur dans /listing/:id)
Comments français. STATUS: done quand terminé.

---

## TODO 11/13 : API Favorites & Toggle Frontend

Implémente le système de favoris:
- Backend:
  - POST /api/favorites : body listing_id, crée favori pour user courant
  - DELETE /api/favorites/:listing_id : supprime favori
  - GET /api/favorites : liste les favoris de l'user avec données listing jointes
- Frontend:
  - Hook useFavorites() pour fetcher
  - Hook useToggleFavorite(listing_id) pour add/remove
  - Mettre à jour la page /my-listings mode 'favorites' pour utiliser vraiment l'API
  - Ajouter bouton cœur (favori) sur les ListingCard dans Catalogue et My-Listings
Comments français. STATUS: done quand terminé.

---

## TODO 12/13 : API Conversations & Messages

Implémente la messagerie:
- Backend:
  - GET /api/conversations : Liste des conversations de l'user avec last_message, nom de l'autre user, photo listing
  - GET /api/conversations/:id/messages : Messages paginés
  - POST /api/conversations/:id/messages : Send message (content)
  - POST /api/conversations : Crée nouvelle conversation (listing_id, seller_id auto depuis listing)
- Vérifier contrainte: une conversation unique par (listing_id, buyer_id)
- Frontend:
  - Mettre à jour /messages pour fetcher conversations
  - Vue conversation avec messages
  - Bouton "Envoyer message" sur listing si connecté
Comments français. STATUS: done quand terminé.

---

## TODO 13/13 : Tests Intégration & Vérification Finale

Vérifie le système complet:
- Test E2E: Register → Login → Create listing avec photo → View in catalogue → Add to favorites → View favorites → Remove from favorites → Logout
- Vérifier que les routes protégées redirigent correctement et reviennent après auth
- Vérifier que database/ n'a PAS été modifié (ne doit pas contenir de nouveaux fichiers, permissions inchangées)
- Vérifier que les noms de routes API correspondent aux tables: /api/listings, /api/categories, /api/users, /api/favorites, /api/conversations, /api/messages
- Vérifier tous les comments sont en français
- Vérifier tous les commits/branches suivent la convention
Documenter tout bug trouvé dans un fichier TEST_RESULTS.md
STATUS: done quand terminé.

---

## Rappels Critiques pour Chaque Agent
1. **NE JAMAIS TOUCHER** `~/.openclaw/workspace/UL/database/` - READ-ONLY
2. Comments = FRANÇAIS, Variables = ANGLAIS
3. Commits: `fonctionnalite:`, `correctif:`, `correctif(securite):`
4. Branches: `fonctionnalite/nom`, `correctif/nom`
5. Terminer avec `STATUS: done` (pas de traduction)
