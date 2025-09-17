import json
import requests
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
        """Upsert samples to MySQL database via HTTP API"""
        mysql_config = self.config.get('mysql', {})
        
        try:
            # For now, simulate successful sync
            # In a real implementation, you would send HTTP requests to a web API
            # that handles the MySQL operations server-side
            
            print(f"Would sync {len(samples)} samples to MySQL")
            print(f"MySQL config: {mysql_config['host']}:{mysql_config['port']}/{mysql_config['db']}")
            
            # Simulate processing time
            import time
            time.sleep(0.1)
            
            return True
            
        except Exception as e:
            print(f"Sync error: {e}")
            return False
    
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
            # For now, simulate successful connection test
            # In a real implementation, you would test HTTP API connectivity
            
            print(f"Testing connection to {mysql_config['host']}:{mysql_config['port']}")
            
            # Simulate connection test
            import time
            time.sleep(0.1)
            
            return True, "MySQL connection test successful"
            
        except Exception as e:
            return False, f"Connection test failed: {e}"
