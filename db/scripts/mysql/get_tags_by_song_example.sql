
SELECT * from artists 
join tracks on artists.id = tracks.artist_id
join tracks_to_tags on tracks_to_tags.track_id = tracks.id
join tags on tracks_to_tags.tag_id = tags.id
where tracks.name = "Mama Mia - Song 2" 
;