USE ulaval_market;

-- Triggers pour mettre à jour favorite_count automatiquement
DELIMITER //

-- Trigger: Incrémente favorite_count quand un favori est ajouté
CREATE TRIGGER IF NOT EXISTS after_favorite_insert
AFTER INSERT ON favorites
FOR EACH ROW
BEGIN
    UPDATE listings 
    SET favorite_count = favorite_count + 1
    WHERE listing_id = NEW.listing_id;
END //

-- Trigger: Décrémente favorite_count quand un favori est supprimé
CREATE TRIGGER IF NOT EXISTS after_favorite_delete
AFTER DELETE ON favorites
FOR EACH ROW
BEGIN
    UPDATE listings 
    SET favorite_count = favorite_count - 1
    WHERE listing_id = OLD.listing_id;
END //

DELIMITER ;
