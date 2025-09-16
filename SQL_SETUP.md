# MySQL Database Setup - SQL Scripts

This directory contains SQL scripts to manually set up the MySQL database for the Microsearch Driver Capture app.

## Files Overview

| File | Purpose | Description |
|------|---------|-------------|
| `setup_complete.sql` | **Complete Setup** | One-file setup for database, tables, and user |
| `create_database.sql` | Database Only | Creates the `microsearch` database |
| `create_tables.sql` | Tables Only | Creates the `samples` table |
| `create_user.sql` | User Only | Creates the `mobile` user with limited privileges |

## Quick Setup (Recommended)

Run the complete setup script:

```bash
mysql -u root -p < setup_complete.sql
```

This will:
- Create the `microsearch` database
- Create the `samples` table with all required fields and indexes
- Create the `mobile` user with limited privileges
- Show verification information

## Step-by-Step Setup

If you prefer to run scripts individually:

### 1. Create Database
```bash
mysql -u root -p < create_database.sql
```

### 2. Create Tables
```bash
mysql -u root -p < create_tables.sql
```

### 3. Create User
```bash
mysql -u root -p < create_user.sql
```

## Database Schema

### Database: `microsearch`
- Character Set: `utf8mb4`
- Collation: `utf8mb4_unicode_ci`

### Table: `samples`

| Field | Type | Description |
|-------|------|-------------|
| `id` | CHAR(36) | UUID primary key (required) |
| `description` | TEXT | Sample description (required) |
| `size_kg` | DECIMAL(6,3) | Weight in kilograms |
| `use_by_date` | DATE | Expiry date (YYYY-MM-DD) |
| `pack_code` | TEXT | Package/batch code |
| `bird_temp_c` | DECIMAL(4,1) | Bird temperature (-5.0 to 20.0°C) |
| `customer` | TEXT | Customer name |
| `retailer` | TEXT | Retailer name (required) |
| `supplier` | TEXT | Supplier name (default: Flixton) |
| `code` | TEXT | Product code (default: GB S011) |
| `sample_number` | INT | Sample number (auto-increment per day) |
| `price_gbp` | DECIMAL(7,2) | Price in GBP (≥ 0) |
| `van_temp_c` | DECIMAL(4,1) | Van temperature (-5.0 to 20.0°C) |
| `created_at_local` | DATETIME | Local creation timestamp |
| `device_id` | VARCHAR(64) | Device identifier |
| `driver_id` | VARCHAR(64) | Driver identifier |
| `received_at_utc` | TIMESTAMP | Server receive timestamp (auto) |

### Indexes
- `idx_samples_created` - On `created_at_local`
- `idx_samples_device` - On `device_id`
- `idx_samples_driver` - On `driver_id`
- `idx_samples_sample_number` - On `sample_number`
- `idx_samples_retailer` - On `retailer` (first 50 chars)
- `idx_samples_supplier` - On `supplier` (first 50 chars)
- `idx_samples_received` - On `received_at_utc`

## User Privileges

### User: `mobile`
- **Password**: Change `mobile_password` in the SQL scripts
- **Host**: `%` (all hosts) - modify for security
- **Privileges**: 
  - `INSERT` - Add new samples
  - `SELECT` - Read existing samples
  - `UPDATE` - Update sample data

### Security Recommendations

1. **Change Default Password**: Update `mobile_password` in the SQL scripts
2. **Restrict Host Access**: Change `'%'` to specific IP ranges like `'192.168.1.%'`
3. **Use SSL**: Enable SSL connections for production
4. **Regular Backups**: Set up automated database backups

## Configuration

After running the SQL scripts, update your `config.json`:

```json
{
  "mysql": {
    "host": "192.168.1.10",
    "port": 3306,
    "user": "mobile",
    "password": "your_actual_password",
    "db": "microsearch"
  }
}
```

## Verification

After setup, verify the installation:

```sql
-- Connect to MySQL
mysql -u mobile -p microsearch

-- Check table exists
SHOW TABLES;

-- Check table structure
DESCRIBE samples;

-- Check user privileges
SHOW GRANTS FOR 'mobile'@'%';

-- Test insert (optional)
INSERT INTO samples (id, description, retailer, supplier, code, sample_number, created_at_local, device_id, driver_id) 
VALUES ('test-uuid-12345', 'Test Sample', 'Test Retailer', 'Flixton', 'GB S011', 1, NOW(), 'TEST_DEVICE', 'TEST_DRIVER');

-- Check the test record
SELECT * FROM samples WHERE id = 'test-uuid-12345';

-- Clean up test record
DELETE FROM samples WHERE id = 'test-uuid-12345';
```

## Troubleshooting

### Connection Issues
- Verify MySQL server is running
- Check firewall settings
- Confirm user credentials in `config.json`

### Permission Issues
- Ensure MySQL user has `CREATE DATABASE` and `CREATE TABLE` privileges
- Check user grants: `SHOW GRANTS FOR 'mobile'@'%';`

### Character Set Issues
- Verify database uses `utf8mb4` character set
- Check table collation: `SHOW CREATE TABLE samples;`

## Alternative: Use Python Setup Script

Instead of SQL scripts, you can use the Python setup script:

```bash
python launch.py --setup-mysql
```

This provides the same functionality with additional error handling and testing.
