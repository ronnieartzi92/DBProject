CREATE VIEW reating_song_album AS
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
               SELECT tracks.id
               FROM tracks
               GROUP BY tracks.id
               HAVING tracks.play_count >= ALL (SELECT trucks.play_count FROM tracks GROUP BY trucks.id)
             ) AS t ON tracks.album = t.album
ORDER BY tracks.play_count DESC
LIMIT 25 );
