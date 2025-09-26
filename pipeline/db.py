import duckdb
import os

DB_PATH = "db/taxi.duckdb"

def get_connection():
    """Get a database connection with proper error handling"""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database file not found: {DB_PATH}")
    return duckdb.connect(DB_PATH)

def run_query_file(filename):
    """Execute a SQL query from a file and return results as DataFrame"""
    try:
        with open(filename, "r") as f:
            query = f.read()
        
        con = get_connection()
        if con is None:
            raise ConnectionError("Failed to establish database connection")
            
        result = con.execute(query).fetchdf()
        con.close()
        return result
    except Exception as e:
        print(f"Error executing query from {filename}: {e}")
        raise
