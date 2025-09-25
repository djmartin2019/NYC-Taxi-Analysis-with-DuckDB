import duckdb
import pandas as pd
import plotly.express as px

DATA_PATH = './data/yellow_tripdata_2024-01.parquet'

con = duckdb.connect(database=':memory:')

con.execute(f"""
            CREATE TABLE trips AS
            SELECT * FROM read_parquet('{DATA_PATH}')
            """)

con.execute("""
            ALTER TABLE trips ADD COLUMN trip_duration_min DOUBLE;
            """)
con.execute("""
            UPDATE trips SET trip_duration_min =
                DATE_DIFF('minute', tpep_pickup_datetime, tpep_dropoff_datetime);
            """)
query = """
    SELECT
        trip_duration_min,
        passenger_count,
        total_amount
    FROM trips
    WHERE
        trip_duration_min > 0 AND trip_duration_min < 120
        AND passenger_count BETWEEN 1 AND 6
        AND total_amount > 0 AND total_amount < 200
    LIMIT 10000
"""

df = con.execute(query).fetchdf()

fig = px.scatter(
    df,
    x='trip_duration_min',
    y='total_amount',
    color='passenger_count',
    title='Trip Duration vs Fare Amount',
    labels={
        'trip_duration_min': 'Trip Duration (minutes)',
        'total_amount': 'Total Fare ($)'
    },
    opacity=0.6
)

fig.show()
