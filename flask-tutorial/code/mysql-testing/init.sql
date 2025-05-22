-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS my_app_db;

-- Switch to the new database
USE my_app_db;

-- Create the users table if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT
);

-- Insert some dummy data only if the table is empty
INSERT IGNORE INTO users (name, email, age) VALUES
('Alice Johnson', 'alice@example.com', 30),
('Bob Williams', 'bob@example.com', 24),
('Charlie Brown', 'charlie@example.com', 35);

-- Create a user for your Python application and grant privileges
-- This user will be used by your Python script
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'app_password';
GRANT ALL PRIVILEGES ON my_app_db.* TO 'app_user'@'%';
FLUSH PRIVILEGES;