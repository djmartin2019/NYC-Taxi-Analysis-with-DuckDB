SELECT
    z.zone AS dropoff_zone,
    COUNT(*) AS dropoffs
FROM taxi t
JOIN taxizones z ON t."DOLocationID" = z."LocationID"
GROUP BY dropoff_zone
ORDER BY dropoffs DESC;
