SELECT artist_id, artist_name, track_id, track_name, img, video_id
FROM artists_newest_track as x
WHERE date_published > DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
AND track_id <= ALL(SELECT track_id FROM artists_newest_track WHERE artist_id = x.artist_id)
ORDER BY date_published DESC;
