#!/usr/bin/env python3
"""
MySQL Database Setup Script for Microsearch Driver Capture
Creates the required database and tables automatically
"""

import json
import pymysql
import sys
from pathlib import Path

def load_config():
    """Load configuration from config.json"""
    config_path = Path('config.json')
    if not config_path.exists():
        print("❌ config.json not found!")
        print("Please create config.json first")
        return None
    
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config.json: {e}")
        return None
    except Exception as e:
        print(f"❌ Error reading config.json: {e}")
        return None

def create_database_and_tables():
    """Create MySQL database and tables"""
    config = load_config()
    if not config:
        return False
    
    mysql_config = config.get('mysql', {})
    if not mysql_config:
        print("❌ MySQL configuration not found in config.json")
        return False
    
    # Extract connection details
    host = mysql_config.get('host')
    port = mysql_config.get('port', 3306)
    user = mysql_config.get('user')
    password = mysql_config.get('password')
    db_name = mysql_config.get('db')
    
    if not all([host, user, password, db_name]):
        print("❌ Missing required MySQL configuration:")
        missing = []
        if not host: missing.append('host')
        if not user: missing.append('user')
        if not password: missing.append('password')
        if not db_name: missing.append('db')
        print(f"Missing: {', '.join(missing)}")
        return False
    
    print(f"Setting up MySQL database: {db_name}")
    print(f"Host: {host}:{port}")
    print(f"User: {user}")
    
    try:
        # Connect to MySQL server (without specifying database)
        print("Connecting to MySQL server...")
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset='utf8mb4',
            autocommit=True
        )
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        print(f"Creating database '{db_name}' if it doesn't exist...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"Database '{db_name}' ready")
        
        # Select the database
        cursor.execute(f"USE `{db_name}`")
        
        # Create samples table
        print("Creating samples table...")
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS samples (
            id CHAR(36) PRIMARY KEY,
            description TEXT NOT NULL,
            size_kg DECIMAL(6,3),
            use_by_date DATE,
            pack_code TEXT,
            bird_temp_c DECIMAL(4,1),
            customer TEXT,
            retailer TEXT,
            supplier TEXT,
            code TEXT,
            sample_number INT,
            price_gbp DECIMAL(7,2),
            van_temp_c DECIMAL(4,1),
            created_at_local DATETIME,
            device_id VARCHAR(64),
            driver_id VARCHAR(64),
            received_at_utc TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_samples_created (created_at_local),
            INDEX idx_samples_device (device_id),
            INDEX idx_samples_driver (driver_id),
            INDEX idx_samples_sample_number (sample_number)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        cursor.execute(create_table_sql)
        print("Samples table created successfully")
        
        # Check if table was created and show structure
        cursor.execute("DESCRIBE samples")
        columns = cursor.fetchall()
        
        print("\nTable structure:")
        print("-" * 80)
        print(f"{'Field':<20} {'Type':<20} {'Null':<8} {'Key':<8} {'Default':<15}")
        print("-" * 80)
        for column in columns:
            field, type_info, null, key, default, extra = column
            print(f"{field:<20} {type_info:<20} {null:<8} {key:<8} {str(default):<15}")
        
        # Test insert/select to verify table works
        print("\nTesting table functionality...")
        test_id = "test-uuid-12345-67890-abcdef"
        
        # Insert test record
        cursor.execute("""
            INSERT INTO samples (
                id, description, retailer, supplier, code, sample_number,
                created_at_local, device_id, driver_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            test_id, "Test Sample", "Test Retailer", "Flixton", "GB S011",
            999, "2024-01-01 12:00:00", "TEST_DEVICE", "TEST_DRIVER"
        ))
        
        # Select test record
        cursor.execute("SELECT id, description, retailer FROM samples WHERE id = %s", (test_id,))
        result = cursor.fetchone()
        
        if result:
            print(f"Test record inserted and retrieved: {result}")
        else:
            print("Test record not found")
            return False
        
        # Clean up test record
        cursor.execute("DELETE FROM samples WHERE id = %s", (test_id,))
        print("Test record cleaned up")
        
        # Show current record count
        cursor.execute("SELECT COUNT(*) FROM samples")
        count = cursor.fetchone()[0]
        print(f"Current records in table: {count}")
        
        connection.close()
        print("\nMySQL database setup completed successfully!")
        print(f"Database: {db_name}")
        print(f"Table: samples")
        print("Ready for mobile app sync!")
        
        return True
        
    except pymysql.Error as e:
        print(f"MySQL error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check MySQL server is running")
        print("2. Verify host, port, user, and password in config.json")
        print("3. Ensure user has CREATE DATABASE and CREATE TABLE privileges")
        print("4. Check firewall settings if connecting to remote MySQL")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def show_sample_data():
    """Show sample data structure for reference"""
    print("\nSample Data Structure:")
    print("=" * 50)
    print("Required fields:")
    print("  - id: UUID (auto-generated)")
    print("  - description: Sample description")
    print("  - retailer: Retailer name")
    print("  - sample_number: Auto-increment per day")
    print("")
    print("Optional fields:")
    print("  - size_kg: Weight in kilograms")
    print("  - use_by_date: Expiry date (YYYY-MM-DD)")
    print("  - pack_code: Package code")
    print("  - bird_temp_c: Bird temperature (-5.0 to 20.0 °C)")
    print("  - customer: Customer name")
    print("  - supplier: Supplier (default: Flixton)")
    print("  - code: Product code (default: GB S011)")
    print("  - price_gbp: Price in GBP")
    print("  - van_temp_c: Van temperature (-5.0 to 20.0 °C)")
    print("  - device_id: Device identifier")
    print("  - driver_id: Driver identifier")

def main():
    """Main setup function"""
    print("Microsearch Driver Capture - MySQL Database Setup")
    print("=" * 55)
    
    # Check if config exists
    if not Path('config.json').exists():
        print("config.json not found!")
        print("Please create config.json with MySQL configuration first.")
        print("\nExample config.json:")
        print("""
{
  "allowed_ssids": ["MicrosearchOps", "MicrosearchGuest"],
  "mysql": {
    "host": "192.168.1.10",
    "port": 3306,
    "user": "mobile",
    "password": "your_password",
    "db": "microsearch"
  },
  "defaults": {
    "supplier": "Flixton",
    "code": "GB S011"
  },
  "device_id": "DEVICE_001",
  "driver_id": "DRIVER_001"
}
        """)
        return
    
    # Create database and tables
    success = create_database_and_tables()
    
    if success:
        show_sample_data()
        print("\nSetup complete! You can now:")
        print("1. Run the mobile app: python launch.py --app")
        print("2. Test sync functionality")
        print("3. Build Android APK: python launch.py --build")
    else:
        print("\nSetup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
