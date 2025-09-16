-- Microsearch Driver Capture - Table Creation Script
-- Creates the samples table for storing driver capture data

-- Ensure we're using the correct database
USE microsearch;

-- Create samples table
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

-- Show table creation confirmation
SELECT 'Table samples created successfully' AS status;

-- Show table structure
DESCRIBE samples;
