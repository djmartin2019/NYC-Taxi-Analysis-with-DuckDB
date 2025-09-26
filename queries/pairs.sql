SELECT
    z1.zone AS pickup_zone,
    z2.zone AS dropoff_zone,
    COUNT(*) AS trip_count
FROM taxi t
JOIN taxizones z1 ON t."PULocationID" = z1."LocationID"
JOIN taxizones z2 ON t."DOLocationID" = z2."LocationID"
GROUP BY pickup_zone, dropoff_zone
ORDER BY trip_count DESC;
