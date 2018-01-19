USE songs_track;
CREATE VIEW rating_song_album AS
SELECT
  tracks.artist_id,
  youtubes.duration,
  tracks.id,
  tracks.img,
  tracks.album,
  tracks.track_name,
  tracks.play_count,
  youtubes.video_id,
  artists.artist_name AS 'artist_name'
FROM youtubes, artists, tracks
  INNER JOIN (
               SELECT tracks.id, tracks.play_count, tracks.album, tracks.artist_id, artists.artist_name AS 'artist_name'
               FROM songs_track.tracks AS tracks, songs_track.artists AS artists
               ORDER BY play_count DESC
               LIMIT 1
             ) AS t
WHERE tracks.album = t.album and t.artist_name = artists.artist_name
GROUP BY tracks.track_name
ORDER BY tracks.play_count DESC

