SELECT *
FROM artists_tracks_youtubes
INNER JOIN tracks_to_tags ON artists_tracks_youtubes.track_id = tracks_to_tags.track_id
WHERE
# getting most common tag in the playlist
tracks_to_tags.tag_id = (
                         select tag_id
                         from tracks_to_play_lists, tracks
                         INNER JOIN tracks_to_tags ON tracks.id = tracks_to_tags.track_id
                         where play_list_id =5
                         and tracks_to_play_lists.track_id = tracks.id
                         GROUP BY tracks_to_tags.tag_id
                         ORDER BY  COUNT(*) DESC
                         LIMIT 1
                         )

# verifying result tracks are not in playlist
AND artists_tracks_youtubes.track_id NOT IN (
            select tracks.id as 'playlist_songs'
            from tracks_to_play_lists, tracks
            where play_list_id =5
            and tracks_to_play_lists.track_id = tracks.id
            )
ORDER BY track_play_count DESC
LIMIT 25