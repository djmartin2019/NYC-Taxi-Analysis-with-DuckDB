# NYC Taxi Data Analysis with DuckDB 🦆🚕

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![DuckDB](https://img.shields.io/badge/DuckDB-0.9+-green.svg)](https://duckdb.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Data](https://img.shields.io/badge/Data-NYC%20Taxi%202024-orange.svg)](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
[![Dashboard](https://img.shields.io/badge/Dashboard-Plotly%20Dash-purple.svg)](https://plotly.com/dash/)

A comprehensive data analytics project demonstrating DuckDB's capabilities for processing large-scale NYC taxi trip data. This project showcases modern data engineering practices with SQL-powered analytics, interactive visualizations, and a clean modular architecture.

## 🎯 Project Overview

This project analyzes 12 months of NYC Yellow Taxi trip data (2024) using DuckDB, a high-performance analytical database. It demonstrates how DuckDB can efficiently process large Parquet files and enable complex SQL analytics without the overhead of traditional database systems.

### Key Features

- **High-Performance Analytics**: Process 12 months of taxi data using DuckDB's columnar engine
- **SQL-First Approach**: Complex analytics written in pure SQL for maximum performance
- **Interactive Dashboard**: Plotly-powered web dashboard with multiple analytical views
- **Modular Architecture**: Clean separation of concerns with dedicated modules for ingestion, queries, and visualization
- **Production-Ready**: Proper error handling, connection management, and scalable design

## 📊 Analytics Capabilities

The project provides insights into:

- **Pickup/Dropoff Patterns**: Most popular taxi zones and routes
- **Tip Analysis**: Average tipping behavior by location
- **Airport Traffic**: Volume and patterns for airport trips
- **Travel Duration**: Average trip times between zone pairs
- **Route Popularity**: Most frequent pickup-dropoff combinations

## 🏗️ Project Structure

```
NYC_Taxi_DuckDB/
├── data/                    # Raw data files
│   ├── taxi_zone_lookup.csv # Zone metadata
│   └── yellow_tripdata_2024-*.parquet  # Monthly trip data
├── db/                      # DuckDB database
│   └── taxi.duckdb         # Main database file
├── pipeline/               # Data processing modules
│   ├── ingest.py          # Database creation and data loading
│   └── db.py              # Database connection utilities
├── queries/               # SQL analytics queries
│   ├── airports.sql       # Airport traffic analysis
│   ├── durations.sql      # Travel time analysis
│   ├── pairs.sql          # Popular route pairs
│   ├── pickups.sql        # Top pickup zones
│   └── tips.sql           # Tip analysis by zone
├── dashboard/             # Web dashboard
│   └── app.py             # Plotly Dash application
└── scripts/               # Utility scripts
    └── run_pipeline.py    # Pipeline execution script
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/NYC_Taxi_DuckDB.git
   cd NYC_Taxi_DuckDB
   ```

2. **Install dependencies**

   ```bash
   pip install duckdb dash plotly pandas
   ```

3. **Build the database**

   ```bash
   python scripts/run_pipeline.py
   ```

4. **Launch the dashboard**

   ```bash
   python dashboard/app.py
   ```

5. **View the dashboard**
   Open your browser to `http://127.0.0.1:8050`

## 📈 Data Pipeline

### Data Ingestion

The pipeline processes 12 months of NYC Yellow Taxi data (2024) stored as Parquet files:

```python
# Creates optimized DuckDB tables from Parquet files
CREATE OR REPLACE TABLE taxi AS
SELECT * FROM read_parquet('data/yellow_tripdata_2024-*.parquet')
WHERE DATE_PART('year', tpep_pickup_datetime) = 2024
```

### Database Schema

- **taxi**: Main trip data table with ~50M+ records
- **TaxiZones**: Zone lookup table with location metadata

### Query Performance

DuckDB's columnar engine enables:

- **Fast aggregations** on large datasets
- **Efficient joins** between trip and zone data
- **Complex analytical queries** with subqueries and CTEs
- **Memory-efficient processing** of Parquet files

## 🔍 Analytics Examples

### Top Pickup Zones

```sql
SELECT
    z.zone AS pickup_zone,
    COUNT(*) AS pickups
FROM taxi t
JOIN taxizones z ON t."PULocationID" = z."LocationID"
GROUP BY pickup_zone
ORDER BY pickups DESC;
```

### Airport Traffic Analysis

```sql
SELECT
    CASE
        WHEN z1.zone LIKE '%Airport%' THEN z1.zone
        WHEN z2.zone LIKE '%Airport%' THEN z2.zone
        ELSE 'None' END AS airport_zone,
    COUNT(*) AS trips
FROM taxi t
JOIN taxizones z1 ON t."PULocationID" = z1."LocationID"
JOIN taxizones z2 ON t."DOLocationID" = z2."LocationID"
WHERE z1.zone LIKE '%Airport%' OR z2.zone LIKE '%Airport%'
GROUP BY airport_zone
ORDER BY trips DESC;
```

## 🎨 Dashboard Features

The interactive dashboard provides five analytical views:

1. **Top Pickups**: Bar chart of most popular pickup zones
2. **Average Tips**: Tip analysis by pickup location
3. **Popular Routes**: Most frequent pickup-dropoff pairs
4. **Airport Traffic**: Volume analysis for airport trips
5. **Travel Duration**: Average trip times between zones

## 🛠️ Technical Stack

- **DuckDB**: High-performance analytical database
- **Python**: Core application language
- **SQL**: Analytics and data processing
- **Plotly Dash**: Interactive web dashboard
- **Parquet**: Efficient columnar data format

## 📊 Performance Characteristics

- **Data Volume**: 12 months of NYC taxi data (~50M+ trips)
- **Processing Time**: Database creation in under 2 minutes
- **Query Performance**: Sub-second response times for complex analytics
- **Memory Usage**: Efficient columnar processing with minimal memory footprint

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NYC Taxi & Limousine Commission for providing the trip data
- DuckDB team for the excellent analytical database
- Plotly team for the powerful visualization framework

## 📞 Contact

Your Name - [@djmartin2019](https://x.com/djmartin2019) - djmartin2019@gmail.com

Project Link: [https://github.com/djmartin2019/NYC_Taxi_DuckDB](https://github.com/djmartin2019/NYC_Taxi_DuckDB)

---

⭐ Star this repository if you found it helpful!
