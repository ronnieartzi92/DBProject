SELECT * 
FROM artists_tracks_youtubes
WHERE track_id IN (
	SELECT MIN(id) FROM tracks
	WHERE(tracks.artist_id, tracks.play_count) IN (
		SELECT DISTINCT tracks.artist_id, MAX(tracks.play_count)
		FROM tracks
		GROUP BY artist_id
	)
	GROUP BY artist_id
)
ORDER BY artist_play_count DESC 