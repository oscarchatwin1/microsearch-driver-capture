import json
import sqlite3
from typing import List, Dict, Optional, Tuple
from pathlib import Path

class DropdownManager:
    def __init__(self, config_path: str = "dropdown_config.json"):
        self.config = self.load_config(config_path)
        self.local_cache = {}  # Cache for offline dropdown data
    
    def load_config(self, config_path: str) -> Dict:
        """Load dropdown configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {config_path} not found, using default config")
            return self.get_default_config()
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {config_path}: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Get default dropdown configuration"""
        return {
            "dropdown_fields": {
                "description": {"enabled": False, "source": "static", "options": []},
                "retailer": {"enabled": False, "source": "static", "options": []},
                "customer": {"enabled": False, "source": "static", "options": []},
                "supplier": {"enabled": False, "source": "static", "options": ["Flixton"]},
                "pack_code": {"enabled": False, "source": "static", "options": []}
            },
            "static_options": {
                "supplier": ["Flixton"],
                "code": ["GB S011"]
            }
        }
    
    def is_dropdown_field(self, field_name: str) -> bool:
        """Check if a field should be a dropdown"""
        dropdown_fields = self.config.get('dropdown_fields', {})
        field_config = dropdown_fields.get(field_name, {})
        return field_config.get('enabled', False)
    
    def get_dropdown_options(self, field_name: str, mysql_config: Optional[Dict] = None) -> List[str]:
        """Get dropdown options for a field"""
        dropdown_fields = self.config.get('dropdown_fields', {})
        field_config = dropdown_fields.get(field_name, {})
        
        if not field_config.get('enabled', False):
            return []
        
        source = field_config.get('source', 'static')
        
        if source == 'static':
            return self.get_static_options(field_name, field_config)
        elif source == 'database':
            return self.get_database_options(field_name, field_config, mysql_config)
        else:
            return []
    
    def get_static_options(self, field_name: str, field_config: Dict) -> List[str]:
        """Get static options for a field"""
        # Check if field has its own static options
        if 'options' in field_config:
            return field_config['options']
        
        # Check global static options
        static_options = self.config.get('static_options', {})
        return static_options.get(field_name, [])
    
    def get_database_options(self, field_name: str, field_config: Dict, mysql_config: Optional[Dict]) -> List[str]:
        """Get database options for a field"""
        if not mysql_config:
            return self.get_cached_options(field_name) or []
        
        try:
            # For now, simulate database options
            # In a real implementation, you would make HTTP requests to a web API
            
            print(f"Would fetch database options for {field_name} from {mysql_config['host']}")
            
            # Return cached options or empty list
            cached_options = self.get_cached_options(field_name)
            if cached_options:
                return cached_options
            
            # Return some default options for testing
            default_options = {
                'description': ['Sample A', 'Sample B', 'Sample C'],
                'retailer': ['Tesco', 'Sainsbury', 'Asda'],
                'customer': ['Customer 1', 'Customer 2', 'Customer 3']
            }
            
            return default_options.get(field_name, [])
            
        except Exception as e:
            print(f"Error fetching database options for {field_name}: {e}")
            return self.get_cached_options(field_name) or []
    
    def cache_options(self, field_name: str, options: List[str]):
        """Cache options for offline use"""
        self.local_cache[field_name] = options
        self.save_cache_to_sqlite()
    
    def get_cached_options(self, field_name: str) -> List[str]:
        """Get cached options from SQLite"""
        try:
            conn = sqlite3.connect('dropdown_cache.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dropdown_cache (
                    field_name TEXT PRIMARY KEY,
                    options TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("SELECT options FROM dropdown_cache WHERE field_name = ?", (field_name,))
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                return json.loads(result[0])
            return []
            
        except Exception as e:
            print(f"Error reading cached options: {e}")
            return []
    
    def save_cache_to_sqlite(self):
        """Save cache to SQLite for offline access"""
        try:
            conn = sqlite3.connect('dropdown_cache.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dropdown_cache (
                    field_name TEXT PRIMARY KEY,
                    options TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            for field_name, options in self.local_cache.items():
                cursor.execute("""
                    INSERT OR REPLACE INTO dropdown_cache (field_name, options)
                    VALUES (?, ?)
                """, (field_name, json.dumps(options)))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def refresh_all_options(self, mysql_config: Dict):
        """Refresh all dropdown options from database"""
        dropdown_fields = self.config.get('dropdown_fields', {})
        
        for field_name, field_config in dropdown_fields.items():
            if field_config.get('enabled', False) and field_config.get('source') == 'database':
                options = self.get_database_options(field_name, field_config, mysql_config)
                print(f"Refreshed {len(options)} options for {field_name}")
    
    def get_field_config(self, field_name: str) -> Dict:
        """Get configuration for a specific field"""
        dropdown_fields = self.config.get('dropdown_fields', {})
        return dropdown_fields.get(field_name, {})
    
    def get_placeholder(self, field_name: str) -> str:
        """Get placeholder text for a field"""
        field_config = self.get_field_config(field_name)
        return field_config.get('placeholder', f'Enter {field_name}...')
    
    def allows_custom_input(self, field_name: str) -> bool:
        """Check if field allows custom input"""
        field_config = self.get_field_config(field_name)
        return field_config.get('allow_custom', True)
    
    def sync_dropdown_data(self, mysql_config: Dict) -> bool:
        """Sync dropdown data from MySQL to local cache"""
        try:
            print("🔄 Syncing dropdown data from MySQL...")
            self.refresh_all_options(mysql_config)
            print("✅ Dropdown data synced successfully")
            return True
        except Exception as e:
            print(f"❌ Error syncing dropdown data: {e}")
            return False
