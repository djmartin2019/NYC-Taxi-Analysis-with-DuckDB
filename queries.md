# NYC Taxi SQL Queries

## Most Popular Pickup & Dropoff Zones
```SQL
    SELECT
      z.zone AS pickup_zone,
      COUNT(*) AS pickups
    FROM taxi t
    JOIN taxizones z ON t."PULocationID" = z."LocationID"
    GROUP BY pickup_zone
    ORDER BY pickups DESC
    LIMIT 10;
```

## Average Fare or Tip By Pickup Zone
```SQL
    SELECT
      z.zone AS pickup_zone,
      AVG(t.total_amount) AS avg_fare,
      AVG(t.tip_amount) AS avg_tip
    FROM taxi t
    JOIN taxizones z ON t."PULocationID" = z."LocationID"
    GROUP BY pickup_zone
    ORDER BY avg_tip DESC
    LIMIT 15;
```

## Common Zone Pairs
```SQL
    SELECT
      z1.zone AS pickup_zone,
      z2.zone AS dropoff_zone,
      COUNT(*) AS trip_count
    FROM taxi t
    JOIN taxizones z1 ON t."PULocationID" = z1."LocationID"
    JOIN taxizones z2 ON t."DOLocationID" = z2."LocationID"
    GROUP BY pickup_zone, dropoff_zone
    ORDER BY trip_count DESC
    LIMIT 20;
```

## Airport Traffic
```SQL
    SELECT
      CASE
        WHEN z1.zone LIKE '%Airport%' THEN z1.zone
        WHEN z2.zone LIKE '%Airport%' THEN z2.zone
        ELSE 'None'
      END AS airport_zone,
      COUNT(*) AS trips
    FROM taxi t
    JOIN taxizones z1 ON t."PULocationID" = z1."LocationID"
    JOIN taxizones z2 ON t."DOLocationID" = z2."LocationID"
    WHERE z1.zone LIKE '%Airport%' OR z2.zone LIKE '%Airport%'
    GROUP BY airport_zone
    ORDER BY trips DESC;
```

## Zone Level Travel Times
```SQL
    WITH durations AS (
      SELECT
        PULocationID,
        DOLocationID,
        DATE_DIFF('minute', tpep_pickup_datetime, tpep_dropoff_datetime) AS duration_min
      FROM taxi
      WHERE trip_distance > 0 AND total_amount > 0
    )

    SELECT
    z1.zone AS pickup_zone,
    z2.zone AS dropoff_zone,
    ROUND(AVG(d.duration_min), 2) AS avg_duration,
    COUNT(*) AS trip_count
    FROM durations AS d
    JOIN TaxiZones z1 ON d.PULocationID = z1.LocationID
    JOIN TaxiZones z2 ON d.DOLocationID = z2.LocationID
    GROUP BY pickup_zone, dropoff_zone
    HAVING trip_count > 100
    ORDER BY avg_duration DESC
    LIMIT 20;
```


