SELECT
  *
FROM artists_tracks_youtubes
  INNER JOIN (
               SELECT artists.id
               FROM artists, (
                               SELECT
                                 artist_id,
                                 count(id) AS 'events'
                               FROM songs_track.events
                               WHERE event_date <= DATE_ADD(CURDATE(), INTERVAL 1 YEAR)
                               GROUP BY artist_id
                             ) t
               WHERE artists.id = t.artist_id
               ORDER BY events DESC, play_count DESC
               LIMIT 5
             ) t
    ON artists_tracks_youtubes.artist_id IN (t.id)
ORDER BY track_play_count DESC
LIMIT 25