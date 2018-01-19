from ..mysql_service import *
from flask import jsonify


class ArtistService:

    @staticmethod
    def get_upcoming_events(artist_id):
        query = """
            select artists.artist_name as 'artist_name',events.artist_id, events.city,events.country,
            events.date,events.id,events.title,events.url,events.venue
            from artists, events
            where artists.id = events.artist_id
            and artists.id = """+artist_id+"""
            order by date
        """
        re = run_get_query(query)
        return jsonify(re)
