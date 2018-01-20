from ..mysql_service import *
from flask import jsonify


class TrackService:

    @staticmethod
    def full_text_search(str_to_search, limit):
        q = """
          SELECT * from artists_tracks_youtubes
          INNER JOIN (SELECT id FROM tracks_isam WHERE MATCH(lyrics,description,track_name) AGAINST ('{}') LIMIT {}) t 
          ON artists_tracks_youtubes.track_id = t.id
        """
        q = q.format(str_to_search, limit)
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
                                  FROM songs_track.events
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
                                                   FROM songs_track.events
                                                   WHERE date <= DATE_ADD(CURDATE(), INTERVAL 1 YEAR)
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