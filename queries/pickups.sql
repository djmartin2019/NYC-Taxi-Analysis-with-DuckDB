SELECT
    z.zone AS pickup_zone,
    COUNT(*) AS pickups
FROM taxi t
JOIN taxizones z ON t."PULocationID" = z."LocationID"
GROUP BY pickup_zone
ORDER BY pickups DESC;
