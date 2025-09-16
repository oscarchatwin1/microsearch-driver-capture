-- Microsearch Driver Capture - Database Creation Script
-- Creates the MySQL database for the mobile app

-- Create database with UTF-8 support
CREATE DATABASE IF NOT EXISTS microsearch 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Use the database
USE microsearch;

-- Show database creation confirmation
SELECT 'Database microsearch created successfully' AS status;
