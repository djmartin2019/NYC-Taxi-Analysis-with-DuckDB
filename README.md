# NYC Taxi Data Analysis with DuckDB 🦆🚕

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![DuckDB](https://img.shields.io/badge/DuckDB-0.9+-green.svg)](https://duckdb.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Data](https://img.shields.io/badge/Data-NYC%20Taxi%202024-orange.svg)](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
[![Dashboard](https://img.shields.io/badge/Dashboard-Plotly%20Dash-purple.svg)](https://plotly.com/dash/)

A demonstration project showcasing DuckDB's capabilities for processing large-scale NYC taxi trip data. This project illustrates how DuckDB can efficiently process Parquet files and enable SQL analytics with minimal setup.

## 🎯 Project Overview

This project analyzes 12 months of NYC Yellow Taxi trip data (2024) using DuckDB, demonstrating how DuckDB can process large datasets directly from Parquet files without requiring a traditional database server.

### Key Features

- **DuckDB Analytics**: Process 12 months of taxi data using DuckDB's columnar engine
- **SQL-First Approach**: Analytics written in pure SQL leveraging DuckDB's capabilities
- **Interactive Dashboard**: Plotly-powered web dashboard with multiple analytical views
- **Modular Architecture**: Clean separation of concerns with dedicated modules for ingestion, queries, and visualization
- **Simple Setup**: Minimal configuration required to get started

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
- ~3GB free disk space for data files

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/djmartin2019/NYC_Taxi_DuckDB.git
   cd NYC_Taxi_DuckDB
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Download NYC Taxi Data**

   You'll need to download the data files from the official NYC TLC website:

   **Data Source**: [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

   **Required Files**:

   - **Yellow Taxi Trip Records**: Download 2024 monthly files (January through December)
     - Example: `yellow_tripdata_2024-01.parquet`, `yellow_tripdata_2024-02.parquet`, etc.
   - **Taxi Zone Lookup Table**: Download the CSV file
     - File: `taxi_zone_lookup.csv`

   **Download Instructions**:

   1. Visit the [NYC TLC Trip Record Data page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
   2. Navigate to the 2024 section
   3. Download all 12 monthly Yellow Taxi Trip Records (PARQUET format)
   4. Download the Taxi Zone Lookup Table (CSV format)
   5. Place all downloaded files in the `data/` directory

   **Expected file structure**:

   ```
   data/
   ├── taxi_zone_lookup.csv
   ├── yellow_tripdata_2024-01.parquet
   ├── yellow_tripdata_2024-02.parquet
   ├── yellow_tripdata_2024-03.parquet
   ├── yellow_tripdata_2024-04.parquet
   ├── yellow_tripdata_2024-05.parquet
   ├── yellow_tripdata_2024-06.parquet
   ├── yellow_tripdata_2024-07.parquet
   ├── yellow_tripdata_2024-08.parquet
   ├── yellow_tripdata_2024-09.parquet
   ├── yellow_tripdata_2024-10.parquet
   ├── yellow_tripdata_2024-11.parquet
   └── yellow_tripdata_2024-12.parquet
   ```

4. **Build the database**

   ```bash
   python scripts/run_pipeline.py
   ```

   This will create a DuckDB database with two tables:

   - `taxi`: Contains all trip records from the Parquet files
   - `TaxiZones`: Contains zone lookup information from the CSV file

5. **Launch the dashboard**

   ```bash
   python dashboard/app.py
   ```

6. **View the dashboard**
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

### DuckDB Benefits

This project demonstrates DuckDB's advantages:

- **Direct Parquet Processing**: No need to import data into a traditional database
- **SQL Analytics**: Familiar SQL syntax for complex analytical queries
- **Columnar Processing**: Efficient handling of analytical workloads
- **Embedded Database**: Runs as a library without requiring a database server

## 🔍 Analytics Examples

### Top Pickup Zones

```sql
SELECT
    z.zone AS pickup_zone,
    COUNT(*) AS pickups
FROM taxi t
JOIN TaxiZones z ON t."PULocationID" = z."LocationID"
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
JOIN TaxiZones z1 ON t."PULocationID" = z1."LocationID"
JOIN TaxiZones z2 ON t."DOLocationID" = z2."LocationID"
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

## 📊 Project Characteristics

- **Data Volume**: 12 months of NYC taxi data (~50M+ trips)
- **Database Size**: DuckDB file grows to ~2GB after processing
- **Setup Time**: Database creation takes a few minutes
- **Query Response**: Interactive queries respond quickly for dashboard use
- **Memory Usage**: Efficient columnar processing with reasonable memory footprint

## 🤝 Contributing

This is a demonstration project, but contributions are welcome! Feel free to submit a Pull Request for improvements.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [NYC Taxi & Limousine Commission](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) for providing the trip data
- DuckDB team for the embedded analytical database
- Plotly team for the visualization framework

## 📊 Data Source

This project uses publicly available data from the NYC Taxi & Limousine Commission (TLC). The data includes:

- **Yellow Taxi Trip Records**: Monthly trip data in Parquet format
- **Taxi Zone Lookup Table**: Zone metadata in CSV format

All data is available for download from the [official TLC Trip Record Data page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). The TLC notes that trip data was collected by authorized technology providers and they make no representations as to the accuracy of the data.

## 📞 Contact

Your Name - [@djmartin2019](https://x.com/djmartin2019) - djmartin2019@gmail.com

Project Link: [https://github.com/djmartin2019/NYC-Taxi-Analysis-with-DuckDB](https://github.com/djmartin2019/NYC-Taxi-Analysis-with-DuckDB)

---

⭐ Star this repository if you found it helpful!
