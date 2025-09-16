-- Microsearch Driver Capture - User Creation Script
-- Creates a limited MySQL user for mobile app access

-- Create mobile user with limited privileges
-- Replace 'mobile_password' with your actual password
CREATE USER IF NOT EXISTS 'mobile'@'%' IDENTIFIED BY 'mobile_password';

-- Grant only necessary privileges for the mobile app
-- INSERT: Add new samples
-- SELECT: Read existing samples (for sync verification)
-- UPDATE: Update sample data if needed
GRANT INSERT, SELECT, UPDATE ON microsearch.samples TO 'mobile'@'%';

-- Optional: Grant privileges for specific IP ranges only
-- Uncomment and modify these lines for better security:
-- CREATE USER IF NOT EXISTS 'mobile'@'192.168.1.%' IDENTIFIED BY 'mobile_password';
-- GRANT INSERT, SELECT, UPDATE ON microsearch.samples TO 'mobile'@'192.168.1.%';

-- Apply privileges
FLUSH PRIVILEGES;

-- Show user creation confirmation
SELECT 'User mobile created successfully' AS status;

-- Show user privileges
SHOW GRANTS FOR 'mobile'@'%';
