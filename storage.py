import sqlite3
import uuid
import json
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
import os

class StorageManager:
    def __init__(self, db_path: str = "samples.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables and indexes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create samples table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS samples (
                id TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                size_kg REAL,
                use_by_date TEXT,
                pack_code TEXT,
                bird_temp_c REAL,
                customer TEXT,
                retailer TEXT,
                supplier TEXT,
                code TEXT,
                sample_number INTEGER,
                price_gbp REAL,
                van_temp_c REAL,
                created_at_local TEXT,
                device_id TEXT,
                driver_id TEXT,
                sync_status TEXT,
                error_msg TEXT
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_samples_status ON samples(sync_status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_samples_created ON samples(created_at_local)")
        
        conn.commit()
        conn.close()
    
    def validate_sample(self, sample_data: Dict) -> Tuple[bool, str]:
        """Validate sample data according to business rules"""
        errors = []
        
        # Required fields
        if not sample_data.get('description'):
            errors.append("Description is required")
        if not sample_data.get('retailer'):
            errors.append("Retailer is required")
        if not sample_data.get('sample_number'):
            errors.append("Sample number is required")
        
        # Temperature validation (-5.0 to 20.0 °C)
        bird_temp = sample_data.get('bird_temp_c')
        if bird_temp is not None:
            try:
                bird_temp = float(bird_temp)
                if bird_temp < -5.0 or bird_temp > 20.0:
                    errors.append("Bird temperature must be between -5.0 and 20.0 °C")
            except (ValueError, TypeError):
                errors.append("Bird temperature must be a valid number")
        
        van_temp = sample_data.get('van_temp_c')
        if van_temp is not None:
            try:
                van_temp = float(van_temp)
                if van_temp < -5.0 or van_temp > 20.0:
                    errors.append("Van temperature must be between -5.0 and 20.0 °C")
            except (ValueError, TypeError):
                errors.append("Van temperature must be a valid number")
        
        # Price validation (>= 0)
        price = sample_data.get('price_gbp')
        if price is not None:
            try:
                price = float(price)
                if price < 0:
                    errors.append("Price must be >= 0")
            except (ValueError, TypeError):
                errors.append("Price must be a valid number")
        
        # Size validation (>= 0)
        size = sample_data.get('size_kg')
        if size is not None:
            try:
                size = float(size)
                if size < 0:
                    errors.append("Size must be >= 0")
            except (ValueError, TypeError):
                errors.append("Size must be a valid number")
        
        # Use-by date validation (today to +60 days)
        use_by = sample_data.get('use_by_date')
        if use_by:
            try:
                if isinstance(use_by, str):
                    use_by_date = datetime.strptime(use_by, '%Y-%m-%d').date()
                else:
                    use_by_date = use_by
                
                today = date.today()
                max_date = today + timedelta(days=60)
                
                if use_by_date < today:
                    errors.append("Use-by date cannot be in the past")
                elif use_by_date > max_date:
                    errors.append("Use-by date cannot be more than 60 days in the future")
            except (ValueError, TypeError):
                errors.append("Use-by date must be in YYYY-MM-DD format")
        
        return len(errors) == 0, "; ".join(errors)
    
    def get_next_sample_number(self) -> int:
        """Get next sample number for today (auto-increment per day)"""
        today = date.today().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT MAX(sample_number) FROM samples 
            WHERE DATE(created_at_local) = ?
        """, (today,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result[0] is None:
            return 1
        else:
            return result[0] + 1
    
    def create_sample(self, sample_data: Dict) -> Tuple[bool, str]:
        """Create a new sample with validation"""
        # Validate data
        is_valid, error_msg = self.validate_sample(sample_data)
        if not is_valid:
            return False, error_msg
        
        # Generate UUID if not provided
        if 'id' not in sample_data:
            sample_data['id'] = str(uuid.uuid4())
        
        # Set defaults
        sample_data.setdefault('supplier', 'Flixton')
        sample_data.setdefault('code', 'GB S011')
        sample_data.setdefault('sync_status', 'pending')
        sample_data.setdefault('created_at_local', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # Auto-increment sample number if not provided
        if not sample_data.get('sample_number'):
            sample_data['sample_number'] = self.get_next_sample_number()
        
        # Insert into database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO samples (
                    id, description, size_kg, use_by_date, pack_code, bird_temp_c,
                    customer, retailer, supplier, code, sample_number, price_gbp,
                    van_temp_c, created_at_local, device_id, driver_id, sync_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sample_data['id'], sample_data['description'], sample_data.get('size_kg'),
                sample_data.get('use_by_date'), sample_data.get('pack_code'),
                sample_data.get('bird_temp_c'), sample_data.get('customer'),
                sample_data['retailer'], sample_data['supplier'], sample_data['code'],
                sample_data['sample_number'], sample_data.get('price_gbp'),
                sample_data.get('van_temp_c'), sample_data['created_at_local'],
                sample_data.get('device_id'), sample_data.get('driver_id'),
                sample_data['sync_status']
            ))
            
            conn.commit()
            return True, "Sample created successfully"
            
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        finally:
            conn.close()
    
    def get_samples(self, status_filter: Optional[str] = None, limit: int = 200) -> List[Dict]:
        """Get samples with optional status filter"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if status_filter:
            cursor.execute("""
                SELECT * FROM samples WHERE sync_status = ? 
                ORDER BY created_at_local DESC LIMIT ?
            """, (status_filter, limit))
        else:
            cursor.execute("""
                SELECT * FROM samples ORDER BY created_at_local DESC LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_sample_by_id(self, sample_id: str) -> Optional[Dict]:
        """Get a specific sample by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM samples WHERE id = ?", (sample_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def update_sample(self, sample_id: str, sample_data: Dict) -> Tuple[bool, str]:
        """Update an existing sample"""
        # Validate data
        is_valid, error_msg = self.validate_sample(sample_data)
        if not is_valid:
            return False, error_msg
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE samples SET
                    description = ?, size_kg = ?, use_by_date = ?, pack_code = ?,
                    bird_temp_c = ?, customer = ?, retailer = ?, supplier = ?,
                    code = ?, sample_number = ?, price_gbp = ?, van_temp_c = ?
                WHERE id = ?
            """, (
                sample_data['description'], sample_data.get('size_kg'),
                sample_data.get('use_by_date'), sample_data.get('pack_code'),
                sample_data.get('bird_temp_c'), sample_data.get('customer'),
                sample_data['retailer'], sample_data['supplier'], sample_data['code'],
                sample_data['sample_number'], sample_data.get('price_gbp'),
                sample_data.get('van_temp_c'), sample_id
            ))
            
            conn.commit()
            return True, "Sample updated successfully"
            
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        finally:
            conn.close()
    
    def delete_sample(self, sample_id: str) -> Tuple[bool, str]:
        """Delete a sample (only if pending)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if sample exists and is pending
            cursor.execute("SELECT sync_status FROM samples WHERE id = ?", (sample_id,))
            result = cursor.fetchone()
            
            if not result:
                return False, "Sample not found"
            
            if result[0] != 'pending':
                return False, "Can only delete pending samples"
            
            cursor.execute("DELETE FROM samples WHERE id = ?", (sample_id,))
            conn.commit()
            return True, "Sample deleted successfully"
            
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        finally:
            conn.close()
    
    def mark_samples_synced(self, sample_ids: List[str]) -> bool:
        """Mark samples as synced"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            placeholders = ','.join(['?' for _ in sample_ids])
            cursor.execute(f"""
                UPDATE samples SET sync_status = 'synced', error_msg = NULL 
                WHERE id IN ({placeholders})
            """, sample_ids)
            
            conn.commit()
            return True
            
        except sqlite3.Error:
            return False
        finally:
            conn.close()
    
    def mark_samples_error(self, sample_ids: List[str], error_message: str) -> bool:
        """Mark samples as having sync error"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            placeholders = ','.join(['?' for _ in sample_ids])
            cursor.execute(f"""
                UPDATE samples SET sync_status = 'error', error_msg = ? 
                WHERE id IN ({placeholders})
            """, [error_message] + sample_ids)
            
            conn.commit()
            return True
            
        except sqlite3.Error:
            return False
        finally:
            conn.close()
    
    def get_sample_counts(self) -> Dict[str, int]:
        """Get counts of samples by status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT sync_status, COUNT(*) FROM samples GROUP BY sync_status
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        counts = {'pending': 0, 'synced': 0, 'error': 0}
        for status, count in results:
            counts[status] = count
        
        return counts
