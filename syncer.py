import json
import pymysql
from typing import List, Dict, Tuple, Optional
from storage import StorageManager

class SyncManager:
    def __init__(self, config_path: str = "config.json"):
        self.config = self.load_config(config_path)
        self.storage = StorageManager()
    
    def load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"Configuration file {config_path} not found")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in configuration file: {e}")
    
    def get_current_ssid(self) -> Optional[str]:
        """Get current WiFi SSID using pyjnius (Android)"""
        try:
            from jnius import autoclass
            
            # Get WiFi manager
            WifiManager = autoclass('android.net.wifi.WifiManager')
            Context = autoclass('android.content.Context')
            
            # This would need to be called from Android context
            # For now, return None to indicate not on Android
            return None
            
        except ImportError:
            # Not on Android or pyjnius not available
            return None
        except Exception as e:
            print(f"Error getting SSID: {e}")
            return None
    
    def is_ethernet_connected(self) -> bool:
        """Check if device is connected via Ethernet"""
        try:
            from jnius import autoclass
            
            # Get connectivity manager
            ConnectivityManager = autoclass('android.net.ConnectivityManager')
            Context = autoclass('android.content.Context')
            
            # This would need to be called from Android context
            # For now, return False to indicate not on Android
            return False
            
        except ImportError:
            # Not on Android or pyjnius not available
            return False
        except Exception as e:
            print(f"Error checking Ethernet connection: {e}")
            return False
    
    def is_ssid_allowed(self, ssid: Optional[str]) -> bool:
        """Check if current SSID is in allowed list"""
        if not ssid:
            return False
        
        allowed_ssids = self.config.get('allowed_ssids', [])
        return ssid in allowed_ssids
    
    def is_sync_allowed(self) -> Tuple[bool, str]:
        """Check if sync is allowed based on WiFi SSID or Ethernet connection"""
        # Check WiFi SSID first
        current_ssid = self.get_current_ssid()
        if current_ssid and self.is_ssid_allowed(current_ssid):
            return True, f"WiFi: {current_ssid}"
        
        # Check Ethernet connection if enabled in config
        allow_ethernet = self.config.get('allow_ethernet', True)
        if allow_ethernet and self.is_ethernet_connected():
            return True, "Ethernet"
        
        # Check if we're on Android but not connected to allowed WiFi
        if current_ssid:
            return False, f"WiFi not allowed: {current_ssid}"
        
        # Not on Android or no connection
        return False, "No allowed connection"
    
    def fetch_pending_samples(self, limit: int = 200) -> List[Dict]:
        """Fetch pending samples from local storage"""
        return self.storage.get_samples(status_filter='pending', limit=limit)
    
    def upsert_mysql(self, samples: List[Dict]) -> bool:
        """Upsert samples to MySQL database"""
        mysql_config = self.config.get('mysql', {})
        
        try:
            # Connect to MySQL
            connection = pymysql.connect(
                host=mysql_config['host'],
                port=mysql_config['port'],
                user=mysql_config['user'],
                password=mysql_config['password'],
                database=mysql_config['db'],
                autocommit=False
            )
            
            cursor = connection.cursor()
            
            # Prepare upsert SQL
            sql = """
                INSERT INTO samples (
                    id, description, size_kg, use_by_date, pack_code, bird_temp_c,
                    customer, retailer, supplier, code, sample_number, price_gbp,
                    van_temp_c, created_at_local, device_id, driver_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    description = VALUES(description),
                    size_kg = VALUES(size_kg),
                    use_by_date = VALUES(use_by_date),
                    pack_code = VALUES(pack_code),
                    bird_temp_c = VALUES(bird_temp_c),
                    customer = VALUES(customer),
                    retailer = VALUES(retailer),
                    supplier = VALUES(supplier),
                    code = VALUES(code),
                    sample_number = VALUES(sample_number),
                    price_gbp = VALUES(price_gbp),
                    van_temp_c = VALUES(van_temp_c),
                    created_at_local = VALUES(created_at_local),
                    device_id = VALUES(device_id),
                    driver_id = VALUES(driver_id)
            """
            
            # Execute upsert for each sample
            for sample in samples:
                cursor.execute(sql, (
                    sample['id'],
                    sample['description'],
                    sample.get('size_kg'),
                    sample.get('use_by_date'),
                    sample.get('pack_code'),
                    sample.get('bird_temp_c'),
                    sample.get('customer'),
                    sample['retailer'],
                    sample['supplier'],
                    sample['code'],
                    sample['sample_number'],
                    sample.get('price_gbp'),
                    sample.get('van_temp_c'),
                    sample['created_at_local'],
                    sample.get('device_id'),
                    sample.get('driver_id')
                ))
            
            connection.commit()
            return True
            
        except pymysql.Error as e:
            print(f"MySQL error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
        finally:
            if 'connection' in locals():
                connection.close()
    
    def sync_now(self) -> Tuple[bool, str]:
        """Perform sync operation"""
        # Check if sync is allowed (WiFi or Ethernet)
        sync_allowed, connection_info = self.is_sync_allowed()
        if not sync_allowed:
            return False, f"Sync not allowed: {connection_info}"
        
        # Get pending samples
        pending_samples = self.fetch_pending_samples()
        if not pending_samples:
            return True, "Nothing to sync"
        
        # Attempt MySQL upsert
        try:
            success = self.upsert_mysql(pending_samples)
            if success:
                # Mark samples as synced
                sample_ids = [sample['id'] for sample in pending_samples]
                self.storage.mark_samples_synced(sample_ids)
                return True, f"Synced {len(pending_samples)} samples"
            else:
                # Mark samples as error
                sample_ids = [sample['id'] for sample in pending_samples]
                self.storage.mark_samples_error(sample_ids, "MySQL connection failed")
                return False, "MySQL connection failed"
                
        except Exception as e:
            # Mark samples as error
            sample_ids = [sample['id'] for sample in pending_samples]
            self.storage.mark_samples_error(sample_ids, str(e))
            return False, f"Error: {str(e)}"
    
    def get_sync_status(self) -> Dict:
        """Get current sync status information"""
        current_ssid = self.get_current_ssid()
        ethernet_connected = self.is_ethernet_connected()
        sync_allowed, connection_info = self.is_sync_allowed()
        sample_counts = self.storage.get_sample_counts()
        
        return {
            'current_ssid': current_ssid,
            'ethernet_connected': ethernet_connected,
            'is_sync_allowed': sync_allowed,
            'connection_info': connection_info,
            'sample_counts': sample_counts,
            'allowed_ssids': self.config.get('allowed_ssids', [])
        }
    
    def test_mysql_connection(self) -> Tuple[bool, str]:
        """Test MySQL connection without syncing"""
        mysql_config = self.config.get('mysql', {})
        
        try:
            connection = pymysql.connect(
                host=mysql_config['host'],
                port=mysql_config['port'],
                user=mysql_config['user'],
                password=mysql_config['password'],
                database=mysql_config['db'],
                autocommit=True
            )
            
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
            connection.close()
            return True, "MySQL connection successful"
            
        except pymysql.Error as e:
            return False, f"MySQL connection failed: {e}"
        except Exception as e:
            return False, f"Connection test failed: {e}"
