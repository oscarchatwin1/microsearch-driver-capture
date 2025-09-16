-- Microsearch Driver Capture - Dropdown Data Tables
-- Creates tables for dropdown field data

USE microsearch;

-- Sample Descriptions Table
CREATE TABLE IF NOT EXISTS sample_descriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255) NOT NULL UNIQUE,
    category VARCHAR(100),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_description (description),
    INDEX idx_category (category),
    INDEX idx_active (active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Sample description options for dropdown';

-- Retailers Table
CREATE TABLE IF NOT EXISTS retailers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    code VARCHAR(50),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_code (code),
    INDEX idx_active (active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Retailer options for dropdown';

-- Customers Table
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    code VARCHAR(50),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_code (code),
    INDEX idx_active (active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Customer options for dropdown';

-- Pack Codes Table
CREATE TABLE IF NOT EXISTS pack_codes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_code (code),
    INDEX idx_active (active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Pack code options for dropdown';

-- Insert sample data
INSERT IGNORE INTO sample_descriptions (description, category) VALUES
('Chicken Breast', 'Poultry'),
('Chicken Thigh', 'Poultry'),
('Chicken Wing', 'Poultry'),
('Beef Mince', 'Red Meat'),
('Beef Steak', 'Red Meat'),
('Pork Chop', 'Red Meat'),
('Salmon Fillet', 'Fish'),
('Cod Fillet', 'Fish'),
('Mixed Vegetables', 'Vegetables'),
('Potatoes', 'Vegetables');

INSERT IGNORE INTO retailers (name, code) VALUES
('Tesco', 'TSC'),
('Sainsbury\'s', 'SBR'),
('Asda', 'ASD'),
('Morrisons', 'MOR'),
('Waitrose', 'WTR'),
('Aldi', 'ALD'),
('Lidl', 'LDL'),
('Co-op', 'COP'),
('Iceland', 'ICE'),
('M&S', 'MNS');

INSERT IGNORE INTO customers (name, code) VALUES
('Restaurant Chain A', 'RCA'),
('Restaurant Chain B', 'RCB'),
('Hotel Group X', 'HGX'),
('Catering Company Y', 'CCY'),
('School District Z', 'SDZ'),
('Hospital Network', 'HN'),
('Corporate Canteen', 'CC'),
('Food Truck Fleet', 'FTF'),
('Local Restaurant', 'LR'),
('Cafe Chain', 'CFC');

INSERT IGNORE INTO pack_codes (code, description) VALUES
('PC001', 'Standard Pack'),
('PC002', 'Large Pack'),
('PC003', 'Family Pack'),
('PC004', 'Bulk Pack'),
('PC005', 'Premium Pack'),
('PC006', 'Organic Pack'),
('PC007', 'Free Range Pack'),
('PC008', 'Special Pack'),
('PC009', 'Seasonal Pack'),
('PC010', 'Limited Edition Pack');

-- Grant privileges to mobile user
GRANT SELECT ON microsearch.sample_descriptions TO 'mobile'@'%';
GRANT SELECT ON microsearch.retailers TO 'mobile'@'%';
GRANT SELECT ON microsearch.customers TO 'mobile'@'%';
GRANT SELECT ON microsearch.pack_codes TO 'mobile'@'%';

FLUSH PRIVILEGES;

-- Show completion status
SELECT 'Dropdown tables created successfully' AS status;
SELECT 'Sample data inserted' AS status;
SELECT 'Mobile user privileges granted' AS status;

-- Show table counts
SELECT 'sample_descriptions' AS table_name, COUNT(*) AS record_count FROM sample_descriptions
UNION ALL
SELECT 'retailers' AS table_name, COUNT(*) AS record_count FROM retailers
UNION ALL
SELECT 'customers' AS table_name, COUNT(*) AS record_count FROM customers
UNION ALL
SELECT 'pack_codes' AS table_name, COUNT(*) AS record_count FROM pack_codes;
