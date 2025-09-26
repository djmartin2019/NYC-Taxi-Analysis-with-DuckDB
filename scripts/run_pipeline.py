from pipeline.ingest import create_db

if __name__ == "__main__":
    print("Creating DuckDB database...")
    create_db()
    print("Done.")
