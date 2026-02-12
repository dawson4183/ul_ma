USE ulaval_market;

DELIMITER //

--procedure a CALL CountTableRows(); pour savoir combien de lignes nous avons dans chaque table
CREATE PROCEDURE IF NOT EXISTS CountTableRows()
BEGIN
    SELECT 
        table_name, 
        table_rows 
    FROM information_schema.tables 
    WHERE table_schema = 'ulaval_market' 
        AND table_name IN ('users', 'users_profiles', 'sessions', 'categories', 'listings', 'listing_pictures', 'favorites', 'conversations', 'messages')
    ORDER BY table_name;
END //

DELIMITER ;
