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
