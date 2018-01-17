CREATE VIEW artists_newest_track AS
SELECT DISTINCT tracks.artist_id, x.artist_name, tracks.id as track_id, tracks.track_name, tracks.img, tracks.play_count, youtubes.video_id, youtubes.date_published
FROM youtubes
INNER JOIN tracks ON youtubes.track_id = tracks.id
INNER JOIN artists AS x ON tracks.artist_id = x.id
AND youtubes.date_published = (
	SELECT MAX(date_published) 
    FROM youtubes
	INNER JOIN tracks ON tracks.id = youtubes.track_id
    WHERE x.id = tracks.artist_id
)
ORDER BY youtubes.date_published DESC;