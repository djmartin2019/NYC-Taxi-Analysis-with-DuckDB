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
