select artist_name , min(track), date_published
from artists_newest_track
where date_published > DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
group by artist_id, date_published
order by date_published desc;
