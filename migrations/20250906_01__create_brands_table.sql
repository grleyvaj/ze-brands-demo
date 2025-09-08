-- yoyo: CREATE TABLE brands
CREATE TABLE IF NOT EXISTS brands (
  id VARCHAR(26) PRIMARY KEY,
  name VARCHAR(128) NOT NULL,
  description VARCHAR(255),
  logo_url VARCHAR(255),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);