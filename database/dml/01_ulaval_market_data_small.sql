USE ulaval_market;

INSERT INTO categories (category_id, name, icon, parent_id, description) VALUES
(1, 'Livres & Cours', '📚', NULL, 'Manuels, notes de cours et livres universitaires'),
(2, 'Sciences', '🔬', 1, 'Livres de sciences et laboratoire'),
(3, 'Génie', '⚙️', 1, 'Manuels de génie et ingénierie'),
(4, 'Lettres & SHS', '📖', 1, 'Sciences humaines, littérature, histoire'),
(5, 'Électronique', '💻', NULL, 'Ordinateurs, tablettes, accessoires tech'),
(6, 'Calculatrices', '🧮', 5, 'Calculatrices graphiques et scientifiques'),
(7, 'Ordinateurs', '🖥️', 5, 'Laptops, desktops et composants'),
(8, 'Fournitures', '✏️', NULL, 'Cahiers, stylos, sacs à dos'),
(9, 'Mobilier', '🪑', NULL, 'Meubles pour appartement étudiant'),
(10, 'Location', '🏠', NULL, 'Sous-location logements, colocs'),
(11, 'Transport', '🚲', NULL, 'Vélos, voitures, transport local'),
(12, 'Billets & Événements', '🎫', NULL, 'Billets pour événements étudiants');

