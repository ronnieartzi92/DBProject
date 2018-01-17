SELECT
  tracks.artist_id,
  youtubes.duration,
  tracks.id,
  tracks.img,
  tracks.name,
  tracks.play_count,
  youtubes.video_id,
  artists.name AS 'artist_name'
FROM youtubes, artists, tracks
  INNER JOIN (
               SELECT artists.id
               FROM artists, (
                               SELECT
                                 artist_id,
                                 count(id) AS 'events'
                               FROM songs_track.events
                               WHERE date <= DATE_ADD(CURDATE(), INTERVAL 1 YEAR)
                               GROUP BY artist_id
                             ) t
               WHERE artists.id = t.artist_id
               ORDER BY events DESC, play_count DESC
               LIMIT 5
             ) t
    ON tracks.artist_id IN (t.id)
WHERE tracks.id = youtubes.track_id AND tracks.artist_id = artists.id
ORDER BY play_count DESC
LIMIT 25