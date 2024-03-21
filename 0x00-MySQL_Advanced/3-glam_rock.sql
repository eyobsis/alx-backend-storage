-- Task: List all bands with Glam rock as their main style, ranked by their longevity
-- QUERY TO LIST GLAM ROCK BANDS RANKED BY LONGEVITY
SELECT band_name,
       IF(split IS NULL OR formed IS NULL, 0, (2022 - formed)) AS lifespan
FROM bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;

