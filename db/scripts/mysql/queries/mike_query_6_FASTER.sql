SELECT *
FROM artists_tracks_youtubes
INNER JOIN(
	SELECT MIN(track_id) AS id
	FROM artists_newest_track
	WHERE date_published > DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
	GROUP BY artist_id
) AS track_ids ON track_ids.id = artists_tracks_youtubes.track_id
ORDER BY track_play_count DESC, date_published DESC;