from ..mysql_service import *
from flask import jsonify


class TrackService:

    @staticmethod
    def full_text_search(str_to_search, limit):
        splited = ",".join(["'"+n+"'" for n in str_to_search.split(' ')])

        q = """
            SELECT * from
            (
                SELECT artists_tracks_youtubes.*
                FROM artists_tracks_youtubes
                    INNER JOIN (SELECT id
                                            FROM tracks_isam
                                            WHERE MATCH(lyrics, description, track_name) AGAINST('{}')) t
                        ON artists_tracks_youtubes.track_id = t.id
                UNION DISTINCT
                (
                    SELECT DISTINCT artists_tracks_youtubes.*
                    FROM artists_tracks_youtubes, tracks_to_tags, tags
                    WHERE artists_tracks_youtubes.track_id = tracks_to_tags.track_id
                                AND tracks_to_tags.tag_id = tags.id
                                AND tags.tag_name IN ({}))
            ) tbl
        ORDER BY track_play_count DESC limit {}
                  """
        q = q.format(str_to_search, splited, limit)
        re = run_get_query(q)
        return jsonify(re)

    @staticmethod
    def concert_tour(limit):
        q = """
            SELECT
              *
            FROM artists_tracks_youtubes
              INNER JOIN (
                           SELECT artist_id
                           FROM (
                                  SELECT
                                    artist_id,
                                    country
                                  FROM events
                                  GROUP BY artist_id, country
                                ) t
                           GROUP BY artist_id
                           ORDER BY count(country) DESC
                           LIMIT 5
                         ) t
                ON artists_tracks_youtubes.artist_id IN (t.artist_id)
            ORDER BY track_play_count DESC
            LIMIT {}
        """
        q = q.format(limit)
        re = run_get_query(q)
        return jsonify(re)

    @staticmethod
    def artist_on_fire(limit):
        q = """
                SELECT
                  *
                FROM artists_tracks_youtubes
                  INNER JOIN (
                               SELECT artists.id
                               FROM artists, (
                                               SELECT
                                                 artist_id,
                                                 count(id) AS 'events'
                                               FROM events
                                               WHERE event_date <= DATE_ADD(CURDATE(), INTERVAL 1 YEAR)
                                               GROUP BY artist_id
                                             ) t
                               WHERE artists.id = t.artist_id
                               ORDER BY events DESC, play_count DESC
                               LIMIT 5
                             ) t
                    ON artists_tracks_youtubes.artist_id IN (t.id)
                ORDER BY track_play_count DESC
                LIMIT {}
                """
        q = q.format(limit)
        re = run_get_query(q)
        return jsonify(re)

    @staticmethod
    def top_of_the_top(limit):
        q = """
                SELECT * 
                FROM artists_tracks_youtubes
                WHERE track_id IN (
                    SELECT MIN(id) FROM tracks
                    WHERE(tracks.artist_id, tracks.play_count) IN (
                        SELECT DISTINCT tracks.artist_id, MAX(tracks.play_count)
                        FROM tracks
                        GROUP BY artist_id
                    )
                    GROUP BY artist_id
                )
                ORDER BY artist_play_count DESC 
                LIMIT {}
                        """
        q = q.format(limit)
        re = run_get_query(q)
        return jsonify(re)

    @staticmethod
    def playlist_mode(playlist_id, limit):
        q = """
                SELECT *
                FROM artists_tracks_youtubes
                INNER JOIN tracks_to_tags ON artists_tracks_youtubes.track_id = tracks_to_tags.track_id
                WHERE
                # getting most common tag in the playlist
                tracks_to_tags.tag_id = (
                                         select tag_id
                                         from tracks_to_play_lists, tracks
                                         INNER JOIN tracks_to_tags ON tracks.id = tracks_to_tags.track_id
                                         where play_list_id ={}
                                         and tracks_to_play_lists.track_id = tracks.id
                                         GROUP BY tracks_to_tags.tag_id
                                         ORDER BY  COUNT(*) DESC
                                         LIMIT 1
                                         )
                
                # verifying result tracks are not in playlist
                AND artists_tracks_youtubes.track_id NOT IN (
                            select tracks.id as 'playlist_songs'
                            from tracks_to_play_lists, tracks
                            where play_list_id ={}
                            and tracks_to_play_lists.track_id = tracks.id
                            )
                ORDER BY track_play_count DESC
                LIMIT {}
                        """
        q = q.format(playlist_id, playlist_id, limit)
        re = run_get_query(q)
        return jsonify(re)

    @staticmethod
    def something_new(limit):
        q = """
                    SELECT *
                    FROM artists_tracks_youtubes
                    INNER JOIN(
                        SELECT MIN(track_id) AS id
                        FROM artists_newest_track
                        WHERE date_published > DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
                        GROUP BY artist_id
                    ) AS track_ids ON track_ids.id = artists_tracks_youtubes.track_id
                    ORDER BY track_play_count DESC, date_published DESC
                    LIMIT {}
                            """
        q = q.format(limit)
        re = run_get_query(q)
        return jsonify(re)

    @staticmethod
    def great_album(limit):
        q = """
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
                          AND tracks.album = (SELECT tracks.album FROM tracks ORDER BY play_count DESC LIMIT 1)
                        LIMIT {}
                                """
        q = q.format(limit)
        re = run_get_query(q)
        return jsonify(re)