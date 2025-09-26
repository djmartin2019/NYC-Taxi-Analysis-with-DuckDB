SELECT
    z.zone AS pickup_zone,
    ROUND(AVG(tip_amount), 2) AS avg_tip,
    COUNT(*) AS trip_count
FROM taxi t
JOIN TaxiZones z ON t."PULocationID" = z."LocationID"
WHERE tip_amount > 0 AND tip_amount < 50  -- Filter out outliers
GROUP BY pickup_zone
HAVING trip_count > 100  -- Only include zones with sufficient data
ORDER BY avg_tip DESC
LIMIT 20;
