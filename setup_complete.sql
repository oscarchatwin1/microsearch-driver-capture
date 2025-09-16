-- Microsearch Driver Capture - Complete Setup Script
-- Run this file to set up the entire database, tables, and user

-- ==============================================
-- 1. CREATE DATABASE
-- ==============================================
CREATE DATABASE IF NOT EXISTS microsearch 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE microsearch;

-- ==============================================
-- 2. CREATE SAMPLES TABLE
-- ==============================================
CREATE TABLE IF NOT EXISTS samples (
    id CHAR(36) PRIMARY KEY COMMENT 'UUID primary key for idempotent sync',
    description TEXT NOT NULL COMMENT 'Sample description (required)',
    size_kg DECIMAL(6,3) COMMENT 'Weight in kilograms (0.000 to 999.999)',
    use_by_date DATE COMMENT 'Expiry date (YYYY-MM-DD format)',
    pack_code TEXT COMMENT 'Package/batch code',
    bird_temp_c DECIMAL(4,1) COMMENT 'Bird temperature in Celsius (-5.0 to 20.0)',
    customer TEXT COMMENT 'Customer name',
    retailer TEXT COMMENT 'Retailer name (required)',
    supplier TEXT COMMENT 'Supplier name (default: Flixton)',
    code TEXT COMMENT 'Product code (default: GB S011)',
    sample_number INT COMMENT 'Sample number (auto-increment per day)',
    price_gbp DECIMAL(7,2) COMMENT 'Price in GBP (0.00 to 99999.99)',
    van_temp_c DECIMAL(4,1) COMMENT 'Van temperature in Celsius (-5.0 to 20.0)',
    created_at_local DATETIME COMMENT 'Local creation timestamp (YYYY-MM-DD HH:MM:SS)',
    device_id VARCHAR(64) COMMENT 'Device identifier',
    driver_id VARCHAR(64) COMMENT 'Driver identifier',
    received_at_utc TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Server receive timestamp (UTC)',
    
    -- Indexes for performance
    INDEX idx_samples_created (created_at_local),
    INDEX idx_samples_device (device_id),
    INDEX idx_samples_driver (driver_id),
    INDEX idx_samples_sample_number (sample_number),
    INDEX idx_samples_retailer (retailer(50)),
    INDEX idx_samples_supplier (supplier(50)),
    INDEX idx_samples_received (received_at_utc)
    
) ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COLLATE=utf8mb4_unicode_ci
COMMENT='Driver sample capture data with offline-first sync support';

-- ==============================================
-- 3. CREATE MOBILE USER
-- ==============================================
-- Create mobile user with limited privileges
-- IMPORTANT: Change 'mobile_password' to your actual password
CREATE USER IF NOT EXISTS 'mobile'@'%' IDENTIFIED BY 'mobile_password';

-- Grant only necessary privileges for the mobile app
GRANT INSERT, SELECT, UPDATE ON microsearch.samples TO 'mobile'@'%';

-- Apply privileges
FLUSH PRIVILEGES;

-- ==============================================
-- 4. VERIFICATION
-- ==============================================
-- Show setup completion status
SELECT 'Microsearch Driver Capture database setup completed successfully!' AS status;

-- Show database info
SELECT 
    'Database' AS component,
    DATABASE() AS name,
    'utf8mb4' AS charset,
    'utf8mb4_unicode_ci' AS collation
UNION ALL
SELECT 
    'Table' AS component,
    'samples' AS name,
    COUNT(*) AS charset,
    'records' AS collation
FROM samples
UNION ALL
SELECT 
    'User' AS component,
    'mobile' AS name,
    'INSERT,SELECT,UPDATE' AS charset,
    'privileges' AS collation;

-- Show table structure
SELECT 'Table Structure:' AS info;
DESCRIBE samples;

-- Show user privileges
SELECT 'User Privileges:' AS info;
SHOW GRANTS FOR 'mobile'@'%';
