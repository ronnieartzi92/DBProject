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
FROM tracks
  INNER JOIN youtubes ON youtubes.track_id = tracks.id
  INNER JOIN artists ON tracks.artist_id = artists.id
  AND tracks.album = (SELECT tracks.album FROM tracks ORDER BY play_count DESC LIMIT 1);

