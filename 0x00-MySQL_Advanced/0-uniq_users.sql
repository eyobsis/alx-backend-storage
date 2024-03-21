-- Task: Create a table named 'users' with specified attributes and constraints
-- CREATE TABLE QUERY FOR USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE, -- UNIQUE EMAILS
    name VARCHAR(255)
);

