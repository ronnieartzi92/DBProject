SELECT DISTINCT x.name, MIN(tracks.name), youtubes.date_published
FROM youtubes
INNER JOIN tracks ON youtubes.track_id = tracks.id
INNER JOIN artists as x ON tracks.artist_id = x.id
WHERE youtubes.date_published > DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
AND youtubes.date_published = (
	SELECT MAX(date_published) 
    FROM youtubes
	INNER JOIN tracks ON tracks.id = youtubes.track_id
    WHERE x.id = tracks.artist_id
)
GROUP BY x.id, youtubes.date_published
ORDER BY youtubes.date_published DESC;