import sqlite3
import sys

def inspect_database(db_path='weather.db'):
    """Inspect SQLite database contents"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get table info
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"Tables: {tables}")
        
        for table in tables:
            print(f"\n=== Table: {table} ===")
            
            # Get column info
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            print("Columns:")
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
            
            # Get record count
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"\nTotal records: {count}")
            
            # Show sample data
            cursor.execute(f"SELECT * FROM {table} ORDER BY timestamp DESC LIMIT 5")
            rows = cursor.fetchall()
            print("\nLatest 5 records:")
            for row in rows:
                print(f"  {row}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'weather.db'
    inspect_database(db_path)