SELECT
  *
FROM artists_tracks_youtubes
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
    ON artists_tracks_youtubes.artist_id IN (t.artist_id)
ORDER BY track_play_count DESC