INSERT INTO users (user_id, idul, email, password_hash, is_verified, is_active, created_at, updated_at, deleted_at) VALUES
(1, 'abk1234', 'alex.b@ulaval.ca', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', TRUE, TRUE, '2024-01-15 10:30:00', '2024-01-15 10:30:00', NULL),
(2, 'jdl5678', 'julie.d@ulaval.ca', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', TRUE, TRUE, '2024-01-20 14:22:00', '2024-01-20 14:22:00', NULL),
(3, 'mtm9012', 'marc.t@ulaval.ca', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', TRUE, TRUE, '2024-02-05 09:15:00', '2024-02-05 09:15:00', NULL),
(4, 'srb3456', 'sarah.r@ulaval.ca', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', TRUE, TRUE, '2024-02-12 16:45:00', '2024-02-12 16:45:00', NULL),
(5, 'lbg7890', 'luc.b@ulaval.ca', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', FALSE, TRUE, '2024-02-18 11:00:00', '2024-02-18 11:00:00', NULL),
(6, 'emc2345', 'emma.c@ulaval.ca', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', TRUE, TRUE, '2024-03-01 13:30:00', '2024-03-01 13:30:00', NULL),
(7, 'nfl6789', 'noah.f@ulaval.ca', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', TRUE, TRUE, '2024-03-10 08:20:00', '2024-03-10 08:20:00', NULL),
(8, 'opg0123', 'olivia.g@ulaval.ca', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', TRUE, FALSE, '2024-03-15 19:00:00', '2024-03-15 19:00:00', '2024-04-01 10:00:00');

INSERT INTO users_profiles (profile_id, username, program, rating, created_at, updated_at) VALUES
(1, 'alex_genie', 'Génie logiciel', 4.75, '2024-01-15 10:30:00', '2024-02-01 14:00:00'),
(2, 'julie_bio', 'Biologie', 5.00, '2024-01-20 14:22:00', '2024-01-20 14:22:00'),
(3, 'marc_chimie', 'Chimie', 4.50, '2024-02-05 09:15:00', '2024-03-01 10:30:00'),
(4, 'sarah_lettres', 'Lettres françaises', 4.00, '2024-02-12 16:45:00', '2024-02-12 16:45:00'),
(5, 'luc_actif', 'Actuariat', 0.00, '2024-02-18 11:00:00', '2024-02-18 11:00:00'),
(6, 'emma_design', 'Design graphique', 4.80, '2024-03-01 13:30:00', '2024-03-15 09:00:00'),
(7, 'noah_droit', 'Droit', 3.50, '2024-03-10 08:20:00', '2024-03-20 16:00:00');

INSERT INTO listings (listing_id, seller_id, title, description, Program, price, category_id, item_condition, location, is_sold, is_deleted, view_count, favorite_count, created_at, updated_at) VALUES
(1, 1, 'Calculatrice TI-83 Plus', 'Calculatrice graphique parfaite pour calcul 1 et 2. Peu utilisée, fonctionne parfaitement. Piles neuves incluses.', 'GEL', 65.00, 6, 'Bon état', 'Pavillon Alexandre-Vachon', FALSE, FALSE, 45, 3, '2024-02-10 10:00:00', '2024-02-10 10:00:00'),
(2, 1, 'Manuel GLO-1901 Introduction à la programmation', 'Livre de cours complet pour GLO-1901. Quelques annotations au crayon mais très propre.', 'GEL', 35.00, 3, 'Bon état', 'Pavillon Adrien-Pouliot', FALSE, FALSE, 28, 1, '2024-02-12 14:30:00', '2024-02-12 14:30:00'),
(3, 2, 'Microscope portable pour labo', 'Microscope de poche 200x, idéal pour les travaux pratiques en biologie. Très bon état.', 'BIO', 120.00, 2, 'Comme neuf', 'Pavillon Charles-Eugène-Marchand', FALSE, FALSE, 15, 5, '2024-02-15 09:00:00', '2024-02-15 09:00:00'),
(4, 2, 'Collection complète Botanique Systématique', '4 volumes de la collection botanique. Incontournable pour les cours avancés.', 'BIO', 80.00, 2, 'Bon état', 'Pavillon Charles-Eugène-Marchand', FALSE, FALSE, 12, 0, '2024-02-18 16:00:00', '2024-02-18 16:00:00'),
(5, 3, 'MacBook Air M1 2020', 'MacBook Air M1, 8GB RAM, 256GB SSD. Parfait pour la programmation et les cours en ligne. Avec chargeur original.', 'CHM', 750.00, 7, 'Comme neuf', 'Résidences étudiantes', FALSE, FALSE, 120, 8, '2024-02-20 11:00:00', '2024-02-22 09:30:00'),
(6, 4, 'Histoire de la littérature française - Tome complet', 'Ouvrage de référence pour les cours de littérature. Édition de poche, très pratique.', 'FLE', 25.00, 4, 'Usagé', 'Pavillon Félix-Antoine-Savard', TRUE, FALSE, 8, 0, '2024-02-22 13:00:00', '2024-02-25 10:00:00'),
(7, 6, 'Affiches et planches design', 'Lot de 20 affiches et planches de design graphique pour inspiration et décoration bureau.', 'DES', 30.00, 8, 'Neuf', 'Pavillon Ferdinand-Vandry', FALSE, FALSE, 22, 4, '2024-03-01 15:00:00', '2024-03-01 15:00:00'),
(8, 6, 'iPad Air 4 + Apple Pencil', 'iPad Air 4ème génération 64GB avec Apple Pencil. Idéal pour prendre des notes en cours.', 'DES', 450.00, 5, 'Comme neuf', 'Pavillon Ferdinand-Vandry', FALSE, FALSE, 65, 6, '2024-03-05 10:00:00', '2024-03-08 14:00:00'),
(9, 7, 'Droit administratif - Dalloz', 'Manuel de référence pour le cours de droit administratif. Édition 2022.', 'DRT', 45.00, 4, 'Bon état', 'Pavillon Gene-H.-Kruger', FALSE, FALSE, 18, 2, '2024-03-10 14:00:00', '2024-03-10 14:00:00'),
(10, 1, 'Chaise de bureau ergonomique', 'Chaise de bureau ajustable, très confortable pour les longues sessions d''étude.', 'GEL', 85.00, 9, 'Bon état', 'Appartement Plateau', FALSE, FALSE, 34, 1, '2024-03-12 09:00:00', '2024-03-12 09:00:00'),
(11, 3, 'Lot de verrerie laboratoire', 'Erlenmeyers, béchers, éprouvettes graduées. Ensemble complet pour les travaux pratiques.', 'CHM', 40.00, 2, 'Comme neuf', 'Pavillon Alexandre-Vachon', FALSE, FALSE, 7, 0, '2024-03-15 16:30:00', '2024-03-15 16:30:00'),
(12, 2, 'Vélo hybride cadet', 'Vélo hybride 21 vitesses, parfait pour se déplacer sur le campus. Avec antivol.', 'BIO', 180.00, 11, 'Bon état', 'Résidences PEPS', FALSE, FALSE, 45, 3, '2024-03-18 11:00:00', '2024-03-20 09:00:00'),
(13, 5, 'Calculatrice scientifique Casio fx-991ES PLUS', 'Calculatrice scientifique non-graphique. Autorisée en examens.', 'ACT', 25.00, 6, 'Comme neuf', 'Pavillon Vachon', FALSE, FALSE, 8, 0, '2024-03-20 13:00:00', '2024-03-20 13:00:00'),
(14, 7, 'Billets Gala Droit 2024 x2', 'Deux billets pour le Gala du Droit 2024. Ne peux pas y assister.', 'DRT', 60.00, 12, 'Neuf', 'Pavillon Gene-H.-Kruger', FALSE, FALSE, 5, 1, '2024-03-22 18:00:00', '2024-03-22 18:00:00'),
(15, 4, 'Éditions complètes Molière', 'Collection des œuvres complètes de Molière. Reliure dure, excellent état.', 'FLE', 40.00, 4, 'Bon état', 'Pavillon Félix-Antoine-Savard', FALSE, TRUE, 3, 0, '2024-03-25 10:00:00', '2024-03-26 09:00:00');

INSERT INTO listing_pictures (picture_id, listing_id, file_path, is_cover, created_at) VALUES
(1, 1, '/uploads/ti83_1.jpg', TRUE, '2024-02-10 10:00:00'),
(2, 1, '/uploads/ti83_2.jpg', FALSE, '2024-02-10 10:01:00'),
(3, 5, '/uploads/macbook_1.jpg', TRUE, '2024-02-20 11:00:00'),
(4, 5, '/uploads/macbook_2.jpg', FALSE, '2024-02-20 11:01:00'),
(5, 5, '/uploads/macbook_3.jpg', FALSE, '2024-02-20 11:02:00'),
(6, 8, '/uploads/ipad_1.jpg', TRUE, '2024-03-05 10:00:00'),
(7, 8, '/uploads/ipad_2.jpg', FALSE, '2024-03-05 10:01:00'),
(8, 12, '/uploads/velo_1.jpg', TRUE, '2024-03-18 11:00:00'),
(9, 10, '/uploads/chaise_1.jpg', TRUE, '2024-03-12 09:00:00'),
(10, 3, '/uploads/microscope_1.jpg', TRUE, '2024-02-15 09:00:00'),
(11, 6, '/uploads/livre_1.jpg', TRUE, '2024-02-22 13:00:00'),
(12, 7, '/uploads/affiches_1.jpg', TRUE, '2024-03-01 15:00:00'),
(13, 14, '/uploads/gala_1.jpg', TRUE, '2024-03-22 18:00:00'),
(14, 11, '/uploads/verrerie_1.jpg', TRUE, '2024-03-15 16:30:00'),
(15, 2, '/uploads/glo1901_1.jpg', TRUE, '2024-02-12 14:30:00');

INSERT INTO favorites (favorite_id, user_id, listing_id, created_at) VALUES
(1, 2, 5, '2024-02-21 09:00:00'),  -- Julie aime le MacBook
(2, 3, 1, '2024-02-11 10:00:00'),  -- Marc aime la TI-83
(3, 4, 8, '2024-03-06 11:00:00'),  -- Sarah aime l''iPad
(4, 6, 12, '2024-03-19 14:00:00'), -- Emma aime le vélo
(5, 1, 12, '2024-03-19 15:00:00'), -- Alex aime le vélo aussi
(6, 2, 8, '2024-03-07 10:00:00'),  -- Julie aime aussi l''iPad
(7, 7, 6, '2024-02-23 16:00:00'),  -- Noah aime le livre d''histoire
(8, 3, 11, '2024-03-16 09:00:00'), -- Marc aime la verrerie
(9, 4, 7, '2024-03-02 13:00:00'),  -- Sarah aime les affiches
(10, 6, 9, '2024-03-11 10:00:00'); -- Emma aime le livre de droit

INSERT INTO conversations (conversation_id, listing_id, buyer_id, seller_id, last_message_at, created_at, updated_at) VALUES
(1, 1, 3, 1, '2024-02-14 16:30:00', '2024-02-12 10:00:00', '2024-02-14 16:30:00'),
(2, 5, 2, 3, '2024-02-23 14:00:00', '2024-02-22 09:00:00', '2024-02-23 14:00:00'),
(3, 8, 4, 6, '2024-03-07 13:30:00', '2024-03-06 10:00:00', '2024-03-07 13:30:00'),
(4, 12, 1, 2, '2024-03-21 11:45:00', '2024-03-19 14:00:00', '2024-03-21 11:45:00'),
(5, 6, 7, 4, '2024-02-24 09:00:00', '2024-02-23 15:00:00', '2024-02-24 09:00:00'),
(6, 10, 2, 1, '2024-03-14 17:00:00', '2024-03-13 10:00:00', '2024-03-14 17:00:00'),
(7, 3, 1, 2, '2024-02-16 12:00:00', '2024-02-15 11:00:00', '2024-02-16 12:00:00'),
(8, 11, 1, 3, '2024-03-17 10:30:00', '2024-03-16 09:00:00', '2024-03-17 10:30:00'),
(9, 9, 6, 7, '2024-03-12 14:30:00', '2024-03-11 10:00:00', '2024-03-12 14:30:00');

INSERT INTO messages (message_id, conversation_id, sender_id, content, is_read, created_at) VALUES
(1, 1, 3, 'Salut! La calculatrice est encore disponible?', TRUE, '2024-02-12 10:00:00'),
(2, 1, 1, 'Oui elle est dispo! Tu es en quel programme?', TRUE, '2024-02-12 11:30:00'),
(3, 1, 3, 'Chimie, j''en ai besoin pour calcul 2. Elle est vraiment en bon état?', TRUE, '2024-02-12 15:00:00'),
(4, 1, 1, 'Oui parfait état, je l''ai utilisée qu''un semestre. Tu peux la voir sur place si tu veux.', TRUE, '2024-02-12 15:30:00'),
(5, 1, 3, 'Super, on peut se voir demain à Vachon?', FALSE, '2024-02-14 16:30:00'),
(6, 2, 2, 'Bonjour! Je suis intéressée par le MacBook. Tu acceptes les négociations?', TRUE, '2024-02-22 09:00:00'),
(7, 2, 3, 'Salut! Je peux descendre à 700$ mais c''est le minimum, il est quasi neuf.', TRUE, '2024-02-22 18:00:00'),
(8, 2, 2, 'D''accord pour 700$. Tu acceptes de me le montrer avant?', TRUE, '2024-02-23 10:00:00'),
(9, 2, 3, 'Pas de problème, on se voit où?', FALSE, '2024-02-23 14:00:00'),
(10, 3, 4, 'Hi! L''iPad est-il encore sous garantie Apple?', TRUE, '2024-03-06 10:00:00'),
(11, 3, 6, 'Oui il reste 4 mois de garantie Apple! Je peux te montrer le reçu.', TRUE, '2024-03-06 16:00:00'),
(12, 3, 4, 'Parfait! Tu l''utilisais avec quelle app principalement?', TRUE, '2024-03-07 09:00:00'),
(13, 3, 6, 'Procreate et Notability surtout. Tu dessines?', FALSE, '2024-03-07 13:30:00'),
(14, 4, 1, 'Hey! Le vélo est-il un homme ou femme?', TRUE, '2024-03-19 14:00:00'),
(15, 4, 2, 'C''est un modèle unisexe, cadre aluminium taille M.', TRUE, '2024-03-19 18:00:00'),
(16, 4, 1, 'Parfait! Je fais 5''10, ça devrait aller. Tu l''as eu quand?', TRUE, '2024-03-20 10:00:00'),
(17, 4, 2, 'L''année dernière, j''ai fait upgradé à un vélo de route depuis.', FALSE, '2024-03-21 11:45:00'),
(18, 5, 7, 'Bonjour, le livre contient-il les annotations du prof? C''est pour Histoire médiévale avec Tremblay.', TRUE, '2024-02-23 15:00:00'),
(19, 5, 4, 'Oui exactement! J''ai mis des post-it sur les pages importantes pour les examens.', FALSE, '2024-02-24 09:00:00'),
(20, 6, 2, 'Salut! Je cherche une chaise pour mon bureau, celle-ci ajuste en hauteur?', TRUE, '2024-03-13 10:00:00'),
(21, 6, 1, 'Oui complètement ajustable, et le dossier incline aussi.', TRUE, '2024-03-13 19:00:00'),
(22, 6, 2, 'Génial! Tu acceptes l''e-Transfer?', FALSE, '2024-03-14 17:00:00'),
(23, 7, 1, 'Le microscope marche encore? Piles incluses?', TRUE, '2024-02-15 11:00:00'),
(24, 7, 2, 'Oui parfait état! Piles incluses, c''est des AAA.', FALSE, '2024-02-16 12:00:00'),
(25, 8, 1, 'Salut Marc! La verrerie est complète que tu montres ou il y en a plus?', TRUE, '2024-03-16 09:00:00'),
(26, 8, 3, 'J''ai exactement ce qui est sur la photo plus quelques éprouvettes en bonus.', FALSE, '2024-03-17 10:30:00'),
(27, 9, 6, 'Coucou! Le manuel est encore à jour pour le cours de Droit admin 1?', TRUE, '2024-03-11 10:00:00'),
(28, 9, 7, 'Oui c''est l''édition demandée cette année. Peu d''annotations dedans.', FALSE, '2024-03-12 14:30:00');
