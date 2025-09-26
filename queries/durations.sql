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
    ROUND(AVG(d.duration_min), 2) AS avg_duration, COUNT(*) AS trip_count
FROM durations AS d
JOIN TaxiZones z1 ON d.PULocationID = z1.LocationID
JOIN TaxiZones z2 ON d.DOLocationID = z2.LocationID
GROUP BY pickup_zone, dropoff_zone
HAVING trip_count > 100
ORDER BY avg_duration DESC;
