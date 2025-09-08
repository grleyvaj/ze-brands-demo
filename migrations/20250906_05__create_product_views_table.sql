-- yoyo: CREATE TABLE views
CREATE TABLE product_views (
    id VARCHAR(26) PRIMARY KEY,
    product_id VARCHAR(26) NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    view_count BIGINT DEFAULT 0,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
