SELECT *
FROM artists_newest_track AS x
WHERE date_published > DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
AND track_id <= ALL(SELECT track_id FROM artists_newest_track WHERE artist_id = x.artist_id)
ORDER BY track_play_count DESC, date_published DESC;
