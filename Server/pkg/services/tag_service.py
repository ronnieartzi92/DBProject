from ..mysql_service import *
from flask import jsonify


class TagService:

    @staticmethod
    def get_all():
        q = """
            SELECT tags.id, tags.tag_name
            from artists inner join tracks on artists.id = tracks.artist_id
            inner join tracks_to_tags as tt on tt.track_id = tracks.id
            inner join tags on tt.tag_id = tags.id
            group by(tags.tag_name)
            order by count(*) desc
            limit 500
        """
        re = run_get_query(q)
        return jsonify(re)