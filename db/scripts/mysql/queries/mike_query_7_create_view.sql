create view artists_newest_track
as
SELECT DISTINCT x.id as artist_id, x.name as artist_name, tracks.id as track_id, tracks.name as track, youtubes.date_published
FROM youtubes
INNER JOIN tracks ON youtubes.track_id = tracks.id
INNER JOIN artists as x ON tracks.artist_id = x.id
AND youtubes.date_published = (
	SELECT MAX(date_published) 
    FROM youtubes
	INNER JOIN tracks ON tracks.id = youtubes.track_id
    WHERE x.id = tracks.artist_id
)
ORDER BY x.name, youtubes.date_published DESC;