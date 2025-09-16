#!/usr/bin/env python3
"""
Test script for Microsearch Driver Capture app
Tests core functionality without requiring Android/Kivy
"""

import json
import uuid
from datetime import datetime, date, timedelta
from storage import StorageManager
from syncer import SyncManager

def test_storage():
    """Test SQLite storage functionality"""
    print("Testing Storage Manager...")
    
    # Initialize storage
    storage = StorageManager("test_samples.db")
    
    # Test sample creation
    sample_data = {
        'description': 'Test Sample',
        'size_kg': 1.5,
        'use_by_date': (date.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
        'pack_code': 'TEST001',
        'bird_temp_c': 4.0,
        'customer': 'Test Customer',
        'retailer': 'Test Retailer',
        'supplier': 'Flixton',
        'code': 'GB S011',
        'sample_number': 1,
        'price_gbp': 10.50,
        'van_temp_c': 2.0,
        'device_id': 'TEST_DEVICE',
        'driver_id': 'TEST_DRIVER'
    }
    
    # Test validation
    is_valid, error_msg = storage.validate_sample(sample_data)
    print(f"Sample validation: {is_valid}")
    if not is_valid:
        print(f"Validation error: {error_msg}")
        return False
    
    # Test creation
    success, message = storage.create_sample(sample_data)
    print(f"Sample creation: {success} - {message}")
    
    if success:
        # Test retrieval
        samples = storage.get_samples()
        print(f"Retrieved {len(samples)} samples")
        
        if samples:
            sample = samples[0]
            print(f"Sample ID: {sample['id']}")
            print(f"Description: {sample['description']}")
            print(f"Sync Status: {sample['sync_status']}")
        
        # Test counts
        counts = storage.get_sample_counts()
        print(f"Sample counts: {counts}")
        
        # Test next sample number
        next_num = storage.get_next_sample_number()
        print(f"Next sample number: {next_num}")
    
    return success

def test_validation():
    """Test validation rules"""
    print("\nTesting Validation Rules...")
    
    storage = StorageManager("test_samples.db")
    
    # Test invalid temperatures
    invalid_sample = {
        'description': 'Invalid Temp',
        'retailer': 'Test Retailer',
        'sample_number': 1,
        'bird_temp_c': 25.0,  # Too high
        'van_temp_c': -10.0    # Too low
    }
    
    is_valid, error_msg = storage.validate_sample(invalid_sample)
    print(f"Invalid temperature validation: {is_valid}")
    print(f"Error message: {error_msg}")
    
    # Test invalid date
    invalid_date_sample = {
        'description': 'Invalid Date',
        'retailer': 'Test Retailer',
        'sample_number': 1,
        'use_by_date': (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')  # Past date
    }
    
    is_valid, error_msg = storage.validate_sample(invalid_date_sample)
    print(f"Invalid date validation: {is_valid}")
    print(f"Error message: {error_msg}")
    
    # Test negative price
    invalid_price_sample = {
        'description': 'Invalid Price',
        'retailer': 'Test Retailer',
        'sample_number': 1,
        'price_gbp': -5.0  # Negative price
    }
    
    is_valid, error_msg = storage.validate_sample(invalid_price_sample)
    print(f"Invalid price validation: {is_valid}")
    print(f"Error message: {error_msg}")

def test_syncer():
    """Test sync manager functionality"""
    print("\nTesting Sync Manager...")
    
    try:
        syncer = SyncManager("config.json")
        
        # Test config loading
        print(f"Allowed SSIDs: {syncer.config.get('allowed_ssids', [])}")
        print(f"MySQL host: {syncer.config.get('mysql', {}).get('host', 'Not configured')}")
        
        # Test SSID checking (will return None on non-Android)
        current_ssid = syncer.get_current_ssid()
        print(f"Current SSID: {current_ssid}")
        
        is_allowed = syncer.is_ssid_allowed(current_ssid)
        print(f"SSID allowed: {is_allowed}")
        
        # Test status
        status = syncer.get_sync_status()
        print(f"Sync status: {status}")
        
        return True
        
    except Exception as e:
        print(f"Sync manager test failed: {e}")
        return False

def test_config():
    """Test configuration file"""
    print("\nTesting Configuration...")
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        print(f"Config loaded successfully")
        print(f"Allowed SSIDs: {config.get('allowed_ssids', [])}")
        print(f"Default supplier: {config.get('defaults', {}).get('supplier', 'Not set')}")
        print(f"Default code: {config.get('defaults', {}).get('code', 'Not set')}")
        
        return True
        
    except Exception as e:
        print(f"Config test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Microsearch Driver Capture - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_config),
        ("Storage Manager", test_storage),
        ("Validation Rules", test_validation),
        ("Sync Manager", test_syncer)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"{test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("Test Results:")
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
    
    # Cleanup test database
    import os
    if os.path.exists("test_samples.db"):
        os.remove("test_samples.db")
        print("\nCleaned up test database")

if __name__ == "__main__":
    main()
