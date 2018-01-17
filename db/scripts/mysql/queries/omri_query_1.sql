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
               SELECT artist_id
               FROM (
                      SELECT
                        artist_id,
                        country
                      FROM songs_track.events
                      GROUP BY artist_id, country
                    ) t
               GROUP BY artist_id
               ORDER BY count(country) DESC
               LIMIT 5
             ) t
    ON tracks.artist_id IN (t.artist_id)
WHERE tracks.id = youtubes.track_id AND tracks.artist_id = artists.id
ORDER BY play_count DESC
LIMIT 25