USE ulaval_market;

ALTER TABLE users ADD INDEX idx_email (email);
ALTER TABLE users ADD INDEX idx_idul (idul);

ALTER TABLE users_profiles ADD INDEX idx_username (username);
ALTER TABLE users_profiles ADD INDEX idx_program (program);
ALTER TABLE users_profiles ADD INDEX idx_rating (rating);

ALTER TABLE sessions ADD INDEX idx_token (token);
ALTER TABLE sessions ADD INDEX idx_user_id (user_id);
ALTER TABLE sessions ADD INDEX idx_token_type (token_type);

ALTER TABLE categories ADD INDEX idx_parent (parent_id);

ALTER TABLE listings ADD INDEX idx_seller (seller_id);
ALTER TABLE listings ADD INDEX idx_category (category_id);
ALTER TABLE listings ADD INDEX idx_price (price);
ALTER TABLE listings ADD FULLTEXT INDEX idx_search (title, description);

ALTER TABLE listing_pictures ADD INDEX idx_listing (listing_id);

ALTER TABLE favorites ADD INDEX idx_user (user_id);

ALTER TABLE conversations ADD INDEX idx_buyer (buyer_id);
ALTER TABLE conversations ADD INDEX idx_seller (seller_id);

ALTER TABLE messages ADD INDEX idx_conversation (conversation_id);
ALTER TABLE messages ADD INDEX idx_sender (sender_id);

