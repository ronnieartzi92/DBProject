
SELECT tags.name as 'Tag', count(*)
from artists inner join tracks on artists.id = tracks.artist_id
inner join tracks_to_tags as tt on tt.track_id = tracks.id
inner join tags on tt.tag_id = tags.id
group by(tags.name)
order by count(*) desc
;