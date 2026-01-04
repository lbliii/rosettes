-- Create table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert data
INSERT INTO users (name, email)
VALUES ('John Doe', 'john@example.com');

-- Select with join
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
ORDER BY o.total DESC
LIMIT 10;

-- Update
UPDATE users
SET name = 'Jane Doe'
WHERE id = 1;

-- Delete
DELETE FROM users WHERE id = 1;
