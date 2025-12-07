import sqlite3
import sys
#type sa terminal og python sqlite_explorer.py

def explore_db(db_path):
    """Interactive SQLite database explorer"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"\n{'='*60}")
        print(f"SQLite Database: {db_path}")
        print(f"{'='*60}\n")
        
        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print("📊 Tables in database:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  ✓ {table_name:<25} ({count} rows)")
        
        print(f"\n{'='*60}")
        print("💡 Commands you can run:")
        print("  - To see table structure: PRAGMA table_info(table_name)")
        print("  - To query data: SELECT * FROM table_name LIMIT 10")
        print(f"{'='*60}\n")
        
        # Interactive mode
        while True:
            query = input("SQL> ").strip()
            
            if query.lower() in ['exit', 'quit', 'q', '.quit', '.exit']:
                print("Goodbye! 👋")
                break
            
            if not query:
                continue
                
            try:
                cursor.execute(query)
                
                if query.strip().upper().startswith('SELECT') or query.strip().upper().startswith('PRAGMA'):
                    results = cursor.fetchall()
                    
                    if results:
                        # Print column names
                        if cursor.description:
                            headers = [desc[0] for desc in cursor.description]
                            print("\n" + " | ".join(headers))
                            print("-" * (sum(len(h) for h in headers) + 3 * len(headers)))
                        
                        # Print rows
                        for row in results:
                            print(" | ".join(str(cell) for cell in row))
                        print(f"\n({len(results)} rows)\n")
                    else:
                        print("(No results)\n")
                else:
                    conn.commit()
                    print("✓ Query executed successfully\n")
                    
            except sqlite3.Error as e:
                print(f"❌ Error: {e}\n")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error opening database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        # Default to Python ecommerce database
        db_path = "E-Commerce-Order-Processing-System-Python/data/ecommerce.db"
    
    explore_db(db_path)
