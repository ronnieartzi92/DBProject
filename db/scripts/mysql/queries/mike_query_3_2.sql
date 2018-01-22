SELECT * 
FROM artists_tracks_youtubes
INNER JOIN 
(
	SELECT MIN(id) as id 
    FROM tracks
	WHERE(tracks.artist_id, tracks.play_count) IN (
		SELECT DISTINCT tracks.artist_id, MAX(tracks.play_count)
		FROM tracks
		GROUP BY artist_id
	)
	GROUP BY artist_id
) AS x ON artists_tracks_youtubes.track_id = x.id 
ORDER BY artist_play_count DESC 