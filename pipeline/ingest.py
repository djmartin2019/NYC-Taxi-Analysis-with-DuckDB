import duckdb

def create_db():
    con = duckdb.connect("./db/taxi.duckdb")
    con.execute("""
        CREATE OR REPLACE TABLE taxi AS
        SELECT * FROM read_parquet('data/yellow_tripdata_2024-*.parquet')
        WHERE DATE_PART('year', tpep_pickup_datetime) = 2024
    """)
    con.execute("""
        CREATE OR REPLACE TABLE TaxiZones AS
        SELECT * FROM read_csv_auto('data/taxi_zone_lookup.csv', HEADER=TRUE)
    """)
    con.close()
