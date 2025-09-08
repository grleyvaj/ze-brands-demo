-- yoyo: CREATE TABLE products
CREATE TABLE IF NOT EXISTS products (
  id VARCHAR(26) PRIMARY KEY,
  sku VARCHAR(64) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  price NUMERIC(10,2) NOT NULL,
  brand_id VARCHAR(26) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  CONSTRAINT fk_brand FOREIGN KEY (brand_id) REFERENCES brands (id)
);
