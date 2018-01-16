from flask import Blueprint, request
from pkg.services.artist_service import *

artist_router = Blueprint('artist', 'artist', url_prefix='/artist')


@artist_router.route("/events", methods=["GET"], strict_slashes=False)
def get_all_tags():
    artist_id = request.args.get("id")
    return ArtistService.get_upcoming_events(artist_id)

