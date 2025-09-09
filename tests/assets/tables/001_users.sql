INSERT INTO users (id, username, email, hashed_password, role, created_at, updated_at) VALUES
('01K4KNRC1B66FPMG6YSCBMJDK4', 'admin', 'admin@example.com', 'hashed_pwd_admin', 'ADMIN', NOW(), NOW()),
('01K4KNRF2EBK6DF0171YXPPQ8B', 'super', 'super@example.com', 'hashed_pwd_super', 'SUPERADMIN', NOW(), NOW()),
('01K4KNRJKABX0FS4Q3RJEQ5RX5', 'anon', 'anon@example.com', 'hashed_pwd_anon', 'ANONYMOUS', NOW(), NOW());
