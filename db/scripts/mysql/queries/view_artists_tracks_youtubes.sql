CREATE VIEW artists_tracks_youtubes AS
SELECT artists.id as artist_id, artists.artist_name, artists.play_count as artist_play_count, tracks.id as track_id, tracks.track_name, tracks.img, 
	tracks.play_count as track_play_count, youtubes.video_id, youtubes.date_published
FROM youtubes
INNER JOIN tracks ON youtubes.track_id = tracks.id
INNER JOIN artists ON tracks.artist_id = artists.id;