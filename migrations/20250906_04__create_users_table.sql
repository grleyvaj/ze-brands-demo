-- yoyo: CREATE TABLE users
CREATE TABLE users (
    id VARCHAR(26) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'ANONYMOUS',
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
