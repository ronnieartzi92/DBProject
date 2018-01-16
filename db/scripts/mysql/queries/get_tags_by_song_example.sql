
SELECT artists.id as 'Artist ID', artists.name as 'Artist', tracks.id as 'Track ID', tracks.name as 'Track', tags.id as 'Tag ID', tags.name as 'Tag' 
from artists inner join tracks on artists.id = tracks.artist_id
inner join tracks_to_tags as tt on tt.track_id = tracks.id
inner join tags on tt.tag_id = tags.id
;